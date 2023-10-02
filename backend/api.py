from models import db, User, Role, Venue, Movie, Show, Booking, roles_users
from flask_security import SQLAlchemySessionUserDatastore,auth_required,current_user, hash_password
from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify, request
from flask import current_app as app
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
from datetime import datetime
import werkzeug
import os
from os import path
import matplotlib.pyplot as plt
import tasks
from cache import cache
import cachingdata 

cd = os.getcwd()

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

 
user_req = reqparse.RequestParser()
user_req.add_argument('email', required=True, help="email required")
user_req.add_argument('name', required=True, help="name required")
user_req.add_argument('password1', required=True, help="password required")

user_fields = {
    'email' : fields.String ,
} 

edit_user_req = reqparse.RequestParser()
edit_user_req.add_argument('email', required=True, help="email required")
edit_user_req.add_argument('name', required=True, help="name required")
edit_user_req.add_argument('password',  required=True, help="password required")

class UsersAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self):
        user=User.query.filter_by(user_id=current_user.user_id).first()
        role_id = db.session.query(roles_users).filter_by(user_id=current_user.user_id).first().role_id
        v = Venue.query.all()
        m = Movie.query.all()
        s = Show.query.all()
        b = Booking.query.all()
        
        if v==[]:
           venues=True
        else:
           venues=[]
           for venue in v:
               vshows = Show.query.filter_by(venue_id=venue.venue_id).all()
               venues.append({'venue_id':venue.venue_id, 'name':venue.name, 'location':venue.location, 'capacity':venue.capacity, 'nshows':len(vshows)})
        
        if m ==[]:
           movies=True
        else:
           movies=[]
           for movie in m:
               movies.append({'movie_id':movie.movie_id, 'name':movie.name, 'poster':movie.poster, 'description':movie.description, 'duration':movie.duration, 'rating':movie.rating, 'tags':movie.tags})
        
        if s == []:
           shows = True
        else:
           shows=[]
           for show in s:
               movie_name = Movie.query.filter_by(movie_id = show.movie_id).first().name
               venue_name = Venue.query.filter_by(venue_id = show.venue_id).first().name
               shows.append({'show_id':show.show_id, 'venue_id':show.venue_id, 'movie_id':show.movie_id, 'venue_name':venue_name, 'movie_name':movie_name, 'datetime':show.datetime, 'date':show.datetime[:10], 'time': show.datetime[11:], 'seats_available':show.seats_available, 'price':show.price})
        
        if b == []:
           bookings=True
        else:
           bookings=[]
           for booking in b:
               bookings.append({'booking_id':booking.booking_id, 'user_id':booking.user_id, 'show_id':booking.show_id, 'datetime':booking.datetime, 'quantity':booking.quantity, 'total_price':booking.total_price, 'status':booking.status})


        return { 'user_id': user.user_id, 'email':user.email, 'name':user.name, 'password':user.password, 'role':role_id, 'venues':venues, 'movies':movies, 'shows':shows, 'bookings':bookings}


    @marshal_with(user_fields)
    def post(self):
        args = user_req.parse_args()
        email = args.get("email")
        name = args.get("name")
        passw = args.get("password1")
        check=User.query.filter_by(email=email).first()
        if check:
            return jsonify('User already exists. Try with another email.'),400
        elif not check:    
            user_datastore.create_user(email=email,name=name, password=hash_password(passw))
            user = User.query.filter_by(email=email).first()
            role = Role.query.filter_by(name='User').first()
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
            data = User.query.filter_by(email=email).first()
            return data,200
        else:
            return jsonify('Error. Please enter the details again.'),500

    @marshal_with(user_fields)    	
    def put(self, uid):
        args = edit_user_req.parse_args()
        email = args.get("email")
        name = args.get("name")
        password = args.get("password")
        print(email, name)
        User.query.filter_by(user_id=current_user.user_id).update(dict(name=name, email=email, password=password))
        db.session.commit()
        data = User.query.filter_by(email=email).first()
        return data,200

    @auth_required('token')
    def delete(self, uid):
        Booking.query.filter_by(user_id=uid).delete()
        User.query.filter_by(user_id=uid).delete()
        db.session.commit()
        cache.delete_memoized(cachingdata.get_user_by_email)
        return {'del':'done'}

        
