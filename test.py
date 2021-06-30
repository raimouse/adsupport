import datetime
from flask import Flask
from flask_apscheduler import APScheduler
app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

text = "g:"
text2 = "1"

def job1():
    global text,text2
    print(text+":"+text2)
    text = "done"
    text2 = "now"
    return "jod 1 is done"

def to(event):
    print(event.code)
    print(event.retval)
    print(event.job_id)
    global text,text2
    print(text+":"+text2)


@app.route('/',methods=['get'])
def status():
    start_time=(datetime.datetime.now()+datetime.timedelta(minutes=1))
    scheduler.add_job("job1:1",job1,trigger='date',run_date=start_time)
    return "ADsupport service is running"

@app.route('/index',methods=['get'])
def index():
    return "index"


if __name__ == '__main__':
    scheduler.add_listener(to,4096)
    scheduler.start()
    app.run()
