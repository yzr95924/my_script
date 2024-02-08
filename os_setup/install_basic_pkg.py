#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
install basic package for ubuntu almalinux rocky
"""

import getopt
import sys
import errno

sys.path.append("../common_include")
_g_proc_name = "install_basic_pkg"

from my_py import logger
from my_py import cmd_handler
from my_py import os_util
from my_py import setup

_g_is_dry_run = False
_g_is_debug = False

_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler = cmd_handler.CmdHandler(handler_name=_g_proc_name)

_g_apt_pkg_list = [
    "vim", "fish", "byobu", "git", "clang"
]
_g_yum_pkg_list = [
    "vim", "fish", "byobu", "git",
]


def install_apt_pkg():
    global _g_logger, _g_cmd_handler
    global _g_is_dry_run, _g_is_debug
    global _g_apt_pkg_list
    ret = 0

    cmd_prefix = "sudo apt-get install"
    for pkg in _g_apt_pkg_list:
        _g_logger.info("apt-get install: {}".format(pkg))
        cmd = cmd_prefix + " " + pkg
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                             is_dry_run=_g_is_dry_run,
                                             is_debug=_g_is_debug)
        if (ret != 0):
            _g_logger.error("apt-get install {} failed: {}".format(
                pkg, os_util.translate_linux_err_code(ret)))
            return ret
    return ret


def install_yum_pkg():
    global _g_logger, _g_cmd_handler
    global _g_is_dry_run, _g_is_debug
    global _g_yum_pkg_list
    ret = 0

    cmd_prefix = "sudo yum install -y"
    for pkg in _g_yum_pkg_list:
        _g_logger.info("yum install: {}".format(pkg))
        cmd = cmd_prefix + " " + pkg
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                             is_dry_run=_g_is_dry_run,
                                             is_debug=_g_is_debug)
        if (ret != 0):
            _g_logger.error("yum install {} failed: {}".format(
                pkg, os_util.translate_linux_err_code(ret)))
            return ret
    return ret


def usage():
    print("Usage: python3 {} -r -d".format(__file__))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")


def parse_param(opts):
    global _g_is_debug, _g_is_dry_run
    for opt, arg in opts:
        if (opt == "-h"):
            usage()
            sys.exit(0)
        elif (opt == "-r"):
            _g_is_dry_run = True
        elif (opt == "-d"):
            _g_is_debug = True
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)


if __name__ == "__main__":
    short_options = "hrd"
    ret = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_options)
    except getopt.GetoptError as err:
        _g_logger.error(str(err))
        usage()
        sys.exit(errno.EINVAL)
    parse_param(opts)

    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)
    os_info = os_util.get_current_os_release()
    if (os_info is None):
        _g_logger.error("get os release info failed")
        sys.exit(errno.EIO)
    else:
        _g_logger.info("get os release: {}, {}".format(
            os_info["ID"], os_info["VERSION_ID"]))

    if (os_info["ID"] == "ubuntu"):
        ret = install_apt_pkg()
    elif (os_info["ID"] == "rocky" or os_info["ID"] == "almalinux"):
        ret = install_yum_pkg()
    else:
        _g_logger.error("not support os release")
        sys.exit(0)

    if (ret != 0):
        _g_logger.info("install basic packages failed ({}): {}".format(
            os_info["ID"], os_util.translate_linux_err_code(ret)))
        sys.exit(ret)
    else:
        _g_logger.info("install basic packages done")
        sys.exit(0)
