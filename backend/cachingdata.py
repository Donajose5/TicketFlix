from models import User, Show, Booking
from cache import cache


@cache.memoize(timeout=10)
def get_shows_by_showId(show_id):
    return Show.query.filter_by(show_id=show_id).first()

@cache.memoize(timeout=10)
def get_bookings_by_bookingId(booking_id):
    return Booking.query.filter_by(booking_id=booking_id).first()

@cache.memoize(timeout=10)
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
