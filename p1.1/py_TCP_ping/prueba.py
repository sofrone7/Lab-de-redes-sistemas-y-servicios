#!/usr/bin/env python3

import sys
import signal
import time

stop = 0

def CtrlCHand(sig, frame):
	stop = 1

signal.signal(signal.SIGINT, CtrlCHand)

while stop != 1:
	print('1 seg')
	time.sleep(1)
