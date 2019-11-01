# -*- coding: UTF-8 -*-
import commands
import subprocess

class XCodeBuildComand:

    def __int__(self):
        pass

    def clean(self, workspace_all_name, scheme_name):
        print "============================= begin clean ======================="
        command = 'xcodebuild clean -workspace ' + workspace_all_name + " -scheme " + scheme_name + " -configuration Release"
        run = subprocess.Popen(command, shell=True)
        run.wait()
        if run.returncode == 0:
            print "============================= clean success ======================="
            return True
        else:
            print "============================= clean fail ======================="
            return False

    def archive(self, workspace_all_name, scheme_name, archive_all_path):
        print "============================= begin archive ======================="
        command = "xcodebuild archive -workspace " + workspace_all_name + \
                  " -scheme " + scheme_name + \
                  " -configuration Release" \
                  " -archivePath " + archive_all_path
        run = subprocess.Popen(command, shell=True)
        run.wait()
        if run.returncode == 0:
            print "============================= archive success ======================="
            return True
        else:
            print "============================= archive fail ======================="
            return False


    def remove_file(self, file_path):
        command = "rm -rf " + file_path
        commands.getoutput(command);


    def export(self, export_plist_all_path, archive_all_path, export_all_path):
        print "============================= begin export ======================="
        command = "xcodebuild -exportArchive -exportOptionsPlist " + export_plist_all_path + \
                  " -archivePath " + archive_all_path + \
                  " -exportPath " + export_all_path + \
                  " -allowProvisioningUpdates"
        run = subprocess.Popen(command, shell=True)
        run.wait()
        if run.returncode == 0:
            print "============================= export success ======================="
        else:
            print "============================= export fail ======================="