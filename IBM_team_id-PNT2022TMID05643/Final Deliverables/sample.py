import flask
from flask import Flask
from flask import request
from flask import json

app=Flask(__name__)

countries={"1":"India", "2":"China", "3":"New York" ,"4":"London" ,"5":"Paris" ,"6":"France" }

@app.route('/data',methods=['GET','POST'])
def api():
    if request.method=='GET':
        return countries
    if request.method=='POST':
        data=request.json
        countries.update(data)
        return 'data got inserted'

@app.route("/data/<id>",methods=['PUT'])
def update(id):
    data=request.form['item']
    countries[str(id)]=data
    return 'data updated'

@app.route("/data/<id>",methods=["DELETE"])
def deleteoperation(id):
    countries.pop(str(id))
    return 'data deleted'

if __name__=='__main__':
    app.run(debug=True)