venue_req = reqparse.RequestParser()
venue_req.add_argument('vname', required=True, help="vname required")
venue_req.add_argument('location', required=True, help="location required")
venue_req.add_argument('capacity', required=True, help="capacity required")

venue_fields = {
    'name' : fields.String ,
    'location': fields.String,
    'capacity': fields.Integer
} 
    	
class VenueAPI(Resource):
    @auth_required('token')
    def get(self):
        v = Venue.query.all()
        venues=[]
        for venue in v:
            venues.append({'venue_id':venue.venue_id, 'name':venue.name, 'location':venue.location, 'capacity':venue.capacity})
        return {'venues': venues}, 200
        

    @marshal_with(venue_fields)
    @auth_required('token')
    def post(self):
        args = venue_req.parse_args()
        vname = args.get("vname")
        location = args.get("location")
        capacity = args.get("capacity")
        check=Venue.query.filter_by(name=vname).first()
        if check:
            return jsonify('Venue name already exists.'),400
        elif not check:
            new_venue = Venue(name=vname, location=location, capacity=capacity)
            db.session.add(new_venue)
            db.session.commit()
            return new_venue,200
        else:
            return jsonify('Error. Please enter the details again.'),500

    @marshal_with(venue_fields)
    @auth_required('token')
    def put(self,vid):
        args = venue_req.parse_args()
        vname = args.get("vname")
        location = args.get("location")
        capacity = args.get("capacity")
        Venue.query.filter_by(venue_id=vid).update(dict(name=vname, location=location, capacity=capacity))
        db.session.commit()
        data=Venue.query.filter_by(venue_id=vid)
        return data, 200

    	
    @auth_required('token')
    def delete(self, vid):
        Show.query.filter_by(venue_id=vid).delete()
        Venue.query.filter_by(venue_id=vid).delete()
        db.session.commit()
        return {'del':'done'}

movie_req = reqparse.RequestParser()
movie_req.add_argument('name', required=True, help="name required")
movie_req.add_argument('poster', required=True, help="poster required")
movie_req.add_argument('description', required=True, help="description required")
movie_req.add_argument('duration', required=True, help="duration required")
movie_req.add_argument('rating')
movie_req.add_argument('tags')

movie_fields = {
    'name' : fields.String ,
    'poster': fields.String,
    'description': fields.String,
    'duration': fields.String,
    'rating': fields.Float,
    'tags': fields.String,
}

class MovieAPI(Resource):
    @auth_required('token')
    @marshal_with(movie_fields)
    def get(self):
        m = Movie.query.all()
        return m, 200

    @auth_required('token')    
    @marshal_with(movie_fields)
    def post(self):
        args = movie_req.parse_args()
        name = args.get("name")
        poster = args.get("poster")
        description = args.get("description")
        duration = args.get("duration")
        rating = args.get("rating")
        tags = args.get("tags")
        print(name, poster, description, duration, rating, tags)
        try:
            new_movie = Movie(name=name, poster=poster, description=description, duration=duration, rating=rating, tags=tags)
            print(new_movie)
            db.session.add(new_movie)
            db.session.commit()
            return new_movie,200
        except:
            print("There was an error")
            return jsonify('Error. Please enter the details again.'),500

    @auth_required('token')
    @marshal_with(movie_fields)
    def put(self, mid):
        args = movie_req.parse_args()
        name = args.get("name")
        poster = args.get("poster")
        description = args.get("description")
        duration = args.get("duration")
        rating = args.get("rating")
        tags = args.get("tags")
        print(name, poster, description, duration, rating)
        Movie.query.filter_by(movie_id=mid).update(dict(name=name, poster=poster, description=description, duration=duration, rating=rating, tags=tags))
        db.session.commit()
        data=Movie.query.filter_by(movie_id=mid)
        return data, 200
        
    @auth_required('token')
    def delete(self, mid):
        sid = Show.query.filter_by(movie_id=mid).first().show_id
        Booking.query.filter_by(show_id=sid).delete()
        Show.query.filter_by(movie_id=mid).delete()
        Movie.query.filter_by(movie_id=mid).delete()
        db.session.commit()
        return {'del':'done'}


