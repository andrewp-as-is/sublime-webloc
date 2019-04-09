#!/usr/bin/env python
import sublime
import sublime_plugin
import plistlib
import subprocess
import sys
import webbrowser

"""
MacOS customize:
/usr/bin/open                           default
path/to/custom/open                     custom
export PATH=path/to/custom:$PATH        ~/.bashrc
"""

MAC = "darwin" in sys.platform.lower()
LINUX = "linux" in sys.platform.lower()
WINDOWS = "win32" in sys.platform.lower() or "cygwin" in sys.platform.lower()


class WeblocCommand(sublime_plugin.WindowCommand):
    @property
    def path(self):
        return sublime.active_window().active_view().file_name()

    @property
    def url(self):
        plist = plistlib.readPlist(self.path)
        return plist.URL

    def browse_mac(self):
        args = ["open", self.url]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        code = process.returncode
        if code != 0:
            raise OSError(stderrdata.decode("utf-8"))

    def browse(self):
        if MAC:
            self.browse_mac()
        else:
            webbrowser.open(self.url)

    def run(self):
        try:
            self.browse()
        except Exception as e:
            msg = "%s\n%s" % (type(e), str(e))
            sublime.error_message(msg)
