#!python3

import os
import subprocess
import sys
import argparse
import distutils.sysconfig

def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--listen' , action='store', dest='listen_address', default='127.0.0.1:4013', help='')
    parser.add_argument('--datadir', action='store', dest='data_dir'      , default='/var/lib/adsd' , help='')
    args = parser.parse_args()

    
    env = dict(os.environ)

    uwsgi_bin = os.path.join(distutils.sysconfig.get_config_var('prefix'),'bin', 'uwsgi')
    
    num_workers = 5

    uwsgi_args = [ 
        uwsgi_bin,
        '-s', '/tmp/adsd.sock' ,
        '--manage-script-name',
        '--mount', '/=ads.server.adsd:app',
        '--http', args.listen_address, #'127.0.0.1:4013',
        '-p', str(num_workers),
        '-M',
        
        #'--master-fifo', '/tmp/adsd.fifo'
    ]

    if 'VIRTUAL_ENV' in os.environ:
        uwsgi_args += [ '--virtualenv', os.environ['VIRTUAL_ENV'] ]
        
    #uwsgi_args +=  [
    #    '--pyargv', 'prova 1 2 3'
    #]
    
    env['CONFIG_LISTEN_ADDRESS'] = args.listen_address
    env['CONFIG_DATA_DIR'      ] = args.data_dir
    
    print(uwsgi_args)
    
    os.execve(uwsgi_bin, uwsgi_args, env)


if __name__ == "__main__":
    main()
