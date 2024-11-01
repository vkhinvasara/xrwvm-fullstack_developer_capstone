# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from django.contrib.auth import logout


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        data = {"userName": ""}
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"}, status=400)

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        login(request, user)
        return JsonResponse({"userName": username, "status": "Registered"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def get_cars(request):
    if request.method == 'GET':
        car_makes = CarMake.objects.all()
        cars_data = []
        for make in car_makes:
            models = CarModel.objects.filter(car_make=make)
            for model in models:
                cars_data.append({
                    "make": make.name,
                    "model": model.name,
                    "type": model.type,
                    "year": model.year.year,
                    "dealer_id": model.dealer_id
                })
        return JsonResponse(cars_data, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...