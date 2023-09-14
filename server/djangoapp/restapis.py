import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url,**kwargs): 
    print(f"get for {url}") 
    try:        
        response = requests.get(url=url, params=kwargs, headers={'Content-Type': 'application/json'})
        #response = requests.get(url="https://chukwudimaco-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews",params={'id': 15},headers={'Content-Type': 'application/json'})
             #, auth=HTTPBasicAuth('apikey', api_key))
        print(response)
    except: 
        print("Network exception occurred")    
    status_code=response.status_code
    print(f"With status {status_code}")
    json_data= json.loads(response.text)
    return json_data





# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        #print(json_result)
        # Get the row list in JSON as dealers
        dealers = json_result #["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []    
    dealer_id=kwargs['dealerId']
    # Call get_request with a URL parameter    
    json_result = get_request(url, id=dealer_id)
    if json_result:
        print(json_result)
        # Get the row list in JSON as dealers
        dealers = json_result #["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            print(dealer_doc)
            # Create a DealerReview object with values in `doc` object            
            dealerReview_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"], sentiment="Positive", id=dealer_doc["id"])
            results.append(dealerReview_obj)
    return results



# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



