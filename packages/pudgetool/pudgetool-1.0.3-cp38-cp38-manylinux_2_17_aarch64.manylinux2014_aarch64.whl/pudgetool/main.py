#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author zhouh zhouhui295@163.com 2014-7-22
import os

from s3 import command as s3cmd

if __name__ == "__main__":
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
