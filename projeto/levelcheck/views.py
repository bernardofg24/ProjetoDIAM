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
from .forms import GameForm, GenreForm, CharacterForm, ArticleForm
from itertools import chain


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
        return HttpResponseRedirect(reverse('levelcheck:login_form'))
    else:
        return render(request, 'levelcheck/create_acc.html')


@login_required(login_url='/levelcheck')
def index(request):
    games = Game.objects.all().order_by('-release')[:5]
    characters = Character.objects.all().order_by('-pub_date')[:5]
    reviews = Review.objects.all().order_by('-pub_date')[:5]
    return render(request, 'levelcheck/index.html', {'games': games, 'characters': characters, 'reviews': reviews})


@login_required(login_url='/levelcheck')
def profile(request, username):
    usergames = UserGames.objects.filter(user_id=request.user.id)
    games = Game.objects.none()
    games_list = list()

    for u in usergames:
        game = Game.objects.get(pk=u.game_id)
        games_list.append(game)

    query_games = list(chain(games, games_list))

    usercharacters = UserCharacters.objects.filter(user_id=request.user.id, type='F')
    characters = Character.objects.none()
    characters_list = list()

    for u in usercharacters:
        character = Character.objects.get(pk=u.character_id)
        characters_list.append(character)

    query_characters = list(chain(characters, characters_list))

    reviews = Review.objects.filter(user_id=request.user.id)

    playing = usergames.filter(type='P').count()
    completed = usergames.filter(type='C').count()
    hold = usergames.filter(type='H').count()
    dropped = usergames.filter(type='D').count()
    plan = usergames.filter(type='F').count()
    total = playing + completed + hold + dropped + plan

    return render(request, 'levelcheck/profile.html', {'username': username, 'games': query_games, 'characters': query_characters, 'reviews': reviews, 'usergames': usergames, 'p': playing, 'c': completed, 'h': hold, 'd': dropped, 'f': plan, 't': total})


@login_required(login_url='/levelcheck')
def game_detail(request, title):
    game = get_object_or_404(Game, pk=title)
    reviews = Review.objects.filter(game_id=game.title)
    return render(request, 'levelcheck/game_detail.html', {'game': game, 'reviews': reviews})


@login_required(login_url='/levelcheck')
def character_detail(request, title, name):
    game = get_object_or_404(Game, pk=title)
    character = get_object_or_404(Character, name=name, game=game)
    character_relation = UserCharacters.objects.filter(user_id=request.user.id, character_id=character.id)
    if not character_relation:
        character_relation = 'E'
    return render(request, 'levelcheck/character_detail.html', {'game': game, 'character': character, 'relation': character_relation})


@login_required(login_url='/levelcheck')
def review_detail(request, username, id):
    review = get_object_or_404(Review, pk=id)
    likes = ReviewFeedback.objects.filter(type='L', review_id=id).count()
    dislikes = ReviewFeedback.objects.filter(type='D', review_id=id).count()
    return render(request, 'levelcheck/review_detail.html', {'review': review, 'likes': likes, 'dislikes': dislikes})


@login_required(login_url='/levelcheck')
def user_detail(request, id):
    profile_owner = get_object_or_404(LevelUser, pk=id)
    if request.user.id == profile_owner.user.id:
        url = reverse('levelcheck:profile', kwargs={'username': request.user.username})
        return HttpResponseRedirect(url)
    return render(request, 'levelcheck/user_detail.html', {'owner': profile_owner})


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
        url = reverse('levelcheck:profile', kwargs={'username': username})
        return HttpResponseRedirect(url)
    else:
        usergames = UserGames.objects.filter(user_id=request.user.id)
        games = Game.objects.none()
        games_list = list()

        for u in usergames:
            game = Game.objects.get(pk=u.game_id)
            games_list.append(game)

        query_games = list(chain(games, games_list))

        usercharacters = UserCharacters.objects.filter(user_id=request.user.id, type='F')
        characters = Character.objects.none()
        characters_list = list()

        for u in usercharacters:
            character = Character.objects.get(pk=u.character_id)
            characters_list.append(character)

        query_characters = list(chain(characters, characters_list))

        reviews = Review.objects.filter(user_id=request.user.id)

        playing = usergames.filter(type='P').count()
        completed = usergames.filter(type='C').count()
        hold = usergames.filter(type='H').count()
        dropped = usergames.filter(type='D').count()
        plan = usergames.filter(type='F').count()
        total = playing + completed + hold + dropped + plan

        return render(request, 'levelcheck/edit_profile.html', {'games': query_games, 'characters': query_characters, 'reviews': reviews, 'usergames': usergames, 'p': playing, 'c': completed, 'h': hold, 'd': dropped, 'f': plan, 't': total})


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
def delete_game(request, title):
    game = get_object_or_404(Game, pk=title)
    game.delete()
    return HttpResponseRedirect(reverse('levelcheck:all_games'))


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
def delete_character(request, title, name):
    character = Character.objects.get(name=name, game_id=title)
    character.delete()
    return HttpResponseRedirect(reverse('levelcheck:all_characters'))


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
def delete_review(request, game_id):
    review = Review.objects.get(game_id=game_id, user_id=request.user.id)
    review.delete()
    return HttpResponseRedirect(reverse('levelcheck:all_reviews'))


