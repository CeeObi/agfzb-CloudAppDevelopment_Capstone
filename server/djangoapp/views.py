from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request,get_dealer_by_state_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method == "POST":        
        username = request.POST['username']
        password = request.POST['psw']        
        user = authenticate(username=username, password=password)        
        if user is not None:            
            login(request, user)
            return redirect( "djangoapp:index")
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)    
    context['message'] = "Invalid username or password."
    return render(request, "djangoapp/login.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
   if request.method == "GET":
       logout(request)
       return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "GET":
       return render(request, "djangoapp/registration.html")


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":        
        url = "https://chukwudimaco-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"            
        # Get dealers from the URL
        dealership_list = get_dealers_from_cf(url)
        context["dealership_list"]=dealership_list        
        # Concat all dealer's short name
        #dealer_names = '=>'.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealership by id` view to render the specific dealer
def get_dealer_by_state(request, dealer_state):
    context = {}
    if request.method == "GET":
        url = "https://chukwudimaco-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"  
        # Get dealers from the URL
        dealers = get_dealer_by_state_from_cf(url, dealerState=dealer_state.title())
        #************
        print(dealers)
        dealer_names = ', '.join([dealer.short_name for dealer in dealers])        
        dealer_state = ', '.join([dealer.st for dealer in dealers])  
        # Return a dealer short name
        return HttpResponse(f"<b>Dealer names:</b> {dealer_names} <br><br> <b>Dealers respective states:</b> {dealer_state}")
    return render(request, 'djangoapp/index.html', context)
    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://chukwudimaco-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"                   
        # Get dealers review from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["reviews_list"]=reviews
        print(context)
        dealer_names = ', '.join([review.name for review in reviews])
        reviewers_sentiment = ', '.join([sentiments.sentiment for sentiments in reviews])
        # Return a list of dealer short name
        #return HttpResponse(f"<b>Reviewer names:</b> {dealer_names} <br><br> <b>Reviewers respective Sentiments:</b> {reviewers_sentiment}")
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    url="https://chukwudimaco-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
     # URL is subject to change for each new lab sessions.
    #if request.method=="POST":
    dealership_id=dealer_id    
    
    #if request.user.is_authenticated:
    
    review = dict()
    review["_id"] = "29bbaee37aadb08c022c2016b"
    review["_rev"] = "1-6d3a316e140863cd"
    review["car_make"] = "CARRRS"
    review["car_model"] = "WOOOOW"
    review["car_year"] = 2010
    review["dealership"] = dealership_id
    review["id"]= 1
    review["name"] = "Dims Obi"
    review["purchase"] = True
    review["purchase_date"]= f"{datetime.utcnow()}"
    review["review"]  = "What an excellent and amazing service"
    result = post_request(url,json_payload=review)    
    return HttpResponse(f"{result['message']}")
#NEED to obtain the values from the web page



