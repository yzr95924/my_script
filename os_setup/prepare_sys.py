#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
set up the os source for different os release
    ubuntu - apt-get source
    centos - yum source, and epel source
'''

import os
import getopt
import sys
import errno

sys.path.append("../common_include")
_g_proc_name = "prepare_sys"

from py import my_logger
from py import my_cmd_handler
from py import my_os_util

_g_is_dry_run = False
_g_is_debug = False
_g_source_list_lib_path = "./source_list_lib"

# for ubuntu
_g_old_apt_source_path = "/etc/apt/sources.list"
_g_bak_apt_source_path = "/etc/apt/sources.list.bak"

# for centos
_g_old_yum_repo_path = "/etc/yum.repos.d"
_g_bak_yum_centos_repo_path = "/etc/yum.repos.d/bak_centos"
_g_bak_yum_epel_repo_path = "/etc/yum.repos.d/bak_epel"

_g_logger = my_logger.get_logger(name=_g_proc_name, is_persist=False)
_g_cmd_handler = my_cmd_handler.CmdHandler(handler_name=_g_proc_name)


def clean_yum_repo_rebuild():
    cmd = "sudo yum clean all"
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "yum clean failed", returncode)
        return returncode

    cmd = "sudo yum makecache"
    try:
        _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                    timeout=30,
                                                    is_dry_run=_g_is_dry_run,
                                                    is_debug=_g_is_debug)
    except TimeoutError:
        _g_logger.error("execution timed out: {}".format(cmd))
        return errno.ETIME
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "yum makecache failed", returncode)
        return returncode

    return returncode


def prepare_apt_source(version: str):
    '''
    prepare the apt source for different ubuntu version

    Args:
        ubuntu version: e.g., 20.04, 22.04

    Returns:
        < 0 failed, == 0 success
    '''
    _g_logger.info("get apt source for: {}".format(version))
    source_file = ""
    cmd = ""
    if (version == "20.04"):
        source_file = "ubuntu_20_04"
    elif (version == "22.04"):
        source_file = "ubuntu_22_04"
    else:
        _g_logger.error(
            "cannot find the source for version: {}".format(version))
        return errno.ENOENT
    returncode = 0

    _g_logger.info("backup old source list")
    if (my_os_util.check_if_file_exits(_g_bak_apt_source_path)):
        _g_logger.error("old source list backup exist: {}".format(
            _g_bak_apt_source_path))
        return errno.EEXIST

    cmd = "sudo cp " + _g_old_apt_source_path + " " + _g_bak_apt_source_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "backup old source list failed", returncode)
        return returncode

    new_source_list_path = os.path.join(_g_source_list_lib_path, source_file)
    cmd = "sudo cp " + new_source_list_path + " " + _g_old_apt_source_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "replace old source list failed", returncode)
        return returncode

    cmd = "sudo apt-get update"
    try:
        _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                    timeout=30,
                                                    is_dry_run=_g_is_dry_run,
                                                    is_debug=_g_is_debug)
    except TimeoutError:
        _g_logger.error("execution timed out: {}".format(cmd))
        return errno.ETIME
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "execution timed out", returncode)
        return returncode

    return 0


def prepare_yum_repo(version: str):
    '''
    prepare the yum source for different ubuntu version

    Args:
        centos version: e.g., 8

    Returns:
        < 0 failed, == 0 success
    '''
    _g_logger.info("get yum source for: {}".format(version))
    cmd = ""
    if (version == "8"):
        source_file_dir = "centos_8_source"
    else:
        _g_logger.error(
            "cannot find the source for version: {}".format(version))
        return errno.ENOENT
    returncode = 0
    final_source_path = os.path.join(_g_source_list_lib_path, source_file_dir)

    _g_logger.info("backup old yum centos repo")
    if (my_os_util.check_if_file_exits(_g_bak_yum_centos_repo_path)):
        _g_logger.error("old yum repo backup exist: {}, {}".format(
            _g_bak_yum_centos_repo_path,
            _g_bak_yum_epel_repo_path))
        return errno.EEXIST

    cmd = "sudo mkdir -p " + _g_bak_yum_centos_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(_g_logger, "create old CentOS backup failed",
                                      returncode)
        return returncode

    cmd = "sudo mv" + " " + \
        os.path.join(_g_old_yum_repo_path, "CentOS*.repo") + \
        " " + _g_bak_yum_centos_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "backup old yum repo failed", returncode)
        return returncode

    cmd = "sudo cp" + " " + \
        os.path.join(final_source_path, "CentOS*.repo") + \
        " " + _g_old_yum_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "replace old yum repo failed", returncode)
        return returncode

    returncode = clean_yum_repo_rebuild()
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "clean and rebuild yum repo failed", returncode)
        return returncode

    cmd = "sudo yum --nogpgcheck -y install epel-release"
    try:
        _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                    timeout=15,
                                                    is_dry_run=_g_is_dry_run,
                                                    is_debug=_g_is_debug)
    except TimeoutError:
        _g_logger.error("execution timed out: {}".format(cmd))
        return errno.ETIME
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "execution timed out", returncode)
        return returncode

    # NOTE: assume only the first run can reach here
    cmd = "sudo mkdir -p " + _g_bak_yum_epel_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "create old epel backup failed", returncode)
        return returncode

    cmd = "sudo mv" + " " + \
        os.path.join(_g_old_yum_repo_path, "/epel*.repo") + \
        " " + _g_bak_yum_epel_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0 or returncode != errno.EEXIST):
        my_os_util.log_error_with_ret(
            _g_logger, "backup old yum epel repo failed", returncode)
        return returncode

    cmd = "sudo cp -r" + " " + \
        os.path.join(final_source_path, "epel*.repo") + \
        " " + _g_old_yum_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "replace old yum epel repo failed", returncode)
        return returncode

    returncode = clean_yum_repo_rebuild()
    if (returncode != 0):
        my_os_util.log_error_with_ret(
            _g_logger, "clean and rebuild yum repo failed", returncode)
        return returncode

    return 0


def usage():
    print("Usage: python3 {} -r -d".format(__file__))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")


if __name__ == "__main__":
    short_options = "hrd"
    ret = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_options)
    except getopt.GetoptError as err:
        _g_logger.error(str(err))
        usage()
        sys.exit(errno.EINVAL)

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

    os_info = my_os_util.get_current_os_release()
    if os_info is None:
        _g_logger.error("get os release info failed")
        sys.exit(errno.EIO)
    else:
        _g_logger.info("get os release: {}, {}".format(
            os_info["ID"], os_info["VERSION_ID"]))

    if os_info["ID"] == "ubuntu":
        ret = prepare_apt_source(os_info["VERSION_ID"])
        if (ret != 0):
            my_os_util.log_error_with_ret(_g_logger, "update apt source failed",
                                          ret)
            sys.exit(ret)
    elif os_info["ID"] == "centos":
        ret = prepare_yum_repo(os_info["VERSION_ID"])
        if (ret != 0):
            my_os_util.log_error_with_ret(_g_logger, "update yum source failed",
                                          ret)
            sys.exit(ret)
    else:
        _g_logger.error("no support os release")
        sys.exit(0)
