# -*- coding: utf-8 -*-
import requests
import json
import time
import calendar
import pymysql
from flask import request, Flask, render_template
from flask_mail import Mail
global a, b, c, d, e, f, g, h, i, j, k, l
global text
import config
import html

current_time =calendar.timegm(time.gmtime())

def test(text):
    hostname = config.hostname
    username = config.username
    password = config.password
    database = config.database

    def doquery(conn):
        cur = conn.cursor()
        a = 'SELECT id FROM users WHERE email = ' + '"' + str(text) + '"'
        cur.execute(a)
        b = cur.fetchone()
        query_result = (b[0])
        return query_result

    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    final_result = doquery(myConnection)
    myConnection.close()

    headers = {'content-type': "application/json"}
    token_url = "https://pm.managedcoder.com/api/v5/issue-token"
    payload1 = {"username": config.api_username, "password": config.api_password, "client_name": "ActiveCollab",
                "client_vendor": "SJI"}
    r = requests.post(token_url, json=payload1, headers=headers)
    token_result = r.json()
    json_string = json.dumps(token_result)
    token_data = json.loads(json_string)
    user_token = token_data['token']


    headers1 = {"X-Angie-AuthApiToken": user_token}
    users_url = "https://pm.managedcoder.com/api/v5/users"
    r = requests.get(users_url, headers=headers1)
    users_result = r.json()
    json_string = json.dumps(users_result)
    users_data = json.loads(json_string)
    user_ids = []
    first_names = []

    for rec in users_data:
        user_ids.append(rec['id'])
        first_names.append(rec['first_name'])
    id = iter(user_ids)
    users = dict(zip(id, id))
    users_info = []
    users_information = []
    for key, value in users.items():
        users_info.append(key)
        users_information.append(value)

    active_collab_link = "https://pm.managedcoder.com"
    headers = {"X-Angie-AuthApiToken": user_token}
    url = 'http://pm.managedcoder.com/api/v5/users/' + str(final_result) + '/tasks'
    r = requests.get(url, headers=headers)
    tasks_result = r.json()
    json_string = json.dumps(tasks_result)
    tasks_data = json.loads(json_string)

    x6 = []
    for rec in tasks_data['tasks']:
        if rec != 0:
            x6.append(rec['name'])

    x7 = []
    for rec1 in tasks_data['tasks']:
        if rec1 != 0:
            x7.append(active_collab_link + rec1['url_path'])

    x9 = []
    for rec2 in tasks_data['tasks']:
        if rec2 != 0:
            x8 = rec2['due_on']
            if x8 is not None:
                if current_time > x8:
                    x9.append(active_collab_link + rec2['url_path'])

    x10 = []
    for rec3 in tasks_data['tasks']:
        if rec3 != 0:
            x8 = rec3['due_on']
            if x8 is None:
                x10.append(active_collab_link + rec3['url_path'])

    x11 = []
    for rec4 in tasks_data['tasks']:
        if rec4 != 0:
            estimate = rec4['estimate']
            if estimate == 0:
                x11.append(active_collab_link + rec4['url_path'])

    def estimate_result():
        estimated_task =[]
        estimate =[]
        final_value =[]
        for rec6 in tasks_data['tasks']:
            if rec6 != 0:
                task_estimate = rec6['estimate']
                if task_estimate != 0:
                    estimate.append(rec6['estimate'])
                if task_estimate > 0:
                    estimated_task.append(active_collab_link + rec6['url_path'])
                    project_id = rec6['project_id']
                    task_id = rec6['id']
                    headers = {"X-Angie-AuthApiToken": user_token}
                    url = 'http://pm.managedcoder.com/api/v5/projects/' + str(project_id) + '/tasks/' + str(
                        task_id) + '/time-records'
                    r = requests.get(url, headers=headers)
                    tasks_result = r.json()
                    json_string = json.dumps(tasks_result)
                    apidata = json.loads(json_string)
                    value_number = []
                    for records in apidata['time_records']:
                        time_tracked = records['value']
                        value_number.append(time_tracked)
                    final_value.append(sum(value_number))
        return estimated_task, estimate, final_value

    final_task, final_estimate, final_time_spent = estimate_result()
    return x6, len(x6), x9, len(x9), x10,len(x10), x11, len(x11),final_task, final_estimate, final_time_spent, x7



app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=config.mail_username,
    MAIL_PASSWORD=config.mail_passowrd,
)
mail = Mail(app)
@app.route('/')
def index():
    return render_template('query.html')

@app.route('/responses', methods=['GET','POST'])
def responses():
    global text
    text = request.form['text1']
    global a, b, c, d, e, f, g, h, i, j, k, l
    a, b, c, d, e,f, g, h, i, j, k, l = test(text)
    return render_template('responses.html', a=a, b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l)


@app.route('/send-mail', methods=['GET','POST'])
def send_mail():
    textarea = request.form['textarea']
    emailid1 = request.form['text2']
    emailid2 = request.form['text3']
    m = textarea
    user1 = emailid1
    user2 = emailid2
    msg = mail.send_message(
        'Active Collab Report',
        sender='qm@sjinnovation.com',
        recipients=[text,user1,user2],
        body=render_template('email_template.html', a=a, b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m)
    )
    return 'Mail sent'



if __name__ == "__main__":
   app.debug = True
   app.run(host='0.0.0.0')