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

from .utils import format_environment


class ProxyConfig(dict):
    '''
    Hold the client's proxy configuration
    '''
    @property
    def http(self):
        return self.get('http')

    @property
    def https(self):
        return self.get('https')

    @property
    def ftp(self):
        return self.get('ftp')

    @property
    def no_proxy(self):
        return self.get('no_proxy')

    @staticmethod
    def from_dict(config):
        '''
        Instantiate a new ProxyConfig from a dictionary that represents a
        client configuration, as described in `the documentation`_.

        .. _the documentation:
            https://docs.docker.com/network/proxy/#configure-the-docker-client
        '''
        return ProxyConfig(
            http=config.get('httpProxy'),
            https=config.get('httpsProxy'),
            ftp=config.get('ftpProxy'),
            no_proxy=config.get('noProxy'),
        )

    def get_environment(self):
        '''
        Return a dictionary representing the environment variables used to
        set the proxy settings.
        '''
        env = {}
        if self.http:
            env['http_proxy'] = env['HTTP_PROXY'] = self.http
        if self.https:
            env['https_proxy'] = env['HTTPS_PROXY'] = self.https
        if self.ftp:
            env['ftp_proxy'] = env['FTP_PROXY'] = self.ftp
        if self.no_proxy:
            env['no_proxy'] = env['NO_PROXY'] = self.no_proxy
        return env

    def inject_proxy_environment(self, environment):
        '''
        Given a list of strings representing environment variables, prepend the
        environment variables corresponding to the proxy settings.
        '''
        if not self:
            return environment

        proxy_env = format_environment(self.get_environment())
        if not environment:
            return proxy_env
        # It is important to prepend our variables, because we want the
        # variables defined in "environment" to take precedence.
        return proxy_env + environment

    def __str__(self):
        return 'ProxyConfig(http={0}, https={1}, ftp={2}, no_proxy={3})'.format(
            self.http, self.https, self.ftp, self.no_proxy)
