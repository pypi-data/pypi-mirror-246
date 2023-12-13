#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import os
import random
import shutil
import subprocess
import sys
from datetime import datetime
from os.path import abspath, dirname, join
from pathlib import Path
from subprocess import check_output, run

import pkg_resources
import requests

IS_WIN = sys.platform == "win32"


def _execute(cmd):
    UNDERLINE = "\033[0;4m"
    RESET = "\033[0;0m"
    print(f"{UNDERLINE}{cmd}{RESET}", flush=True)
    print(flush=True)
    p = subprocess.Popen(
        cmd,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    for line in iter(p.stdout.readline, ""):
        print("|", line.rstrip(), flush=True)
    p.wait()  # wait until process finishes, also sets returncode
    return p.returncode


def win_app_data_folder():
    import winreg

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
    )
    value, _ = winreg.QueryValueEx(key, "AppData")
    return winreg.ExpandEnvironmentStrings(value)


def win_personal_folder():
    import winreg

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
    )
    value, _ = winreg.QueryValueEx(key, "Personal")
    return winreg.ExpandEnvironmentStrings(value)


def home_folder():
    return os.path.expanduser("~")


root_folder = Path(win_app_data_folder() if IS_WIN else home_folder())
emzed_folder = root_folder / ("emzed3" if IS_WIN else ".emzed3")
spyder_folder = emzed_folder / "spyder"
remote_venv_folder = emzed_folder / "remote_venv"
document_folder = Path(win_personal_folder() if IS_WIN else home_folder())

emzed_projects = root_folder / ("emzed3_projects" if IS_WIN else ".emzed3_projects")


def _find_in(project_folder, options):
    for name in options:
        if IS_WIN:
            path = project_folder / ".venv" / "Scripts" / name
        else:
            path = project_folder / ".venv" / "bin" / name

        if path.exists():
            return path.absolute()
    return None


def pip_in(project_folder):
    return _find_in(project_folder, ("pip", "pip3", "pip.exe", "pip3.exe"))


def pytest_in(project_folder):
    return _find_in(project_folder, ("pytest", "py.test", "pytest.exe", "py.test.exe"))


def tox_in(project_folder):
    return _find_in(project_folder, ("tox", "tox.exe"))


def twine_in(project_folder):
    return _find_in(project_folder, ("twine", "twine.exe"))


def has_build(project_folder):
    executable = python_executable_in(project_folder / ".venv")
    proc = run(f'"{executable}" -m build --help', shell=True, capture_output=True)
    return proc.returncode == 0


def python_executable_in(venv_folder):
    if IS_WIN:
        executable = venv_folder / "Scripts" / "python.exe"
    else:
        executable = venv_folder / "bin" / "python3"
    return executable.absolute()


def get_active_project():
    active_project_file = emzed_folder / "active_project.txt"
    if active_project_file.exists():
        active_project = active_project_file.read_text().strip()
        if active_project:
            folder = emzed_projects / active_project
            if folder.exists() and folder.is_dir():
                return str(active_project)
    return None


def get_project_folder(name):
    return emzed_projects / name


def set_next_active_project(path):
    """schedule active project for next kernel startup"""

    if not emzed_folder.exists():
        emzed_folder.mkdir()
    next_active_project_file = emzed_folder / "next_active_project.txt"
    next_active_project_file.write_text(path)


def update_active_project():
    """checks if anther project is scheduled for activation
    and handles this"""

    next_active_project_file = emzed_folder / "next_active_project.txt"
    if not next_active_project_file.exists():
        return
    next_active_project = next_active_project_file.read_text().strip()
    active_project_file = emzed_folder / "active_project.txt"
    active_project_file.write_text(next_active_project)
    next_active_project_file.unlink()


"""
don't implement package imports here!

remote_interpreter_startup.py runs in its own virtual environment and has no
emzed_spyder installed.  locally.
"""


cache_invalidation_token = str(random.random())

DOWNLOAD_URL = (
    "https://gitlab.com/emzed3/emzed-spyder/-/raw/main/setup_files_remote_shell"
    f"/setup_remote_shell_{sys.platform}.txt"
    f"?{cache_invalidation_token}"
)


IS_WIN = sys.platform == "win32"


def setup_venv_for_remote_interpreter(destination=None):
    if destination is None:
        destination = remote_venv_folder
    if not is_valid_venv(destination):
        create_fresh_venv(destination)
    return python_executable_in(destination)


