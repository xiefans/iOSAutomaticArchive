# -*- coding: UTF-8 -*-
import commands
import json
import os
import sys
import time
import urllib
import zipfile

from biplist import *
import requests

from src.XCodeBuildComand import XCodeBuildComand


class AutomaticArchive:
    command = XCodeBuildComand()

    def __init__(self, configFilePath):
        config = readPlist(sys.path[0] + "/" + configFilePath)
        self.method = config["method"]
        self.workspacePath = config["workspacePath"]
        self.workspaceName = config["workspaceName"]
        self.schemeName = config["schemeName"]
        self.archivePath = config["archivePath"]
        self.provisioningProfiles = config["provisioningProfiles"]
        self.bundleId = config["bundleId"]
        self.signingCertificate = config["signingCertificate"]
        self.teamID = config["teamID"]
        self.exportFileName = config["exportFileName"]
        self.isUploadDSYM = config["isUploadDSYM"]
        self.appId = config["appId"]
        self.appKey = config["appKey"]
        self.dsymFileUploadUrl = config["dsymFileUploadUrl"]

        # 完整的workspace文件名称
        self.workspaceAllName = self.workspaceName + ".xcworkspace"
        # xcarchive的文件目录
        self.archiveFilePath = self.archivePath + "/" + self.schemeName + ".xcarchive"
        # export plist 的完整名称
        self.exportPlistAllFileName = self.exportFileName + ".plist"
        # export ipa 包的结果路径
        self.exportTargetAllPath = self.archivePath + "/" + self.schemeName

    def archive(self):
        os.chdir(self.workspacePath)
        if self.command.clean(self.workspaceAllName, self.schemeName):
            if self.command.archive(self.workspaceAllName, self.schemeName, self.archiveFilePath):
                self.generateExportPlist()
                self.command.export(self.exportPlistAllFileName, self.archiveFilePath, self.exportTargetAllPath)
                self.command.remove_file(self.exportPlistAllFileName)
                if self.isUploadDSYM:
                    self.uploadDSYM()

    def uploadDSYM(self):
        print "============================= uploading dsym files ======================="
        name = self.schemeName + ".app.dSYM"
        uploadPath = self.archivePath + "/" + name + ".zip"
        time.sleep(2)

        z = zipfile.ZipFile(uploadPath, 'w', zipfile.ZIP_STORED)
        for i in os.walk(self.archiveFilePath + "/dSYMs/" + name):
            for n in i[2]:
                path = i[0].split("/dSYMs/")[1]
                z.write("".join((i[0],'/',n)), path + "/" + n)
        z.close()
        # 上传
        file = open(uploadPath, 'r')
        url = self.dsymFileUploadUrl
        files = {"file": file}

        bundleId = urllib.quote(self.bundleId)
        productVersion = urllib.quote("1.2.0(100)")
        fileName = urllib.quote(name + ".zip")
        data = {
                "app_key": self.appKey,
                "app_id": self.appId,
                "api_version": "1",
                "symbolType": "2",
                "bundleId": bundleId,
                "productVersion": productVersion,
                "fileName": fileName,
                "channel": "appstore"
                }
        res = requests.post(url + "?app_key=" + self.appKey + "&app_id=" + self.appId, data, files=files)
        dict = json.loads(res)
        if dict['rtcode'] == 0 & dict['data']['reponseCode'] == "0":
            print "============================= upload success ======================="
        else:
            print "============================= upload fail ======================="

    def generateExportPlist(self):
        data = open(self.exportPlistAllFileName, 'w')
        data.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n")
        data.write(
            "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">" + "\n")
        data.write("<plist version=\"1.0\">" + "\n")
        data.write("<dict>" + "\n")
        data.write("	<key>compileBitcode</key>" + "\n")
        data.write("	<false/>" + "\n")
        data.write("	<key>destination</key>" + "\n")
        data.write("	<string>export</string>" + "\n")
        data.write("	<key>method</key>" + "\n")
        data.write("	<string>" + self.method + "</string>" + "\n")
        data.write("	<key>provisioningProfiles</key>" + "\n")
        data.write("	<dict>" + "\n")
        data.write("		<key>" + self.bundleId + "</key>" + "\n")
        data.write("		<string>" + self.provisioningProfiles + "</string>" + "\n")
        data.write("	</dict>" + "\n")
        data.write("	<key>signingCertificate</key>" + "\n")
        data.write("	<string>" + self.signingCertificate + "</string>" + "\n")
        data.write("	<key>signingStyle</key>" + "\n")
        data.write("	<string>manual</string>" + "\n")
        data.write("	<key>stripSwiftSymbols</key>" + "\n")
        data.write("	<true/>" + "\n")
        data.write("	<key>teamID</key>" + "\n")
        data.write("	<string>" + self.teamID + "</string>" + "\n")
        data.write("</dict>" + "\n")
        data.write("</plist>" + "\n")
        data.close()

    def upload_dandelion(self):
        pass

    def upload_appstore(self):
        pass

    def send_email(self):
        pass
