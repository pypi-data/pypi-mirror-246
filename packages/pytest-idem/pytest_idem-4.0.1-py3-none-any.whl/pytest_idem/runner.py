import contextlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import types
import unittest.mock as mock
import uuid
from typing import Any
from typing import Dict
from typing import List

import dict_tools.data
import pop.hub
import yaml
from idem.exec.init import ExecReturn

# Get a list of all the built-in types
PRIMITIVE_TYPES = (i for i in types.__dict__.values() if isinstance(i, type))


class IdemRunException(Exception):
    ...


def generate_acct_key(*, crypt_plugin: str = "fernet") -> str:
    """
    Create a new acct_key using the named plugin and return it as a string
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="acct")

    return hub.crypto[crypt_plugin].generate_key()


def generate_acct_file(
    data, *, acct_key: str, crypt_plugin: str = "fernet"
) -> pathlib.Path:
    """
    Generate an acct_file based
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="acct")

    # Make sure the acct data is serializable
    data = ensure_serializable(data)

    acct_str = hub.crypto[crypt_plugin].encrypt(data=data, key=acct_key)

    with tempfile.NamedTemporaryFile(suffix=".yml.fernet", delete=False) as fh:
        fh.write(acct_str)
        path = pathlib.Path(fh.name)
        return path


def ensure_serializable(obj):
    def _default(x):
        if hasattr(x, "__dict__"):
            return x.__dict__
        else:
            return str(x)

    # Convert the object to a json string
    json_str = json.dumps(obj, default=_default)
    # Convert it back to itself
    return json.loads(json_str)


def run_sls(
    sls: List[str],
    runtime: str = "parallel",
    test: bool = False,
    invert_state: bool = False,
    acct_file: str = None,
    acct_key: str = None,
    ret_data: str = "running",
    sls_offset: str = "sls",
    param_offset: str = None,
    params: Dict[str, Any] = None,
    cache_dir: str = None,
    sls_sources: List[str] = None,
    param_sources: List[str] = None,
    hard_fail_on_collect: bool = False,
    acct_data: Dict[str, Any] = None,
    managed_state: Dict = None,
    render: str = "jinja|yaml|replacements",
    hub: pop.hub.Hub = None,
    run_name: str = None,
):
    """
    Run a list of sls references from idem/tests/sls/
    """
    if not hub:
        # Patch the PYTHONPATH to have the project's testing tpath plugin
        hub = pop.hub.Hub()
        hub.pop.sub.add(dyne_name="idem")
        patch_hub(hub)

    if run_name is None:
        run_name = "test"
    hub.idem.RUN_NAME = name = run_name
    hub.idem.resolve.HARD_FAIL = hard_fail_on_collect
    return _run_sls(
        hub,
        name=name,
        sls=sls,
        runtime=runtime,
        test=test,
        acct_file=acct_file,
        acct_key=acct_key,
        ret_data=ret_data,
        sls_offset=sls_offset,
        param_offset=param_offset,
        params=params,
        cache_dir=cache_dir,
        sls_sources=sls_sources,
        param_sources=param_sources,
        acct_data=acct_data,
        render=render,
        invert_state=invert_state,
        managed_state=managed_state,
    )


def _run_sls(
    hub,
    name: str,
    sls: List[str],
    runtime: str,
    test: bool,
    acct_file: str,
    acct_key: str,
    ret_data: str,
    sls_offset: str,
    param_offset: str,
    params: List[str],
    cache_dir: str,
    sls_sources: List[str],
    param_sources: List[str],
    acct_data: Dict[str, Any],
    render: str,
    managed_state: Dict = None,
    invert_state: bool = False,
):
    """
    A private function to verify that the output of the various sls runners is consistent
    """
    # SLS sources and param sources need to be kept strictly separate
    from .plugin import TESTS_DIR

    if sls and not sls_sources:
        if sls_offset:
            sls_dir = TESTS_DIR / sls_offset
        else:
            sls_dir = TESTS_DIR
        assert sls_dir.exists(), sls_dir
        sls_sources = [f"file://{sls_dir}"]

    if params and not param_sources:
        if param_offset is None:
            param_dir = TESTS_DIR / "sls" / "params"
        else:
            param_dir = TESTS_DIR / param_offset

        assert param_dir.exists(), param_dir
        param_sources = [f"file://{param_dir}"]

    hub.pop.loop.create()
    remove_cache = False
    if cache_dir is None:
        remove_cache = True
        cache_dir = tempfile.mkdtemp()
    else:
        # Cleanup is being handled by the caller
        hub.idem.managed.KEEP_CACHE_FILE = True
    context = hub.idem.managed.context(
        run_name=name, cache_dir=cache_dir, esm_plugin="local"
    )
    try:
        hub.pop.loop.CURRENT_LOOP.run_until_complete(
            _async_apply(
                hub,
                context,
                name=name,
                sls_sources=sls_sources,
                render=render,
                runtime=runtime,
                subs=["states", "nest"],
                cache_dir=cache_dir,
                sls=sls,
                test=test,
                invert_state=invert_state,
                acct_file=acct_file,
                acct_key=acct_key,
                param_sources=param_sources,
                params=params,
                acct_data=acct_data,
                managed_state=managed_state,
            )
        )
    finally:
        hub.pop.loop.CURRENT_LOOP.close()
        if remove_cache:
            shutil.rmtree(cache_dir, ignore_errors=True)
    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        raise IdemRunException("\n".join(errors))
    if ret_data == "all":
        return hub.idem.RUNS[name]
    else:
        return hub.idem.RUNS[name]["running"]


