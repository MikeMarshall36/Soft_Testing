from API_test import *
from API_data import *
import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
petList = test.get_list_of_pets(key,'my_pets')

@pytest.mark.parametrize("login, passwd, expected_result", [(login,passwd, key)])
def test_get_apiKey(login,passwd,expected_result):
    res = test.get_api_key(login,passwd)
    assert res == expected_result

@pytest.fixture()
def list_of_pets():
    global key
    test = PetFriends_testing()
    result = test.get_list_of_pets(key)
    return result

def test_list_of_pets(list_of_pets):
    assert list_of_pets['pets'] != '' and len(list_of_pets['pets']) != 0

@pytest.mark.parametrize("name, animal_type, age, expexted_result",[('Oleg', 'SlaveANIN', '12', petList), ('Murka', 'cat', '8', petList)])
def test_post_pet_np(name,animal_type, age,expexted_result):
    res = test.post_pet_creation(key, name, animal_type, age)
    expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res['id'] in expexted_result['pets'][0]['id']
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",[('Oleg', 'DvorTeryer', '12', test_pic_2, petList),('Murka', 'cat', '8',test_pic ,petList)])
def test_post_pet_pic(name, animal_type, age, picture, expexted_result):
    res = test.post_set_pet(key, name, animal_type, age, picture)
    expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res['id'] in expexted_result['pets'][0]['id'] and res['pet_photo'] in expexted_result['pets'][0]['pet_photo']
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",[('Oleg', 'DvorTeryer', '12', test_pic_2, petList),('Murka', 'cat', '8',test_pic ,petList)])
def test_post_pic(name,animal_type,age,picture,expexted_result):
    res = test.post_pet_creation(key, name, animal_type, age)
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    test.post_set_image(key,res,picture)
    expexted_result = test.get_list_of_pets(key, 'my_pets')
    for i in range(len(pre_cond)):
        if expexted_result['pets'][i]['pet_photo'] == res['pet_photo'] and pre_cond['pets'][i]['pet_photo'] != res['pet_photo'] and pre_cond['pets'][i]['pet_photo'] == '':
            print('ok')
            assert pre_cond != expexted_result and res['pet_photo'] in expexted_result['pets'][0]['pet_photo']
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture ,expexted_result",[('Oleg', 'DvorTeryer', '12', test_pic, petList),('Murka', 'cat', '8', test_pic_43 ,petList)])
def test_put_pet_info(name,animal_type,age,picture,expexted_result):
    res = test.post_set_pet(key, name, animal_type, age, picture)
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    test.put_edit_pet_info(key, res, animal_type='Creature X')
    expexted_result = test.get_list_of_pets(key, 'my_pets')
    for i in range(len(pre_cond)):
        if expexted_result['pets'][i]['animal_type'] == res['animal_type'] and pre_cond['pets'][i]['panimal_type'] != res['animal_type'] and pre_cond['pets'][i]['animal_type'] == '':
            print('ok')
            assert pre_cond != expexted_result and res['animal_type'] in expexted_result['pets'][0]['animal_type']
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",[('Oleg', 'DvorTeryer', '12', test_pic_2, petList),('Murka', 'cat', '8',test_pic ,petList)])
def test_delete_pets(name,animal_type,age,picture,expexted_result):
    res = test.post_pet_creation(key, name, animal_type, age)
    pre_cond = test.get_list_of_pets(key, 'my_pets')
    test.delete_pets(key,res)
    expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res not in expexted_result['pets'] and expexted_result != pre_cond