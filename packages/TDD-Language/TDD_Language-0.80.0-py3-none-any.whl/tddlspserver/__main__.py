"""exampleLSPServer package."""

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import logging
import os
import subprocess

from .server import tdd_server

# TODO Set up logging /usr/lib/python3.10/asyncio/log.py
#  /usr/lib/python3.10/asyncio/selector_events.py
# logging.basicConfig( filename = "tddDSL_pygls.log", level = logging.DEBUG, filemode = "w" )
logging.basicConfig(level=logging.DEBUG)


def add_arguments(parser):
    parser.prog = "TDD-Language-Server"
    parser.description = "A program for a language server based on the test driven development ocean-dsl"
    parser.epilog = "TDD-DSL Language Server"

    parser.add_argument(
        "--tcp", dest="tcp", action="store_true",
        help="Use TCP server"
    )
    parser.add_argument(
        "--ws", dest="ws", action="store_true",
        help="Use WebSocket server"
    )
    parser.add_argument(
        "--host", dest="host", default="127.0.0.1",
        help="Bind to this address"
    )
    parser.add_argument(
        "--port", dest="port", type=int, default=2087,
        help="Bind to this port"
    )
    parser.add_argument(
        "-f", "--fxtran", dest="fxtran", type=fxtran_executable, default="fxtran",
        help="Path to fxtran"
    )

    parser.add_argument(
        "-m", "--metric", dest="metric", default="Testability Factor",
        help="Metric to sort SuT recommendations, e.g. Testability Factor"
    )


def fxtran_executable(path: str):
    """
    Check for valid fxtran path.

    :param path: readable path to fxtran executable
    :return: valid path
    """
    # Add help argument to succeed.
    cmd: str = " ".join([path, "-help"])

    try:
        # Call 'fxtran -help' via subprocess
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise argparse.ArgumentTypeError(
            f"Did not found fxtran. command '{e.cmd}' return with error (code {e.returncode}): {e.output}. Provide valid path via -f path_to_fxtran or add fxtran to system PATH.")

    return path


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    if args.fxtran:
        # Add fxtran path
        tdd_server.fxtran_path = args.fxtran

    if args.metric:
        # Add sort metric
        tdd_server.sort_metric = args.metric

    if args.tcp:
        # Start server via tcp
        tdd_server.start_tcp(args.host, args.port)
    elif args.ws:
        # Start server via WebSocket
        tdd_server.start_ws(args.host, args.port)
    else:
        # Start server via IO
        tdd_server.start_io()


if __name__ == "__main__":
    main()
