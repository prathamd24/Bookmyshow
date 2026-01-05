from django.db import models
from django.contrib.auth.models import User 


class Movie(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
    ]

    LANGUAGE_CHOICES = [
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
    ]

    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    rating = models.FloatField()
    description = models.TextField(default="No description available")
    cast = models.CharField(max_length=200)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    # ✅ New field for YouTube trailer
    trailer_url = models.URLField(blank=True, null=True, help_text="Paste YouTube trailer URL")

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('theater', 'seat_number')  # ✅ ensures no duplicate seat numbers in the same theater

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)  # ✅ one seat can only be booked once
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'