def is_valid_venv(folder):
    if not folder.exists():
        print(f"folder {folder} does not exist.")
        return False

    executable = python_executable_in(folder)

    if not executable.exists():
        print(f"no executable at {executable}")
        sys.stdout.flush()
        return False

    if not _venv_python_is_up_to_date(executable):
        print(
            f"python in venv {folder} is outdated. you might consider to recreate it."
        )

    for package in ("emzed", "emzed_gui", "emzed_spyder_kernels"):
        return_code = _execute(f'"{executable}" -c "import {package}"')
        if return_code == 0:
            continue
        if return_code == 120:
            print(
                f"import {package} worked, but python.exe returned 120 during shutdown"
            )
            continue
        print(f"import {package} failed")
        sys.stdout.flush()
        return False

    return True


def find_site_packages(venv_root_folder):
    site_packages = list(venv_root_folder.glob("**/site-packages"))
    if site_packages:
        return site_packages[0]
    return None


def _venv_python_is_up_to_date(executable):
    try:
        print(f'"{executable}" -c "import sys; print(sys.version_info[:3])"')
        version_str = check_output(
            f'"{executable}" -c "import sys; print(sys.version_info[:3])"',
            shell=True,
            text=True,
        ).strip()

        version_tuple = eval(version_str)
    except Exception as e:
        print(f"checking python version failed: {e}")
        return False

    if version_tuple[:2] < sys.version_info[:2]:
        print(f"python version in venv  : {'.'.join(map(str, version_tuple))}")
        print(f"python version in spyder: {'.'.join(map(str, sys.version_info[:3]))}")
    return version_tuple[:2] >= sys.version_info[:2]


def create_fresh_venv(folder, *, inherit_from=None):
    started = datetime.now()

    if folder.exists():
        if folder.is_file():
            folder.unlink()
        else:
            shutil.rmtree(folder)
    print(f"create virtual env at {folder}")
    sys.stdout.flush()

    if _execute(f'{sys.executable} -u -m venv "{folder}"'):
        print(f"creating virtual env at {folder} failed")
        sys.stdout.flush()

    python_executable = python_executable_in(folder)
    before = os.getcwd()
    try:
        os.chdir(folder)
        setup_venv(python_executable, inherit_from, folder)
    finally:
        os.chdir(before)
    assert is_valid_venv(folder)

    needed = datetime.now() - started
    print()
    print(f"setting up virtual environment needed {needed!s}")
    print()


def setup_venv(executable, inherit_from=None, folder=None):
    if _execute(f'{executable} -c "import ensurepip; ensurepip.bootstrap()"'):
        print(f"creating virtual env at {folder} failed")
        sys.stdout.flush()

    pip_install = f'"{executable}" -u -m pip install'

    def install(args):
        cmd = f"{pip_install} {args}"
        print()
        print(cmd)
        sys.stdout.flush()

        p = subprocess.Popen(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            text=True,
        )

        for line in iter(p.stdout.readline, ""):
            print(line.rstrip())
        sys.stdout.flush()
        p.wait()
        if p.returncode:
            raise IOError("the last commaned failed.")

    install("-U pip")

    if inherit_from:
        if sys.platform == "win32":
            install("pywin32")
        site_packages = find_site_packages(folder)
        assert (
            site_packages is not None
        ), f"venv at {folder} has not site-packages sub folder"
        (site_packages / "remote_venv.pth").write_text(str(inherit_from))

    os.environ["QT_API"] = "pyqt5"

    installed_in_edit_mode = False
    try:
        location = pkg_resources.require("emzed_spyder")[0].location
        installed_in_edit_mode = location.endswith("/emzed_spyder/src")
    except Exception:
        pass

    if installed_in_edit_mode:
        print("emzed.spyder is installed in edit mode")
        # important during local testing
        with open(
            os.path.join(
                os.path.dirname(location),
                "setup_files_remote_shell",
                f"setup_remote_shell_{sys.platform}.txt",
            )
        ) as fh:
            pip_install_args = fh.read()

    else:
        print("download requirements file")
        response = requests.get(DOWNLOAD_URL)
        try:
            response.raise_for_status()
        except IOError as e:
            raise IOError(f"could not download setup files from {DOWNLOAD_URL}: {e}")

        pip_install_args = response.text

    for args in pip_install_args.split("\n"):
        args = args.strip()
        if args:
            install(args)

    here = dirname(abspath(__file__))
    install("-e {}".format(join(here, "emzed_spyder_kernels")))

    return executable


def active_python_exe():
    project_name = get_active_project()
    if project_name is None:
        return python_executable_in(remote_venv_folder)
    project_folder = get_project_folder(project_name)
    return python_executable_in(project_folder / ".venv")


def is_project(name):
    python_exe = python_executable_in(emzed_projects / name / ".venv")
    setup_py = emzed_projects / name / "setup.py"
    return python_exe.exists() and os.access(python_exe, os.X_OK) and setup_py.exists()


def is_valid_project(name):
    """more extensive check than is_project"""
    project_folder = get_project_folder(name)
    return is_valid_venv(project_folder / ".venv")
