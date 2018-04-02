#!flask/bin/python
from flask import Flask,jsonify,redirect,render_template,url_for
from flask_cors import CORS
import pandas as pd
import numpy as np
import csv
import json
import xgboost as xgb
from flask import Response


app = Flask(__name__)
CORS(app)

import pickle
#forest=pickle.load(open('forest2.pkl','rb'))
forest=pickle.load(open('/src/xgb.pkl','rb'))

addr=pd.read_excel('/src/clustering.xlsx')
addr=addr.iloc[:,[1,2,4]]
address_cal=addr[['緯度','經度']].values

data=pd.read_csv('/src/test1.csv')
data=data[data['緯度']!='unknown']
data_cal=data[['緯度','經度']].astype(float).values


def calDistance(start,end):
    phi_1=start[0]*np.pi/180
    lambda_1=start[1]*np.pi/180
    phi_2=end[0]*np.pi/180
    lambda_2=end[1]*np.pi/180
    
    delta_lambda=lambda_2-lambda_1
    delta_phi=phi_2-phi_1
    
    distance=6371*2*np.arcsin(
        np.sqrt(
            np.square(np.sin(0.5*delta_phi))+
                np.cos(phi_1)*np.cos(phi_2)*np.square(np.sin(0.5*delta_lambda))
        )
    )
    return distance
def haha(aa,length):
    return [aa]*length


@app.route('/')
def index():
    return "hello! world"

@app.route('/motherFucker', methods=['GET'])
def test():
    return str(forest.predict(test_file)[0])

@app.route('/sum/<int:aaaa>/<int:bbbb>', methods=['GET'])
def gg(aaaa,bbbb):
    abc=aaaa+bbbb
    return str(abc)

@app.route('/test/<string:abc>', methods=['GET'])
def show(abc):
    gg=abc.split(',')
    area=[float(gg[10])]
    room=[float(gg[5])]
    living=[float(gg[6])]
    bath=[float(gg[7])]
    houseYear=[float(gg[2])]
    parkNum=[float(gg[3])+float(gg[4])]
    manage=[0]
    manage[0]=int(gg[-1])
    lng=[float(gg[-2])]
    lat=[float(gg[-3])]
    cluster=[0,0,0,0]
    #transfer floor
    transferFloor=[0]*26
    transfer_dict={1:0,10:1,11:2,12:3,13:4,14:5,15:6,16:7,17:8,18:9,19:10
              ,2:11,20:12,21:13,22:14,23:15,24:16,25:17,3:18,4:19,5:20
               ,6:21,7:22,8:23,9:24,0:25}
    transferFloor[transfer_dict.get(int(gg[9]))]=1

    #total floor
    totalFloor=[0]*29
    if int(gg[8])<=28:
        totalFloor[int(gg[8])-1]=1
    elif int(gg[8])==30:
        totalFloor[28]=1
    buildingType=[0]*4
    buildingType[int(gg[1])]=1
    tradeYear=[0,0,0,0,0,1]
    district=[0]*12
    district[int(gg[0])]=1
    parking=[0,0]
    if int(gg[3])>0:
        parking[0]=1
    if int(gg[4])>0:
        parking[1]=1
    aa=[lat[0],lng[0]]
    test=haha(aa,len(address_cal))
    g=list(map(calDistance,test,address_cal))

    ggg=pd.DataFrame(g)
    tt=addr.iloc[ggg.idxmin(),2].values[0]
    cluster[tt-1]=1
    
    hh=area+room+living+bath+houseYear+parkNum+manage+lng+lat+cluster+transferFloor+totalFloor+buildingType+tradeYear+district+parking
    result=forest.predict(np.array([hh]))
    result=result[0]*3.305785
    ddd={1:'樂活住宅區',2:'經濟住宅區',3:'精華住宅區',4:'教育住宅區'}
    return jsonify({'price':str(result),'clustering':str(ddd.get(tt))})

@app.route('/relation/<string:abc>', methods=['GET'])
def relation(abc):
    ll=abc.split(',')
    #gg=data.iloc[0]
    bb=[float(ll[0]),float(ll[1])]
    test=haha(bb,len(data_cal))
    g=list(map(calDistance,test,data_cal))
    ggg=pd.DataFrame(g)
    target=ggg.sort_values(by=0)[:20]
    tt=(data.iloc[target.index])
    tt[['建物移轉總面積平方公尺']]=np.round(tt[['建物移轉總面積平方公尺']]/3.305785)
    tt[['單價每平方公尺']]=np.round(tt[['單價每平方公尺']]*3.305785/10000).astype(int).astype(str)+'萬元'
    tt=tt.to_json(force_ascii=False,orient='records')
    r=Response(tt)
    r.headers["Content-Type"]="application/json; charset=utf-8"
    return r

    #return jsonify(addr=tt[1],buildingtype=tt[5],cluster=tt[-1],price=(tt[10])*3.305785)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
