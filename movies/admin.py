from django.contrib import admin
from .models import Movie, Theater, Seat,Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'language', 'rating')
    search_fields = ('name', 'genre', 'language')
    # ✅ Include trailer_url in the form
    fields = ('name', 'genre', 'language', 'rating', 'description', 'cast', 'image', 'trailer_url')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie','theater','booked_at']
