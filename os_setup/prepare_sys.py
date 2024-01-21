#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
set up the os source for different os release
    ubuntu - apt-get source
    centos - yum source, and epel source
    rocky - yum source, and epel source
    almalinux - yum source, and epel source
'''

import os
import getopt
import sys
import errno

sys.path.append("../common_include")
_g_proc_name = "prepare_sys"

from my_py import logger
from my_py import cmd_handler
from my_py import os_util
from my_py import setup

_g_is_dry_run = False
_g_is_debug = False
_g_source_list_lib_path = "./source_list_lib"

_g_os_id = ""
_g_os_release_version = ""

# for ubuntu
_g_old_apt_source_path = "/etc/apt/sources.list"
_g_bak_apt_source_path = "/etc/apt/sources.list.bak"

# for centos & rocky
_g_old_yum_repo_path = "/etc/yum.repos.d"
_g_bak_yum_repo_dict = {
    "centos": "/etc/yum.repos.d/bak_centos",
    "rocky": "/etc/yum.repos.d/bak_rocky",
    "epel": "/etc/yum.repos.d/bak_epel",
    "almalinux": "/etc/yum.repos.d/bak_alma"
}

_g_yum_file_prefix_dict = {
    "centos": "CentOS*.repo",
    "rocky": "Rocky*.repo",
    "epel": "epel*.repo",
    "almalinux": "almalinux*.repo"
}

_g_new_yum_dir_dict = {
    "centos": "centos_8_source",
    "rocky": "rocky_8_source",
    "almalinux": "alma_8_source"
}

_g_rocky_support_version = {"8.8"}
_g_almalinux_support_version = {"8.8"}
_g_centos_support_version = {"8"}

_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler = cmd_handler.CmdHandler(handler_name=_g_proc_name)


def clean_yum_repo_rebuild():
    cmd = "sudo yum clean all"
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("yum clean failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
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
        _g_logger.error("yum makecache failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode

    return returncode


def backup_old_source(backup_dir: str, target_prefix: str):
    '''
    backup target prefix file in /etc/yum.repos.d into backup_dir

    Args:
        backup_dir:
            path of backup dir
        target_prefix:
            target file prefix

    Returns:
        returncode:
            return code
    '''
    returncode = 0
    cmd = ""
    cmd = "sudo mkdir -p" + " " + backup_dir
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("create old source backup folder failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode

    cmd = "sudo mv" + " " + \
        os.path.join(_g_old_yum_repo_path, target_prefix) + " " + \
        backup_dir
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("backup old source failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode
    return 0


def replace_new_source(source_dir: str, target_prefix: str):
    '''
    replace new source in /etc/yum.repos.d

    Args:
        source_dir:
            source dir path
        target_prefix:
            target file prefix

    Returns:
        returncode:
            return code
    '''

    cmd = "sudo cp -r" + " " + \
        os.path.join(source_dir, target_prefix) + " " + \
        _g_old_yum_repo_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("replace old yum source failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode
    return 0


def install_epel():
    '''
    install epel
    '''
    cmd = "sudo yum --nogpgcheck -y install epel-release"
    returncode = 0
    try:
        _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                    is_dry_run=_g_is_dry_run,
                                                    is_debug=_g_is_debug)
    except TimeoutError:
        _g_logger.error("execution timed out: {}".format(cmd))
        return errno.ETIME
    if (returncode != 0):
        _g_logger.error("execution timed out: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode
    return 0


def prepare_yum_and_epel_repo():
    '''
    prepare the centos source for different ubuntu version

    Args:
        None

    Returns:
        < 0 failed, == 0 success
    '''
    if _g_os_id == "centos":
        _g_logger.info("get centos source for: {}".format(
            _g_os_release_version))
        if (_g_os_release_version in _g_centos_support_version):
            source_file_dir = _g_new_yum_dir_dict[_g_os_id]
        else:
            _g_logger.error("not support for this version")
            return errno.ENOENT
    elif _g_os_id == "rocky":
        _g_logger.info("get rocky source for: {}".format(
            _g_os_release_version))
        if (_g_os_release_version in _g_rocky_support_version):
            source_file_dir = _g_new_yum_dir_dict[_g_os_id]
        else:
            _g_logger.error("not support for this version")
            return errno.ENOENT
    elif _g_os_id == "almalinux":
        _g_logger.info("get almalinux source for: {}".format(
            _g_os_release_version))
        if (_g_os_release_version in _g_almalinux_support_version):
            source_file_dir = _g_new_yum_dir_dict[_g_os_id]
        else:
            _g_logger.error("not support for this version")
            return errno.ENOENT
    else:
        _g_logger.error("not support os release")
        return errno.ENOENT

    returncode = 0
    final_source_path = os.path.join(_g_source_list_lib_path, source_file_dir)

    _g_logger.info("backup old yum centos repo")
    if (os_util.FS.check_if_file_exist(_g_bak_yum_repo_dict[_g_os_id])):
        _g_logger.error("old yum repo backup exist: {}, {}".format(
            _g_bak_yum_repo_dict[_g_os_id],
            _g_bak_yum_repo_dict["epel"]))
        return errno.EEXIST

    returncode = backup_old_source(_g_bak_yum_repo_dict[_g_os_id],
                                   _g_yum_file_prefix_dict[_g_os_id])
    if (returncode != 0):
        _g_logger.error("backup old {} source failed: {}".format(
            _g_os_id, os_util.translate_linux_err_code(returncode)))
        return returncode

    returncode = replace_new_source(final_source_path,
                                    _g_yum_file_prefix_dict[_g_os_id])
    if (returncode != 0):
        _g_logger.error("replace old {} source failed: {}".format(
            _g_os_id, os_util.translate_linux_err_code(returncode)))
        return returncode

    returncode = clean_yum_repo_rebuild()
    if (returncode != 0):
        _g_logger.error("rebuild {} source failed: {}".format(
            _g_os_id, os_util.translate_linux_err_code(returncode)))
        return returncode

    returncode = install_epel()
    if (returncode != 0):
        _g_logger.error("install {} epel release failed: {}".format(
            _g_os_id, os_util.translate_linux_err_code(returncode)))
        return returncode

    # NOTE: assume only the first run can reach here
    returncode = backup_old_source(_g_bak_yum_repo_dict["epel"],
                                   _g_yum_file_prefix_dict["epel"])
    if (returncode != 0):
        _g_logger.error("backup old epel source failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode

    returncode = replace_new_source(final_source_path,
                                    _g_yum_file_prefix_dict["epel"])
    if (returncode != 0):
        _g_logger.error("replace old epel source failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode

    returncode = clean_yum_repo_rebuild()
    if (returncode != 0):
        _g_logger.error("rebuild {} source failed: {}".format(
            _g_os_id, os_util.translate_linux_err_code(returncode)
        ))
        return returncode
    return 0


def prepare_ubuntu_source():
    '''
    prepare the apt source for different ubuntu version

    Args:
        None

    Returns:
        < 0 failed, == 0 success
    '''
    _g_logger.info("get apt source for: {}".format(
        _g_os_release_version))
    source_file = ""
    cmd = ""
    if (_g_os_release_version == "20.04"):
        source_file = "ubuntu_20_04"
    elif (_g_os_release_version == "22.04"):
        source_file = "ubuntu_22_04"
    else:
        _g_logger.error(
            "cannot find the source for version: {}".format(
                _g_os_release_version))
        return errno.ENOENT
    returncode = 0

    _g_logger.info("backup old source list")
    if (os_util.FS.check_if_file_exist(_g_bak_apt_source_path)):
        _g_logger.error("old source list backup exist: {}".format(
            _g_bak_apt_source_path))
        return errno.EEXIST

    cmd = "sudo cp" + " " + _g_old_apt_source_path + " " + _g_bak_apt_source_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("backup old source list failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode

    new_source_list_path = os.path.join(_g_source_list_lib_path, source_file)
    cmd = "sudo cp" + " " + new_source_list_path + " " + _g_old_apt_source_path
    _, _, returncode = _g_cmd_handler.run_shell(cmd=cmd,
                                                is_dry_run=_g_is_dry_run,
                                                is_debug=_g_is_debug)
    if (returncode != 0):
        _g_logger.error("replace old source list failed: {}".format(
            os_util.translate_linux_err_code(returncode)))
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
        _g_logger.error("execution timed out: {}".format(
            os_util.translate_linux_err_code(returncode)))
        return returncode
    return 0


def usage():
    print("Usage: python3 {} -r -d".format(__file__))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("centos: 8")
    print("ubuntu: 22.04")
    print("rocky: 8.8")
    print("almalinux: 8.8")


if __name__ == "__main__":
    short_options = "hrd"
    ret = 0
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

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

    os_info = os_util.get_current_os_release()
    if os_info is None:
        _g_logger.error("get os release info failed")
        sys.exit(errno.EIO)
    else:
        _g_logger.info("get os release: {}, {}".format(
            os_info["ID"], os_info["VERSION_ID"]))

    if os_info["ID"] == "ubuntu":
        _g_os_id = os_info["ID"]
        _g_os_release_version = os_info["VERSION_ID"]
        ret = prepare_ubuntu_source()
        if (ret != 0):
            _g_logger.error("update ubuntu source failed: {}".format(
                os_util.translate_linux_err_code(ret)))
            sys.exit(ret)
    elif os_info["ID"] in _g_new_yum_dir_dict:
        _g_os_id = os_info["ID"]
        _g_os_release_version = os_info["VERSION_ID"]
        ret = prepare_yum_and_epel_repo()
        if (ret != 0):
            _g_logger.error("update yum and epel failed ({}): {}".format(
                os_info["ID"], os_util.translate_linux_err_code(ret)))
            sys.exit(ret)
    else:
        _g_logger.error("not support os release")
        sys.exit(0)