async def _async_apply(hub, context, *args, **kwargs):
    """
    Call the sls runner with an async context manager
    """
    managed_state = kwargs.pop("managed_state")
    if managed_state is not None:
        return await hub.idem.state.apply(managed_state=managed_state, *args, **kwargs)
    else:
        async with context as managed_state:
            return await hub.idem.state.apply(
                *args, **kwargs, managed_state=managed_state
            )


def run_sls_validate(
    sls: List[str],
    runtime: str = "parallel",
    test: bool = False,
    sls_offset: str = "sls/validate",
):
    """
    Run SLS validation on SLS refs in idem/tests/*/validate
    """
    from .plugin import TESTS_DIR

    name = "test"
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="idem")
    render = "jinja|yaml|replacements"
    cache_dir = tempfile.mkdtemp()
    sls_dir = TESTS_DIR / sls_offset
    sls_sources = [f"file://{sls_dir}"]
    hub.pop.loop.create()
    hub.pop.Loop.run_until_complete(
        hub.idem.state.validate(
            name,
            sls_sources,
            render,
            runtime,
            ["states", "nest"],
            cache_dir,
            sls,
            test,
        )
    )
    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        return errors
    return hub.idem.RUNS[name]


def run_yaml_block(yaml_block: str, **kwargs):
    """
    Run states defined in a yaml string
    """
    sls_run = str(uuid.uuid4())

    data = {f"{sls_run}.sls": yaml.safe_load(yaml_block)}

    return run_sls_source(
        sls=[sls_run],
        sls_sources=[f"json://{json.dumps(data)}"],
        render="json",
        **kwargs,
    )


def run_sls_source(
    sls: List[str],
    sls_sources: List[str],
    run_name: str = "run_yaml_block",
    hub: pop.hub.Hub = None,
    **kwargs,
):
    """
    Run states defined in sls sources
    """
    if hub is None:
        hub = pop.hub.Hub()
        hub.pop.sub.add(dyne_name="idem")
        patch_hub(hub)
        hub.pop.loop.create()

    run_sls(
        sls=sls,
        sls_sources=sls_sources,
        hub=hub,
        run_name=run_name,
        **kwargs,
    )

    assert not hub.idem.RUNS[run_name]["errors"], "\n".join(
        hub.idem.RUNS[run_name]["errors"]
    )
    return hub.idem.RUNS[run_name]["running"]


@contextlib.contextmanager
def tpath_hub(tpath_dir: str = None):
    """
    Add "idem_plugin" to the test path
    """
    if not tpath_dir:
        from .plugin import TESTS_DIR

        tpath_dir = str(TESTS_DIR / "tpath")

    with mock.patch("sys.path", [tpath_dir] + sys.path):
        hub = pop.hub.Hub()
        hub.pop.sub.add(dyne_name="idem")

        hub.pop.loop.create()

        yield hub

        hub.pop.loop.CURRENT_LOOP.close()


def patch_hub(hub, tpath_dir: str = None):
    """
    Add the specified path to the python environment then reload all the subs on the hub
    If no tpath_dir is specified, then project_root/tests/tpath will be used
    """
    if not tpath_dir:
        from .plugin import TESTS_DIR

        tpath_dir = str(TESTS_DIR / "tpath")

    if not os.path.isdir(tpath_dir):
        return

    # Patch the PYTHONPATH to have the project's testing tpath plugin
    with mock.patch("sys.path", [tpath_dir] + sys.path):
        # Reload all the dynamic subs
        for dyne in ("acct", "esm", "source", "tool", "exec", "states"):
            hub._dscan = False
            hub.pop.sub.reload(dyne)
            hub.pop.sub.load_subdirs(hub[dyne], recurse=True)


