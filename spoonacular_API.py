import requests

class Spoonacular_Handler:
    def __init__(self, username, first_name, last_name,email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def create_user(self):
        url = "https://api.spoonacular.com/users/connect"
        params = {
            'apiKey' :'',
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
        r = requests.post(url=url, params=params)
        return r.json()

new_user = Spoonacular_Handler("mighty", "merna","luke", "mernaluke@hotmail.com")
print(new_user.create_user())