from flask import Flask, render_template, request, flash, redirect
##from tensorflow.keras.models import load_model
import sqlite3
import pickle
import csv
import os
import numpy as np
import random
import requests
import warnings
warnings.filterwarnings('ignore')
model = pickle.load(open('LL.pkl', 'rb'))
import telepot
bot=telepot.Bot("8208441106:AAHhvxCmsiDIZ_-Xy9Z6023KZkcqn2DYy7o")
chatid="1594545404"
try:
    from serial_test import Read
    print("\n\n\n Hardware Connected \n\n\n ")
except:
    print("\n\n\n  Hardware Not Connected ")
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry , Incorrect Credentials Provided,  Try Again')
        else:
            try:
                dat=Read()
            except:
                dat=[125,96,56,96]
            return render_template('logged.html',hb=dat[0],temp=dat[1],bp=dat[2],oxy=dat[3])

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/kidneyPage")
def kidneyPage():
    try:
        dat=Read()
    except:
        dat=[125,96,56,96]
    return render_template('logged.html',hb=dat[0],temp=dat[1],bp=dat[2],oxy=dat[3])


@app.route("/predictPage", methods = ['POST', 'GET'])
def predictPage():
    
 
    name = request.form['name']
    Age = request.form['age']
    sex = request.form['sex']
    if sex==1:
        sex="MALE"
    else:
        sex="FEMALE"
    bp = request.form['bp']
    oxy = request.form['oxy']
    print(oxy)
    hb = request.form['heart']
    ecg = request.form['ecg']
    Temperature = request.form['Temperature']
    to_predict_list = np.array([[bp,oxy,hb,ecg,Temperature]])
    print(to_predict_list)
    prediction = model.predict(to_predict_list)
    output = prediction[0]
    print("Prediction is {}  :  ".format(output))
    print(output)
    
    # Check the output values and retrive the result with html tag based on the value
    ['bp','oxy','hb','ecg','Temperature','result']
    if output == 1:
        result="Healthy" 
        med=""
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)))
    if output == 2:
        result="Fever" 
        med="Diagnosis Drugs for Fever  \n  Paracetamol \n acetaminophen \n Tylenol  \n aspirin \n  Acephen  \n Ecpirin \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION:  https://maps.app.goo.gl/ftDTGkrZBpgXdNGs9"))
    if output == 3:
        result="Chest Pain" 
        med="Diagnosis Drugs for chest_pain \n Amlodipine \n Nadroparin \n Isosorbide \n Nifedipine \n Atenolol \n Diltiazem \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/ftDTGkrZBpgXdNGs9"))
    if output == 4:
        result="Critical" 
        med="You are critical \n concern the doctor nearby"
        print("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/ftDTGkrZBpgXdNGs9")
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/ftDTGkrZBpgXdNGs9"))
    #####################################################################################################
    s_data=[name,Age,sex,bp,oxy,hb,ecg,Temperature,result]
    csv_file = 'Log.csv'

    file_exists = os.path.isfile(csv_file)

    columns = ['Name','Age','Sex','BP', 'SPO2', 'HB', 'ECG', 'Temperature', 'result']

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(columns)
        writer.writerow(s_data)

    print("Data stored successfully in CSV file.")
    #####################################################################################################
    
#            bp=dat[0],oxy=dat[1],hb=dat[2],temp=dat[3],ecg=dat[4]
    api_key = 'ZN45Y5AINAQYN1E1'
    

    # Construct the URL with the API key and field values
    url = f'https://api.thingspeak.com/update?api_key={api_key}&field1={bp}&field2={oxy}&field3={hb}&field4={Temperature}&field5={ecg}&field6={output}'

    # Make the GET request to upload the data
    response = requests.get(url)

    # Check the response status
    if response.status_code == 200:
        print("Data uploaded successfully.")
    else:
        print(f"Failed to upload data. Status code: {response.status_code}")
    
    # out=output
    print(result,output)
    return render_template('predict.html', result = result,out=output,name =name,med=med )  #,out=out)

    # return render_template('logged.html')

@app.route('/msg',methods = ['POST', 'GET'])
def msg():
    if request.method == 'POST':
        fileName=request.form['filename']
        img='dataset/'+fileName
        bot.sendPhoto(chatid, photo=open(img,'rb'))

    return render_template('logged.html')


if __name__ == '__main__':
	app.run(debug = True, use_reloader=False)
