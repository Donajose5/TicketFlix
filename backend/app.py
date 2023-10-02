from os import path
from flask import Flask , render_template,request,redirect,flash
from models import *
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from flask_restful import Api
from flask_cors import CORS
from api import *
from celery.schedules import crontab
from cache import cache
from tasks import monthly_reminder, daily_reminder
import workers
from flask import send_file


app= Flask(__name__)

cd= path.abspath(path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
#app.config['SECURITY_USERNAME_ENABLE']=True
# app.config['SECURITY_TRACKABLE']=True
app.config['SECRET_KEY'] = "yudw890_ASHudb^T^%VSA%&*CASGVHSbsjdbjsd"
app.config['SECURITY_PASSWORD_SALT'] = 'Thi$_is@#super9secrets%$'
app.config['WTF_CSRF_ENABLED'] = False
app.config["SECURITY_TOKEN_AUTHENTICATION_KEY"] = "auth_token"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['CELERY_ENABLE_UTC'] = False
app.config['CELERY_TIMEZONE']='Asia/Kolkata'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 100

api=Api(app)
CORS(app)
db.init_app(app)
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
app.security = Security(app, user_datastore)
cache.init_app(app)

celery = workers.celery
app.app_context().push()

celery.conf.update(
     broker_url='redis://localhost:6379/1',
     result_backend='redis://localhost:6379/2'
 )

celery.Task = workers.ContextTask

app.app_context().push()

class DownloadAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self, bid):
        job = tasks.download_ticket(bid)
        return {'booking':'ticket'}, 200

class ExportAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self, vid):
        job = tasks.export_csv(vid, current_user.user_id)
        return {'export':'csv'}, 200

api.add_resource(UsersAPI, '/api/user', '/api/user/<int:uid>')
api.add_resource(VenueAPI, '/api/venue','/api/venue/<int:vid>')
api.add_resource(MovieAPI, '/api/movie', '/api/movie/<int:mid>')
api.add_resource(ShowAPI, '/api/show','/api/show/<int:sid>')
api.add_resource(BookingAPI, '/api/booking','/api/booking/<int:bid>')
api.add_resource(SummaryAPI, '/api/summary')
api.add_resource(SearchAPI, '/api/searching','/api/searching/<string:searchquery>')
api.add_resource(DownloadAPI, '/api/download/<int:bid>')
api.add_resource(ExportAPI, '/api/export/<int:vid>')


@app.route('/')
def start():
    if not path.exists('sqlite:///database.sqlite3'):
        db.create_all()
    return "hello"


import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 

@app.route("/hello", methods=['GET','POST'])
def hello():
    job=tasks.just_say_hello()
    #return str(job), 200
    return "hi just checking"

@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    print("Inside monthly report function")
    sender.add_periodic_task(crontab(hour=16, minute=19, day_of_month="26"), monthly_reminder.s(), name='everymonth')

@celery.on_after_finalize.connect
def daily_remainder(sender, **kwargs):
    print("Inside daily remainder function")
    sender.add_periodic_task(crontab(hour=19, minute=10, day_of_week="*"), daily_reminder.s(), name='everymonth')

celery.conf.timezone = 'Asia/Kolkata'

if __name__=="__main__":
    app.run(debug=True, port=5000)



