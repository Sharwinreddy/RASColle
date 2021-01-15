from flask import Flask
from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request, session
from flask import send_file, send_from_directory, safe_join, abort
import time
from flaskthreads import AppContextThread
#from celery import Celery
import os
import csv
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
#celery configuration
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Initialize Celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)
'''
@celery.task()
def runscan(domain):
    #self.update_state('started')
    os.system("cd api && python3 allSub.py "+str(domain))#running subdomain scan
    #self.update_state('finished')
#running scan
@app.route('/scan/<domain>', methods=['GET','POST'])
def scan(domain):
    task = runscan.apply_async(args=[str(domain)])
    return 'started'

#status update
@app.route('/status/<task_id>')
def scanstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
#getting data to populate the output
'''
def getOutput(projectnumber,subdomain):
    with open("static/output/"+projectnumber+"/"+subdomain+".csv", newline='',encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

@app.route('/<projectnumber>/<subdomain>', methods=['GET','POST'])
def output_result(projectnumber,subdomain):

    return render_template('tables_dynamic.html',data=getOutput(projectnumber,subdomain),pnumber=projectnumber,sub=subdomain)

if __name__ == '__main__':
   app.run(debug = True)
   app.run(host = '0.0.0.0',port=5000,threaded=True)
