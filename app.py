from flask import Flask
from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request, session ,jsonify
from flask import send_file, send_from_directory, safe_join, abort
import time
#from flaskthreads import AppContextThread
from celery import Celery
import os
import csv
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
#celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def runscan(self,domain,projectnumber):
    self.update_state('started subdomainscan')
    os.system("cd api && python3 allSub.py "+str(domain)+" "+projectnumber)#running subdomain scan
    self.update_state('finished subdomainscan')
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
#running scan
@app.route('/scan/<projectnumber>/<domain>', methods=['GET','POST'])
def scan(domain,projectnumber):
    task = runscan.apply_async(args=[str(domain),str(projectnumber)])
    print(str(task.id))
    return redirect(url_for(scanstatus),task_id=str(task.id))

#status update
@app.route('/status/<task_id>')
def scanstatus(task_id):
    task = runscan.AsyncResult(task_id)
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

#output function
def getOutput(projectnumber,subdomain):
    with open("static/output/"+projectnumber+"/"+subdomain+".csv", newline='',encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data
#scan_output
@app.route('/<projectnumber>/<subdomain>', methods=['GET','POST'])
def output_result(projectnumber,subdomain):

    return render_template('tables_dynamic.html',data=getOutput(projectnumber,subdomain),pnumber=projectnumber,sub=subdomain)
#404 render_template
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
#500 render_template
@app.errorhandler(500)
def internal_error(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_error)

if __name__ == '__main__':
   app.run(debug = True, ssl_context=('certs/cert.pem', 'certs/key.pem'))
   app.run(host = '0.0.0.0',port=5000,threaded=True)
