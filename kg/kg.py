#coding:utf-8
import sys
import re
sys.path.append('..')
from conf import get_args
from py2neo import *
class data(object):
    def __init__(self):
        self.args=get_args()
        self.data_process()

    def data_process(self):
        # 操作を初期化する
        self.data_init()

        # データを挿入する
        self.insert_datas()


    def data_init(self):
        # グラフデータベースへの接続
        print('データの前処理を開始する')
        self.graph = Graph("bolt://localhost:7687",user=self.args.neo4j_user,password=self.args.neo4j_password)
        self.selector=NodeSelector(self.graph)
        self.graph.delete_all()

    def insert_datas(self):
        print('データの挿入を開始')
        with open('../data/dataset.txt','r',encoding='utf-8') as f:
            lines,num=f.readlines(),-1
            for line in lines:
                num+=1
                if num%500==0:
                    print('現在の処理進捗:{}/{}'.format(lines.index(line),len(lines)))
                line=line.strip().split('\t')
                if len(line)!=3:
                    print('insert_datas間違い:',line)
                    continue
                self.insert_one_data(line)


    def insert_one_data(self,line):
        if '' in line:
            print('insert_one_data間違い',line)
            return

        start=self.look_and_create(line[0])
        for name in self.get_items(line[2]):
            end=self.look_and_create(name)
            r=Relationship(start,line[1],end,name=line[1])
            self.graph.create(r)#存在するときに新しいものを作成しません

        #　ノードが存在しない場合は検索し、存在しない場合は作成します
    def look_and_create(self,name):
        end=self.graph.find_one(label="onepiece",property_key="name",property_value=name)
        if end==None:
            end=Node('onepiece',name=name)
        return end

    def get_items(self,line):
        if '{' not in line and '}' not in line:
            return [line]
        #　確認する
        if '{' not in line or '}' not in line:
            print('get_items Error',line)
        lines= [w[1:-1] for w in re.findall('{.*?}',line)]
        return lines

if __name__=='__main__':
    data=data()
