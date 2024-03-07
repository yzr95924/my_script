#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
mount/umount/format lustre in a single machine
"""

import os
import getopt
import sys
import errno
import socket

sys.path.append("../common_include")
_g_proc_name = "lustre_setup"

from my_py import logger
from my_py import setup
from my_py import os_util
from my_py import cmd_handler

_g_is_dry_run = False
_g_is_debug = False
_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler = cmd_handler.CmdHandler(handler_name=_g_proc_name)
_g_is_umount = False
_g_is_format = False
_g_ost_mount_point_prefix = "/mnt/ost"
_g_mdt_mount_point_prefix = "/mnt/mdt"
_g_mgt_mount_point = "/mnt/mgt"
_g_client_mount_point = "/mnt/l_lfs"
_g_lustre_fs_name = "l_lfs"
_g_mkfs_cmd = "sudo mkfs.lustre"

_g_ost_dev_list= [
    "/dev/nvme0n5",
    "/dev/nvme0n6",
]
_g_mdt_dev_list = [
    "/dev/nvme0n3",
    "/dev/nvme0n4",
]
_g_mgt_dev_list = [
    "/dev/nvme0n2",
]


def usage():
    print("Usage: python3 {} -r -d -u".format(_g_proc_name))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-u (optional): umount mode")
    print("-f (optional): reformat mode")


def mount_umount_lustre_client(is_mount: bool):
    """mount/umount(kill) lustre client

    Args:
        is_mount (bool): mount/umount option

    Returns:
        ret: ret code
    """
    if (not is_mount):
        cmd = "sudo fuser -k" + " " + _g_client_mount_point
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                 is_dry_run=_g_is_dry_run,
                                 is_debug=_g_is_debug,
                                 is_verbose=True)
        if (ret != 0):
            if (os_util.FS.is_folder_mount(_g_client_mount_point)):
                _g_logger.error("kill mount client failed: {}".format(
                    os_util.translate_linux_err_code(ret)
                ))
                return ret
            else:
                _g_logger.warning("client not mounted, ignore")

        cmd = "sudo umount -t lustre -l" + " " + _g_client_mount_point
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                             is_dry_run=_g_is_dry_run,
                                             is_debug=_g_is_debug,
                                             is_verbose=False)
        if (ret != 0):
            if (os_util.FS.is_folder_mount(_g_client_mount_point)):
                _g_logger.error("umount lustre client failed: {}".format(
                    os_util.translate_linux_err_code(ret)
                ))
                return ret
            else:
                _g_logger.warning("client not mounted, ignore")
    else:
        ret = os_util.FS.mkdir_p(_g_client_mount_point, is_root=True)
        if (ret != 0):
            _g_logger.error("mkdir client mount point {} failed: {}".format(
                _g_mgt_mount_point, os_util.translate_linux_err_code(ret)
            ))
            return ret
        mgs_nid = os_util.Network.get_ip_address() + "@tcp"
        cmd = "sudo mount -t lustre" + " " \
            + mgs_nid + ":/" + _g_lustre_fs_name + " " \
            + _g_client_mount_point
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                             is_dry_run=_g_is_dry_run,
                                             is_debug=_g_is_debug,
                                             is_verbose=False)
        if (ret != 0):
            _g_logger.error("mount lustre client failed: {}".format(
                os_util.translate_linux_err_code(ret)
            ))
            return ret
    return 0


def mount_umount_all_ost_mdt_mgt(tgt_type: int, is_mount: bool):
    """mount/umount lustre ost/mdt

    Args:
        is_mount (bool): mount/umount option

    Returns:
        ret: ret code
    """
    idx = 0
    if (tgt_type == "ost"):
        for ost_dev in _g_ost_dev_list:
            mount_point = _g_ost_mount_point_prefix + "_" + str(idx)
            if (is_mount):
                cmd = "sudo mount -t lustre" + " " + ost_dev + " " + mount_point
            else:
                cmd = "sudo umount -t lustre -l" + " " + mount_point
            _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                                 is_dry_run=_g_is_dry_run,
                                                 is_debug=_g_is_debug,
                                                 is_verbose=False)
            if (ret != 0):
                if (is_mount):
                    _g_logger.error("mount ost {} failed: {}".format(
                        mount_point, os_util.translate_linux_err_code(ret)
                    ))
                    return ret
                else:
                    if (os_util.FS.is_folder_mount(mount_point)):
                        _g_logger.error("umount ost {} failed: {}".format(
                            mount_point, os_util.translate_linux_err_code(ret)
                        ))
                        return ret
                    else:
                        _g_logger.warning("ost {} not mounted, ignore".format(
                            mount_point))
            idx = idx + 1
    elif (tgt_type == "mdt"):
        for mdt_dev in _g_mdt_dev_list:
            mount_point = _g_mdt_mount_point_prefix + "_" + str(idx)
            if (is_mount):
                cmd = "sudo mount -t lustre" + " " + mdt_dev + " " + mount_point
            else:
                cmd = "sudo umount -t lustre -l" + " " + mount_point
            _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                                 is_dry_run=_g_is_dry_run,
                                                 is_debug=_g_is_debug,
                                                 is_verbose=False)
            if (ret != 0):
                if (is_mount):
                    _g_logger.error("mount mdt {} failed: {}".format(
                        mount_point, os_util.translate_linux_err_code(ret)
                    ))
                    return ret
                else:
                    if (os_util.FS.is_folder_mount(mount_point)):
                        _g_logger.error("umount mdt {} failed: {}".format(
                            mount_point, os_util.translate_linux_err_code(ret)
                        ))
                        return ret
                    else:
                        _g_logger.warning("mdt {} not mounted, ignore".format(
                            mount_point))
            idx = idx + 1
    elif (tgt_type == "mgt"):
        if (is_mount):
            cmd = "sudo mount -t lustre" + " " + _g_mgt_dev_list[0] + " " + _g_mgt_mount_point
        else:
            cmd = "sudo umount -t lustre -l" + " " + _g_mgt_mount_point
        _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                             is_dry_run=_g_is_dry_run,
                                             is_debug=_g_is_debug,
                                             is_verbose=False)
        if (ret != 0):
            if (is_mount):
                _g_logger.error("mount mgt {} failed: {}".format(
                    _g_mgt_mount_point, os_util.translate_linux_err_code(ret)
                ))
                return ret
            else:
                if (os_util.FS.is_folder_mount(_g_mgt_mount_point)):
                    _g_logger.error("umount mgt {} failed: {}".format(
                        _g_mgt_mount_point, os_util.translate_linux_err_code(ret)
                    ))
                    return ret
                else:
                    _g_logger.warning("mgt {} not mounted, ignore".format(
                        _g_mgt_mount_point))
    else:
        _g_logger.error("format tgt_type invalid: {}".format(tgt_type))
        return errno.EINVAL
    return 0


def start_lustre():
    """start lustre

    Returns:
        ret: return code
    """

    ret = mount_umount_all_ost_mdt_mgt("mgt", is_mount=True)
    if (ret != 0):
        _g_logger.error("start mgt failed")
        return ret
    ret = mount_umount_all_ost_mdt_mgt("mdt", is_mount=True)
    if (ret != 0):
        _g_logger.error("start mdt failed")
        return ret
    ret = mount_umount_all_ost_mdt_mgt("ost", is_mount=True)
    if (ret != 0):
        _g_logger.error("start ost failed")
        return ret

    _g_logger.info("start mount lustre client")
    ret = mount_umount_lustre_client(is_mount=True)
    if (ret != 0):
        _g_logger.error("start lustre client failed")
        return ret

    _g_logger.info("start lustre cluster done!")
    return 0


def stop_lustre_unload_mod():
    """stop lustre and unload lustre modules

    Returns:
        ret_code: return code
    """

    _g_logger.info("start to stop lustre")
    ret = mount_umount_lustre_client(is_mount=False)
    if (ret != 0):
        _g_logger.error("stop lustre client failed")
        return ret

    ret = mount_umount_all_ost_mdt_mgt("mdt", is_mount=False)
    if (ret != 0):
        _g_logger.error("stop mdt failed")
        return ret

    ret = mount_umount_all_ost_mdt_mgt("mgt", is_mount=False)
    if (ret != 0):
        _g_logger.error("stop mgt failed")
        return ret

    ret = mount_umount_all_ost_mdt_mgt("ost", is_mount=False)
    if (ret != 0):
        _g_logger.error("stop ost failed")
        return ret

    _g_logger.info("start to unload lustre modules")
    cmd = "sudo lustre_rmmod"
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                             is_dry_run=_g_is_dry_run,
                             is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("unload lustre modules failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    _g_logger.info("stop lustre cluster and unload lustre done!")
    return 0


def format_ost_mdt(tgt_type: str, index: int, dev_path: str, mount_opt=""):
    """format ost/mdt dev and mkdir mount point

    Args:
        tgt_type (str): mdt/ost
        index (int): index number
        dev_path (str): dev path
        mount_opt (str, optional): mount options. Defaults to "".

    Returns:
        ret: ret code
    """
    global _g_logger, _g_cmd_handler
    if (tgt_type not in ["ost", "mdt"]):
        _g_logger.error("format tgt_type invalid: {}".format(tgt_type))
        return errno.EINVAL

    mgs_nid = os_util.Network.get_ip_address() + "@tcp"
    cmd = _g_mkfs_cmd + " " \
        + "--fsname=" + _g_lustre_fs_name + " " \
        + "--" + tgt_type + " " \
        + "--servicenode=" + mgs_nid + " " \
        + "--mgsnode=" + mgs_nid + " " \
        + "--reformat" + " " \
        + "--index=" + str(index) + " " \
        + "--mkfsoptions=" + "\"" + mount_opt + "\"" + " " \
        + dev_path
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=True,
                                         is_verbose=False)
    if (ret != 0):
        _g_logger.error("format {}: {}, {} failed: {}".format(
            tgt_type, index, dev_path,
            os_util.translate_linux_err_code(ret)))
    else:
        _g_logger.info("format {}: {}, {} successful".format(
            tgt_type, index, dev_path))
    return 0


def format_mgt(dev_path: str, mount_opt=""):
    """format mgt dev and mkdir mount point

    Args:
        dev_path (str): dev path
        mount_opt (str, optional): mount options. Defaults to "".

    Returns:
        ret: ret code
    """
    global _g_logger, _g_cmd_handler
    mgs_nid = os_util.Network.get_ip_address() + "@tcp"

    cmd = _g_mkfs_cmd + " " \
        + "--fsname=" + _g_lustre_fs_name + " " \
        + "--mgs" + " " \
        + "--servicenode=" + mgs_nid + " " \
        + "--reformat" + " " \
        + "--mkfsoptions=" + "\"" + mount_opt + "\"" + " " \
        + dev_path

    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=True,
                                         is_verbose=False)

    if (ret != 0):
        _g_logger.error("format mgt: {}, failed: {}".format(
            dev_path, os_util.translate_linux_err_code(ret)))
    else:
        _g_logger.info("format mgt: {} successful".format(dev_path))

    ret = os_util.FS.mkdir_p(_g_mgt_mount_point, is_root=True)
    if (ret != 0):
        _g_logger.error("mkdir ost mount point {} failed: {}".format(
            _g_mgt_mount_point, os_util.translate_linux_err_code(ret)
        ))
        return ret
    return 0


def format_all_mdt_ost_mgt():
    """format all ost and mdt

    Returns:
        ret_code: return code
    """
    ost_idx = 0
    mdt_idx = 0
    ret = 0
    mount_point = ""

    # NOTE: ignore ret value of umount all lustre entities
    cmd = "sudo umount -t lustre -a -l"
    _g_cmd_handler.run_shell(cmd=cmd,
                             is_dry_run=_g_is_dry_run,
                             is_debug=_g_is_debug,
                             is_verbose=True)

    for ost_dev in _g_ost_dev_list:
        ret = format_ost_mdt("ost", ost_idx, ost_dev)
        if (ret != 0):
            _g_logger.error("format ost failed: {}".format(
                os_util.translate_linux_err_code(ret)
            ))
            return ret

        mount_point = _g_ost_mount_point_prefix + "_" + str(ost_idx)
        ret = os_util.FS.mkdir_p(mount_point, is_root=True)
        if (ret != 0):
            _g_logger.error("mkdir ost mount point {} failed: {}".format(
                mount_point, os_util.translate_linux_err_code(ret)
            ))
            return ret
        ost_idx = ost_idx + 1
    _g_logger.info("format all ost done!")

    for mdt_dev in _g_mdt_dev_list:
        ret = format_ost_mdt("mdt", mdt_idx, mdt_dev)
        if (ret != 0):
            _g_logger.error("format mdt failed: {}".format(
                os_util.translate_linux_err_code(ret)
            ))
            return ret

        mount_point = _g_mdt_mount_point_prefix + "_" + str(mdt_idx)
        ret = os_util.FS.mkdir_p(mount_point, is_root=True)
        if (ret != 0):
            _g_logger.error("mkdir mdt mount point {} failed: {}".format(
                mount_point, os_util.translate_linux_err_code(ret)
            ))
            return ret
        mdt_idx = mdt_idx + 1
    _g_logger.info("format all mdt done!")

    ret = format_mgt(_g_mgt_dev_list[0])
    if (ret != 0):
        _g_logger.error("format mgt failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    _g_logger.info("format mgt done!")
    return 0


if __name__ == "__main__":
    short_options = "rdhuf"
    ret = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_options)
    except getopt.GetoptError as err:
        _g_logger.error(str(err))
        sys.exit(errno.EINVAL)

    for opt, arg in opts:
        if (opt == "-h"):
            usage()
            sys.exit(0)
        elif (opt == "-r"):
            _g_is_dry_run = True
        elif (opt == "-d"):
            _g_is_debug = True
        elif (opt == "-u"):
            _g_is_umount = True
        elif (opt == "-f"):
            _g_is_format = True
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

    if (_g_is_format):
        _g_logger.info("start to format lustre")
        ret = format_all_mdt_ost_mgt()
        sys.exit(ret)
    if (_g_is_umount):
        _g_logger.info("start to umount lustre cluster and unload lustre modules")
        ret = stop_lustre_unload_mod()
        sys.exit(ret)

    _g_logger.info("start to mount lustre cluster")
    ret = start_lustre()
    sys.exit(ret)