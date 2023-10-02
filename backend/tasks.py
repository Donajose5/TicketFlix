from workers import celery
from jinja2 import Template
from weasyprint import HTML
import csv
import os
from emailgenr import send_email
from models import db, User, Role, Venue, Movie, Show, Booking, roles_users
from celery.schedules import crontab
import pandas as pd
from flask import send_file

def format_report(template1,data):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(bookings=data)


def pdf_report(details, temp, filen):
    msg = format_report(temp,data=details)
    html = HTML(string=msg)
    file_name = filen
    html.write_pdf(target=file_name)

wrkng_dir = os.path.abspath(os.path.dirname(__file__))
path_s = os.path.join(wrkng_dir, "static/")
path_t = os.path.join(wrkng_dir, "templates/")

@celery.task()
def just_say_hello():
    print("----------------------Inside task")
    print("Hello namee");

@celery.task()
def monthly_reminder():
    print("inside monthly report task----------------------------------------------")
    b = Booking.query.all()
    bookings = []
    count=0
    for booking in b:
        count+=1
        show = Show.query.filter_by(show_id=booking.show_id).first()
        movie_name = Movie.query.filter_by(movie_id=show.movie_id).first().name
        venue = Venue.query.filter_by(venue_id=show.venue_id).first()
        user_name = User.query.filter_by(user_id=booking.user_id).first().name
        show_date = show.datetime[:10]
        show_time = show.datetime[11:]
        bookings.append({'SNo':count, 'booking_id':booking.booking_id, 'user_id':booking.user_id, 'User': user_name,'Movie':movie_name, 'Venue': venue.name, 'Location': venue.location, 'Date':show_date, 'Time': show_time, 'booking_time':booking.datetime, 'quantity':booking.quantity, 'Price':booking.total_price, 'Status':booking.status})
        
    pdf_report(bookings, "./templates/monthly_report.html", 'Bookings.pdf')
    emailid = 'projuserno1@gmail.com'         # email id to which the report will be sent
    print(emailid)
    with open(path_t+'monthly_report.html','r') as f:
        template = Template(f.read())
    send_email(emailid,'Monthly Report',template.render(bookings=bookings),content="html",attachment="Bookings.pdf")    

@celery.task()
def daily_reminder():
    print("inside daily reminder task----------------------------------------------")
    user_ids = db.session.query(roles_users).filter_by(role_id=2).all()
    for i in user_ids:
        user_id = i[0]
        user_name = User.query.filter_by(user_id=user_id).first().name
        user_email = User.query.filter_by(user_id=user_id).first().email
        bookings = {'user_name':user_name}
        fn = str(user_id)+'reminder.pdf'
        pdf_report(bookings, "./templates/daily_reminder.html", fn)
        with open(path_t+'daily_reminder.html','r') as f:
            template = Template(f.read())
        send_email(user_email,'Daily Reminder',template.render(bookings=bookings),content="html",attachment=fn)


@celery.task()
def download_ticket(bid):
    print("inside download ticket task")
    b = Booking.query.filter_by(booking_id=bid).first()
    u = User.query.filter_by(user_id=b.user_id).first()
    s = Show.query.filter_by(show_id=b.show_id).first()
    v = Venue.query.filter_by(venue_id=s.venue_id).first()
    m = Movie.query.filter_by(movie_id=s.movie_id).first()
    booking = {'booking_id':bid, 'user_name':u.name, 'movie_name':m.name, 'venue_name':v.name, 'location':v.location, 'date':s.datetime[:10], 'time':s.datetime[11:], 'tickets':b.quantity}
    fn = str(bid)+'_ticket.pdf'
    pdf_report(booking, "./templates/booking_ticket.html",fn)
    emailid = u.email
    print(emailid)
    with open(path_t+'booking_ticket.html','r') as f:
        template = Template(f.read())
    send_email(emailid,'Booked Ticket',template.render(bookings=booking),content="html",attachment=fn) 
    

@celery.task()
def export_csv(vid, uid):
    print("inside export csv task")
    venue = Venue.query.filter_by(venue_id=vid).first()
    s = Show.query.filter_by(venue_id=vid).all()
    v = {'Venue ID':venue.venue_id, 'Name':venue.name, 'Location':venue.location, 'Capacity':venue.capacity, 'Number of Shows':len(s)}
    venue_df = pd.DataFrame(v, index=[0])
    fn = "venue_"+str(venue.venue_id)+".csv"
    venue_df.to_csv(fn)
    emailid = User.query.filter_by(user_id = uid).first().email
    body = """
    Dear User,
    
    You have downloaded the venue details.
    
    Regards,
    TicketFlix
    """
    with open(path_t+'booking_ticket.html','r') as f:
        template = Template(f.read())
    send_email(emailid,'Venue Details',body,content="csv",attachment=None,fn=fn) 
 
    

