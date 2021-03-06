#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#the script has to be executed from a Lafs directory

from jinja2 import Environment, FileSystemLoader
import yaml

dir_path = "/Users/sergeyn/Data_Files/Online_Cources/OtusNetDesign/config_files/Leafs/"

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
template_ospf = env.get_template('leafs_underlay_ospf_cfg.j2')
template_isis = env.get_template('leafs_underlay_isis_cfg.j2')
template_ebgp = env.get_template('leafs_underlay_ebgp_cfg.j2')
template_mcast = env.get_template('leafs_underlay_mcast_cfg.j2')
template_vpc = env.get_template('leafs_vpc_cfg.j2')
template_l2vpn = env.get_template('leafs_overlay_l2vpn_cfg.j2')
template_l3vpn = env.get_template('leafs_overlay_l3vpn_cfg.j2')

def ospf_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_ospf.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/OSPF_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

def isis_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_isis.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/ISIS_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

def ebgp_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_ebgp.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/EBGP_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

def mcast_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_mcast.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/MCAST_UNDERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

def vpc_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_vpc.ios'
            if 'vpc' in leaf.keys():
                print(f'Config file {filename} has been created')
                with open(f"LEAFS/VPC_LEAFS/{filename}",'w') as fw:
                    fw.write(template.render(leaf))
            else:
                print('\n' + leaf['name'] + ' is not a VPC member!')

def l2vpn_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_l2vpn.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/EVPN_TYPE2_OVERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

def l3vpn_config_gen(template):
    with open("data_files/leafs_params.yaml", 'r') as fr:
        leafs = yaml.safe_load(fr)
        for leaf in leafs:
            filename = leaf['name']+'_l3vpn.ios'
            print(f'Config file {filename} has been created')
            with open(f"LEAFS/EVPN_TYPE3_OVERLAY/{filename}",'w') as fw:
                fw.write(template.render(leaf))

if __name__ == '__main__':
    #ospf_config_gen(template_ospf)
    #isis_config_gen(template_isis)
    #ebgp_config_gen(template_ebgp)
    #mcast_config_gen(template_mcast)
    #vpc_config_gen(template_vpc)
    #l2vpn_config_gen(template_l2vpn)
    l3vpn_config_gen(template_l3vpn)
