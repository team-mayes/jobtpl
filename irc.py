#!/usr/bin/python

from optparse import OptionParser
import shutil
import os.path
import sys
from string import Template

def get_tpl(fname):
    tplfile = open(fname, 'r')
    tpl = Template(tplfile.read())
    tplfile.close()
    return tpl

def write_tpl(tpl, tgt, params):
    # Using safe as the namespace is polluted in some envs
    result= tpl.safe_substitute(params)
    comfile = open(tgt, 'w')
    comfile.write(result)
    comfile.close()

def fill_opts(chk, opts, direct):
    tpl_params = dict()
    split_chk = os.path.splitext(chk)
    basename = split_chk[0] + "irc" + direct[0]
    tpl_params['basechk'] = chk 
    tpl_params['chkfile'] = basename + split_chk[1]
    tpl_params['comfile'] = basename + '.com'
    tpl_params['logfile'] = basename + '.log'
    tpl_params['jobfile'] = basename + '.job'
    tpl_params['direction'] = direct
        
    return tpl_params

def copy_chk(params, comtpl, jobtpl):
    shutil.copy2(params['basechk'], params['chkfile'])
    write_tpl(comtpl, params['comfile'], params)
    write_tpl(jobtpl, params['jobfile'], params)    

def parse_cmdline(args):
    usage = "usage: %prog [options] checkfile"
    parser = OptionParser(usage=usage)
    parser.add_option('-C', '--comtpl', help='.com template file', default='irccomtpl')
    parser.add_option('-j', '--jobtpl', help='.job template file', default='jobtpl')
    
    (options, args) = parser.parse_args()
    if (len(args) == 0):
        sys.stderr.write("Check file required\n")
        parser.print_help()
        parser.exit(-1)
    
    return (options, args[0])

def run(opts, chk):
    comtpl = get_tpl(opts.comtpl)
    jobtpl = get_tpl(opts.jobtpl)
    copy_chk(fill_opts(chk, opts, 'forward'), comtpl, jobtpl)
    copy_chk(fill_opts(chk, opts, 'reverse'), comtpl, jobtpl)

if __name__ == '__main__':
    opts, chk = parse_cmdline(sys.argv[1:])
    run(opts, chk)