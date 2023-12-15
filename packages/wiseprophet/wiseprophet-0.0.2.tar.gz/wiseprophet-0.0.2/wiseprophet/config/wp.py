import json
import sys
import os
import io


try :
    tmp_path = os.getcwd()
    o_configFile = open(f'{tmp_path}/config/app.config.json', encoding = 'utf-8-sig')
    # o_configFile = open(f'/root/wp-platform.v1/assets/config/app.config.json', encoding = 'utf-8-sig')
    a = os.getcwd()
except Exception as e:
    if e.strerror == 'No such file or directory':
        o_configFile = open('../../assets/config/app.config.json', encoding = 'utf-8-sig')
    else:        
        raise Exception(e.strerror)

o_config = json.load(o_configFile)


def getConfig(p_type,p_key):
    # print(o_config)
    if p_type != '':
        s_value = o_config[p_type][p_key]
        
        if s_value in ['true', 'false']:
            s_value = o_config[p_type].getboolean(p_key)
    else:
        s_value = o_config[p_key]
    return s_value