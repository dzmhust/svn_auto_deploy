# -*- coding: utf-8 -*- 
'''
Created on 2016年12月1日

@author: dzm
'''
import os
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import util
import command

COMMAMD_SVN_LIST = 'svn list '
COMMAMD_SVN_EXPORT = 'svn export --force '
COMMAMD_SVN_IMPORT = 'svn import -m -F '
COMMAMD_SVN_AUTHORIZATION = ' --username chenxw --password chenxiaowei'
COMMAMD_WAR_COMPRESS = 'jar -cvfM0 '
#COMMAMD_MAVEN_BUILD = 'mvn install -DskipTests'
#COMMAMD_MAVEN_PACKAGE = 'mvn package -DskipTests'
COMMAMD_MAVEN_CLEAN = 'mvn clean-Dmaven.test.skip=true'
COMMAMD_MAVEN_BUILD = 'mvn install -Dmaven.test.skip=true'
COMMAMD_MAVEN_PACKAGE = 'mvn package  -Dmaven.test.skip=true'

CODE_FOLDER_NAME = 'code'
FORMATE_WAR = '.war'
FOLDER_TARGET = 'target'

EXPORT_CODE_SUCCESS = 'Exported revision'
MAVEN_BUILD_SUCCESS = 'BUILD SUCCES'
COMPRESS_SUCCESS = '正在添加'

class Build(object):
    '''
    classdocs
    '''

    def __init__(self):
        param_list = util.get_params()
        self.project_name = param_list[1]
        self.project_list = util.get_comma_seprated_list(param_list[2])
        self.svn_code_repository = param_list[3]
        self.svn_username = param_list[4]
        self.svn_password = param_list[5]
        self.svn_auth = ' --username ' + self.svn_username + ' --password ' + self.svn_password
        print('svn_auth: ' + self.svn_auth)
        self.workspace = os.getcwd()
        self.war_name = self.project_name + FORMATE_WAR
        print('war name is :'+self.war_name)
        self.conf_dir = util.get_conf_dir(self.project_name)
        print('conf_dir is :'+self.conf_dir)
        
    def get_conf_list(self):
        print('conf dir: ' + self.conf_dir)
        return os.listdir(self.conf_dir)
    
    def checkout_code(self):
        result = False
        print('checkout svn code start')
        for project in self.project_list:
            print(project)
            check_result = command.execute(COMMAMD_SVN_EXPORT + util.url_join(self.svn_code_repository, project) + self.svn_auth)
            if not util.execute_result(EXPORT_CODE_SUCCESS, check_result):
                return False
            else:
                result = True
        return result
    
    def compress_war(self):
        dest_war = os.path.join(self.workspace,self.project_name+FORMATE_WAR)
        print('dest_war is :' + dest_war)
        project_folder = os.path.join(FOLDER_TARGET,self.project_name)
        os.chdir(os.path.abspath(project_folder))
        relativeFileList = os.listdir(os.getcwd())
        file_list_str = util.list_to_str(relativeFileList)
        print(COMMAMD_WAR_COMPRESS + dest_war + ' ' + file_list_str)
        result = command.execute(COMMAMD_WAR_COMPRESS + dest_war + ' ' + file_list_str)
        return util.execute_result(COMPRESS_SUCCESS, result)
    
    def modify_config(self):
        conf_list = self.get_conf_list()
#         print('conf_list is :'+conf_list)
        for conf in conf_list:
            dest = self.get_dets_conf_through_war(conf)
            if(not len(dest) == 0):    
                print('\cp ' + os.path.join(self.conf_dir, conf) + ' ' + os.path.abspath(dest) )
                command.execute('\cp ' + os.path.join(self.conf_dir, conf) + ' ' + dest )
                print('dest is :' + dest)
    
    def get_dets_conf_through_war(self, conf):
#         project_folder = os.path.abspath(FOLDER_TARGET).join(self.project_name)
        project_folder = os.path.join(FOLDER_TARGET, self.project_name)
#         os.chdir(os.path.abspath(project_folder))
        print('project_folder is :' + project_folder)
        for fpathe,dirs,fs in os.walk(project_folder):
            for f in fs:
                if(conf == f):
                    return(os.path.join(fpathe,f))
        return ''
    
    def mvn_build(self):
        buildResult = False
        for project in self.project_list:
            command.execute(COMMAMD_MAVEN_CLEAN)
            if project == self.project_list[-1]:
                cmd = COMMAMD_MAVEN_PACKAGE
            else:
                cmd = COMMAMD_MAVEN_BUILD
            print('maven build ' + project + ' start')
            os.chdir(os.path.join(self.workspace, project))
            result = command.execute(cmd)
            #for r in result:
                #print(r)
            print('maven build ' + project + ' end')
            if not util.execute_result(MAVEN_BUILD_SUCCESS, result):
                print('进入 maven失败流程')
                return False
            else:
                buildResult = True                
        return buildResult
        
    def start(self):
        #step1: checkout code from svn
        check_result = self.checkout_code()
        if check_result == False:
            print('checkout fail')
            sys.exit(1)
        else:
            print('checkout success')
        # step2: maven build
        print('mvn_result start')
        mvn_result = self.mvn_build()
        if mvn_result == False:
            print('maven fail')
            #return
            sys.exit(1)
        else:
            print('maven success')
        # step3 modify config 
        self.modify_config()
        #compress to .war
        self.compress_war()
        
        
if __name__ == '__main__':
    build = Build()
    build.start()
    