def run_ex(
    path,
    args,
    kwargs,
    acct_file=None,
    acct_key=None,
    acct_blob=None,
    acct_profile: str = "default",
):
    """
    Pass in an sls list and run it!
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="idem")
    patch_hub(hub)
    hub.states.test.ACCT = ["test_acct"]
    hub.pop.loop.create()
    ret = hub.pop.Loop.run_until_complete(
        hub.idem.ex.run(
            path=path,
            args=args,
            kwargs=kwargs,
            acct_file=acct_file,
            acct_key=acct_key,
            acct_blob=acct_blob,
            acct_profile=acct_profile,
        )
    )
    assert isinstance(ret, ExecReturn)
    assert bool(ret) is ret.result
    assert ret.result is ret["result"]
    assert ret.comment is ret["comment"]
    assert ret.ref is ret["ref"]
    return ret


def idem_cli(
    subcommand: str,
    *args,
    pre_subcommand_args: List[str] = None,
    env: Dict[str, str] = None,
    check: bool = False,
    acct_data: Dict[str, Any] = None,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    """
    Shell out to run an idem subcommand on the cli and parse the output as json
    """
    runpy = pathlib.Path(__file__).parent / "run.py"

    # Make sure all the inputs are strings
    args = [str(a) for a in args]
    if pre_subcommand_args is None:
        pre_subcommand_args = ()
    else:
        pre_subcommand_args = [str(a) for a in pre_subcommand_args]

    # Ensure a json parseable output
    if subcommand in ("state", "exec", "describe", "decrypt", "doc") and not any(
        "--output" in a for a in args
    ):
        args.append("--output=json")

    # default to not using esm for tests unless explicitly instructed otherwise
    # This way tests can be run in parallel
    if subcommand == "state" and not any("--esm-plugin" in a for a in args):
        args.append("--esm-plugin=null")

    command = [
        str(a)
        for a in (sys.executable, runpy, *pre_subcommand_args, str(subcommand), *args)
    ]

    if env is None:
        env = {}

    # Windows needs this one thing in a clean environment
    if os.name == "nt" and "SYSTEMROOT" not in env:
        env["SYSTEMROOT"] = os.getenv("SYSTEMROOT")

    # Patch the PYTHONPATH to have the project's testing tpath plugin
    if "PYTHONPATH" not in env:
        from .plugin import TESTS_DIR

        TPATH_DIR = str(TESTS_DIR / "tpath")
        if os.path.isdir(TPATH_DIR):
            env["PYTHONPATH"] = TPATH_DIR

    acct_file = None
    if acct_data:
        acct_key = generate_acct_key()
        acct_file = generate_acct_file(acct_data["profiles"], acct_key=acct_key)

        env["ACCT_KEY"] = acct_key
        env["ACCT_FILE"] = str(acct_file.absolute())
        # The new default profile is the first one defined in the acct data
        first_provider = next(iter(acct_data["profiles"].values()))
        first_profile = next(iter(first_provider.keys()))
        env["ACCT_PROFILE"] = first_profile
    elif os.environ.get("ACCT_FILE") and os.environ.get("ACCT_KEY"):
        # These can be easily overwritten by cli flags
        # make sure that ACCT information for tests is easily propagated
        if "ACCT_KEY" not in env:
            env["ACCT_KEY"] = os.environ.get("ACCT_KEY")
        if "ACCT_FILE" not in env:
            env["ACCT_FILE"] = os.environ.get("ACCT_FILE")
        if "ACCT_PROFILE" not in env:
            env["ACCT_PROFILE"] = os.environ.get("ACCT_PROFILE", "default")

    try:
        ret = subprocess.run(command, capture_output=True, encoding=encoding, env=env)
    finally:
        if acct_file:
            acct_file.unlink()

    stdout = ret.stdout
    stderr = ret.stderr
    if check:
        assert ret.returncode == 0, stderr or stdout

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        data = {}

    return dict_tools.data.NamespaceDict(
        command=" ".join(command),
        env=env,
        stdout=stdout,
        stderr=stderr,
        retcode=ret.returncode,
        result=ret.returncode == 0,
        json=data,
    )


@contextlib.contextmanager
def named_tempfile(delete: bool = True, *args, **kwargs):
    """
    Create a named temporary file with workarounds for Windows to be able to open it multiple times like unix
    """
    fh = tempfile.NamedTemporaryFile(delete=False, *args, **kwargs)
    fh.close()

    path = pathlib.Path(fh.name)
    yield path
    if delete:
        try:
            path.unlink()
        except FileNotFoundError:
            # It was already removed
            ...
