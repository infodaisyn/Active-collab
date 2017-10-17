import requests
import json
import time
import calendar
import pymysql
from flask import request, Flask, render_template
current_time =calendar.timegm(time.gmtime())

def test(text):
    hostname = '34.206.187.63'
    username = 'pmmanage_office'
    password = 'Z&JBhS6C!qc5P'
    database = 'pmmanage_act5'

    def doquery(conn):
        cur = conn.cursor()
        a = 'SELECT id FROM users WHERE email = ' + '"' + str(text) + '"'
        print(a)
        cur.execute(a)
        b = cur.fetchone()
        query_result = (b[0])
        return query_result

    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    final_result = doquery(myConnection)
    myConnection.close()

    headers = {'content-type': "application/json"}
    token_url = "https://pm.managedcoder.com/api/v5/issue-token"
    payload1 = {"username": "", "password": "", "client_name": "ActiveCollab",
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
    print("Total number of tasks assigned: ", len(x6))
    print("Tasks name: ", ', '.join(x6))

    x7 = []
    for rec1 in tasks_data['tasks']:
        if rec1 != 0:
            x7.append(active_collab_link + rec1['url_path'])
    print("Task url's: ", ', '.join(x7))

    x9 = []
    for rec2 in tasks_data['tasks']:
        if rec2 != 0:
            x8 = rec2['due_on']
            if x8 is not None:
                if current_time > x8:
                    x9.append(active_collab_link + rec2['url_path'])
    print("Task overdue: ", ', '.join(x9))
    print("Total number of overdue tasks : ", len(x9))

    x10 = []
    for rec3 in tasks_data['tasks']:
        if rec3 != 0:
            x8 = rec3['due_on']
            if x8 is None:
                x10.append(active_collab_link + rec3['url_path'])
    print("Task without due date: ", ', '.join(x10))
    print("Total number of tasks without due date: ", len(x10))

    x11 = []
    for rec4 in tasks_data['tasks']:
        if rec4 != 0:
            estimate = rec4['estimate']
            if estimate == 0:
                x11.append(active_collab_link + rec4['url_path'])
    print("Task without estimate: ", ', '.join(x11))
    print("Total number of tasks without estimate: ", len(x11))


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
                    print("Task url with estimate: ", estimated_task, "Estimated Time: ", estimate)
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
                    print("Total Time spent on a task:", final_value)
        return estimated_task, estimate, final_value

    final_task, final_estimate, final_time_spent = estimate_result()
    return x6, len(x6), x9, len(x9), x10,len(x10), x11, len(x11),final_task, final_estimate, final_time_spent, x7




app = Flask(__name__)
@app.route('/')
def index():
    return render_template('query.html')

@app.route('/responses', methods=['GET','POST'])
def responses():
    text = request.form['text1']
    a, b, c, d, e,f, g, h, i, j, k, l = test(text)
    return render_template('responses.html', a=a,b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l )


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
