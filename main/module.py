# -*- coding: utf-8 -*-
import numpy as np
import os
import time
from threading import Thread
from py2neo import Node,Relationship,size,order,Graph,NodeSelector
from conf import get_args


class KnowGraph():
    def __init__(self):
        self.graph = Graph('http://localhost:7474',user=self.args.neo4j_user,password=self.args.neo4j_password)
        self.write_to_statistics()
    #単一のエンティティを見つける
    def lookup_entry(self,client_params,server_param):
        #ネットワーク検索の深さの設定をサポート
        start_time = time.time()
        params ={'name':client_params["entry1"],"deep":4}
        cont = []

        edges=set()
        self.lookup_entry_deep(edges,params,0)
        if len(edges)==0:
            server_param['result']={"success":'false'}
            cont.append('ヒットしませんでした')
            return cont
        else:
            server_param['result']={'edges':[list(i) for i in edges],"success":'true'}
            print('今回の検索トリプルの数は:{},時間:{}s'.format(len(edges),time.time()-start_time))
            memo = server_param['result']
            for item in memo['edges']:
                str = item[0] +"系"+item[1]+"："+item[2]
                cont.append(str)

            return cont

    #クエリ統計
    def lookup_statistics(self,client_params,server_param):
        result=self.graph.data("MATCH (n) RETURN n")
        with open('../data/statistics.txt','r',encoding='utf-8') as f:
            api_nums=f.readline().strip()
        server_param['result']={'total_nums':len(result),'api_nums':api_nums,"success":'true'}

    #APIアクセス時間をカウントする
    def write_to_statistics(self):
        with open('../data/statistics.txt','r',encoding='utf-8') as f:
            api_nums=int(f.readline().strip())+1
        with open('../data/statistics.txt','w',encoding='utf-8') as f:
            f.write(str(api_nums)+'\n')

    #限られた検索の深さ
    def lookup_entry_deep(self,edges,params,deep):
        #現在のルックアップの深さは、必要な深さと等しくてはなりません
        if deep >= params['deep']:
            return
        #前方参照
        params['name'] = '.*'+params['name']+'.*'
        result1=self.graph.data("match (s)-[r]->(e) where s.name=~ '{}' return s.name,r.name,e.name".format(params['name']))
        result2=self.graph.data("match (e)<-[r]-(s) where e.name=~ '{}' return s.name,r.name,e.name".format(params['name']))
        result3=self.graph.data("match (s)-[r]->(e) where r.name=~ '{}' return s.name,r.name,e.name".format(params['name']))
        if len(result1)==0 and len(result2)==0 and len(result3)==0:
            return
        for item in result1:
            edges.add((item['s.name'],item['r.name'],item['e.name']))
            if  item['s.name'] != item['e.name']:#避ける：両面テープ：中国語名：両面テープの無限ループ
                params['name']=item['e.name']
                self.lookup_entry_deep(edges,params.copy(),deep+1)

        for item in result2:
            edges.add((item['s.name'],item['r.name'],item['e.name']))
            if  item['s.name'] != item['e.name']:#避ける：両面テープ：中国語名：両面テープの無限ループ
                params['name']=item['e.name']
                self.lookup_entry_deep(edges,params.copy(),deep+1)

        for item in result3:
            edges.add((item['s.name'],item['r.name'],item['e.name']))
            if  item['s.name'] != item['e.name']:#避ける：両面テープ：中国語名：両面テープの無限ループ
                params['name']=item['e.name']
                self.lookup_entry_deep(edges,params.copy(),deep+1)
