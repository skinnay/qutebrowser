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

import sys

import pytest_bdd as bdd


if not hasattr(sys, 'frozen'):
    bdd.scenarios('.')


@bdd.given(bdd.parsers.parse("I set {sect} -> {opt} to {value}"))
def set_setting(quteproc, sect, opt, value):
    quteproc.set_setting(sect, opt, value)


@bdd.given(bdd.parsers.parse("I open {path}"))
def open_path(quteproc, path):
    quteproc.open_path(path, new_tab=True)


@bdd.when(bdd.parsers.parse("I open {path}"))
def open_path_when(quteproc, path):
    quteproc.open_path(path)


@bdd.when(bdd.parsers.parse("I run {command}"))
def run_command(quteproc, command):
    quteproc.send_cmd(command)


@bdd.when(bdd.parsers.parse("I reload"))
def reload(qtbot, httpbin, quteproc, command):
    with qtbot.waitSignal(httpbin.new_request, raising=True):
        quteproc.send_cmd(':reload')


@bdd.then(bdd.parsers.parse("{path} should be loaded"))
def path_should_be_loaded(httpbin, path):
    requests = httpbin.get_requests()
    assert requests[-1] == httpbin.Request('GET', '/' + path)


@bdd.then(bdd.parsers.parse("The requests should be:\n{pages}"))
def list_of_loaded_pages(httpbin, pages):
    requests = [httpbin.Request('GET', '/' + path.strip())
                for path in pages.split('\n')]
    assert httpbin.get_requests() == requests


@bdd.then(bdd.parsers.parse('the error "{msg}" should be shown.'))
def expect_error(quteproc, msg):
    quteproc.mark_expected(category='message', loglevel='ERROR', msg=msg)
