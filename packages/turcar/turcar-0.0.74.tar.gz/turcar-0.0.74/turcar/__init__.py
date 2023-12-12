import logging
import os.path
import platform
import signal
import sys
import time
from logging import getLogger
from typing import TYPE_CHECKING, List, Optional, cast
import tkinter
from tkinter import messagebox
import os
import requests
import psutil

from turcar.check_for_updates import CheackUpdates

from turcar.common import is_private_python, is_virtual_executable

_last_module_count = 0
_last_modules = set()

_last_time = time.time()

logger = getLogger(__name__)


def report_time(label: str) -> None:
    """
    Method for finding unwarranted imports and delays.
    """
    # return

    global _last_time, _last_module_count, _last_modules

    log_modules = True

    t = time.time()
    mod_count = len(sys.modules)
    mod_delta = mod_count - _last_module_count
    if mod_delta > 0:
        mod_info = f"(+{mod_count - _last_module_count} modules)"
    else:
        mod_info = ""
    logger.info("TIME/MODS %s %s %s", f"{t - _last_time:.3f}", label, mod_info)

    if log_modules and mod_delta > 0:
        current_modules = set(sys.modules.keys())
        logger.info("NEW MODS %s", list(sorted(current_modules - _last_modules)))
        _last_modules = current_modules

    _last_time = t
    _last_module_count = mod_count


report_time("After defining report_time")

SINGLE_INSTANCE_DEFAULT = True
BACKEND_LOG_MARKER = "turcar's backend.log"


def _get_known_folder(ID):
    # http://stackoverflow.com/a/3859336/261181
    # http://www.installmate.com/support/im9/using/symbols/functions/csidls.htm
    import ctypes.wintypes

    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, ID, 0, SHGFP_TYPE_CURRENT, buf)
    assert buf.value
    return buf.value


def _get_roaming_appdata_dir():
    return _get_known_folder(26)


def _get_local_appdata_dir():
    return _get_known_folder(28)


def _compute_turcar_user_dir():
    if os.environ.get("turcar_USER_DIR", ""):
        return os.path.expanduser(os.environ["turcar_USER_DIR"])
    elif is_portable():
        if sys.platform == "win32":
            root_dir = os.path.dirname(sys.executable)
        elif sys.platform == "darwin":
            root_dir = os.path.join(
                os.path.dirname(sys.executable), "..", "..", "..", "..", "..", ".."
            )
        else:
            root_dir = os.path.join(os.path.dirname(sys.executable), "..")
        return os.path.normpath(os.path.abspath(os.path.join(root_dir, "user_data")))
    elif is_virtual_executable(sys.executable) and not is_private_python(sys.executable):
        return os.path.join(sys.prefix, ".turcar")
    elif sys.platform == "win32":
        return os.path.join(_get_roaming_appdata_dir(), "turcar")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/turcar")
    else:
        # https://specifications.freedesktop.org/basedir-spec/latest/ar01s02.html
        data_home = os.environ.get(
            "XDG_CONFIG_HOME", os.path.expanduser(os.path.join("~", ".config"))
        )
        return os.path.join(data_home, "turcar")


def _read_configured_debug_mode():
    if not os.path.exists(CONFIGURATION_FILE):
        return False

    try:
        with open(CONFIGURATION_FILE, encoding="utf-8") as fp:
            for line in fp:
                if "debug_mode" in line and "True" in line:
                    return True
        return False
    except Exception:
        import traceback

        traceback.print_exc()
        return False


