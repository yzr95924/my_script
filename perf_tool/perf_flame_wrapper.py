#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import errno
import os

sys.path.append("../common_include")
_g_proc_name = "perf_flame_wrapper"

from my_py import logger
from my_py import setup
from my_py import os_util
from my_py import cmd_handler
from my_py import third_lib
from my_py import common_tool

_g_is_dry_run = False
_g_is_debug = False
_g_target_name = ""
_g_monitor_freq = 100
_g_output_svg_filename = os_util.FS.convert_to_abspath("~/perf_flame.svg")
_g_logger = logger.get_logger(name=_g_proc_name)
_g_cmd_handler= cmd_handler.CmdHandler(handler_name=_g_proc_name)
_g_tmp_result_dir = "/tmp/perf_flame"
_g_flame_graph_dir = os_util.FS.convert_to_abspath("~/FlameGraph")
_g_flame_graph_url = "https://github.com/brendangregg/FlameGraph.git"


def usage():
    print("Usage: python3 {} -r -d -p proc_name -f freq -o output_svg".format(
        _g_proc_name
    ))
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-p: monitor process name")
    print("-f: monitor frequency")
    print("-o: output svg file name")


def clone_flame_graph_from_remote():
    _g_logger.info("clone FlameGraph from {}".format(_g_flame_graph_url))
    cmd = "git clone" + " " + _g_flame_graph_url + " " + _g_flame_graph_dir
    _, _, ret_code = _g_cmd_handler.run_shell(cmd=cmd,
                                              is_dry_run=_g_is_dry_run,
                                              is_debug=_g_is_debug,
                                              is_verbose=True)
    if (ret_code != 0):
        _g_logger.error("clone FlameGraph failed: {}".format(
            os_util.translate_linux_err_code(ret_code)
        ))
        return ret_code
    return 0


def start_to_perf(pid_list: list):
    pid_list_str = ""
    for cur_pid in pid_list:
        if (len(pid_list_str) == 0):
            pid_list_str = pid_list_str + str(cur_pid)
        else:
            pid_list_str = pid_list_str + "," + str(cur_pid)

    output_file = os.path.join(_g_tmp_result_dir,
                               "{}.perf.data".format(_g_target_name))
    cmd = "sudo perf record" + " " + "-F {}".format(_g_monitor_freq) + " " \
        + "-p {}".format(pid_list_str) + " " + "-g" + " " \
        + "-o {}".format(output_file)

    _, _, ret_code = _g_cmd_handler.run_shell(cmd=cmd,
                                              is_dry_run=_g_is_dry_run,
                                              is_debug=_g_is_debug)
    if (ret_code != 0):
        _g_logger.error("perf record failed: {}".format(
            os_util.translate_linux_err_code(ret_code)
        ))
        return ret_code
    return 0

def param_check():
    if (len(_g_target_name) == 0):
        _g_logger.error("proc_name is invalid: {}".format(_g_target_name))
        sys.exit(errno.EINVAL)
    if (_g_monitor_freq <= 0):
        _g_logger.error("freq is invalid: {}".format(_g_monitor_freq))
        sys.exit(errno.EINVAL)


if __name__ == "__main__":
    short_opts = "p:f:o:rdh"
    ret_code = 0

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
        elif (opt == "-p"):
            _g_target_name = arg
        elif (opt == "-f"):
            _g_monitor_freq = int(arg)
        elif (opt == "-o"):
            _g_output_svg_file_name = arg
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)

    param_check()
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

    _g_logger.info("start to monitor {} with {}".format(_g_target_name, _g_monitor_freq))
    os_util.FS.mkdir_p(_g_tmp_result_dir)

    is_exist = os_util.FS.check_if_file_exist(path=_g_flame_graph_dir)
    if (not is_exist):
        _g_logger.warning("not found flame graph in {}".format(_g_flame_graph_dir))
        ret_code = clone_flame_graph_from_remote()
        if (ret_code != 0):
            sys.exit(ret_code)
    else:
        _g_logger.info("FlameGraph dir is in {}".format(_g_flame_graph_dir))

    target_pid_list = third_lib.Util.find_process_with_keyword(keyword=_g_target_name)
    if (len(target_pid_list) == 0):
        _g_logger.warning("target process not find")
        sys.exit(common_tool.RETURN_OK)
    else:
        _g_logger.info("{} pid list: {}".format(_g_target_name, target_pid_list))

    start_to_perf(pid_list=target_pid_list)