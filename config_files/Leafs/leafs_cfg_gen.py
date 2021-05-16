#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#the script has to be executed from a Lafs directory

from jinja2 import Environment, FileSystemLoader
import yaml

dir_path = "/Users/sergeyn/Data_Files/Online_Cources/OtusNetDesign/config_files/Leafs/"

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('leafs_underlay_cfg.j2')

with open("data_files/leafs_params.yaml", 'r') as f:
    leafs = yaml.safe_load(f)
    for leaf in leafs:
        filename = leaf['name']+'.ios'
        with open(f"LEAFS/{filename}",'w') as f:
            f.write(template.render(leaf))