show_req = reqparse.RequestParser()
show_req.add_argument('venue_id', required=True, help="venue id required")
show_req.add_argument('movie_id', required=True, help="movie id required")
show_req.add_argument('datetime', required=True, help="datetime required")
show_req.add_argument('seats_available')
show_req.add_argument('price', required=True, help="price required")

show_fields = {
    'venue_id' : fields.Integer ,
    'movie_id': fields.Integer,
    'datetime': fields.String,
    'seats_available': fields.Integer,
    'price': fields.Integer,
}


class ShowAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self):
        s = Show.query.all()
        shows = [] 
        for show in s:
            v = Venue.query.filter_by(venue_id=show.venue_id).first()
            m = Movie.query.filter_by(movie_id=show.movie_id).first()
            shows.append({'show_id':show.show_id, 'venue_id':show.venue_id, 'movie_id':show.movie_id, 'venue_name':v.name, 'venue_location':v.location, 'movie_name':m.name, 'poster':m.poster, 'description':m.description, 'rating':m.rating, 'tags':m.tags, 'date':show.datetime[:10], 'time':show.datetime[11:], 'datetime':show.datetime, 'seats_available':show.seats_available, 'price':show.price})
        return {'display_shows':shows}, 200
    
    @auth_required('token')
    @marshal_with(show_fields)
    def post(self):
        args = show_req.parse_args()
        venue_id = args.get("venue_id")
        movie_id = args.get("movie_id")
        datetime = args.get("datetime")
        price = args.get("price")
        try:
            sa = Venue.query.filter_by(venue_id=venue_id).first().capacity
            new_show = Show(venue_id=venue_id, movie_id=movie_id, datetime=datetime, seats_available=sa, price=price)
            db.session.add(new_show)
            db.session.commit()
            return new_show,200
        except:
            cache.delete_memoized(cachingdata.get_shows_by_showId)
            return jsonify('Error. Please enter the details again.'),500
    
    @auth_required('token')
    @marshal_with(show_fields)
    def put(self, sid):
        args = show_req.parse_args()
        venue_id = int(args.get("venue_id"))
        movie_id = args.get("movie_id")
        datetime = args.get("datetime")
        seats_available = int(args.get("seats_available"))
        price = args.get("price")
        sa = Show.query.filter_by(show_id=sid).first().seats_available - seats_available
        Show.query.filter_by(show_id=sid).update(dict(venue_id=venue_id, movie_id=movie_id, datetime=datetime, seats_available=seats_available, price=price))
        db.session.commit()
        data=Show.query.filter_by(show_id=sid)
        cache.delete_memoized(cachingdata.get_shows_by_showId)
        return data, 200
    
    @auth_required('token')
    def delete(self, sid):
        Booking.query.filter_by(show_id=sid).delete()
        Show.query.filter_by(show_id=sid).delete()
        db.session.commit()
        cache.delete_memoized(cachingdata.get_shows_by_showId)
        return {'del':'done'}
    	
booking_req = reqparse.RequestParser()
booking_req.add_argument('show_id', required=True, help="show id required")
booking_req.add_argument('datetime', required=True, help="datetime required")
booking_req.add_argument('quantity', required=True, help="seats_available required")
booking_req.add_argument('total_price', required=True, help="price required")
booking_req.add_argument('status', required=True, help="status required")

