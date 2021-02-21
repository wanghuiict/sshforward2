#encoding: utf-8

import os
import sys
from jinja2 import Environment, FileSystemLoader
import json
import yaml

def load_yml(f):
    with open(f, 'r') as fd:
        y = yaml.load(fd)
        return y

def generate_conf(vault, conf):
    data = load_yml('%s/.vault/%s'%(os.environ['HOME'], vault))
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('%s.j2'%conf)
    outf = '%s/.vault/%s'%(os.environ['HOME'], conf)
    with open(outf, 'w') as fout:
        content = template.render(data)
        fout.write(content)
    print('%s'%outf)

def _ssh_forward_info(top):
    for k1 in top.keys():
        if k1[0:3] == 'ssh':
            ssh = top[k1]
            forward = ssh.get('forward')
            rules=[]
            if forward != None:
                print('SSH Host: %s@%s:%s'%(ssh['user'], ssh['host'], ssh['port']))
                for k2 in forward.keys():
                    print('%-10s\t%21s:%-5s\t%21s:%-5s'%(k2, forward[k2]['host'], forward[k2]['port'], forward[k2]['rhost'], forward[k2]['rport']))
                _ssh_forward_info(ssh.get('forward'))

def _ssh_forward_expect(top):
    for k1 in top.keys():
        if k1[0:3] == 'ssh':
            ssh = top[k1]
            forward = ssh.get('forward')
            rules=[]
            if forward != None:
                for k2 in forward.keys():
                    rules.append('-L %s:%s:%s:%s'%(forward[k2]['host'], forward[k2]['port'], forward[k2]['rhost'], forward[k2]['rport']))
                expect = "\
expect {\n\
    -re \"assword:\" {\n\
        send \"%s\\r\"\n\
        exp_continue\n\
    }\n\
    -re \"/.ssh/id_dsa':\" {\n\
       send \"%s\\r\"\n\
       exp_continue\n\
    }\n\
    -re \"/.ssh/id_rsa':\" {\n\
       send \"%s\\r\"\n\
       exp_continue\n\
    }\n\
}" % (ssh['pass'], ssh['pass'], ssh['pass'])
                print('spawn ssh -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -f -N %s %s -p %s -l %s'%( ' '.join(rules), ssh['host'], ssh['port'], ssh['user']))
                print("%s"%expect)
                _ssh_forward_expect(ssh.get('forward'))

def print_ssh_forward_expect(jsonf):
    with open(jsonf) as f:
        d = json.load(f)
        _ssh_forward_expect(d)

def print_ssh_forward_info(jsonf):
    with open(jsonf) as f:
        d = json.load(f)
        _ssh_forward_info(d)

if __name__ == '__main__':
    f = sys.argv[1]
    op = sys.argv[2]

    if op == 'expect':
        print_ssh_forward_expect(f)
    elif op == 'info':
        print_ssh_forward_info(f)
    elif op == 'genconf':
        vault = sys.argv[3]
        generate_conf(vault, f)

