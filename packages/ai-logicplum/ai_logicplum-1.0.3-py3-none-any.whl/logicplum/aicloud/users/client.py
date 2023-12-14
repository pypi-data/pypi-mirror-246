import requests

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"

def create_account(name,email):
    data = {
    "name": name,           #Client Name
    "email": email, #Client Email
    }
    url = f"{base_url}/client/"
    headers = {"Authorization":api_token}
    response = requests.post(url,json=data,headers=headers)
    return response.json()


def create_app(name,client_id):
    data = {
    "name": name,                  
    "client": client_id  
    }
    url = f"{base_url}/app/"
    headers = {"Authorization":api_token}
    response = requests.post(url,json=data,headers=headers)
    return response.json()



   
   