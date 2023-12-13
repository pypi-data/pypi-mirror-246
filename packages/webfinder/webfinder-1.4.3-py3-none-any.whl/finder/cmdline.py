# -*- coding: utf-8 -*-
"""
Cmd line parser
"""
import sys

from finder import utils
from finder.server import cmd_http_server

if __name__ == '__main__':
    """
    cli main
    """
    # sys.argv.append('--user')
    # sys.argv.append('admin')
    # sys.argv.append('--password')
    # sys.argv.append('pass')

    sys.argv.append('--hidden')
    sys.argv.append('-r')
    sys.argv.append('-q')
    sys.argv.append('-u')
    sys.argv.append('-m')
    sys.argv.append('--zip')
    #
    sys.argv.append('-d')
    sys.argv.append(utils.get_home())
    # sys.argv.append('--help')
    cmd_http_server()
