import ctypes
import importlib
import platform
import sys
import threading
import subprocess
from functools import cache
import regex
from flatten_everything import flatten_everything, ProtectedList

recompiled = regex.compile(r"(?:\b[a-z]+=.*?\s+(?=\w+=))")

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetExitCodeProcess.argtypes = [
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    GetExitCodeProcess.restype = ctypes.c_int
    CloseHandle.restype = ctypes.c_int

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


def killthread(threadobject):
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


@cache
def get_short_path_name(long_name):
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


class LogCatFrame:
    r"""
    Class for capturing and parsing Android device logs using ADB.

    Args:
    - adb_path (str): Path to the ADB executable.
    - device_serial (str): Serial number of the target Android device.
    - print_output (bool): Flag to control whether to print log output to the console.
    - su (bool): Flag indicating whether to use 'su' (superuser) for logcat command (default is True).
    - clear_logcat (bool): Flag indicating whether to clear existing logcat logs before starting (default is True).

    Methods:
    - __init__(self, adb_path, device_serial, print_output, su=True, clear_logcat=True):
        Initializes a LogCatFrame instance.

    - start_recording(self):
        Starts capturing Android device logs using the specified ADB path and device serial.
        If `clear_logcat` is True, it clears existing logcat logs before starting.
        The captured logs are stored in the instance's `alldata` attribute.

    - _read_stdout(self, pr):
        Internal method for reading and printing logcat output.
        Used by the `start_recording` method in a separate thread.

    - parse_all_data(self, as_pandas=False):
        Parses the captured logs into a list of dictionaries.
        If `as_pandas` is True, converts the list into a Pandas DataFrame (requires Pandas to be installed).

    - parse_activities(self):
        Parses executed activities from the captured logs.
        Returns a list of tuples containing the executed command and associated variables.

    - get_short_path_name(long_name):
        Returns the short path name for the given long file name.
        Only applicable on Windows; on other platforms, it returns the input unchanged.


    from logcatframe import LogCatFrame

    adblog = LogCatFrame(
        adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
        device_serial="emulator-5554",
        print_output=True,
        su=True,
        clear_logcat=True,
    )
    adblog.start_recording()
    df=adblog.parse_all_data(as_pandas=True)
    listoflist=adblog.parse_all_data(as_pandas=False)
    activities=adblog.parse_activities()
    from PrettyColorPrinter import add_printer # optional
    add_printer(1)
    print(df)
    print(listoflist)
    print(activities)


    # [('am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000 -n com.android.settings/.Settings -b [47,217][161,363]',
    #   [['act', 'android.intent.action.MAIN'],
    #    ['cat', '[android.intent.category.LAUNCHER]'],
    #    ['flg', '0x10200000'],
    #    ['cmp', 'com.android.settings/.Settings'],
    #    ['bnds', '[47,217][161,363] (has extras)']]),
    #  ('am start -f 0x8000 -n com.android.settings/.Settings$PowerUsageSummaryActivity',
    #   [['flg', '0x8000'],
    #    ['cmp',
    #     'com.android.settings/.Settings$PowerUsageSummaryActivity (has extras)']]),
    #  ('am start -f 0x8000 -n com.android.settings/.Settings$DisplaySettingsActivity',
    #   [['flg', '0x8000'],
    #    ['cmp',
    #     'com.android.settings/.Settings$DisplaySettingsActivity (has extras)']]),
    #  ('am start -a com.android.intent.action.SHOW_BRIGHTNESS_DIALOG -n com.android.systemui/.settings.BrightnessDialog',
    #   [['act', 'com.android.intent.action.SHOW_BRIGHTNESS_DIALOG'],
    #    ['cmp', 'com.android.systemui/.settings.BrightnessDialog']]),
    #  ('am start -f 0x8000 -n com.android.settings/.Settings$SystemDashboardActivity',
    #   [['flg', '0x8000'],
    #    ['cmp',
    #     'com.android.settings/.Settings$SystemDashboardActivity (has extras)']]),
    #  ('am start -a android.intent.action.MAIN -n com.android.settings/.SubSettings',
    #   [['act', 'android.intent.action.MAIN'],
    #    ['cmp', 'com.android.settings/.SubSettings (has extras)']])]
    """
    def __init__(
        self,
        adb_path,
        device_serial,
        print_output,
        su=True,
        clear_logcat=True,
    ):
        self.clear_logcat = clear_logcat
        self.adb_path = get_short_path_name(adb_path)
        self.su = su
        self.device_serial = device_serial
        self.alldata = []
        self.print_output = print_output
        self.pr = None

    def _read_stdout(
        self,
        pr,
    ):
        try:
            for l in iter(pr.stdout.readline, b""):
                if self.print_output:
                    print(l)
                self.alldata.append(l)
        except Exception:
            try:
                self.pr.stdout.close()
            except Exception as fe:
                sys.stderr.write(f"{fe}")
                sys.stderr.flush()

    def start_recording(self):
        if self.clear_logcat:
            _ = subprocess.run(
                f"{self.adb_path} -s {self.device_serial} shell logcat -c",
                **invisibledict,
            )
        try:
            if self.su:
                cmds = f"{self.adb_path} -s {self.device_serial} shell su -c 'logcat -D -b all -v --format=long descriptive epoch monotonic printable uid usec UTC year zone'"

            else:
                cmds = f"{self.adb_path} -s {self.device_serial} shell logcat -D -b all -v --format=long descriptive epoch monotonic printable uid usec UTC year zone"

            pr = subprocess.Popen(
                cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                bufsize=0,
                **invisibledict,
            )
            t3 = threading.Thread(target=self._read_stdout, kwargs={"pr": pr})
            t3.start()
            input("Press ENTER to stop")
            killall(
                pr,
                t3,
            )
        except Exception as fe:
            sys.stderr.write(f"{fe}")
            sys.stderr.flush()

    def parse_all_data(self, as_pandas=False):
        d = [
            a[-1][:-1] + [q.strip() for q in a[-1][-1].split(":", maxsplit=1)]
            for a in (
                flatten_everything(
                    [
                        [
                            ProtectedList(
                                [zz.decode("utf-8", "ignore").split(maxsplit=9)]
                            )
                            for zz in [
                                y.splitlines()[0].rsplit(maxsplit=1)[-1]
                                + b" "
                                + str(uni).encode()
                                + b" "
                                + str(uni2).encode()
                                + b" "
                                + z
                                for uni2, z in enumerate(y.splitlines()[1:])
                                if z
                            ]
                        ]
                        for uni, y in enumerate(
                            b"\n".join(self.alldata).split(b"--------- ")
                        )
                    ]
                )
            )
        ]

        if as_pandas:
            try:
                pd = importlib.import_module("pandas")
                return pd.DataFrame(
                    d,
                    columns=[
                        "aa_event",
                        "aa_id",
                        "aa_subid",
                        "aa_date",
                        "aa_time",
                        "aa_t1",
                        "aa_t2",
                        "aa_t3",
                        "aa_description",
                        "aa_key",
                        "aa_value",
                    ],
                )
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()
        return d

    def parse_activities(self):
        df = self.parse_all_data(as_pandas=False)
        executed_activities = []
        for k in df:
            try:
                if k[-1].startswith("START"):
                    q = k[-1]
                    q2 = q.split("{", maxsplit=1)[-1].rsplit("}", maxsplit=1)[0]
                    allvars = [
                        h.strip().split("=", maxsplit=1)
                        for h in (recompiled.findall(q2 + " aaaa="))
                    ]
                    wholecommand = "am start "
                    for a in allvars:
                        a0 = a[0][:1]
                        wholecommand = (
                            wholecommand
                            + f'-{a0 if a[0] != "cmp" else "n"} {a[1].strip("[]") if  a[0] =="cat" else a[1]  } '
                        )
                    executed_activities.append(
                        (wholecommand.replace(" (has extras)", "").strip(), allvars)
                    )
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()
        return executed_activities


def killall(*args):
    for arg in args:
        try:
            arg.kill()
        except Exception:
            try:
                killthread(arg)
            except Exception:
                pass
