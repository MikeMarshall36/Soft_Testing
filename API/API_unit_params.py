from API_test import *
from API_data import *
import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


@pytest.mark.parametrize("login, passwd, expected_result", log_in_data)
def test_get_apiKey(login,passwd,expected_result):
    func = test.get_api_key(login,passwd)
    status, res = func
    assert status == 200
    assert res == expected_result



@pytest.mark.parametrize("input_key, expected_result", list_data)
def test_get_list(input_key,expected_result):
    status, res = test.get_list_of_pets(input_key)
    assert status == 200
    assert res == expected_result

@pytest.mark.parametrize("name, animal_type, age, expexted_result", no_pic_data)
def test_post_pet_np(name,animal_type, age,expexted_result):
    status, res = test.post_pet_creation(key, name, animal_type, age)
    _,expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res['name'] in expexted_result['pets'][0]['name'] and status == 200 and res['name'] == name
    test.delete_pets(key, res)


@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",pic_dataN)
def test_post_pet_pic(name, animal_type, age, picture, expexted_result):
    status, res = test.post_set_pet(key, name, animal_type, age, picture)
    _,expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res['name'] in expexted_result['pets'][0]['name'] and res['pet_photo'] in expexted_result['pets'][0]['pet_photo'] and res['name'] == name and status == 200
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",[('Oleg', 'DvorTeryer', '12', test_pic_2, petList),('Murka', 'cat', '8',test_pic ,petList)])
def test_post_pic(name,animal_type,age,picture,expexted_result):
    _,res = test.post_pet_creation(key, name, animal_type, age)
    _,pre_cond = test.get_list_of_pets(key, 'my_pets')
    status,_= test.post_set_image(key,res,picture)
    _,expexted_result = test.get_list_of_pets(key, 'my_pets')
    for i in range(len(pre_cond)):
        if expexted_result['pets'][i]['pet_photo'] == res['pet_photo'] and pre_cond['pets'][i]['pet_photo'] != res['pet_photo'] and pre_cond['pets'][i]['pet_photo'] == '':
            print('ok')
            assert pre_cond != expexted_result and res['pet_photo'] in expexted_result['pets'][0]['pet_photo'] and status == 200
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",doble_typed)
def test_put_pet_info(name,animal_type,age,picture,expexted_result):
    _,res = test.post_set_pet(key, name, animal_type, age, picture)
    _,pre_cond = test.get_list_of_pets(key, 'my_pets')
    status,_=test.put_edit_pet_info(key, res, animal_type='Creature X')
    _,expexted_result = test.get_list_of_pets(key, 'my_pets')
    for i in range(len(pre_cond)):
        if expexted_result['pets'][i]['animal_type'] == res['animal_type'] and pre_cond['pets'][i]['panimal_type'] != res['animal_type'] and pre_cond['pets'][i]['animal_type'] == '':
            print('ok')
            assert pre_cond != expexted_result and res['animal_type'] in expexted_result['pets'][0]['animal_type'] and status == 200
    test.delete_pets(key, res)

@pytest.mark.parametrize("name, animal_type, age, picture,expexted_result",pic_dataN)
def test_delete_pets(name,animal_type,age,picture,expexted_result):
    _,res = test.post_pet_creation(key, name, animal_type, age)
    _,pre_cond = test.get_list_of_pets(key, 'my_pets')
    status, _ = test.delete_pets(key,res)
    _,expexted_result = test.get_list_of_pets(key, 'my_pets')
    assert res not in expexted_result['pets'] and expexted_result != pre_cond and status == 200
