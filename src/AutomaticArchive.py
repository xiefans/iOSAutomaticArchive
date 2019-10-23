# -*- coding: UTF-8 -*-
import commands
import os
import time
import subprocess


WORKSPACE_PATH = "/Users/user/Desktop/ios"
WORKSPACE_NAME = "BookKeeping"
SCHEME_NAME = "BookKeeping"
ARCHIVE_PATH = "/Users/user/Desktop/Archive"

class AutomaticArchive:

    def __int__(self):
        pass

    def beginArchive(self, workspace_name, scheme_name, archive_path):
        if (self.clean(workspace_name, scheme_name)):
            if (self.archive(workspace_name, scheme_name, archive_path)):
                self.export(archive_path, scheme_name, archive_path)
                self.remove_archive(archive_path, scheme_name)


    def clean(self, workspace_name, scheme_name):
        print "============================= begin clean ======================="
        start = time.time()
        command = 'xcodebuild clean -workspace ' + workspace_name + ".xcworkspace" + " -scheme " + scheme_name + " -configuration Release"
        run = subprocess.Popen(command, shell=True)
        run.wait()
        end = time.time()
        if run.returncode == 0:
            print "============================= clean success time(%.2fs) =======================" % (end - start)
            return True
        else:
            print "============================= clean fail time(%.2fs) =======================" % (end - start)
            return False


    def archive(self, workspace_name, scheme_name, archive_path):
        print "============================= begin archive ======================="
        start = time.time()
        command = "xcodebuild archive -workspace " + workspace_name + ".xcworkspace -scheme " + scheme_name + " -configuration Release -archivePath " + archive_path + "/" + scheme_name + ".xcarchive"
        run = subprocess.Popen(command, shell=True)
        run.wait()
        end = time.time()
        if run.returncode == 0:
            print "============================= archive success time(%.2fs) =======================" % (end - start)
            return True
        else:
            print "============================= archive fail time(%.2fs) =======================" % (end - start)
            return False


    def remove_archive(self, archive_path, scheme_name):
        command = "rm -rf " + archive_path + "/" + scheme_name + ".xcarchive"
        commands.getoutput(command);


    def export(self, archive_path, scheme_name, export_path):
        print "============================= begin export ======================="
        start = time.time()
        command = "xcodebuild -exportArchive -exportOptionsPlist ExportOptions.plist -archivePath "+ archive_path +"/" + scheme_name + ".xcarchive -exportPath " + export_path + "/" + scheme_name + " -allowProvisioningUpdates"
        run = subprocess.Popen(command, shell=True)
        run.wait()
        end = time.time()
        if run.returncode == 0:
            print "============================= export success time(%.2fs) =======================" % (end - start)
        else:
            print "============================= export fail time(%.2fs) =======================" % (end - start)


    def upload_dandelion(self):
        pass


    def upload_appstore(self):
        pass


    def send_email(self):
        pass


if __name__ == '__main__':
    archive = AutomaticArchive()
    # workspace_path = raw_input("请输入workspace路径（工程根目录）：")
    # workspace_name = raw_input("情输入workspace名称：")
    # scheme_name = raw_input("请输入scheme名称：")
    workspace_path = WORKSPACE_PATH
    workspace_name = WORKSPACE_NAME
    scheme_name = SCHEME_NAME
    archive_path = ARCHIVE_PATH
    os.chdir(workspace_path)
    archive.beginArchive(workspace_name, scheme_name, archive_path)