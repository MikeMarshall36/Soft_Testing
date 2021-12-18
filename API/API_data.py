from API_test import *
import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

passwd = 'data2002'
login = 'AlexBit@gmail.ru'
name = 'Мурзик'
animal_type = 'КОООООООООООООТ'
age = '3'
test_pic = 'H_7261fZBcFb_F.jpg'
name_t = 'Oleg'
animal_type_t = 'Существо Z'
age_t = '99999'
test_pic_2 = 'b7bd08d6f29a4178a33c6d53680f044f.jpg'
test_pic_3 = '.jpg'

test = PetFriends_testing()
key = test.get_api_key(login, passwd)
pet = test.post_pet_creation(key, 'Tom', 'Cat', '14')
creation = test.post_set_pet(key,'Мурка', 'Кошка', '4','85MgKN.jpg')
pets = test.get_list_of_pets(key)
photo = test.post_set_image(key, pet, '12929640885_674811ecd3_o.jpg')
test.put_edit_pet_info(key, pet, 'Том', 'НЕ_КОТ', '12')
pss = test.get_list_of_pets(key,'my_pets')
negative_pet = (key, name_t, animal_type_t , age_t)
