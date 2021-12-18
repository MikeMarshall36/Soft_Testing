import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
passwd = 'data2002'
login = 'AlexBit@gmail.ru'
name = 'Valera'
animal_type = 'Bastard'
age = '23'
test_pic = 'maxresdefault (1).jpg'
name_t = 'Oleg'
animal_type_t = 'Bastard'
age_t = '25'
test_pic_2 = 'vehicle-airplane-aircraft-military-aircraft-Lockheed-Martin-F-35-Lightning-II-Mikoyan-MiG-29-McDonnell-Douglas-F-15-Eagle-Lockheed-Martin-McDonnell-Douglas-F-4-Phantom-II-F-35-Lightning-II-air-force-McDonnell-Do.jpg'
test_pic_3 = '.jpg'


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

        print(status, result)
        return result

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
        return result

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
        return result

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
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return result

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
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return result

    def delete_pets(self, auth_key:json, pet_id:json):
        data = {'pet_id':pet_id['id']}
        petID = data['pet_id']
        header = {'auth_key':auth_key['key']}
        res = requests.delete(self.base_url + f'/api/pets/{petID}', headers=header)
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return result

    def put_edit_pet_info(self, auth_key:json, pet_id:json, name:str='', animal_type:str='', age:str=''):
        data = {'name': name, 'animal_type': animal_type, 'age': age, 'pet_id':pet_id['id']}
        petID = data['pet_id']
        print('ID:',petID)
        header = {'auth_key':auth_key['key']}
        res = requests.put(self.base_url + f'/api/pets/{petID}', headers=header, data=data)
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(res.status_code,result)
        return result

test = PetFriends_testing()

key = test.get_api_key(login, passwd)
pet = test.post_pet_creation(key, 'Tom', 'Cat', '14')
creation = test.post_set_pet(key,'Мурка', 'Кошка', '4','85MgKN.jpg')
pets = test.get_list_of_pets(key)
photo = test.post_set_image(key, pet, '12929640885_674811ecd3_o.jpg')
test.put_edit_pet_info(key, pet, 'Том', 'НЕ_КОТ', '12')
pss = test.get_list_of_pets(key,'my_pets')

@pytest.fixture()
def get_api_key_pos():
    global login, passwd
    test = PetFriends_testing()
    result = test.get_api_key(login, passwd)
    return result

def test_get_api_key_pos(get_api_key_pos):
    assert get_api_key_pos['key'] !='' and len(get_api_key_pos['key']) > 0

@pytest.fixture()
def list_of_pets():
    global key
    test = PetFriends_testing()
    result = test.get_list_of_pets(key)
    print(result)
    return result

def test_list_of_pets(list_of_pets):
    assert list_of_pets['pets'] != '' and len(list_of_pets['pets']) != 0

@pytest.fixture()
def post_pet_creat():
    global name, animal_type, age, key
    test = PetFriends_testing()
    result = test.post_pet_creation(key, name, animal_type, age)
    return result


def test_post_pet_creat(post_pet_creat):
    petList = test.get_list_of_pets(key,'my_pets')
    assert post_pet_creat['id'] in petList['pets'][0]['id']
    test.delete_pets(key, post_pet_creat)

@pytest.fixture()
def post_set_pic():
    global name, animal_type, age, key, test_pic
    test_pet = test.post_pet_creation(key, name, animal_type, age)
    pre_cond = test.get_list_of_pets(key,'my_pets')
    pre_cond = pre_cond['pets'][0]
    test.post_set_image(key, test_pet,test_pic)
    post_cond = test.get_list_of_pets(key,'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

def test_post_set_pic(post_set_pic):
    assert post_set_pic != False

@pytest.fixture()
def post_full_creation():
    global name_t, animal_type_t, age_t, key, test_pic_2
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    test_pet = test.post_set_pet(key, name_t, animal_type_t, age_t, test_pic_2)
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

def test_post_set_pet(post_full_creation):
    assert post_full_creation != False

@pytest.fixture()
def delete_pet():
    global key, pet
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    test.delete_pets(key,pet)
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

def test_delete_pet(delete_pet):
    assert delete_pet != False

@pytest.fixture()
def put_pet_info():
    test_pet = test.post_set_pet(key,name_t,animal_type_t,age_t,test_pic_2)
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    updated_pet = test.put_edit_pet_info(key,test_pet,animal_type='Существо X')
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

def test_put_pet_info(put_pet_info):
    assert put_pet_info != False

## Негативные тесты

@pytest.fixture()
def negative_list_of_pets():
    test = PetFriends_testing()
    result = test.get_list_of_pets(key)
    print(result)
    return result

@pytest.mark.xfail(reason='Отсутствует API ключ')
def test_negative_list_of_pets():
    assert list_of_pets['pets'] != '' and len(list_of_pets['pets']) != 0

@pytest.fixture()
def negative_pet_set_pic():
    test_pet = test.post_pet_creation(key, name, animal_type, age)
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    test.post_set_image(key, test_pet, test_pic_3)
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

@pytest.mark.xfail(reason='Используется несуществующая картинка')
def test_negative_pet_set_pic(negative_pet_set_pic):
    assert negative_pet_set_pic != False

@pytest.fixture()
def negative_delete_pet():
    global key,pet
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    test.delete_pets(key,pet)
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

@pytest.mark.xfail(reason='Введённый петомец не существует в БД или был из неё удалён ранее')
def test_negative_delete_pet(negative_delete_pet):
    assert negative_delete_pet != False
