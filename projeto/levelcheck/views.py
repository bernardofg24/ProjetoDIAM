from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import GameForm, GenreForm, CharacterForm


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if not request.user.is_authenticated:
                login(request, user)
                return HttpResponseRedirect('index')
            else:
                return render(request, 'levelcheck/login_form.html', {'err_dupe': "You're already logged in."})
        else:
            return render(request, 'levelcheck/login_form.html', {'err_creds': "Username or Password are incorrect."})
        return
    else:
        return render(request, 'levelcheck/login_form.html')


@login_required(login_url='/levelcheck')
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/levelcheck')


def create_acc(request):
    if request.method == 'POST':
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            return render(request, 'levelcheck/create_acc.html', {'err_username': "Username in use."})
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'levelcheck/create_acc.html', {'err_email': "E-mail in use."})

        email = request.POST['email']
        password = request.POST['password']
        birthday = request.POST['birthday']
        src = "/website/images/jiggly.jpg"
        joined = timezone.now()

        u = User.objects.create_user(username, email, password)
        u.save()
        level = LevelUser(user=u, birthday=birthday, img_src=src, joined=joined)
        level.save()
        stats = UserStats(leveluser=level)
        stats.save()
        return HttpResponseRedirect(reverse('levelcheck:login_form'))
    else:
        return render(request, 'levelcheck/create_acc.html')


@login_required(login_url='/levelcheck')
def index(request):
    games = Game.objects.all().order_by('-release')[:5]
    characters = Character.objects.all().order_by('-pub_date')[:5]
    return render(request, 'levelcheck/index.html', {'games': games, 'characters': characters})


@login_required(login_url='/levelcheck')
def profile(request, username):
    return render(request, 'levelcheck/profile.html', {'username': username})


@login_required(login_url='/levelcheck')
def game_detail(request, title):
    game = get_object_or_404(Game, pk=title)
    return render(request, 'levelcheck/game_detail.html', {'game': game})


@login_required(login_url='/levelcheck')
def character_detail(request, title, name):
    game = get_object_or_404(Game, pk=title)
    character = get_object_or_404(Character, name=name, game=game)
    return render(request, 'levelcheck/character_detail.html', {'game': game, 'character': character})


@login_required(login_url='/levelcheck')
def review_detail(request, username, id):
    review = get_object_or_404(Review, pk=id)
    return render(request, 'levelcheck/review_detail.html', {'review': review})


@login_required(login_url='/levelcheck')
def edit_profile(request, id):
    if request.method == 'POST':
        leveluser = get_object_or_404(LevelUser, pk=id)
        username = leveluser.user.username

        if request.POST["gender"]:
            gender = request.POST["gender"]
        else:
            gender = leveluser.gender

        birthday = request.POST["birthday"]
        location = request.POST["location"]
        bio = request.POST["bio"]

        photo_filepath = request.FILES.get("photo", None)

        if photo_filepath is not None:
            src = request.FILES["photo"]
            fs = FileSystemStorage()
            filename = fs.save(src.name, src)
            uploaded_file_url_full = fs.url(filename)
            uploaded_file_url = uploaded_file_url_full.split("/", 3)[3]
            uploaded_file_url = "/" + uploaded_file_url
        else:
            uploaded_file_url = leveluser.img_src

        leveluser.gender = gender
        leveluser.birthday = birthday
        leveluser.location = location
        leveluser.bio = bio
        leveluser.img_src = uploaded_file_url

        leveluser.save(update_fields=["gender", "birthday", "location", "bio", "img_src"])
        return HttpResponseRedirect(reverse('levelcheck:profile', args=username))
    else:
        return render(request, 'levelcheck/edit_profile.html')


@login_required(login_url='/levelcheck')
def create_game(request):
    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES)
        if game_form.is_valid():
            game_form.save()
        return HttpResponseRedirect(reverse('levelcheck:index'))
    else:
        game_form = GameForm()
        return render(request, 'levelcheck/create_game.html', context={"game_form": game_form})


@login_required(login_url='/levelcheck')
def create_genre(request):
    if request.method == "POST":
        genre_form = GenreForm(request.POST)
        if genre_form.is_valid():
            genre_form.save()
        return HttpResponseRedirect(reverse('levelcheck:index'))
    else:
        genre_form = GenreForm()
        return render(request, 'levelcheck/create_genre.html', context={"genre_form": genre_form})


@login_required(login_url='/levelcheck')
def create_character(request):
    if request.method == "POST":
        character_form = CharacterForm(request.POST, request.FILES)
        if character_form.is_valid():
            character_form.save()
        return HttpResponseRedirect(reverse('levelcheck:index'))
    else:
        character_form = CharacterForm()
        return render(request, 'levelcheck/create_character.html', context={"character_form": character_form})


@login_required(login_url='/levelcheck')
def create_review(request, title):
    if request.method == "POST":
        review_title = request.POST['title']
        user = request.user
        game = get_object_or_404(Game, pk=title)
        text = request.POST['text']
        rating = request.POST['rating']

        r = Review(review_title=review_title, user=user, game=game, text=text, rating=rating)
        r.save()
        return HttpResponseRedirect(reverse('levelcheck:index'))
    else:
        game = get_object_or_404(Game, pk=title)
        return render(request, 'levelcheck/create_review.html', {"game": game})


@login_required(login_url='/levelcheck')
def all_games(request):
    games = Game.objects.all().order_by('-release')
    return render(request, 'levelcheck/all_games.html', context={'games': games})


@login_required(login_url='/levelcheck')
def all_characters(request):
    characters = Character.objects.all().order_by('-pub_date')
    return render(request, 'levelcheck/all_characters.html', context={'characters': characters})


@login_required(login_url='/levelcheck')
def all_reviews(request):
    reviews = Review.objects.all().order_by('-pub_date')
    return render(request, 'levelcheck/all_reviews.html', context={'reviews': reviews})


@login_required(login_url='/levelcheck')
def review_feedback_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_feedback = ReviewFeedback.objects.filter(review_id=review_id, user_id=request.user.id)
    if review_feedback:
        review_feedback = ReviewFeedback.objects.get(review_id=review_id, user_id=request.user.id)
        review_feedback.type = "L"
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)
    else:
        review_feedback = ReviewFeedback(type="L", review_id=review_id, user_id=request.user.id)
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)


@login_required(login_url='/levelcheck')
def review_feedback_dislike(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_feedback = ReviewFeedback.objects.filter(review_id=review_id, user_id=request.user.id)
    if review_feedback:
        review_feedback = ReviewFeedback.objects.get(review_id=review_id, user_id=request.user.id)
        review_feedback.type = "D"
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)
    else:
        review_feedback = ReviewFeedback(type="D", review_id=review_id, user_id=request.user.id)
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)

