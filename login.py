from flask import Response, request
from flask_cors import CORS


import json
import json
import sqlite3 as sql
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testsecretkey'
database_locale = 'webhunt.db'
CORS(app)

@app.route('/sign', methods=['POST'])
# @cross_origin()
def user_create():
    user_profile=("uid","name","phno","pwd")
    msg="No"
        
    try:
        # print("ok")
        uname = request.form['uname']
        password = request.form['pwd']
        phno=request.form['phno']
        success=True
        print(uname,password)
        with sql.connect(database_locale) as conn:
            curr=conn.cursor()
            curr.execute("SELECT name from users")
            usernames = curr.fetchall()
            # print("okkk")
            for x in usernames:
                
                if x[0]==uname:
                    success=False
        #print(success)
        if success:
            #print("ok2")
            curr.execute("INSERT INTO users (name,phno,pwd) VALUES (?,?,?)",(uname,phno,password,) )
            conn.commit()
            print(uname)

            curr.execute("SELECT uid,name,phno,pwd FROM users WHERE name = ?",(uname,))
            user_details = curr.fetchone()  
            print(user_details)  
           
            msg = "Record successfully added"
            
            if len(user_details) == len(user_profile):
                result = {user_profile[i] : user_details[i] for i, _ in enumerate(user_profile)}
                conn.commit()
                print(result)
                return Response(response=json.dumps({"user_details": result}),status=200,mimetype="application/json")
            else:
                conn.commit()
                return Response(response=json.dumps({"message" : "Error"}), status=401,mimetype="applicatiion/json")

        else:
            return Response(response=json.dumps({"message" : "Username already exists!"}), status=200,mimetype="application/json")
    except Exception as e:
        print(e)
        # conn.rollback()
        msg = "error in insert operation"
        return Response(response=json.dumps({"message" : msg}), status=500,mimetype="application/json")
     
        

@app.route('/loginUser', methods=['POST'])
def login():
    user_profile=("uid","uname","phno","pwd")
    msg=None
    uname = request.form["uname"]
    password = request.form["pwd"]
    print(uname,password)

    try:
        
        with sql.connect(database_locale) as conn:
            
            curr=conn.cursor()
            
            curr.execute("SELECT * FROM users WHERE name = ?", (uname,))
            user_details = curr.fetchone()
            
            print(user_details)
            if user_details[3]==password:

                conn.commit()
                #conn.close()
                
                if len(user_details)==len(user_profile):
                    result = {user_profile[i] : user_details[i] for i,x in enumerate(user_profile)}
                    return Response(response=json.dumps({"user_details":result}),status=200, mimetype="application/json")
            else:
                return Response(response=json.dumps({"message" : "Credentials incorrect"}),status=405,mimetype="applicatiion/json")

    except Exception as e :
        #conn.rollback()
        print(e)
        return Response(response=json.dumps({"message" : "ERROR"}),status=405,mimetype="applicatiion/json")

if __name__ == '__main__':
    app.run(debug=True,port=8082)