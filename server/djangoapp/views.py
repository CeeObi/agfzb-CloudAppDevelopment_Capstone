from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarDealer,CarModel,DealerCarInventory
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request,get_dealer_by_state_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from random import *
from datetime import datetime
import logging
import json

REVIEWER_ID=0
# Get an instance of a logger
logger = logging.getLogger(__name__)


#######Queries the django admin database to collect carmake and carmodel information
def get_car_collections():
    car_models = list(CarModel.objects.all().values().order_by('name'))
    car_makes = list(CarMake.objects.all().values().order_by('name'))
    car_collections={}
    for each_car_make in car_makes:
        each_car_id = each_car_make["id"]
        car_make_name = each_car_make["name"]    
        car_collections[car_make_name] = []
        for each_car_model in car_models:                    
            if each_car_id == each_car_model["model_id"]:              
                car_collections[car_make_name].append(each_car_model)
    return car_collections

   


def get_cars_by_dealer_id(dealer_id):
    dealer_id=dealer_id
    all_car_collections=get_car_collections()    
    all_dealer_makes_availabe = []
    for makes in all_car_collections:                
        make_of_car=all_car_collections[makes]    
        for indxs in range(0,len(make_of_car)):            
            all_models = make_of_car[indxs]      
            all_models["mod_mak_yr"] = f"{all_models['name']}-{makes}-{all_models['year'].strftime('%Y')}"
            if all_models["dealer_id"] == dealer_id:   
                add_to_car_inventory = DealerCarInventory(id=all_models["id"] , dealer_id=all_models["dealer_id"], name=all_models["name"], model_id=all_models["model_id"], bodytype=all_models["bodytype"], year=all_models["year"], mod_mak_yr=all_models["mod_mak_yr"])
                print(add_to_car_inventory)
                all_dealer_makes_availabe.append(add_to_car_inventory)    
    return all_dealer_makes_availabe
#########End of Queries to django Database    
            
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
        url = "https://chukwudimaco-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealership_list = get_dealers_from_cf(url)
        context["dealership_list"]=dealership_list        
        # Concat all dealer's short name
        #dealer_names = '=>'.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealership by state` view to render the specific dealer
def get_dealer_by_state(request, dealer_state):
    context = {}
    if request.method == "GET":
        url = "https://chukwudimaco-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
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
def get_dealer_details(request, dealer_id, dealer_name):
    context = {}
    if request.method == "GET":
        url = "https://chukwudimaco-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers review from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["reviews_list"]=reviews
        context["id"]=dealer_id
        context["name"]=dealer_name
        # dealer_names = ', '.join([review.name for review in reviews])
        # reviewers_sentiment = ', '.join([sentiments.sentiment for sentiments in reviews])
        # Return a list of dealer short name
        #return HttpResponse(f"<b>Reviewer names:</b> {dealer_names} <br><br> <b>Reviewers respective Sentiments:</b> {reviewers_sentiment}")
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id, dealer_name):
    context = {}    
    if request.method == "POST":
        global REVIEWER_ID
        REVIEWER_ID += 1
        url="https://chukwudimaco-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        # URL is subject to change for each new lab sessions.
        #if request.method=="POST":
        fullname = request.POST['fullname']
        car = request.POST['car'].split("-")        
        car_model=car[0]
        car_make=car[1]
        car_year=car[2]        
        purchasedate = request.POST['purchasedate']
        try:
            purchasecheck = request.POST['purchasecheck']
            purchasecheck = "True"
        except:
            purchasecheck = "False"
        content = request.POST['content']
        dealership_id=dealer_id   
        dealers_name=dealer_name 
        review = {}
        review["_id"] = f"{randint(1,(10**25))}"
        review["_rev"] = f"{randint(1,(10**25))}"
        #Still need to query admin site for car make
        review["car_make"] = car_make
        review["car_model"] = car_model
        review["car_year"] = car_year
        review["dealership"] = dealership_id
        review["id"] = REVIEWER_ID
        review["name"] = fullname        
        review["purchase"] = purchasecheck
        review["purchase_date"]= purchasedate
        review["review"]  = content
        review["review_time"] = f"{datetime.utcnow()}"
        review["dealer_name"] = dealers_name       
        result = post_request(url,json_payload=review)           
        #return HttpResponse(review)   
        return redirect("djangoapp:dealer_details", dealer_id=dealership_id,dealer_name=dealer_name)
    else:
        dealercars_by_id=get_cars_by_dealer_id(dealer_id)  
        context["id"]=dealer_id
        context["name"]=dealer_name
        context["models_to_sell"]=dealercars_by_id 
        return render(request,'djangoapp/add_review.html', context)


