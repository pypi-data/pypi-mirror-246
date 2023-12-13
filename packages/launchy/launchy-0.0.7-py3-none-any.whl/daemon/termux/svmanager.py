# -*- coding: utf-8 -*-
import os.path
import platform
import shutil

SERVICE_ROOT = "/data/data/com.termux/files/usr/var/service"

# SERVICE_ROOT = "/Users/seven/Desktop/test"

RUN_TEMPLATE = "#!/data/data/com.termux/files/usr/bin/sh\nexec {0} 2>&1"


def support_os():
    """
    support
    :return:
    """
    linux = platform.system().lower() == "linux"
    aarch64 = platform.machine().lower() == "aarch64"
    support_dir = os.path.exists(SERVICE_ROOT)
    return linux and aarch64 and support_dir


def _get_service_root():
    """
    get service root
    """
    if not os.path.exists(SERVICE_ROOT):
        os.mkdir(SERVICE_ROOT)
    if not os.path.isdir(SERVICE_ROOT):
        raise RuntimeError("Service root is not dir")
    return SERVICE_ROOT


def _read_file(file):
    """
    read file
    :param file:
    :return:
    """
    with open(file, 'r') as f:
        content = f.read()
    return content.strip()


# --------------------
def sv_list_item(index, serlist):
    """
    sv list item
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


def sv_list():
    """
    get service list
    :return:
    """
    service_root = _get_service_root()
    service_list = [x for x in os.listdir(service_root) if os.path.exists(os.path.join(SERVICE_ROOT, x, "run"))]
    result = []
    index = 1
    for service in service_list:
        service_dir = os.path.join(SERVICE_ROOT, service)
        run_file = os.path.join(service_dir, "run")
        supervise_dir = os.path.join(service_dir, "supervise")
        pid_file = os.path.join(supervise_dir, "pid")
        if os.path.exists(run_file) and os.path.exists(pid_file):
            run_content = _read_file(run_file)
            pid_content = _read_file(pid_file)
            if pid_content and int(pid_content) > 0:
                status = "Running"
            else:
                status = "Stopped"
            result.append({
                "index": index,
                "name": service,
                "run": run_content,
                "pid": pid_content,
                "status": status
            })
            index = index + 1
    return result


def sv_start(name):
    """
    start
    :param name:
    :return:
    """
    if not sv_status(name):
        cmd = "sv-enable {0}".format(name)
        return os.system(cmd)


def sv_stop(name):
    """
    stop
    :param name:
    :return:
    """
    cmd = "sv-disable {0}".format(name)
    return os.system(cmd)


def sv_restart(name):
    """
    restart
    :param name:
    :return:
    """
    if sv_status(name):
        sv_stop(name)
    return sv_start(name)


def sv_status(name):
    """
    check status
    :param name:
    :return:
    """
    pid_file = os.path.join(SERVICE_ROOT, name, "supervise", "pid")
    pid_content = _read_file(pid_file)
    return pid_content and int(pid_content) > 0


def sv_run_file(name):
    """
    sv run file
    :param name:
    :return:
    """
    return os.path.join(SERVICE_ROOT, name, "run")


def sv_edit(name, run_content):
    """
    edit service
    :param name:
    :param run_content:
    :return:
    """
    run_file = os.path.join(SERVICE_ROOT, name, "run")
    with open(run_file, 'w') as f:
        f.write(run_content)


def sv_create(name, run_content):
    """
    sv create
    :param name:
    :param run_content:
    :return:
    """
    service_dir = os.path.join(SERVICE_ROOT, name)
    if os.path.exists(service_dir):
        raise RuntimeError("service exist")
    os.mkdir(service_dir)
    run_file = os.path.join(service_dir, "run")
    with open(run_file, 'w') as f:
        f.write(RUN_TEMPLATE.format(run_content))


def sv_rm(name):
    """
    sv rm
    :param name:
    :return:
    """
    if sv_status(name=name):
        sv_stop(name)
    service_dir = os.path.join(SERVICE_ROOT, name)
    shutil.rmtree(service_dir)