@login_required(login_url='/levelcheck')
def create_article(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
        return HttpResponseRedirect(reverse('levelcheck:index'))
    else:
        article_form = ArticleForm()
        return render(request, 'levelcheck/create_article.html', context={"article_form": article_form})


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
def all_users(request):
    users = User.objects.all().exclude(is_superuser=1).order_by('-last_login')
    empty = Game.objects.none()
    levelusers_list = list()

    for u in users:
        leveluser = LevelUser.objects.get(user_id=u.id)
        levelusers_list.append(leveluser)

    query_levelusers = list(chain(empty, levelusers_list))

    return render(request, 'levelcheck/all_users.html', context={'levelusers': query_levelusers})


@login_required(login_url='/levelcheck')
def review_feedback_vote(request, review_id, type):
    review = get_object_or_404(Review, id=review_id)
    review_feedback = ReviewFeedback.objects.filter(review_id=review_id, user_id=request.user.id)
    if review_feedback:
        review_feedback = ReviewFeedback.objects.get(review_id=review_id, user_id=request.user.id)
        review_feedback.type = type
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)
    else:
        review_feedback = ReviewFeedback(type=type, review_id=review_id, user_id=request.user.id)
        review_feedback.save()
        url = reverse('levelcheck:review_detail', kwargs={'username': review.user.username, 'id': review.id})
        return HttpResponseRedirect(url)


@login_required(login_url='/levelcheck')
def user_games_stats(request, title, type):
    game = get_object_or_404(Game, pk=title)
    game_stats = UserGames.objects.filter(game_id=game.title, user_id=request.user.id)
    if game_stats:
        game_stats = UserGames.objects.get(game_id=game.title, user_id=request.user.id)
        game_stats.type = type
        game_stats.save()
        url = reverse('levelcheck:game_detail', kwargs={'title': game.title})
        return HttpResponseRedirect(url)
    else:
        game_stats = UserGames(type=type, game_id=title, user_id=request.user.id)
        game_stats.save()
        url = reverse('levelcheck:game_detail', kwargs={'title': game.title})
        return HttpResponseRedirect(url)


@login_required(login_url='/levelcheck')
def user_characters_favourites(request, title, name):
    character = get_object_or_404(Character, game_id=title, name=name)
    user_characters = UserCharacters.objects.filter(game_id=title, character_id=character.id, user_id=request.user.id)
    if user_characters:
        user_characters = UserCharacters.objects.get(game_id=title, character_id=character.id, user_id=request.user.id)
        user_characters.delete()
        url = reverse('levelcheck:character_detail', kwargs={'title': title, 'name': character.name})
        return HttpResponseRedirect(url)
    else:
        user_characters = UserCharacters(type="F", game_id=title, character_id=character.id, user_id=request.user.id)
        user_characters.save()
        url = reverse('levelcheck:character_detail', kwargs={'title': title, 'name': character.name})
        return HttpResponseRedirect(url)


@login_required(login_url='/levelcheck')
def follower_followed(request, owner_id):
    followed = get_object_or_404(LevelUser, pk=owner_id)
    relation = UserFollowers.objects.filter(followed_id=followed.user.id, follower_id=request.user.id)
    if relation:
        relation = UserFollowers.objects.get(followed_id=followed.user.id, follower_id=request.user.id)
        relation.delete()
        url = reverse('levelcheck:user_detail', kwargs={'id': followed.id})
        return HttpResponseRedirect(url)
    else:
        relation = UserFollowers(type="F", followed_id=followed.user.id, follower_id=request.user.id)
        relation.save()
        url = reverse('levelcheck:user_detail', kwargs={'id': followed.id})
        return HttpResponseRedirect(url)
