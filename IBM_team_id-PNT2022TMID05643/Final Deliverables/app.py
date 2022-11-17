from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import requests

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fdd69919;PWD=AlJ8IeJp3OlE98qL",'','')

@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    name=x[0]
    email=x[1]
    phone=x[2]
    city=x[3]
    infect=x[4]
    blood=x[5]
    password=x[6]
    sql = "SELECT * FROM user WHERE email =? "
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('register.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  user VALUES (?, ?, ?, ?, ?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, phone)
        ibm_db.bind_param(prep_stmt, 4, city)
        ibm_db.bind_param(prep_stmt, 5, infect)
        ibm_db.bind_param(prep_stmt, 6, blood)
        ibm_db.bind_param(prep_stmt, 7, password)
        ibm_db.execute(prep_stmt)
        return render_template('register.html', pred="Registration Successful, please login using your details")
       
           
        

@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    sql = "SELECT * FROM user WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.bind_param(stmt,2,passw)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(user,passw)
    if account:
            return redirect(url_for('stats'))
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username / password !") 
      
        
@app.route('/stats')
def stats():
    countsQL = "SELECT count(blood) FROM user"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='O Positive'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x1 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='A Positive'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x2 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='B Positive'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x3 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='AB Positive'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x4 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='O Negative'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x5 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='A Negative'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x6 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='B Negative'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x7 = ibm_db.fetch_assoc(stmt)
    countsQL = "SELECT count(*) FROM user WHERE BLOOD ='AB Negative'"
    stmt = ibm_db.prepare(conn, countsQL)
    ibm_db.execute(stmt)
    x8 = ibm_db.fetch_assoc(stmt)
    print(x8)
    return render_template('stats.html',b=x,b1=x1,b2=x2,b3=x3,b4=x4,b5=x5,b6=x6,b7=x7,b8=x8)

@app.route('/requester')
def requester():
    return render_template('request.html')



@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    address = request.form['address']
    print(address)
    reqsql = "SELECT * FROM user WHERE blood=?"
    stmt = ibm_db.prepare(conn, reqsql)
    ibm_db.bind_param(stmt,1,bloodgrp)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)
    msg = "Need Plasma of your blood group for: "+address
    while data != False:
        print ("The Phone is : ", data["PHONE"])
        url ="https://www.fast2sms.com/dev/bulkV2?authorization=sW8nSMRxjC6JQ3z0TI1keUcvH95h7oNiq2mZXlpgBYbAPKGrEFqXxlbJkGDmziBgEKTP0tS82MFrpw56&route=v3&sender_id=FTWSMS&message="+msg+"&language=english&flash=0&numbers="+str(data["PHONE"])
        result=requests.request("GET",url)
        print(result.text)
        data = ibm_db.fetch_assoc(stmt)
    return render_template('request.html', pred="Your request is sent to the concerned people.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

