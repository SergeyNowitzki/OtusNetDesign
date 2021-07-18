#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#the script has to be executed from a Lafs directory

from jinja2 import Environment, FileSystemLoader
import yaml

dir_path = "/Users/sergeyn/Data_Files/Online_Cources/OtusNetDesign/config_files/Spines/"

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
template_ospf = env.get_template('spines_underlay_ospf_cfg.j2')
template_isis = env.get_template('spines_underlay_isis_cfg.j2')
template_ebgp = env.get_template('spines_underlay_ebgp_cfg.j2')
template_mcast = env.get_template('spines_underlay_mcast_cfg.j2')
template_l2vpn = env.get_template('spines_overlay_l2vpn_cfg.j2')

def ospf_config_gen(template):
    with open("data_files/spines_params.yaml", 'r') as f:
        spines = yaml.safe_load(f)
        for spine in spines:
            filename = spine['name']+'_ospf.ios'
            print(f'Config file {filename} has been created')
            with open(f"SPINES/OSPF_UNDERLAY/{filename}",'w') as f:
                f.write(template.render(spine))

def isis_config_gen(template):
    with open("data_files/spines_params.yaml", 'r') as fr:
        spines = yaml.safe_load(fr)
        for spine in spines:
            filename = spine['name']+'_isis.ios'
            print(f'Config file {filename} has been created')
            with open(f"SPINES/ISIS_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(spine))

def ebgp_config_gen(template):
    with open("data_files/spines_params.yaml", 'r') as fr:
        spines = yaml.safe_load(fr)
        for spine in spines:
            filename = spine['name']+'_ebgp.ios'
            print(f'Config file {filename} has been created')
            with open(f"SPINES/EBGP_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(spine))

def mcast_config_gen(template):
    with open("data_files/spines_params.yaml", 'r') as fr:
        spines = yaml.safe_load(fr)
        for spine in spines:
            filename = spine['name']+'_mcast.ios'
            print(f'Config file {filename} has been created')
            with open(f"SPINES/MCAST_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(spine))

def l2vpn_config_gen(template):
    with open("data_files/spines_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_l2vpn.ios'
            print(f'Config file {filename} has been created')
            with open(f"SPINES/EVPN_TYPE2_OVERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

if __name__ == '__main__':
    #ospf_config_gen(template_ospf)
    #isis_config_gen(template_isis)
    #ebgp_config_gen(template_ebgp)
    #mcast_config_gen(template_mcast)
    l2vpn_config_gen(template_l2vpn)