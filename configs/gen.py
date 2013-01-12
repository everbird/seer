#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from string import Template

import config

def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate supervisord.conf
    config_path = os.path.join(current_dir, 'templates/supervisord.conf.template')
    with open(config_path) as f:
        content = Template(f.read())\
                .substitute(**config.__dict__)
        output_path = os.path.join(current_dir, '../supervisord.conf')
        with open(output_path, 'w') as o:
            o.write(content)

    print 'done.'



if __name__ == '__main__':
    run()
