from API_test import *
from API_data import *
import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

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
    test.delete_pets(key, negative_pet)
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


@pytest.fixture()
def negative_pet_set_pic():
    test.delete_pets(key, negative_pet)
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
    global key,negative_pet
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    pre_cond = pre_cond['pets'][0]
    test.delete_pets(key,negative_pet)
    post_cond = test.get_list_of_pets(key, 'my_pets')
    post_cond = ['pets'][0]
    if post_cond != pre_cond:
        test.delete_pets(key, pre_cond)
        return True
    else:
        return False

@pytest.mark.xfail(reason='Введённый петомец не существует в базе данных сайта')
def test_negative_delete_pet(negative_delete_pet):
    assert negative_delete_pet != False
