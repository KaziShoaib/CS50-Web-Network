from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    posts = Post.objects.order_by("-posted_at").all()
    like_count = [len(post.liked_by.all()) for post in posts]
    if request.user.is_authenticated:
        like_flag = [request.user in post.liked_by.all() for post in posts]
    else:
        like_flag = [''] * len(posts) 

    return render(request, "network/index.html", {
        "data": zip(posts , like_count, like_flag)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        text = request.POST['text']
        post = Post(poster=request.user, text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/create.html")


@csrf_exempt
@login_required
def post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        except:
            return JsonResponse({"error": "Post not found."}, status=404)
        data = json.loads(request.body)
        if data.get("user_id") is not None:
            user_id = int(data.get("user_id"))
            try:
                user = User.objects.get(pk=user_id)
            except:
                return JsonResponse({"error": "User not found."}, status=404)
            if user not in post.liked_by.all():
                post.liked_by.add(user)
            else:
                post.liked_by.remove(user)
            post.save()
            return HttpResponse(status=204)
        if data.get("new_content") is not None:
            new_content = data.get("new_content")
            post.text = new_content
            post.save()
            return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": " PUT request required."
        }, status=400)