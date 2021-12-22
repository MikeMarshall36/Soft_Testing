import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json



class PetFriends_testing:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str) -> json:

        header = {'email': email,'password': password}

        res = requests.get(self.base_url +'api/key', headers=header)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def get_list_of_pets(self, auth_key:json, filter: str = '') -> json:

        header = {'auth_key':auth_key['key']}
        filter = {'filter':filter}

        res = requests.get(self.base_url +'api/pets', headers=header, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        print(status, result)
        return status, result

    def post_pet_creation(self, auth_key:json, name:str, animal_type:str, age:str) -> json:
        header ={'auth_key': auth_key['key']}
        data = {'name':name, 'animal_type':animal_type, 'age':age}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=header, params=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(status, result)
        return status, result

    def post_set_pet(self, auth_key:json, name:str, animal_type:str, age:str, pet_photo:str) -> json:
        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age':age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        header = {'auth_key':auth_key['key'],'Content-Type':data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=header, data=data)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_set_image(self, auth_key:json, pet_id:json, pet_photo:str) -> json:
        data = MultipartEncoder(
            fields={'pet_id': pet_id['id'],
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    }
        )
        petID = data.fields['pet_id']
        print(petID)
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'/api/pets/set_photo/{petID}', headers=header, data=data)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pets(self, auth_key:json, pet_id:json):
        data = {'pet_id':pet_id['id']}
        petID = data['pet_id']
        header = {'auth_key':auth_key['key']}
        res = requests.delete(self.base_url + f'/api/pets/{petID}', headers=header)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_edit_pet_info(self, auth_key:json, pet_id:json, name:str='', animal_type:str='', age:str='', pet_photo:str='placeholder.jpg'):
        data = MultipartEncoder(
            fields={'pet_id': pet_id['id'],'name': name, 'animal_type': animal_type, 'age': age, 'pet_id':pet_id['id'],
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    }
        )
        petID = data.fields['pet_id']
        print('ID:',petID)
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + f'/api/pets/{petID}', headers=header, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
