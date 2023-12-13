#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"""
launchctl utils by Seven
"""

import argparse
import getpass
import os
import plistlib
import sys

import prettytable as tp

from daemon import utils, version

__version__ = '1.0.0'

USER_LAUNCH_AGENTS = os.path.expanduser("~/Library/LaunchAgents")
SYSTEM_LAUNCH_AGENTS = "/Library/LaunchAgents"
PREFIX_LABEL = "org.seven"
CMD_LOAD = "launchctl load -w {}"
CMD_UNLOAD = "launchctl unload -w {}"
ROOT_CMD_LOAD = "sudo launchctl load -w {}"
ROOT_CMD_UNLOAD = "sudo launchctl unload -w {}"
CMD_LIST = "launchctl list"
# Status
STATUS_RUNNING = "Running"
STATUS_OK = "Ok"
STATUS_UNLOADED = "Unloaded"

# 默认编辑器
# CMD_EDITOR = "/usr/bin/vim"
CMD_EDITOR = "/usr/local/bin/subl"


def calendar(hour: int = 0,
             minute: int = 0,
             weekday: int = 0,
             day: int = 0,
             month: int = 0):
    """
    build calendar
    :param hour:
    :param minute:
    :param weekday:
    :param day:
    :param month:
    :return:
    """
    ca = {}
    if hour > 0:
        ca["Hour"] = hour
    if minute > 0:
        ca["Minute"] = minute
    if weekday > 0:
        ca["Weekday"] = weekday
    if day > 0:
        ca["Day"] = day
    if month > 0:
        ca["Month"] = month
    if not bool(ca):
        raise RuntimeError("calendar empty")
    return ca


def plist_build(label: str,
                program_arguments: list = None,
                out_path: str = "/dev/null",
                error_path: str = "/dev/null",
                start_calendar_interval=None,
                start_interval: int = 0,
                working_dir: str = None,
                output_dir: str = USER_LAUNCH_AGENTS,
                keep_alive: bool = True,
                disabled: bool = False,
                run_at_load: bool = True,
                need_load: bool = True):
    """
    build plist
    :param output_dir:
    :param label:
    :param program_arguments:
    :param out_path:
    :param error_path:
    :param start_calendar_interval:
    :param start_interval:
    :param working_dir:
    :param keep_alive:
    :param disabled:
    :param run_at_load:
    :param need_load:
    :return:
    """
    if not label:
        raise ValueError("label empty")
    if not program_arguments:
        raise ValueError("program arguments empty")
    label = "{}.{}".format(PREFIX_LABEL, label)
    pl = dict(
        Label=label,
        ProgramArguments=program_arguments,
        KeepAlive=keep_alive,
        RunAtLoad=run_at_load,
        StandardOutPath=out_path,
        StandardErrorPath=error_path
    )
    if working_dir:
        pl["WorkingDirectory"] = working_dir
    if start_interval > 0:
        pl["StartInterval"] = start_interval
    if start_calendar_interval:
        pl["StartCalendarInterval"] = start_calendar_interval
    if disabled:
        pl["Disabled"] = disabled

    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        plist = os.path.join(output_dir, label + ".plist")
        is_exec = False
        if os.path.exists(plist):
            x = input(u"[{}] exist,\n Do you want to continue? [y/n]: ".format(plist))
            if x == "y":
                is_exec = True
                service = _service_by_label(label=label)
                if service:
                    cmd_unload = CMD_UNLOAD.format(plist)
                    utils.my_print(cmd_unload)
                    os.system(cmd_unload)
                os.remove(plist)
        else:
            is_exec = True
        if is_exec:
            with open(plist, "wb") as f:
                plistlib.dump(pl, f)
            if need_load:
                _plist_load(label, plist)
            return plist
        else:
            raise RuntimeError("User Cancel")
    else:
        raise ValueError("output dir empty")


def _status_label(status: str, pid: str):
    """
    return status label
    :param status:
    :param pid:
    :return:
    """
    if pid == "-":
        return STATUS_OK
    else:
        p = int(pid)
        if p > 0:
            return utils.Color.green(STATUS_RUNNING)
        else:
            return STATUS_OK


def _label_from_plist(plist: str):
    with open(plist, "rb") as fp:
        pl = plistlib.load(fp)
    if not bool(pl):
        return None
    else:
        return pl["Label"]


def plist_list():
    """
    plist list
    :return:
    """
    result_plist = []
    result = []
    user_plists = os.listdir(USER_LAUNCH_AGENTS)
    if user_plists and len(user_plists) > 0:
        for plist in user_plists:
            if plist.endswith(".plist"):
                result_plist.append(os.path.join(USER_LAUNCH_AGENTS, plist))
    if os.access(SYSTEM_LAUNCH_AGENTS, os.R_OK):
        system_plists = os.listdir(SYSTEM_LAUNCH_AGENTS)
        if system_plists and len(system_plists) > 0:
            for plist in system_plists:
                if plist.endswith(".plist"):
                    result_plist.append(os.path.join(SYSTEM_LAUNCH_AGENTS, plist))
    serlist = _service_list()
    if len(result_plist) > 0 and len(serlist) > 0:
        result_plist.sort()
        for plist in result_plist:
            label = _label_from_plist(plist)
            if label:
                temp = None
                for ser in serlist:
                    if label == ser["label"]:
                        temp = ser
                        break
                if temp:
                    pid = ser["pid"]
                    status = _status_label(status=ser["status"], pid=pid)
                else:
                    pid = "-"
                    status = utils.Color.red(STATUS_UNLOADED)
                result.append(
                    {"pid": pid, "status": status, "label": label, "plist": plist,
                     "system": plist.startswith(SYSTEM_LAUNCH_AGENTS)})
    if len(result) > 0:
        for index, tab in enumerate(result):
            tab["index"] = index + 1
    return result


def _service_list():
    """
    service list
    :return:
    """
    result = []
    cmd_result = os.popen(cmd=CMD_LIST).readlines()
    if cmd_result and len(cmd_result) > 0:
        for line in cmd_result:
            item = line.strip().split("\t")
            if len(item) == 3:
                pid = item[0].strip()
                status = item[1].strip()
                label = item[2].strip()
                if pid.lower() != "pid" and status.lower() != "status":
                    result.append({"pid": pid, "status": status, "label": label})
    return result


def _service_by_label(label):
    """
    get service by label
    :param label:
    :return:
    """
    result = _service_list()
    service = None
    if result and len(result) > 0:
        for r in result:
            if label == r["label"]:
                service = r
                break
    return service


def _plist_by_label(label: str):
    """
    plist by label
    :param label:
    :return:
    """
    result = plist_list()
    plists = []
    if result and len(result) > 0:
        for r in result:
            if label.lower() in r["label"].lower():
                plists.append(r)
    if len(plists) != 1:
        return None
    else:
        return plists[0]


def _plist_load(label, plist):
    """
    plist load
    :param label:
    :param plist:
    :return:
    """
    cmd_load = CMD_LOAD.format(plist)
    utils.my_print(cmd_load)
    os.system(cmd_load)
    service = _service_by_label(label=label)
    if service:
        if int(service["pid"]) > 0:
            utils.my_print_green("Done[{}]".format(service["pid"]))
        else:
            utils.my_print_red("Error")
    else:
        raise RuntimeError("service empty")


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def _get_ser_by_index(index, serlist):
    """
    get ser by index
    :param index:
    :param serlist:
    :return:
    """
    ser = None
    for server in serlist:
        if index == str(server["index"]):
            ser = server
            break
    return ser


def cmd_list(args):
    """
    list
    :param args:
    :return:
    """
    tool = args.tool
    serlist = plist_list()
    if not serlist or len(serlist) == 0:
        utils.my_print_red("server list empty")
        return
    table = tp.PrettyTable(["Index", "Label", "Status", "User"])
    for ser in serlist:
        table.add_row(
            [utils.Color.green(str(ser["index"])), str(ser["label"]), str(ser["status"]),
             str(ser["system"] and utils.Color.yellow("System") or utils.Color.blue(getpass.getuser()))])
    table.set_style(16)
    table.align["Index"] = "c"
    table.align["Label"] = "l"
    table.align["Status"] = "c"
    table.align["User"] = "c"
    print(table)
    if tool:
        ser = None
        answer = True
        while answer:
            x = input(utils.Color.green("Please enter an index: "))
            s = _get_ser_by_index(x, serlist)
            if s:
                ser = s
                answer = False
            else:
                utils.my_print_red("Please enter the correct index")
        utils.my_print("[{0}]-{1}-{2}\n".format(ser["index"], ser["label"], ser["status"]))
        need_start = STATUS_UNLOADED in ser["status"]
        label = utils.Color.green("Start") if need_start else utils.Color.red("Stop")
        x = input("{0} the service [{1}] - [y/n] :".format(label, ser["label"]))
        if x == "y":
            args.label = ser["label"]
            if need_start:
                cmd_start(args)
            else:
                cmd_stop(args)
        else:
            utils.my_print_red("User Cancel")


def cmd_start(args):
    """
    start
    :param args:
    :return:
    """
    label = args.label
    ser = _plist_by_label(label=label)
    if ser:
        plist = ser["plist"]
        system = ser["system"]
        if system:
            cmd = CMD_LOAD.format(plist)
        else:
            cmd = CMD_LOAD.format(plist)
        # my_print(message=cmd)
        os.system(cmd)
        cmd_status(args)
    else:
        utils.my_print_red("Input label error")


def cmd_stop(args):
    """
    stop
    :param args:
    :return:
    """
    label = args.label
    ser = _plist_by_label(label=label)
    if ser:
        plist = ser["plist"]
        system = ser["system"]
        if system:
            cmd = CMD_UNLOAD.format(plist)
        else:
            cmd = CMD_UNLOAD.format(plist)
        # my_print(message=cmd)
        os.system(cmd)
    else:
        utils.my_print_red("Input label error")


def cmd_restart(args):
    """
    restart
    :param args:
    :return:
    """
    cmd_stop(args)
    cmd_start(args)


def cmd_status(args):
    """
    status
    :param args:
    :return:
    """
    label = args.label
    ser = _plist_by_label(label=label)
    if ser:
        utils.my_print("[{}] {}-{}".format(ser["pid"], ser["status"], ser["label"]))
    else:
        utils.my_print_red("Input label error")


def cmd_edit(args):
    """
    edit
    :param args:
    :return:
    """
    label = args.label
    editor = args.editor
    ser = _plist_by_label(label=label)
    if ser:
        os.system("{} {}".format(editor, ser["plist"]))
    else:
        utils.my_print_red("Input label error")


def cmd_rm(args):
    """
    rm
    :param args:
    :return:
    """
    label = args.label
    ser = _plist_by_label(label=label)
    if ser:
        plist = ser["plist"]
        status = ser["status"]
        if STATUS_RUNNING in status:
            utils.my_print_red("The service is running, please stop first")
        else:
            x = input(u"plist : {},\n Do you want to delete? [y/n]: ".format(utils.Color.red(plist)))
            if x == "y":
                os.remove(plist)
            else:
                utils.my_print_red("user cancel")
    else:
        utils.my_print_red("input label error")


def cmd_create(args):
    """
    create
    :param args:
    :return:
    """
    label = args.label
    editor = args.editor
    edit = args.edit
    try:
        plist = plist_build(label=label,
                            need_load=False,
                            program_arguments=["xxx", "xxx", "xxx"])
        if edit:
            os.system("{} {}".format(editor, plist))
        utils.my_print_green("Done")
    except Exception as e:
        utils.my_print_red(e)
    except KeyboardInterrupt:
        utils.my_print_red("User Interrupt")


def execute():
    """
    execute point
    :return:
    """
    if len(sys.argv) == 1:
        sys.argv.append('list')
    parser = argparse.ArgumentParser(description='Manage background services {0}'.format(version.VERSION),
                                     epilog='make it easy')
    parser.add_argument("-e", "--editor", type=str, help=u'editor default[{}]'.format(CMD_EDITOR),
                        default=CMD_EDITOR)
    subparsers = parser.add_subparsers(title=u"Available commands")
    subparsers.required = True

    parser_list = subparsers.add_parser("list",
                                        help=u"List services for the current user (or root).")
    parser_list.set_defaults(func=cmd_list)
    parser_list.add_argument("-t", "--tool", help="show tools", action='store_true', default=False)

    parser_start = subparsers.add_parser("start", help=u"Start the service [label]")
    parser_start.set_defaults(func=cmd_start)
    parser_start.add_argument("label", type=str, help=u'service [label]')

    parser_stop = subparsers.add_parser("stop", help=u"stop the service [label]")
    parser_stop.set_defaults(func=cmd_stop)
    parser_stop.add_argument("label", type=str, help=u'service [label]')

    parser_restart = subparsers.add_parser("restart", help=u"restart the service [label]")
    parser_restart.set_defaults(func=cmd_restart)
    parser_restart.add_argument("label", type=str, help=u'service [label]')

    parser_status = subparsers.add_parser("status", help=u"service [label] status")
    parser_status.set_defaults(func=cmd_status)
    parser_status.add_argument("label", type=str, help=u'service [label]')
    parser_status.add_argument('--path', help='show plist path', action='store_true', default=False)

    parser_edit = subparsers.add_parser("edit", help=u"edit service [label]")
    parser_edit.set_defaults(func=cmd_edit)
    parser_edit.add_argument("label", type=str, help=u'service [label]')

    parser_rm = subparsers.add_parser("rm", help=u"rm the service [plist]")
    parser_rm.set_defaults(func=cmd_rm)
    parser_rm.add_argument("label", type=str, help=u'service [label]')

    parser_create = subparsers.add_parser("create", help=u"create the service [plist]")
    parser_create.set_defaults(func=cmd_create)
    parser_create.add_argument("label", type=str, help=u'service [label]')
    parser_create.add_argument('--edit', help='edit service [label]', action='store_true', default=False)

    # parser args
    args = parser.parse_args()
    args.func(args)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

def execute_aria2():
    # -D : 新开启进程，不受服务管控，因此不需要添加
    try:
        plist_build(label="aria2",
                    program_arguments=["/opt/homebrew/bin/aria2c", "--enable-rpc", "--rpc-listen-all"])
    except Exception as e:
        utils.my_print_red(e)
    except KeyboardInterrupt:
        utils.my_print_red("User Interrupt")


def execute_filebrowser():
    try:
        plist_build(label="filebrowser",
                    program_arguments=["/opt/homebrew/bin/filebrowser",
                                       "-d",
                                       "/Users/seven/soft/filebrowser/filebrowser.db",
                                       "-r",
                                       "/Users/seven/Public",
                                       "-p",
                                       "8080"],
                    out_path="/Users/seven/soft/filebrowser/filebrowser.log",
                    error_path="/Users/seven/soft/filebrowser/filebrowser-error.log")
    except Exception as e:
        utils.my_print_red(e)
    except KeyboardInterrupt:
        utils.my_print_red("User Interrupt")


def execute_gitiles():
    try:
        plist_build(label="gitiles",
                    working_dir="/Users/seven/soft/gitiles",
                    program_arguments=["/Users/seven/soft/android/jdk8u312-full.jdk/bin/java",
                                       "-jar",
                                       "gitiles-v1.0.0.jar",
                                       "-d",
                                       "/Users/seven/mirror",
                                       "--home",
                                       "/Users/seven/soft/gitiles"])
    except Exception as e:
        utils.my_print_red(e)
    except KeyboardInterrupt:
        utils.my_print_red("User Interrupt")


def test():
    sys.argv.append("list")
    sys.argv.append("--tool")


if __name__ == '__main__':
    execute()
