# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Test testprocess.Process."""

import sys

import pytest
from PyQt5.QtCore import QProcess

import testprocess

pytestmark = [pytest.mark.not_frozen]


class Line:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return 'Line({!r})'.format(self.data)


class PythonProcess(testprocess.Process):

    """A testprocess which runs the given Python code."""

    def __init__(self):
        super().__init__()
        self.proc.setReadChannel(QProcess.StandardOutput)
        self.code = None

    def _parse_line(self, line):
        print("LINE: {}".format(line))
        if line.strip() == 'ready':
            self.ready.emit()
        return Line(line)

    def _executable_args(self):
        return (sys.executable, ['-c', 'import sys; print("ready"); sys.stdout.flush(); ' + self.code])


@pytest.yield_fixture
def pyproc():
    proc = PythonProcess()
    yield proc
    proc.terminate()


def test_wait_for(pyproc):
    pyproc.code = "import time; time.sleep(0.5); print('foobar')"
    pyproc.start()
    pyproc.wait_for(data="foobar")
