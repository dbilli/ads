#!python3

import os
import subprocess
import sys
import argparse
import distutils.sysconfig

LISTEN_ADDRESS = '127.0.0.1:4013'
DATA_DIR       = '/var/lib/adsd'
LOG_FILE       = '/var/log/adsd.log'
NUM_WORKERS    = 5


# IMPORTANT: Do not change name because shell command 
#      ads-daemon -----> ads.server.launcher:main
def main():

    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('-D'       , action='store_true', dest='debug_mode'    , default=False           ,           help='Enable debug mode.')
    parser.add_argument('--listen' , action='store'     , dest='listen_address', default=LISTEN_ADDRESS  , type=str, help='Listen address <ip>:<port>. (default: %s)' % (LISTEN_ADDRESS))
    parser.add_argument('--datadir', action='store'     , dest='data_dir'      , default=DATA_DIR        , type=str, help='Temporary directory for data. (default: %s)' % (DATA_DIR))
    parser.add_argument('--logfile', action='store'     , dest='logfile'       , default=LOG_FILE        , type=str, help='Log file. (default: %s)' % (LOG_FILE))
    parser.add_argument('--workers', action='store'     , dest='workers'       , default=NUM_WORKERS     , type=int, help='Number of workers. (default: %s)' % (NUM_WORKERS))
    args = parser.parse_args()

    # Locate where uWSGI executable is
    uwsgi_bin = os.path.join(distutils.sysconfig.get_config_var('prefix'),'bin', 'uwsgi')

    # Prepare WSGI args    
    uwsgi_args = [ 
        uwsgi_bin,

        '--http', args.listen_address,
        '-p', str(args.workers),

        #'-s', '/tmp/adsd.sock' ,

        # tell uWSGI to rewrite PATH_INFO and SCRIPT_NAME according to mount-points
        '--manage-script-name',
        
        # Just ONE Flask application (app) at '/' prefix
        '--mount', '/=ads.server.adsd:app',

        # enable master process.  it allows graceful reloading, exports statistics and dozens of other things
        '-M',
        #'--master-fifo', '/tmp/adsd.fifo',

        #'--logformat', '%(ctime) %(pid)[%(wid)]: request=%(rsize) response=%(size) status=%(status) ',
        '--logger', 'file:%s' % (args.logfile),
    ]
    
    if args.debug_mode:
        uwsgi_args += [
            '--logger', 'stdio',
        ]

    # We are inside a virtualenv? Run uwsgi inside the same virtualenv
    if 'VIRTUAL_ENV' in os.environ:
        uwsgi_args += [ '--virtualenv', os.environ['VIRTUAL_ENV'] ]

    #        
    # Pass settings to Flask in the environment (and not on command line with --pyargv)
    #
    env = dict(os.environ)
    env['CONFIG_LISTEN_ADDRESS'] = args.listen_address
    env['CONFIG_DATA_DIR'      ] = args.data_dir
    env['CONFIG_DEBUG_MODE'    ] = 'on' if args.debug_mode else ''
    
    if args.debug_mode:
        print("Executing:", ' '.join(uwsgi_args))
    
    os.execve(uwsgi_bin, uwsgi_args, env)


if __name__ == "__main__":
    main()
