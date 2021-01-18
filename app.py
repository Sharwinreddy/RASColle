from flask import Flask
from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request, session ,jsonify
from flask import send_file, send_from_directory, safe_join, abort
import time
#from flaskthreads import AppContextThread
from celery import Celery
import os
import csv
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
#celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def runscan(self,domain):
    connection = sqlite3.connect("small_db.db")
    projectnumbersql = ''' select * from scans'''
    cursor = connection.cursor()
    cursor.execute(projectnumbersql)
    projectnumber=len(cursor.fetchall())+1
    projectnumber=str(projectnumber)
    sqlstat= ''' INSERT INTO scans(Project_Number,Status,Domain)
                      VALUES(?,?,?) '''
    statusupdate=''' update scans set Status = ?  where Project_Number= ?'''
    params=[projectnumber,'Started',domain]
    cursor.execute(sqlstat,params)
    connection.commit()
    self.update_state('started subdomainscan')
    os.system("cd api && python3 allSub.py "+str(domain)+" "+projectnumber)#running subdomain scan
    cursor.execute(statusupdate,['Sudomain Enumuration Done',projectnumber])
    connection.commit()
    self.update_state('started screenshots')
    os.system("cd api && python3 screenshot.py "+str(domain)+" "+projectnumber)
    cursor.execute(statusupdate,['alldone',projectnumber])
    connection.commit()
    self.update_state('all done')
    return redirect(url_for('dashboard'))
#running scan
@app.route('/scan', methods=['GET','POST'])
def scan():
    task = runscan.apply_async(args=[str(request.form['domain'])])
    print(str(task.id))
    return redirect(url_for('dashboard'))

#status update
@app.route('/status/<task_id>')
def scanstatus(task_id):
    task = runscan.AsyncResult(task_id)
    return task.state
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

#getting Statistics
def getstats():
    connection = sqlite3.connect("small_db.db")
    stast='''select * from scans'''
    cursor = connection.cursor()
    cursor.execute(stast)
    list=[]
    result = cursor.fetchall()
    sub=0
    lsub=0
    '''
    for r in result:
        temp=[]
        if r[1]!='':
            sub=sub+int(r[1])
            lsub=lsub+int(r[2])
    connection.close()
    '''
    return [sub,lsub]
#getscan details
def getscans():
    connection = sqlite3.connect("small_db.db")
    scans='''select * from scans'''
    cursor = connection.cursor()
    cursor.execute(scans)
    list=[]
    result = cursor.fetchall()
    for r in result:
        list.append(r)
    connection.close()
    return list
#dashboard rendering
@app.route('/dashboard')
def dashboard():
    stats=getstats()
    return render_template('dashboard.html',total=str(stats[0]),live=str(stats[1]),scans=getscans())


if __name__ == '__main__':
   app.run(debug = True, ssl_context=('certs/cert.pem', 'certs/key.pem'))
   app.run(host = '0.0.0.0',port=5000,threaded=True)
