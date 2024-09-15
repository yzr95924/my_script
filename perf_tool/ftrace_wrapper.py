#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import errno
import os
import time

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
_g_set_ftrace_filter = "set_ftrace_filter"
_g_set_current_tracer = "current_tracer"
_g_ftrace_switch = "tracing_on"
_g_trace_result = "trace"
_g_ftrace_func_name = ""
_g_is_func_graph = False
_g_timeout = 0
_g_output_path = ""

_g_function_graph_setting_tbl = {
    _g_set_current_tracer:          "function_graph",
    "max_graph_depth":              "2",
    "options/funcgraph-tail":       "1",
    "options/funcgraph-proc":       "1",
}

_g_function_setting_tbl = {
    _g_set_current_tracer:          "function",
    "options/func_stack_trace":     "1",
}

def usage():
    print("Usage: python3 {} -r -d -g -t [timeout] -f [func_name] -o [output_file]".format(_g_proc_name))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-t (optional): timeout")
    print("-g (optional): use function_graph")
    print("-f: function name")
    print("-o: output file")

def set_tracing_opt(opt: str, val: str):
    full_opt_path = os.path.join(_g_ftrace_prefix, opt)
    cmd = "sudo echo " + val + " > " + full_opt_path
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set {} to {} failed: {}".format(
            full_opt_path, val, os_util.translate_linux_err_code(ret)
        ))
        return ret
    return common_tool.RETURN_OK

def reset_tracing_result():
    """reset tracing result and option

    Returns:
        int: standard error code
    """
    ret = set_tracing_opt(_g_set_ftrace_filter, "")
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("reset {} failed".format(_g_set_ftrace_filter))
        return ret

    ret = set_tracing_opt(_g_trace_result, "0")
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("reset {} failed".format(_g_trace_result))
        return ret

    option_map = {}
    if (_g_is_func_graph):
        option_map = _g_function_graph_setting_tbl
    else:
        option_map = _g_function_setting_tbl

    # traverse all option key in the corresponding option_map
    for opt_key in option_map.keys():
        if (opt_key == _g_set_current_tracer):
            ret = set_tracing_opt(opt_key, "nop")
        else:
            ret = set_tracing_opt(opt_key, "0")
        if (ret != common_tool.RETURN_OK):
            _g_logger.error("reset {} failed".format(opt_key))
            return ret
    return common_tool.RETURN_OK

def set_tracing_switch(switch_on: bool):
    """set tracing switch

    Args:
        switch_on (bool): on/off

    Returns:
        int: standard error code
    """
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
    return common_tool.RETURN_OK

def setup_trace_option(opt_table: dict[str, str]):
    """setup tracing option with the given option table

    Args:
        opt_table (dict[str, str]): option table

    Returns:
        int: standard error code
    """
    # set tracing function name
    ret = set_tracing_opt(_g_set_ftrace_filter, _g_ftrace_func_name)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set function name failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    for opt_key in opt_table.keys():
        ret = set_tracing_opt(opt_key, opt_table[opt_key])
        if (ret != common_tool.RETURN_OK):
            _g_logger.error("set {} failed".format(opt_key))
            return ret
    return common_tool.RETURN_OK

def setup_function_trace():
    """setup for function tracing

    Returns:
        int: standard error code
    """
    # step-1: set tracing function name
    ret = set_tracing_opt(_g_set_ftrace_filter, _g_ftrace_func_name)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set function name failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    return common_tool.RETURN_OK

def start_tracing():
    # step-1: clean current result
    ret = set_tracing_switch(False)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set tracing switch to False failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    _g_logger.info("set tracing switch to False done")

    ret = reset_tracing_result()
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("reset tracing result failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    _g_logger.info("reset tracing result done")

    # step-2: setup tracer type
    if (_g_is_func_graph):
        _g_logger.info("set function_graph trace for {}".format(
            _g_ftrace_func_name
        ))
        ret = setup_trace_option(_g_function_graph_setting_tbl)
    else:
        _g_logger.info("set function trace for {}".format(
            _g_ftrace_func_name
        ))
        ret = setup_trace_option(_g_function_setting_tbl)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("setup tracing option failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    # step-3: set tracing switch on
    ret = set_tracing_switch(True)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set tracing switch to True failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    _g_logger.info("set tracing switch to True done")
    return common_tool.RETURN_OK

def stop_tracing():
    _g_logger.info("start to stop tracing")
    # step-1: set tracing switch
    ret = set_tracing_switch(False)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("set tracing switch to False failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    full_result_path = os.path.join(_g_ftrace_prefix, _g_trace_result)
    cmd = "sudo cat " + full_result_path + " > " + _g_output_path
    _, _, ret = _g_cmd_handler.run_shell(cmd=cmd,
                                         is_dry_run=_g_is_dry_run,
                                         is_debug=_g_is_debug)
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("get result failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret

    ret = reset_tracing_result()
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("reset tracing result failed: {}".format(
            os_util.translate_linux_err_code(ret)
        ))
        return ret
    return common_tool.RETURN_OK

def parse_param(opts):
    global _g_is_dry_run, _g_is_debug
    global _g_is_func_graph, _g_ftrace_func_name, _g_timeout, _g_output_path
    for opt, arg in opts:
        if (opt == "-h"):
            usage()
            sys.exit(common_tool.RETURN_OK)
        if (opt == "-r"):
            _g_is_dry_run = True
        elif (opt == "-d"):
            _g_is_debug = True
        elif (opt == "-g"):
            _g_is_func_graph = True
        # opt with arg
        elif (opt == "-f"):
            _g_ftrace_func_name = arg
        elif (opt == "-t"):
            _g_timeout = int(arg)
        elif (opt == "-o"):
            _g_output_path = arg
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)

if __name__ == "__main__":
    short_opts = "f:o:t:rdhg"
    ret = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_opts)
    except Exception as err:
        _g_logger.error(str(err))
        sys.exit(errno.EINVAL)
    parse_param(opts)

    if (len(_g_ftrace_func_name) == 0 or len(_g_output_path) == 0):
        _g_logger.error("input param is invalid")
        sys.exit(errno.EINVAL)
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

    # step-1: check is current is root
    if (not os_util.Permission.is_current_root()):
        _g_logger.error("need to run {} with root permission".format(_g_proc_name))
        sys.exit(errno.EPERM)

    # step-2: start tracing
    ret = start_tracing()
    if (ret != common_tool.RETURN_OK):
        _g_logger.error("start tracing failed")
        sys.exit(ret)

    # step-3: wait to stop tracing
    if (_g_timeout != 0):
        _g_logger.info("stop tracing in {}s".format(_g_timeout))
        time.sleep(_g_timeout)
    else:
        try:
            while True:
                time.sleep(3)
        except KeyboardInterrupt:
                _g_logger.info("trigger keyboard interrupt to stop")
    stop_tracing()