# :todo yb
def is_portable():
    # it can be explicitly declared as portable or shared ...
    portable_marker_path = os.path.join(os.path.dirname(sys.executable), "portable_turcar.ini")
    shared_marker_path = os.path.join(os.path.dirname(sys.executable), "shared_turcar.ini")

    if os.path.exists(portable_marker_path) and not os.path.exists(shared_marker_path):
        return True
    elif not os.path.exists(portable_marker_path) and os.path.exists(shared_marker_path):
        return False

    # ... or it becomes implicitly portable if it's on a removable drive
    abs_location = os.path.abspath(__file__)
    if sys.platform == "win32":
        drive = os.path.splitdrive(abs_location)[0]
        if drive.endswith(":"):
            from ctypes import windll

            return windll.kernel32.GetDriveTypeW(drive) == 2  # @UndefinedVariable
        else:
            return False
    elif sys.platform == "darwin":
        # not exact heuristics
        return abs_location.startswith("/Volumes/")
    else:
        # not exact heuristics
        return abs_location.startswith("/media/") or abs_location.startswith("/mnt/")


_turcar_VERSION = None


def get_version():
    global _turcar_VERSION
    if _turcar_VERSION:
        return _turcar_VERSION
    try:
        package_dir = os.path.dirname(sys.modules["turcar"].__file__)
        with open(os.path.join(package_dir, "VERSION"), encoding="ASCII") as fp:
            _turcar_VERSION = fp.read().strip()
            return _turcar_VERSION
    except Exception:
        return "0.0.0"


turcar_USER_DIR = _compute_turcar_user_dir()
CONFIGURATION_FILE = os.path.join(turcar_USER_DIR,
                                  "configuration.ini")  # '/Users/yubo/Library/turcar/configuration.ini'
_CONFIGURED_DEBUG = _read_configured_debug_mode()

_IPC_FILE = None

# todo yb
'''
其目的是获取用于进程间通信（IPC）的文件路径。
这个文件路径用于在不同的 turcar 实例之间传递信息
'''


def get_ipc_file_path():
    global _IPC_FILE
    if _IPC_FILE:
        return _IPC_FILE

    if sys.platform == "win32":
        base_dir = _get_local_appdata_dir()
    else:
        base_dir = os.environ.get("XDG_RUNTIME_DIR")
        if not base_dir or not os.path.exists(base_dir):
            base_dir = os.environ.get("TMPDIR")

    if not base_dir or not os.path.exists(base_dir):
        base_dir = turcar_USER_DIR

    for name in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        if name in os.environ:
            username = os.environ.get(name)
            break
    else:
        username = os.path.basename(os.path.expanduser("~"))

    ipc_dir = os.path.join(base_dir,
                           "turcar-%s" % username)  # '/var/folders/7k/wf8jrd_506q1pw8hg21zvwm00000gn/T/turcar-yubo'
    os.makedirs(ipc_dir, exist_ok=True)

    if not sys.platform == "win32":
        os.chmod(ipc_dir, 0o700)

    _IPC_FILE = os.path.join(ipc_dir, "ipc.sock")
    print("get_ipc_file_path")
    current_os = platform.system()
    print(current_os)
    print(_IPC_FILE)
    return _IPC_FILE


def _check_welcome():
    from turcar import misc_utils

    if not os.path.exists(CONFIGURATION_FILE) and not misc_utils.running_on_rpi():
        from turcar.config import ConfigurationManager
        from turcar.first_run import FirstRunWindow

        mgr = ConfigurationManager(CONFIGURATION_FILE)

        win = FirstRunWindow(mgr)
        win.mainloop()

        if win.ok and sys.platform == "darwin":
            macos_app_path = _get_macos_app_path()
            if macos_app_path:
                # Shouldn't proceed to the main window in the same process, as TkAqua will crash on opening a menu
                # or saving a file (https://github.com/turcar/turcar/issues/2860).
                # Let's restart.
                print("Restarting", macos_app_path)
                os.system(f"open -n '{macos_app_path}'")
                sys.exit(0)

        return win.ok
    else:
        return True


def _get_macos_app_path() -> Optional[str]:
    if sys.platform != "darwin":
        return None
    orig_argv = _get_orig_argv()
    if not orig_argv:
        return None

    if orig_argv[0].endswith("turcar.app/Contents/MacOS/turcar"):
        return orig_argv[0][: -len("/Contents/MacOS/turcar")]

    return None


