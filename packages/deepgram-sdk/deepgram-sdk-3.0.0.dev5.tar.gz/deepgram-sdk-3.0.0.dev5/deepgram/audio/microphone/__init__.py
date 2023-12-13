# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pyaudio
import logging, verboselogs

from .microphone import Microphone
from .constants import LOGGING, FORMAT, CHANNELS, RATE, CHUNK


def microphone(
    push_callback,
    verbose=LOGGING,
    format=FORMAT,
    rate=RATE,
    chunk=CHUNK,
    channels=CHANNELS,
):
    return Microphone(push_callback, verbose, format, rate, chunk, channels)
