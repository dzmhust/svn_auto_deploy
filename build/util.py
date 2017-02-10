# -*- coding: utf-8 -*- 
'''
Created on 2016年12月1日

@author: dzm
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from urlparse import urljoin, urlunparse, urlparse
from posixpath import normpath

DIR_TMP_WAR = 'tmp_war'
DIR_CONF = 'conf'

def get_params():
    '''
    获取参数清单
    '''
    paramList = sys.argv
    return paramList

def get_comma_seprated_list(strList):
    return strList.split(',')

def get_conf_dir(project_name):
    currtnt_path = os.getcwd()
    dir_abs_conf_path = os.path.join(os.path.dirname(currtnt_path),DIR_CONF)
#    print(os.path.join(dir_abs_conf_path, project_name))
    return os.path.join(dir_abs_conf_path, project_name)

def byte_str_list(resultList):
    strList = []
    for result in resultList:
        #字符串处理，去掉最后一个字符，因为最后一个字符无法在屏幕显示
        result = result.decode('utf-8').strip('\n')[:-1] 
#        print(result)
        strList.append(result)
    return strList

def url_join(base, url):
    if not base[-1] == '/':
        base = base + '/'
    url1 = urljoin(base, url)
    print('url1 is :'+url1)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def execute_result(expect, resultList):
    print('expect is:'+expect)
    for result in resultList:
        print('result is :'+result)
        if expect in result:
            return True    
    return False

def list_to_str(list):
    return ' '.join(list)