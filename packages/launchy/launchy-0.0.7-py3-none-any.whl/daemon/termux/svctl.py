# -*- coding: utf-8 -*-
import argparse
import os
import sys

import prettytable as tp

from daemon import utils
from daemon import version
from daemon.termux import svmanager
from daemon.utils import Color


def cmd_list(args):
    show_tool = args.tool
    result = svmanager.sv_list()
    if len(result) == 0:
        utils.my_print_red("service empty")
        return
    table = tp.PrettyTable(["Index", "Label", "Pid", "Status"])
    for item in result:
        pid = str(item["pid"])
        if not pid:
            pid = "-"
        else:
            pid = Color.green(pid)
        status = str(item["status"])
        name = str(item["name"])
        index = str(item["index"])
        if status == "Running":
            status = Color.green(status)
            name = Color.green(name)
            index = Color.green(index)
        else:
            status = Color.red(status)

        table.add_row([index, name, pid, status])
    table.set_style(16)
    table.align["Index"] = "c"
    table.align["Label"] = "c"
    table.align["Pid"] = "c"
    table.align["Status"] = "c"
    print(table)
    if show_tool:
        ser = None
        answer = True
        while answer:
            x = input(Color.green("Please enter an index: "))
            s = svmanager.sv_list_item(x, result)
            if s:
                ser = s
                answer = False
            else:
                utils.my_print_red("Please enter the correct index")
        utils.my_print("[{0}]-{1}-{2}\n".format(ser["index"], ser["name"], ser["status"]))
        need_start = "Stopped" in ser["status"]
        label = utils.Color.green("Start") if need_start else utils.Color.red("Stop")
        x = input("{0} the service [{1}] - [y/n] :".format(label, ser["name"]))
        if x == "y":
            args.label = ser["name"]
            if need_start:
                cmd_start(args)
            else:
                cmd_stop(args)
        else:
            utils.my_print_red("User Cancel")


def cmd_start(args):
    label = args.label
    svmanager.sv_start(name=label)


def cmd_stop(args):
    label = args.label
    svmanager.sv_stop(name=label)


def cmd_restart(args):
    label = args.label
    svmanager.sv_restart(name=label)


def cmd_status(args):
    label = args.label
    if svmanager.sv_status(label):
        utils.my_print_green("Running")
    else:
        utils.my_print_red("Stop")


def cmd_edit(args):
    label = args.label
    run_file = svmanager.sv_run_file(name=label)
    os.system("vi {0}".format(run_file))


def cmd_create(args):
    try:
        name = input(Color.yellow("Please input service name: "))
        run_content = input(Color.yellow("Please input run script: "))
        svmanager.sv_create(name=name, run_content=run_content)
        utils.my_print_green("Done")
    except RuntimeError as e:
        utils.my_print_red(str(e))


def execute():
    if not svmanager.support_os():
        utils.my_print_red("Not Support")
        return
    if len(sys.argv) == 1:
        sys.argv.append('list')
    parser = argparse.ArgumentParser(description="termux services manager {0}".format(version.VERSION),
                                     epilog="make it easy")
    # sub cmd
    subparsers = parser.add_subparsers(title="Available commands")

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

    parser_edit = subparsers.add_parser("edit", help=u"edit service [label]")
    parser_edit.set_defaults(func=cmd_edit)
    parser_edit.add_argument("label", type=str, help=u'service [label]')

    parser_create = subparsers.add_parser("create", help=u"create the service [run]")
    parser_create.set_defaults(func=cmd_create)

    # parse args
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    sys.argv.append("create")
    execute()
