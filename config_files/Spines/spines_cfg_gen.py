#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#the script has to be executed from a Lafs directory

from jinja2 import Environment, FileSystemLoader
import yaml

dir_path = "/Users/sergeyn/Data_Files/Online_Cources/OtusNetDesign/config_files/Leafs/"

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('spines_underlay_ospf_cfg.j2')

with open("data_files/spines_params.yaml", 'r') as f:
    spines = yaml.safe_load(f)
    for spine in spines:
        filename = spine['name']+'.ios'
        print(filename)
        with open(f"SPINES/{filename}",'w') as f:
            f.write(template.render(spine))