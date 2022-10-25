import ctypes, requests, datetime, sched, time, math, json
from os import times, times_result
import re
import os

import pathlib
bob = pathlib.Path().resolve()

print(bob)
ctypes.windll.user32.SystemParametersInfoW(20, 0, f'{bob}\images\Sunny\\00635.png', 0)