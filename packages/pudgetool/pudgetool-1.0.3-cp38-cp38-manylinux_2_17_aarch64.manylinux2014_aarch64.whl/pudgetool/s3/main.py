#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author zhouh zhouhui295@163.com 2014-7-22

import utils

params = {
    "endpoint_url": "http://s3.mytest.com:8443",
    "access_key": "Z4UYWCVHBN6L6CVLKPYG",
    "secret_key": "ldiCSWX6raIcAeubEcp7pQs8uC2ipgtzOfRgM9QL"
}

if __name__ == "__main__":
    bucket = "test"
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    objects = s3c.list_objects(Bucket=bucket)
    contents = objects['Contents']
    for i in range(len(contents)):
        obj = contents[i]
        print("{}\t\t{}\r\n".format(obj["Key"], obj["Size"]))   