booking_fields = {
    'user_id' : fields.Integer ,
    'show_id': fields.Integer,
    'datetime': fields.String,
    'quantity': fields.Integer,
    'total_price': fields.Integer,
    'status': fields.String,
}

 
class BookingAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self):
        b = Booking.query.filter_by(user_id=current_user.user_id).all()
        if b==[]:
            bookings=True
        else:
            bookings = []
            for booking in b:
                show = Show.query.filter_by(show_id=booking.show_id).first()
                movie_name = Movie.query.filter_by(movie_id=show.movie_id).first().name
                venue = Venue.query.filter_by(venue_id=show.venue_id).first()
                show_date = show.datetime[:10]
                show_time = show.datetime[11:]
                bookings.append({'user_id':current_user.user_id, 'booking_id':booking.booking_id, 'show_id':booking.show_id, 'venue_id':show.venue_id, 'movie_id':show.movie_id, 'movie_name':movie_name, 'venue_name': venue.name, 'venue_location': venue.location, 'show_date':show_date, 'show_time': show_time, 'show_datetime':show.datetime, 'seats_available':show.seats_available,'price':show.price, 'booking_datetime':booking.datetime, 'quantity':booking.quantity, 'total_price':booking.total_price, 'status':booking.status})
        return {'bookings':bookings}, 200
    
    @auth_required('token')
    @marshal_with(booking_fields)
    def post(self):
        args = booking_req.parse_args()
        show_id = int(args.get("show_id"))
        datetime = args.get("datetime")
        quantity = int(args.get("quantity"))
        total_price = int(args.get("total_price"))
        status = args.get("status")
        print(show_id, datetime, quantity,total_price, quantity)
        try:
            new_booking = Booking(user_id=current_user.user_id, show_id=show_id, datetime=datetime, quantity=quantity, total_price=total_price, status=status)
            db.session.add(new_booking)
            db.session.commit()
            return new_booking,200
        except:
            cache.delete_memoized(cachingdata.get_bookings_by_bookingId)
            return jsonify('Error. Please enter the details again.'),500
    
    @auth_required('token')
    @marshal_with(booking_fields)
    def put(self, bid):
        args = booking_req.parse_args()
        show_id = int(args.get("show_id"))
        datetime = args.get("datetime")
        quantity = int(args.get("quantity"))
        total_price = int(args.get("total_price"))
        status = args.get("status")
        Booking.query.filter_by(booking_id=bid).update(dict(user_id=current_user.user_id, show_id=show_id, datetime=datetime, quantity=quantity, total_price=total_price, status=status))
        db.session.commit()
        data=Booking.query.filter_by(booking_id=bid)
        cache.delete_memoized(cachingdata.get_bookings_by_bookingId)
        return data, 200

    @auth_required('token')
    def delete(self, bid):
        Booking.query.filter_by(booking_id=bid).delete()
        db.session.commit()
        cache.delete_memoized(cachingdata.get_bookings_by_bookingId)
        return {'del':'done'}


class SearchAPI(Resource):
    @auth_required('token')
    def get(self, searchquery):
        s = Show.query.all()
        print("---------------searchquery-------------------")
        searchquery = searchquery.lower()
        shows = [] 
        for show in s:
            v = Venue.query.filter_by(venue_id=show.venue_id).first()
            m = Movie.query.filter_by(movie_id=show.movie_id).first()
            if((searchquery in m.name.lower()) or (searchquery in m.tags.lower()) or (searchquery in v.name.lower()) or (searchquery in v.location.lower())):
                shows.append({'show_id':show.show_id, 'venue_id':show.venue_id, 'movie_id':show.movie_id, 'venue_name':v.name, 'venue_location':v.location, 'movie_name':m.name, 'poster':m.poster, 'description':m.description, 'rating':m.rating, 'tags':m.tags, 'date':show.datetime[:10], 'time':show.datetime[11:], 'datetime':show.datetime, 'seats_available':show.seats_available, 'price':show.price})
        if shows == []:
            shows = True
        return {'display_shows':shows},200
       
class SummaryAPI(Resource):
    @auth_required('token')
    def get(self):
        print("summary API")
        return {'summary':'summary'},200
       
