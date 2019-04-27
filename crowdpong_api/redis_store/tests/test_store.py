#!/usr/bin/env python
#
#  Copyright (c) 2018 Red Hat, Inc.  <bowe@redhat.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
"""
__author__ = 'Bowe Strickland <bowe@redhat.com>'
__docformat__ = 'restructuredtext'

import logging; log = logging.getLogger(__name__)
DEBUG = log.debug; INFO = log.info; WARN = log.warning; ERROR = log.error
#logging.basicConfig(level=logging.INFO)

import pytest
from ..store import RedisStore

@pytest.fixture
def redis():
    r = RedisStore(name="unittest")
    yield r
    r._destroy()


def test_store(redis):
    redis['foo'] = "bar"
    assert redis['foo'] == "bar"

def test_missing(redis):
    with pytest.raises(KeyError):
        redis['foo'] == "bar"

def test_missing(redis):
    redis['foo'] = "bar"
    del redis['foo']
    with pytest.raises(KeyError):
        redis['foo'] == "bar"

def test_load(redis):
    redis['foo'] = "bar"
    redis.load()
    assert redis['foo'].decode() == "bar"

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    import sys

# vi: ts=4 expandtab

