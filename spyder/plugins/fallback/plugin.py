# -*- coding: utf-8 -*-

# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Fallback completion plugin.

Wraps FallbackActor to provide compatibility with SpyderCompletionPlugin API.
"""

# Standard library imports
import logging

# Local imports
from spyder.api.completion import SpyderCompletionPlugin
from spyder.plugins.fallback.actor import FallbackActor


logger = logging.getLogger(__name__)


class FallbackPlugin(SpyderCompletionPlugin):
    COMPLETION_CLIENT_NAME = 'fallback'

    def __init__(self, parent):
        SpyderCompletionPlugin.__init__(parent)
        self.fallback_actor = FallbackActor(self)
        self.fallback_actor.sig_fallback_ready.connect(
            lambda: self.sig_plugin_ready.emit(self.COMPLETION_CLIENT_NAME))
        self.fallback_actor.sig_set_tokens.connect(self.sig_response_ready)
        self.started = False
        self.requests = {}

    def start(self):
        if not self.started:
            self.fallback_actor.start()
            self.started = True

    def shutdown(self):
        if self.started:
            self.fallback_actor.stop()

    def send_request(self, language, req_type, req, req_id=None):
        request = {
            'type': req_type,
            'file': req['file'],
            'id': req_id,
            'msg': req
        }
        self.fallback_actor.sig_mailbox.emit(request)
