import requests
import json
import random
import string

class MailGW():
    
    def __init__(self):
        self.base_url = "https://api.mail.gw"#can be
        
    def gen_random_password(self):
        random_number = random.randint(1000, 9999)
        random_lowercase_letters = ''.join([random.choice(string.ascii_lowercase) for n in range(8)])
        random_uppercase_letters = ''.join([random.choice(string.ascii_lowercase) for n in range(8)])
        
        random_prefix = random.choice("!#$*")
        random_password = f"{random_lowercase_letters}{random_number}{random_uppercase_letters}"
        return random_number, random_lowercase_letters, random_uppercase_letters, random_password

    def get_domain_list(self):
        request = requests.get(self.base_url + "/domains")
        data = json.loads(request.text)
        domains = [item["domain"] for item in data["hydra:member"]]
        return domains
        
    def gen_random_email(self):
        while True:
            random_number, random_lowercase_letters, random_uppercase_letters, random_password = self.gen_random_password()
            domains = self.get_domain_list()
            random_domain_from_list = random.choice(domains)
        
            data = {
                "address": f"{random_uppercase_letters}{random_number}{random_lowercase_letters}@{random_domain_from_list}",
                "password": random_password
            }
        
            response = requests.post(self.base_url + "/accounts", json=data)
            token = requests.post(self.base_url + "/token", json=data).json()
            if 200 <= response.status_code < 204:
                return data, token
            else:
                print(f"mail.gw Account creation failed. Retrying...")
        
    def main(self):
        self.gen_random_email()

if __name__ == "__main__":
    tempmail = MailGW()
    tempmail.main()