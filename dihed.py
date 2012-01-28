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

def fill_opts(chk, opts, dihedral, idx, direct):
    tpl_params = dict()
    split_chk = os.path.splitext(chk)
    basename = "%sd%d%s" % (split_chk[0], idx + 1, direct)
    tpl_params['basechk'] = chk 
    tpl_params['stepcount'] = opts.stepcount
    tpl_params['angle'] = opts.angle
    tpl_params['chkfile'] = basename + split_chk[1]
    tpl_params['comfile'] = basename + '.com'
    tpl_params['dihedral'] = dihedral
    tpl_params['logfile'] = basename + '.log'
    tpl_params['jobfile'] = basename + '.job'
    return tpl_params
    

def copy_chk(params, comtpl, jobtpl):
    shutil.copy2(params['basechk'], params['chkfile'])
    write_tpl(comtpl, params['comfile'], params)
    write_tpl(jobtpl, params['jobfile'], params)    

def parse_cmdline(args):
    usage = "usage: %prog [options] checkfile"
    parser = OptionParser(usage=usage)
    parser.add_option('-C', '--comtpl', help='.com template file', default='comtpl')
    parser.add_option('-j', '--jobtpl', help='.job template file', default='jobtpl')
    parser.add_option('-d', '--dihedrals', help='Input file of dihedrals to scan, one per line', default='dihedrals')
    parser.add_option('-s', '--stepcount', help='The number of steps', type='int', default=15)
    parser.add_option('-a', '--angle', help='The angle in degrees for each step', type='float', default=12.0)
    
    (options, args) = parser.parse_args()
    if (len(args) == 0):
        sys.stderr.write("Check file required\n")
        parser.print_help()
        parser.exit(-1)
    
    return (options, args[0])

def run(opts, chk):
    comtpl = get_tpl(opts.comtpl)
    jobtpl = get_tpl(opts.jobtpl)
    fp = open(opts.dihedrals, 'r')
    for i, dihed in enumerate(fp):
        dihed = dihed.strip()
        copy_chk(fill_opts(chk, opts, dihed, i, 'f'), comtpl, jobtpl)
        copy_chk(fill_opts(chk, opts, dihed, i, 'b'), comtpl, jobtpl)
    fp.close()

if __name__ == '__main__':
    opts, chk = parse_cmdline(sys.argv[1:])
    run(opts, chk)