# -*- coding: UTF-8 -*-

import os
import time
from src.AutomaticArchive import AutomaticArchive

if __name__ == '__main__':
    method = raw_input("1. appstore\n2. addhoc\n请输入序号：");
    if method == "1":
        method = "appstore"
    elif method == "2":
        method = "addhoc"
    else:
        method = "appstore"

    start = time.time()
    archive = AutomaticArchive("Resource/AEConfig-" + method + ".plist")
    archive.archive()
    end = time.time()
    print "used time %.2fs" % (end - start)