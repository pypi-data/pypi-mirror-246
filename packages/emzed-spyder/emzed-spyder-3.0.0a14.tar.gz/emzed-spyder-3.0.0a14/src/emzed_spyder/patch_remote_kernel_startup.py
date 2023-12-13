#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import subprocess
import sys
import xml.etree.ElementTree as et
from datetime import datetime

import requests
from requests.exceptions import ConnectionError

from .utils import (
    active_python_exe,
    get_active_project,
    get_project_folder,
    is_project,
    python_executable_in,
    update_active_project,
)


def set_emzed_spyder_kernels():
    import spyder.plugins.ipythonconsole.utils.kernelspec as kernelspec

    class PatchedKernelSpec(kernelspec.SpyderKernelSpec):
        def __init__(self, is_cython=False, is_pylab=False, is_sympy=False, **kwargs):
            kernelspec.KernelSpec.__init__(self, **kwargs)
            self.is_cython = is_cython
            self.is_pylab = is_pylab
            self.is_sympy = is_sympy

            self.display_name = "Python 3 (emzed.spyder)"
            self.language = "python3"
            self.resource_dir = ""

        @property
        def argv(self):
            result = super().argv

            update_active_project()
            active_project = get_active_project()
            if active_project and is_project(active_project):
                project_folder = get_project_folder(active_project)
                python_exe = python_executable_in(project_folder / ".venv")
                result[0] = str(python_exe)
            result[2] = "emzed_spyder_kernels"
            return result

        @property
        def env(self):
            result = super().env
            active_project = get_active_project()
            if active_project and is_project(active_project):
                project_folder = get_project_folder(active_project)
                result["EMZED_ACTIVE_PROJECT"] = str(project_folder)
            return result

    kernelspec.SpyderKernelSpec = PatchedKernelSpec


ITALICS = "\033[0;3m"
RESET = "\033[0;0m"
BLUE_FG = "\033[0;34m"
RED_FG = "\033[0;31m"

LIGHT_GREEN_FG = "\033[1;32m"
WHITE_FG = "\033[1;37m"

WELCOME = r"""{FG_LOGO}                                 _
                                | |
     _____ ____  _____ _____  __| |
    | ___ |    \(___  ) ___ |/ _  |
    | ____| | | |/ __/| ____( (_| |
    |_____)_|_|_(_____)_____)\____|
{FG_TEXT}
{ITALICS}
      Copyright (c) 2020 ETH Zurich
             Scientific IT Services
              https://emzed.ethz.ch
{RESET}
run {ITALICS}emzed_help(){RESET} for an overview of available functions.
"""

latest_version_check = None


def set_banner(remote_interpreter):
    from spyder.plugins.ipythonconsole.widgets.shell import (
        ShellWidget,
        create_qss_style,
    )

    def _banner_default(self, _orig=ShellWidget._banner_default):
        _, dark_fg = create_qss_style(self.syntax_style)
        if dark_fg:
            FG_LOGO = RED_FG
            FG_TEXT = BLUE_FG
        else:
            FG_LOGO = LIGHT_GREEN_FG
            FG_TEXT = WHITE_FG

        global latest_version_check

        active_project_exe = active_python_exe()
        if active_project_exe is not None:
            remote_interpreter = active_project_exe

        # only check versions at startup or at max once per day when one opens a new
        # console:
        if (
            latest_version_check is None
            or (datetime.now() - latest_version_check).days >= 1
        ):
            try:
                extra = "\n".join(update_message(remote_interpreter, FG_LOGO, FG_TEXT))
            except Exception:
                import traceback

                extra = traceback.format_exc()
            latest_version_check = datetime.now()
        else:
            extra = ""

        return (
            WELCOME.format(
                FG_LOGO=FG_LOGO, FG_TEXT=FG_TEXT, ITALICS=ITALICS, RESET=RESET
            )
            + extra
        )

    ShellWidget._banner_default = _banner_default


def update_message(remote_interpreter, color_logo, color_fg):
    lines = []
    found_new = False
    for package, latest_version, local_version, error in check_updates(
        remote_interpreter
    ):
        if error is not None:
            lines.append(
                color_logo + f"error when checking updates for {package}" f": {error}"
            )
        else:
            latest_str = (
                ".".join(map(str, latest_version)).replace("a.", "a").replace("b.", "b")
            )
            if local_version < latest_version:
                print(package, local_version, latest_version, file=sys.stderr)
                line = color_fg + f"{package:10s}: new version {latest_str} available."
                found_new = True
                lines.append(line)

    if found_new:
        lines.append("")
        lines.append(f"please run {color_logo}emzed_update(){color_fg}")

    latest_emzed_spyder, current_emzed_spyder, msg = _check_emzed_spyder_update()
    if msg:
        lines.append("")
        lines.append(color_logo + msg)
    if (
        latest_emzed_spyder is not None
        and current_emzed_spyder is not None
        and latest_emzed_spyder > current_emzed_spyder
    ):
        current = (
            ".".join(map(str, current_emzed_spyder))
            .replace("a.", "a")
            .replace("b.", "b")
        )
        latest = (
            ".".join(map(str, latest_emzed_spyder))
            .replace("a.", "a")
            .replace("b.", "b")
        )
        lines.append(
            f"{color_fg}emzed-spyder: current version is {current},"
            f" new version {latest} available."
        )
        lines.append(
            f"{color_logo}you must close emzed.spyder first and then use pip or a"
            " new installer to upgrade."
        )

    return lines


def check_updates(remote_interpreter):
    for package in ("emzed", "emzed-gui"):
        yield _check_update(remote_interpreter, package)


def _check_update(remote_interpreter, package):
    latest = _latest_version(package)
    if latest is None:
        return (package, None, None, f"could not determine latest version of {package}")

    local_version = _local_version(remote_interpreter, package)
    if isinstance(local_version, str):
        local_version = _split_version(local_version)
        # local_version = (local_version + (0, 0))[:3]
    if not isinstance(local_version, tuple):
        return (package, latest, None, "could not determine local version")

    return package, latest, local_version, None


def _check_emzed_spyder_update():
    latest_version = _latest_version("emzed_spyder")
    if latest_version is None:
        return None, None, "could not determine latest version of emzed_spyder"
    from . import __version__ as current_version_str

    current_version = _split_version(current_version_str)
    return latest_version, current_version, None


def _latest_version(package):
    try:
        response = requests.get(f"https://pypi.org/rss/project/{package}/releases.xml")
    except ConnectionError:
        return None

    if response.status_code == 404:
        raise ValueError(f"looks like package {package} is not on pypi.org")
    if response.status_code != 200:
        return None

    doc = et.fromstring(response.text)

    return max([_split_version(node.text) for node in doc.findall("*/item/title")])


def _split_version(version):
    tp = version.split(".")
    major, minor, debug, *rest = tp

    major = int(major)
    minor = int(minor)

    if "a" in debug:
        debug, a = debug.split("a")
        version = (major, minor, int(debug), "a", int(a))
    elif "b" in debug:
        debug, a = debug.split("b")
        version = (major, minor, int(debug), "b", int(a))
    else:
        version = (major, minor, int(debug), *rest)

    return version


def _local_version(remote_interpreter, package_local):
    try:  # will fail as version is not specified, will print available versions
        # to stderr then:
        line = f"{remote_interpreter} -m pip show {package_local}"
        output = subprocess.check_output(
            line.split(), stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError:
        return None

    for line in output.split("\n"):
        if line.startswith("Version: "):
            version = _split_version(line.removeprefix("Version: "))
            return version
