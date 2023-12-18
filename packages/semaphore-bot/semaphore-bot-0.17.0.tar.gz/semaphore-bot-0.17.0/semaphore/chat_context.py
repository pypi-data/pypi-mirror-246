#!/usr/bin/env python
#
# Semaphore: A simple (rule-based) bot library for Signal Private Messenger.
# Copyright (C) 2020-2023 Lazlo Westerhof <semaphore@lazlo.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""This module contains an object that represents the context of a chat."""
from __future__ import annotations

from typing import Any, Dict, Match, TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import Bot
    from .job_queue import JobQueue
    from .message import Message


class ChatContext(object):
    """This object represents the context of a chat."""

    def __init__(self,
                 message: Message,
                 match: Match,
                 job_queue: JobQueue,
                 bot: Bot) -> None:
        self.message: Message = message
        self.match: Match = match
        self.job_queue: JobQueue = job_queue
        self.bot: Bot = bot
        self.data: Dict[str, Any] = {}
