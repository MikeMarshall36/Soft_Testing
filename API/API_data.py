from API_test import *
import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

passwd = 'data2002'
login = 'AlexBit@gmail.ru'
login_N = 'User_is_fake@gmail.ru'
passwd_N = 'StillFake'
test_pic = 'H_7261fZBcFb_F.jpg'
test_pic_2 = 'b7bd08d6f29a4178a33c6d53680f044f.jpg'
test_pic_3 = '.jpg'
test_pic_4 = '12929640885_674811ecd3_o.jpg'
test_pic_43 = '85MgKN.jpg'

test = PetFriends_testing()
key = test.get_api_key(login, passwd)
key_n = '1238976432-0285342-3249'
petList = test.get_list_of_pets(key,'my_pets')
petList_main = test.get_list_of_pets(key)

no_pic_data = [('Oleg', 'SlaveANIN', '12', petList),
               ('Murka', 'cat', '8', petList),
               ('Valentin', 'perrot', '2', petList)
               ]

pic_dataN = [('Oleg', 'SlaveANIN', '12',test_pic, petList),
               ('Murka', 'cat', '8',test_pic_2, petList),
               ('Valentin', 'perrot', '2',test_pic_43, petList),
                pytest.param('Kirill','dog','3',test_pic_3, petList, marks=pytest.mark.xfail(reason='Обращение к несущетвующей картинке'))
               ]

doble_typed = [('Oleg', 'DvorTeryer', '12', test_pic, petList),
               ('Murka', 'cat', '8', test_pic_43 ,petList),
               ('Valentin', 'perrot', '2',test_pic_43, petList),
               pytest.param('Kirill','Creature X','3',test_pic_4, petList, marks=pytest.mark.xfail(reason='Новые данные соответствуют предыдущим'))
               ]

log_in_data = [(login,passwd, key),
               pytest.param(login_N, passwd_N, key, marks=pytest.mark.xfail(reason='Не зарегистрированный пользователь'))
               ]

list_data = [(key, petList_main),
             pytest.param(key_n, petList_main, marks=pytest.mark.xfail(reason='Не верный API ключ'))]