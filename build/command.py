# -*- coding: utf-8 -*- 
'''
Created on 2016年12月2日

@author: dzm
'''
import subprocess
import util

def execute(commandLine):
    output = []
    p = subprocess.Popen(commandLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        output.append(line)    
    retval = p.wait()
    #print(output)
    output = util.byte_str_list(output)
    print(output)
    return output

if __name__ == '__main__':
    execute('svn list http://www.svnchina.com/svn/wds/monitor --username 1234 --password 56789')