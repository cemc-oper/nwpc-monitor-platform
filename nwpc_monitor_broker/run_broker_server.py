#!/usr/bin/env python
"""
run a simple nwpc_monitor_broker server.

Set environment variable NWPC_MONITOR_BROKER_CONFIG.
"""
import argparse
import os
import sys

if 'NWPC_MONITOR_PLATFORM_BASE' in os.environ:
    sys.path.append(os.environ['NWPC_MONITOR_PLATFORM_BASE'])


def runserver():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
DESCRIPTION
    Run nwpc monitor broker.""")

    parser.add_argument(
        "-c", "--config-file",
        help="config file path",
        required=True
    )

    args = parser.parse_args()
    os.environ['NWPC_MONITOR_BROKER_CONFIG'] = args.config_file

    from nwpc_monitor_broker import app

    app.run(
        host=app.config['BROKER_CONFIG']['host']['ip'],
        port=app.config['BROKER_CONFIG']['host']['port']
    )

if __name__ == '__main__':
    runserver()
