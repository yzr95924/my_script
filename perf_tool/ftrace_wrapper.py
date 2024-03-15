#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import errno
import os

sys.path.append("../common_include")
_g_proc_name = "ftrace_wrapper"

from my_py import logger
from my_py import setup
from my_py import os_util
from my_py import cmd_handler
from my_py import common_tool

_g_is_dry_run = False
_g_is_debug = False
_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler = cmd_handler.CmdHandler(handler_name=_g_proc_name)
_g_ftrace_prefix = "/sys/kernel/debug/tracing"
_g_ftrace_switch = "tracing_on"
_g_trace_result = "trace"
_g_tracer = "current_tracer"
_g_tracer_nop = "nop"
_g_ftrace_func_name = ""


def usage():
    print("Usage: python3 {} -r -d -f func_name".format(_g_proc_name))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-f: function name")


def set_tracing_opt(opt: str, val: str):
    full_opt_path = os.path.join(_g_ftrace_prefix, opt)
    cmd = "sudo echo " + val + " > " + full_opt_path
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("set {} to {} failed: {}".format(
            full_opt_path, val, os_util.translate_linux_err_code(ret)
        ))
        return ret
    return 0


def reset_tracing_result():
    ret = set_tracing_opt(_g_tracer, _g_tracer_nop)
    if (ret != 0):
        _g_logger.error("reset tracer failed")
        return ret

    ret = set_tracing_opt(_g_trace_result, "")
    if (ret != 0):
        _g_logger.error("reset tracing result failed")
        return ret
    return 0

def set_tracing_switch(switch_on: bool):
    full_ftrace_switch = os.path.join(_g_ftrace_prefix, _g_ftrace_switch)
    switch_flag = "0"
    if (switch_on):
        switch_flag = "1"

    cmd = "sudo echo " + switch_flag + " > " + full_ftrace_switch
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != 0):
        _g_logger.error("set {} to {} failed: {}".format(
            full_ftrace_switch,
            switch_flag,
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    return 0


if __name__ == "__main__":
    short_opts = "f:rdh"
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
        elif (opt == "-f"):
            _g_ftrace_func_name = arg
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)

    if (len(_g_ftrace_func_name) == 0):
        _g_logger.error("input func_name is null")
        sys.exit(errno.EINVAL)
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)