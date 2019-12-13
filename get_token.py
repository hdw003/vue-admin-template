from flask import abort, jsonify, Flask, request, Response
from flask_cors import CORS, cross_origin
import random
import os
import re
import json

app = Flask(__name__)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Max-Age'] = '86400'
    resp.status = '200'
    return resp


app.after_request(after_request)


@app.route("/getToken", methods=['GET', 'POST'])
def getToken():
    result = os.popen('kubectl config view').read().split("\n")
    x = ""
    for line in result:
        if line.find("token") != -1:
            x = line
    # y = ['1','2','3']
    # x = json.dumps(y)
    y = {'code':20000,'data':{'total':1,'token':x}}
    return jsonify(y)


@app.route("/restart", methods=['GET', 'POST'])
def restart():
    x = "fails"
    try:
        print('success')
        para = request.args.get('podName')
        result = os.popen("kubectl get pod %s -n twstest -o yaml | kubectl replace --force -f -" % (para)).read().split("\n")
        x = "success"
    except Exception as identifier:
        x = "error: %s" % (identifier)
    finally:
        pass
    return x


@app.route("/getServices", methods=['GET', 'POST'])
def getServices():
    para = request.args.get('')
    result = os.popen('kubectl get pods -n twstest').read().split("\n")
    servicesList = []
    podResault = []
    for index in range(len(result)):
        if 0 < index < (len(result) - 1):
            k = result[index].partition(" ")
            podResault = os.popen('kubectl describe pods %s -n twstest' % (k[0])).read().split("\n")
            svc = ''
            for index1 in range(len(podResault)-1):
                if podResault[index1].startswith('Containers:'):
                    svc = podResault[index1+1].rstrip(':')
            servicesList.append({'id':index,'timestamp':svc,'title':k[0],'type':'','reviewer':'11','status':k[2].lstrip().partition(" ")[2].lstrip().partition(" ")[0]})
    # x = {'code':20000,'data':{'total':100,'items':[{'id':'1','timestamp':1222048755754,'title':'aa','type':'1','reviewer':'11','status':'aa'}]}}
    x = {'code':20000,'data':{'total':100,'items':servicesList}}
    return jsonify(x)


# @app.route("/reload", methods=['GET', 'POST'])
# def reload():
#     result=os.popen("kubectl get pods -n twstest | grep tws-alpine| awk  -F ' '  '{print $1}'  |kubectl get pod -n twstest -o yaml | kubectl replace --force -f - ").read()
#     x=""
#     for line in result:
#         if(line.find("token")!=-1):
#             x=line
#     return x

if __name__ == "__main__":
    if __name__ == "__main__":
        app.config['JSON_AS_ASCII'] = False
        app.run(
            host="0.0.0.0",
            port=48991,
            debug=True
        )
