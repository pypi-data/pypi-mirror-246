#
# Signal.py
# Aidlab-SDK
# Created by Szymon Gesicki on 07.11.2021.
#

from enum import IntEnum

class Signal(IntEnum):
    ecg = 0
    respiration = 1
    skin_temperature = 2
    motion = 3
    battery = 4
    activity = 5
    orientation = 6
    steps = 7
    heart_rate = 8
    sound_volume = 10
    rr = 11
    pressure = 12
    respiration_rate = 14
    body_position = 15