from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import Movie, Theater, Seat, Booking


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


@login_required(login_url='/login/')
def book_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    booking = Booking.objects.create(user=request.user, movie=movie)

    subject = f"🎟 Ticket Confirmation for {movie.name}"
    message = f"""
        <h2>Hi {request.user.username},</h2>
        <p>Your booking is confirmed!</p>
        <ul>
            <li><strong>Movie:</strong> {movie.name}</li>
            <li><strong>Genre:</strong> {movie.genre}</li>
            <li><strong>Language:</strong> {movie.language}</li>
            <li><strong>Booking ID:</strong> {booking.id}</li>
        </ul>
        <p>Enjoy your show! 🍿</p>
        <p><em>BookMyShow Clone</em></p>
    """

    try:
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        messages.success(request, "Booking confirmed! A confirmation email has been sent.")
    except Exception as e:
        messages.error(request, f"Booking created but email failed: {str(e)}")

    return redirect('profile')


def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})


@login_required(login_url='/login/')
def book_seats(request, theater_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_ids = data.get('seats', [])
            movie_id = data.get('movie_id')
            theater_id = data.get('theater_id')

            if not seat_ids:
                return JsonResponse({'status': 'error', 'message': 'No seats selected'}, status=400)

            theater = get_object_or_404(Theater, id=theater_id)
            movie = get_object_or_404(Movie, id=movie_id)

            error_seats = []

            for seat_id in seat_ids:
                seat = get_object_or_404(Seat, id=seat_id, theater=theater)

                if seat.is_booked:
                    error_seats.append(seat.seat_number)
                    continue

                try:
                    booking = Booking.objects.create(
                        user=request.user,
                        seat=seat,
                        movie=movie,
                        theater=theater
                    )
                    seat.is_booked = True
                    seat.save()

                    subject = f"🎟 Ticket Confirmation for {movie.name}"
                    message = f"""
                        <h2>Hi {request.user.username},</h2>
                        <p>Your booking is confirmed!</p>
                        <ul>
                            <li><strong>Movie:</strong> {movie.name}</li>
                            <li><strong>Theater:</strong> {theater.name}</li>
                            <li><strong>Seat:</strong> {seat.seat_number}</li>
                            <li><strong>Booking ID:</strong> {booking.id}</li>
                        </ul>
                        <p>Enjoy your show! 🍿</p>
                        <p><em>BookMyShow Clone</em></p>
                    """
                    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])
                    email.content_subtype = "html"
                    email.send(fail_silently=False)

                except IntegrityError:
                    error_seats.append(seat.seat_number)
                    continue
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f"Email failed: {str(e)}"}, status=500)

            if error_seats:
                return JsonResponse({
                    'status': 'error',
                    'message': f"Seats already booked: {', '.join(error_seats)}"
                }, status=400)

            messages.success(request, "Booking successful! Confirmation email sent.")
            return redirect('profile')

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@login_required(login_url='/login/')
def seat_selection(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    return render(request, 'movies/seat_selection.html', {
        'theater': theater,
        'seats': seats
    })
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})
