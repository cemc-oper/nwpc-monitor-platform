#!/usr/bin/env python
import os
import sys

if os.environ.has_key('NWPC_MONITOR_PLATFORM_BASE'):
    sys.path.append(os.environ['NWPC_MONITOR_PLATFORM_BASE'])

from nwpc_monitor_broker import app


def runserver():
    port = 5101
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()
