#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import errno
import os

sys.path.append("../common_include")
_g_proc_name = "blktrace_wrapper"

from my_py import logger
from my_py import setup
from my_py import os_util
from my_py import cmd_handler
from my_py import common_tool

_g_is_dry_run = False
_g_is_debug = False
_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler = cmd_handler.CmdHandler(handler_name=_g_proc_name)
_g_blktrace = "blktrace"
_g_blkparse = "blkparse"
_g_blk_analyzer = "btt"
_g_dev_name = ""
_g_result_dir = "/tmp/blk_result"
_g_tmp_summary_name = "tmp_summary"
_g_summary_suffix = "_summary"
_g_iostat_suffix = "_iostat"
_g_during_time = ""

def usage():
    print("Usage: python3 {} -r -d -i dev_name -t during_time".format(_g_proc_name))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-i: input dev name")
    print("-t (optional): during time")
    print("Note: recommend to use blktrace's latest version: git://git.kernel.dk/blktrace.git")


def start_blk_trace(during_time=90):
    _g_logger.info("set during_time: {}s".format(during_time))
    cmd_handler.set_keyboard_interrupt()
    ret = 0
    base_dev_name = os.path.basename(_g_dev_name)
    cmd = "cd" + " " + _g_result_dir + "; " \
        + _g_blktrace + " " + "-d" + " " + _g_dev_name + " " \
        + "-o" + " " + base_dev_name + " " \
        + "-w" + " " + str(during_time)
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        if (cmd_handler._g_interrupt_enable and ret < 0):
            _g_logger.warning("interrupt is enabled, ignore ret: {}".format(ret))
        else:
            _g_logger.error("start blktrace on dev {} failed: {}".format(
                _g_dev_name, os_util.translate_linux_err_code(ret)
            ))
            cmd_handler.remove_keyboard_interrupt()
            return ret
    cmd_handler.remove_keyboard_interrupt()
    return 0


def parse_blk_trace_result():
    base_dev_name = os.path.basename(_g_dev_name)
    cmd = "cd" + " " + _g_result_dir + "; " \
        + _g_blkparse + " " + "-i" + " " + base_dev_name + ".blktrace." + " " \
        + "-d" + " " + _g_tmp_summary_name
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("parse blktrace result failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    return 0


def print_blk_trace_result():
    base_dev_name = os.path.basename(_g_dev_name)
    tmp_summary_full_path = os.path.join(_g_result_dir, _g_tmp_summary_name)
    cmd = _g_blk_analyzer + " " + "-i" + " " + tmp_summary_full_path + " " \
        + "-I" + " " + base_dev_name + _g_iostat_suffix  + " " \
        + ">" + " " + base_dev_name + _g_summary_suffix
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("generate the blktrace summary failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    return 0


def clean_tmp_result():
    cmd = "rm -rf " + _g_result_dir
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("remove tmp result dir failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    cmd = "rm -rf " + "*iops_fp*"
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("remove *iops_fp* failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    cmd = "rm -rf " + "*mbps_fp*"
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("remove *mbps_fp* failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    return 0

if __name__ == "__main__":
    short_opts = "t:i:rdh"
    ret = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_opts)
    except Exception as err:
        _g_logger.error(str(err))
        sys.exit(errno.EINVAL)

    for opt, arg in opts:
        if (opt == "-h"):
            usage()
            sys.exit(common_tool.RETURN_OK)
        if (opt == "-r"):
            _g_is_dry_run = True
        elif (opt == "-d"):
            _g_is_debug = True
        elif (opt == "-i"):
            _g_dev_name = arg
        elif (opt == "-t"):
            _g_during_time = arg
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)

    if (len(_g_dev_name) == 0):
        _g_logger.error("input dev_name is null")
        usage()
        sys.exit(errno.EINVAL)
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

    if (not os_util.Permission.is_current_root()):
        _g_logger.error("need to run this with root permission")
        sys.exit(errno.EPERM)
    _g_logger.info("start to monitor the dev: {}".format(_g_dev_name))

    os_util.FS.mkdir_p(_g_result_dir)
    if (len(_g_during_time) != 0):
        ret = start_blk_trace(int(_g_during_time))
    else:
        ret = start_blk_trace()

    if (ret != 0):
        _g_logger.error("start blktrace failed")
        sys.exit(ret)
    _g_logger.info("start blktrace done")

    ret = parse_blk_trace_result()
    if (ret != 0):
        _g_logger.error("parse blktrace failed")
        sys.exit(ret)
    _g_logger.info("parse blktrace done")

    ret = print_blk_trace_result()
    if (ret != 0):
        _g_logger.error("print blktrace failed")
        sys.exit(ret)
    _g_logger.info("print blktrace done")

    ret = clean_tmp_result()
    if (ret != 0):
        _g_logger.error("clean tmp result failed")
        sys.exit(ret)
    _g_logger.info("clean tmp result done")

    sys.exit(0)