def prevent_multiple_instances(process_name):
    # 获取当前操作系统
    current_os = platform.system()
    if current_os == "Windows":
        user_id = os.getlogin()
    else:  # 默认为Ubuntu或其他Linux发行版
        # 获取当前用户ID
        user_id = os.geteuid()
    # 获取所有进程列表
    for proc in psutil.process_iter():
        try:
            # 获取进程相关信息
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])

            # 如果进程属于当前用户并且名称匹配，杀死进程
            if pinfo['name'] == process_name and pinfo['username'] == user_id:
                os.kill(pinfo['pid'], signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def launch():
    # import runpy
    # 调用函数，传入要禁止重复的Python程序名称
    try:

        # 获取当前Python程序的进程ID
        pid = psutil.Process().pid
        print("当前进程ID:", pid)

        # 获取当前Python程序的进程信息
        process = psutil.Process(pid)
        print("进程名称:", process.name())
        print("父进程ID:", process.ppid())
        print("命令行:", process.cmdline())
        print("内存使用量:", process.memory_info().rss)
        print("CPU使用率:", process.cpu_percent())

        prevent_multiple_instances('python.exe')
    except Exception as e:
        root = tkinter.Tk()
        root.withdraw()
        return messagebox.showerror('正在打开中', '请勿重复打开')

    try:
        response = requests.get('https://pypi.org/pypi/turcar/json')
        if response.status_code == 200:
            data = response.json()
            # 获取项目最新版本
            version = data["info"]["version"]
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 指定要获取内容的文件名
            file_name = "VERSION"
            # 拼接文件路径
            file_path = os.path.join(current_dir, file_name)
            # 空校验
            if os.path.exists(file_path):
                # 打开文件并读取内容
                with open(file_path, 'r') as file:
                    content = file.read()
                    # print(f"File: {file_name}")
                    print(f"VERSION: {content}")
                    # 处理读取文件中的回车情况
                    if version != content.strip():
                        # if current_os == "Windows":
                        #     pass
                        # else:  # 默认为Ubuntu或其他Linux发行版
                        cheack = CheackUpdates()
                        # 添加判断是为了区分，否则会点什么都退出
                        if cheack.cheack_version(version) == True:
                            return
        else:
            # 后端返回不等于两百的逻辑
            pass

    except Exception as e:
        root = tkinter.Tk()
        root.withdraw()
        return messagebox.showerror('无网络连接', '请按ctrl + q,并联系家长进行网络配置')

    if sys.executable.endswith("turcar.exe"):
        # otherwise some library may try to run its subprocess with turcar.exe
        # NB! Must be pythonw.exe not python.exe, otherwise Runner thinks console
        # is already allocated.
        sys.executable = sys.executable[: -len("turcar.exe")] + "pythonw.exe"

    set_dpi_aware()

    # try:
    #     runpy.run_module("turcar.customize", run_name="__main__")
    # except ImportError as e:
    #     pass

    # messagebox.showinfo('成功了', '其实已经成功了')
    prepare_turcar_user_dir()
    _configure_frontend_logging()

    if not _check_welcome():
        return 0

    if _should_delegate():
        try:
            _delegate_to_existing_instance(sys.argv[1:])
            print("Delegated to an existing turcar instance. Exiting now.")
            return 0
        except Exception:
            import traceback

            traceback.print_exc()

    # Did not or could not delegate

    try:
        from turcar import workbench

        bench = workbench.Workbench()

        # if sys.platform == "linux":
        #     bench.resizable(width=False, height=False)
        #     bench.attributes('-fullscreen', True)  # 隐藏标题栏
        #     bench.geometry("{0}x{1}+0+0".format(bench.winfo_screenwidth(), bench.winfo_screenheight()))

        bench.mainloop()
        return 0

    except Exception:
        import tkinter as tk
        import traceback
        from logging import exception

        exception("Internal launch or mainloop error")
        from turcar import ui_utils

        dlg = ui_utils.LongTextDialog("Internal error", traceback.format_exc())
        ui_utils.show_dialog(dlg, tk._default_root)
        return -1
    finally:
        runner = get_runner()
        if runner is not None:
            runner.destroy_backend()

    return 0


def prepare_turcar_user_dir():
    if not os.path.exists(turcar_USER_DIR):
        os.makedirs(turcar_USER_DIR, mode=0o700, exist_ok=True)

        # user_dir_template is a post-installation means for providing
        # alternative default user environment in multi-user setups
        template_dir = os.path.join(os.path.dirname(__file__), "user_dir_template")

        if os.path.isdir(template_dir):
            import shutil

            def copy_contents(src_dir, dest_dir):
                # I want the copy to have current user permissions
                for name in os.listdir(src_dir):
                    src_item = os.path.join(src_dir, name)
                    dest_item = os.path.join(dest_dir, name)
                    if os.path.isdir(src_item):
                        os.makedirs(dest_item, mode=0o700)
                        copy_contents(src_item, dest_item)
                    else:
                        shutil.copyfile(src_item, dest_item)
                        os.chmod(dest_item, 0o600)

            copy_contents(template_dir, turcar_USER_DIR)


def _should_delegate():
    if not os.path.exists(get_ipc_file_path()):
        # no previous instance
        return False

    from turcar.config import try_load_configuration

    configuration_manager = try_load_configuration(CONFIGURATION_FILE)
    configuration_manager.set_default("general.single_instance", SINGLE_INSTANCE_DEFAULT)
    return configuration_manager.get_option("general.single_instance")


def _delegate_to_existing_instance(args):
    import socket

    from turcar import workbench

    transformed_args = []
    for arg in args:
        if not arg.startswith("-"):
            arg = os.path.abspath(arg)

        transformed_args.append(arg)

    try:
        sock, secret = _create_client_socket()
    except Exception:
        # Maybe the lock is abandoned or the content is corrupted
        try:
            os.remove(get_ipc_file_path())
        except Exception:
            import traceback

            traceback.print_exc()
        raise

    data = repr((secret, transformed_args)).encode(encoding="utf_8")

    sock.settimeout(2.0)
    sock.sendall(data)
    sock.shutdown(socket.SHUT_WR)
    response = bytes([])
    while len(response) < len(workbench.SERVER_SUCCESS):
        new_data = sock.recv(2)
        if len(new_data) == 0:
            break
        else:
            response += new_data

    if response.decode("UTF-8") != workbench.SERVER_SUCCESS:
        raise RuntimeError("Unsuccessful delegation")


def _create_client_socket():
    import socket

    timeout = 2.0

    if sys.platform == "win32":
        with open(get_ipc_file_path(), "r") as fp:
            port = int(fp.readline().strip())
            secret = fp.readline().strip()

        # "localhost" can be much slower than "127.0.0.1"
        client_socket = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    else:
        client_socket = socket.socket(socket.AF_UNIX)  # @UndefinedVariable
        client_socket.settimeout(timeout)
        client_socket.connect(get_ipc_file_path())
        secret = ""

    return client_socket, secret


def _configure_frontend_logging() -> None:
    _configure_logging(get_frontend_log_file(), _choose_logging_level())


def configure_backend_logging() -> None:
    _configure_logging(get_backend_log_file(), None)


def get_backend_log_file():
    return os.path.join(turcar_USER_DIR, "backend.log")


def get_frontend_log_file():
    return os.path.join(turcar_USER_DIR, "frontend.log")


def _get_orig_argv() -> Optional[List[str]]:
    try:
        from sys import orig_argv  # since 3.10

        return sys.orig_argv
    except ImportError:
        # https://stackoverflow.com/a/57914236/261181
        import ctypes

        argc = ctypes.c_int()
        argv = ctypes.POINTER(ctypes.c_wchar_p if sys.version_info >= (3,) else ctypes.c_char_p)()
        try:
            ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(argc), ctypes.byref(argv))
        except AttributeError:
            # See https://github.com/turcar/turcar/issues/2206
            # and https://bugs.python.org/issue40910
            # This symbol is not available in turcar.exe built agains Python 3.8
            return None

        # Ctypes are weird. They can't be used in list comprehensions, you can't use `in` with them, and you can't
        # use a for-each loop on them. We have to do an old-school for-i loop.
        arguments = list()
        for i in range(argc.value):
            arguments.append(argv[i])

        return arguments


