#encoding: utf-8

import os
from jinja2 import Environment, FileSystemLoader
import json
import yaml

def generate_html(data):
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('a.html.j2')
    with open(os.environ['HOME'] + '/a.html', 'w') as fout:
        html_content = template.render(data)
        fout.write(html_content)

def load_yml(f):
    with open(f, 'r') as fd:
        y = yaml.load(fd)
        return y

if __name__ == "__main__":
       #result = {'user1': "myname", 'pass1':'password'}
       result = load_yml('a.yml')
       generate_html(result)
       print("Please check %s"%os.environ['HOME'] + '/a.html')
