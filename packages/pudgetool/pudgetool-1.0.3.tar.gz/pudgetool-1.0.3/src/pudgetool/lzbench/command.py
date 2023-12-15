#!/usr/bin/env python3.9  
# -*- coding: utf-8 -*-  
#  
# BSC-licensed Python package template  
#  
# This file is distributed under the terms of the BSC license.  
# See LICENSE for more details.  
#  
"""  
Module lzbench  
"""

import click
from . import utils

params = {
    "endpoint_url": "http://s3.mytest.com:8443",
    "access_key": "Z4UYWCVHBN6L6CVLKPYG",
    "secret_key": "ldiCSWX6raIcAeubEcp7pQs8uC2ipgtzOfRgM9QL"
}

@click.group()
def lzbench():
    pass

@lzbench.group()
def analyze():
    pass

@analyze.command()
@click.option('--dir', '-d', help='input a directory')
@click.option('--alg', '-a', help='input a compression algorithm')
@click.option('--output', '-o', help='output file name')
def analyze(dir: str, alg: str, output: str):
    import os
    import pandas as pd
    with open(os.path.join(dirpath, filename)) as f:
        # bw_df = pd.read_csv(f, sep=",", header=0, names=[
        #     'Compressor name', 'Compression speed','Decompression speed','Compressed size', 'Ratio','Filename'])
        bw_df = pd.read_csv(f, sep=",")

        # data filter
        bw_df = bw_df.dropna(subset=['Compressor name'])
        bw_df = bw_df[bw_df['Compressor name'].str.contains(alg)]
        data = bw_df['Compressor name'].str.strip().str.split('-').str
        bw_df['Compressor name'] = data[0]
        bw_df['Compressor Level'] = data[1]
        
        # cut ' MB/S'
        # bw_df['Compression speed'] = bw_df['Compression speed'].str.strip().str[:-5].astype(float)
        # bw_df['Decompression speed'] = bw_df['Decompression speed'].str.strip().str[:-5].astype(float)
        bw_df['Processes'] = len(bw_files)
        bw_df['Processes'].astype(int)
        
        get_filename = lambda s: os.path.splitext(os.path.basename(s))[0]
        bw_df["Filename"] = bw_df["Filename"].apply(get_filename)
        bw_df["Filename"].rename("Dataset")

        # calc
        if len(df) == 0:
            df = pd.concat([df, bw_df])
        else:
            df['Compression speed'] += bw_df['Compression speed']
            df['Decompression speed'] += bw_df['Decompression speed']

@analyze.command()
@click.option('--name', '-n', help='bucket name')
def delete(name):
    pass

@analyze.command()
@click.option('--name', '-n', help='bucket name')
def list(name):
    pass

@lzbench.group()
def save():
    pass

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', help='prefix path')
@click.option('--file', '-f', help='file name')
def put(bucket, prefix, file):
    import os
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    file_name = os.path.basename(file)
    with open(file, 'rb') as f:
        s3c.upload_fileobj(f, bucket, file_name)

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', default="", help='prefix path')
@click.option('--file', '-f', help='file name')
def get(bucket, prefix, file):
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    with open(file, 'wb') as f:
        s3c.download_fileobj(bucket, file, f)

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', help='prefix path')
def list(bucket, prefix):
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    objects = s3c.list_objects(Bucket=bucket)
    contents = objects['Contents']
    for i in range(len(contents)):
        obj = contents[i]
        click.echo("{}\t{}\t".format(obj["Key"], obj["Size"]))