def _configure_logging(log_file, console_level=None):
    logFormatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(threadName)s] %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S"
    )

    file_handler = logging.FileHandler(log_file, encoding="UTF-8", mode="w")
    file_handler.setFormatter(logFormatter)

    main_logger = logging.getLogger("turcar")
    contrib_logger = logging.getLogger("turcarcontrib")
    pipkin_logger = logging.getLogger("pipkin")

    # NB! Don't mess with the main root logger, because (CPython) backend runs user code
    for logger in [main_logger, contrib_logger, pipkin_logger]:
        logger.setLevel(_choose_logging_level())
        logger.propagate = False  # otherwise it will be also reported by IDE-s root logger
        logger.addHandler(file_handler)

    if console_level is not None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logFormatter)
        console_handler.setLevel(console_level)
        for logger in [main_logger, contrib_logger]:
            logger.addHandler(console_handler)

    # Log most important info as soon as possible
    main_logger.info("turcar version: %s", get_version())
    main_logger.info("cwd: %s", os.getcwd())
    main_logger.info("original argv: %s", _get_orig_argv())
    main_logger.info("sys.executable: %s", sys.executable)
    main_logger.info("sys.argv: %s", sys.argv)
    main_logger.info("sys.path: %s", sys.path)
    main_logger.info("sys.flags: %s", sys.flags)

    import faulthandler

    fault_out = open(os.path.join(turcar_USER_DIR, "frontend_faults.log"), mode="w")
    faulthandler.enable(fault_out)


