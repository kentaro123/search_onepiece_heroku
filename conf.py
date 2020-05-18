#coding:utf-8
'''
Created on 2017年12月11日

@author: qiujiahao

@email:997018209@qq.com

'''
#数据路径

import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-nu','--neo4j_user', help='neo4j登録名',type=str,default='neo4j')
    parser.add_argument('-np','--neo4j_password', help='neo4jパスワード',type=str,default='kentaro')
    parser.add_argument('-p','--http_port', help='httpポート',type=int,default='7687')
    args = parser.parse_args()
    return args
