from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from movies.models import Movie, Booking
from django.contrib.auth.models import User
from django.http import HttpResponse

def check_admin_user(request):
    exists = User.objects.filter(username='admin').exists()
    return HttpResponse(f"Admin exists: {exists}")

GENRES = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Thriller']
LANGUAGES = ['Hindi', 'English', 'Tamil', 'Telugu']

def home(request):
    movies = Movie.objects.all()
    selected_genre = request.GET.get('genre')
    selected_language = request.GET.get('language')

    if selected_genre and selected_genre != 'All':
        movies = movies.filter(genre=selected_genre)

    if selected_language and selected_language != 'All':
        movies = movies.filter(language=selected_language)

    context = {
        'movies': movies,
        'selected_genre': selected_genre,
        'selected_language': selected_language,
        'genres': GENRES,
        'languages': LANGUAGES,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # ✅ use URL name instead of '/'
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'bookings': bookings
    })

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/reset_password.html', {'form': form})
