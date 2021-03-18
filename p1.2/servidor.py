#!/usr/bin/env python3

import sys
import socket

if len(sys.argv) != 2:
  print('Usage:', sys.argv[0], '<Server Port>\n')
  
ServPort = sys.argv[1]