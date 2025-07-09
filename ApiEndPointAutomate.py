#Automate API end points like Get,Post,Put,Delete
#Use random library to generate random email 

import requests
import json
import random

#base url 
base_url = "https://gorest.co.in"

#Auth token
access_token = "cd010ddcae42b698621f7ef563373f1a26ca0891baf5c7c6e3fc2b4bb96b7dbd"

#headers
headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

#bearer token
auth_token = ""

#this will call get request and return json
def Getrequest():
    response = requests.get(base_url+"/public/v2/users", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    print(json.dumps(user_data,indent=4))

#this will call post request and return the new json added
def Postrequest():
    user_json = {
        "name": "Surya7725 Kaul",
        "email": "surya7725_kaul@hand.test",
        "gender": "female",
        "status": "inactive"
    }
    response = requests.post(base_url+"/public/v2/users",json=user_json, headers=headers)
    assert response.status_code == 201
    #print(response.status_code)
    user_data = response.json()
    print(json.dumps(user_data, indent=4))


#this will call post request and return the new json added
def Putrequest():
    user_json = {
        "name": "Surya7725b Kaul",
        "email": "surya7725b_kaul@hand.test",
        "gender": "female",
        "status": "active"
    }
    response = requests.put(base_url+"/public/v2/users/7989796",json=user_json, headers=headers)
    assert response.status_code == 200
    print(response.status_code)
    user_data = response.json()
    print(json.dumps(user_data, indent=4))

#this will call delete request 
def Deleterequest():
    
    response = requests.delete(base_url+"/public/v2/users/7989796", headers=headers)
    assert response.status_code == 204
    print(response.status_code)
   



Getrequest()
#Postrequest()
#Putrequest()
#Deleterequest()