def get_user_base_directory_for_plugins() -> str:
    return os.path.join(turcar_USER_DIR, "plugins")


def get_sys_path_directory_containg_plugins() -> str:
    from turcar.misc_utils import get_user_site_packages_dir_for_base

    return get_user_site_packages_dir_for_base(get_user_base_directory_for_plugins())


def set_dpi_aware():
    # https://stackoverflow.com/questions/36134072/setprocessdpiaware-seems-not-to-work-under-windows-10
    # https://bugs.python.org/issue33656
    # https://msdn.microsoft.com/en-us/library/windows/desktop/dn280512(v=vs.85).aspx
    # https://github.com/python/cpython/blob/master/Lib/idlelib/pyshell.py
    if sys.platform == "win32":
        try:
            import ctypes

            PROCESS_SYSTEM_DPI_AWARE = 1
            ctypes.OleDLL("shcore").SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
        except (ImportError, AttributeError, OSError):
            pass


if TYPE_CHECKING:
    # Following imports are required for MyPy
    # http://mypy.readthedocs.io/en/stable/common_issues.html#import-cycles
    import turcar.workbench
    from turcar.running import Runner
    from turcar.shell import ShellView
    from turcar.workbench import Workbench

_workbench = None  # type: Optional[Workbench]


def get_workbench() -> "Workbench":
    return cast("Workbench", _workbench)


_runner = None  # type: Optional[Runner]


def set_logging_level(level=None):
    if level is None:
        level = _choose_logging_level()

    logging.getLogger("turcar").setLevel(level)


def _choose_logging_level():
    if in_debug_mode():
        return logging.DEBUG
    else:
        return logging.INFO


def in_debug_mode() -> bool:
    # Value may be something other than string when it is set in Python code
    return (
            os.environ.get("turcar_DEBUG", False)
            in [
                "1",
                1,
                "True",
                True,
                "true",
            ]
            or _CONFIGURED_DEBUG
    )


def get_runner() -> "Runner":
    return cast("Runner", _runner)


def get_shell() -> "ShellView":
    return cast("ShellView", get_workbench().get_view("ShellView"))


report_time("After loading turcar module")
