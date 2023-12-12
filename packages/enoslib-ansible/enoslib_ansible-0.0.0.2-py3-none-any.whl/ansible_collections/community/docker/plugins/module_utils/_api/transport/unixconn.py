# -*- coding: utf-8 -*-
# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import socket

from ansible.module_utils.six import PY2

from .basehttpadapter import BaseHTTPAdapter
from .. import constants

from .._import_helper import HTTPAdapter, urllib3, urllib3_connection


RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer


class UnixHTTPConnection(urllib3_connection.HTTPConnection, object):

    def __init__(self, base_url, unix_socket, timeout=60):
        super(UnixHTTPConnection, self).__init__(
            'localhost', timeout=timeout
        )
        self.base_url = base_url
        self.unix_socket = unix_socket
        self.timeout = timeout
        self.disable_buffering = False

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.unix_socket)
        self.sock = sock

    def putheader(self, header, *values):
        super(UnixHTTPConnection, self).putheader(header, *values)
        if header == 'Connection' and 'Upgrade' in values:
            self.disable_buffering = True

    def response_class(self, sock, *args, **kwargs):
        if PY2:
            # FIXME: We may need to disable buffering on Py3 as well,
            # but there's no clear way to do it at the moment. See:
            # https://github.com/docker/docker-py/issues/1799
            kwargs['buffering'] = not self.disable_buffering

        return super(UnixHTTPConnection, self).response_class(sock, *args, **kwargs)


class UnixHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    def __init__(self, base_url, socket_path, timeout=60, maxsize=10):
        super(UnixHTTPConnectionPool, self).__init__(
            'localhost', timeout=timeout, maxsize=maxsize
        )
        self.base_url = base_url
        self.socket_path = socket_path
        self.timeout = timeout

    def _new_conn(self):
        return UnixHTTPConnection(
            self.base_url, self.socket_path, self.timeout
        )


class UnixHTTPAdapter(BaseHTTPAdapter):

    __attrs__ = HTTPAdapter.__attrs__ + ['pools',
                                         'socket_path',
                                         'timeout',
                                         'max_pool_size']

    def __init__(self, socket_url, timeout=60,
                 pool_connections=constants.DEFAULT_NUM_POOLS,
                 max_pool_size=constants.DEFAULT_MAX_POOL_SIZE):
        socket_path = socket_url.replace('http+unix://', '')
        if not socket_path.startswith('/'):
            socket_path = '/' + socket_path
        self.socket_path = socket_path
        self.timeout = timeout
        self.max_pool_size = max_pool_size
        self.pools = RecentlyUsedContainer(
            pool_connections, dispose_func=lambda p: p.close()
        )
        super(UnixHTTPAdapter, self).__init__()

    def get_connection(self, url, proxies=None):
        with self.pools.lock:
            pool = self.pools.get(url)
            if pool:
                return pool

            pool = UnixHTTPConnectionPool(
                url, self.socket_path, self.timeout,
                maxsize=self.max_pool_size
            )
            self.pools[url] = pool

        return pool

    def request_url(self, request, proxies):
        # The select_proxy utility in requests errors out when the provided URL
        # doesn't have a hostname, like is the case when using a UNIX socket.
        # Since proxies are an irrelevant notion in the case of UNIX sockets
        # anyway, we simply return the path URL directly.
        # See also: https://github.com/docker/docker-py/issues/811
        return request.path_url
