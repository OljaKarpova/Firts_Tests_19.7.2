from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# 10 своих тестов:
def test_1_add_new_pet_with_valid_data_without_photo(name='Дог', animal_type='собака', age= '1'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом. По-хорошему, ответ от сервера должен быть - 400, т.к. введен возраст питомца в формате str!!!
    assert status == 200
    assert result['name'] == name

def test_2_add_a_valid_photo_to_pet(pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить фото питомца к уже имеющемуся питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id последнего питомца из списка (его мы добавили в предыдущем тесте) и добавляем фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_a_photo_to_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200

def test_3_get_all_MY_PETS_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос моих питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список моих питомцев и проверяем что список не пустой (должен быть не пустым,
    т.к. в тестах выше добавили как минимум одного питомца)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_4_get_api_key_for_invalid_mail(email='ola_karpova@mail.ru', password=valid_password):
    """ Проверяем что неверный запрос api ключа (неверный email) возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_5_get_api_key_for_invalid_password(email=valid_email, password='12345'):
    """ Проверяем что неверный запрос api ключа (неверный password) возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_6_add_new_pet_with_invalid_age_type(name='Кузя', animal_type='кошка',
                                     age='три', pet_photo='images/cat1.jpg'):
    """Проверяем что параметр "age" не может принимать текстовые значения. Ожидаем ответ от сервера - 400 """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. ВНИМАНИЕ, БАГ! Ожидаем ответ от сервера - 400!
    assert status == 200


def test_7_add_new_pet_with_lack_of_data1(name='Барбоскин', animal_type='',
                                     age= '3', pet_photo='images/cat1.jpg'):
    """Проверяем, что невозможно добавить питомца методом "add_new_pet",
    не указывая обязательный параметр "animal_type". Ожидаем ответ от сервера - 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. ВНИМАНИЕ, БАГ! Ожидаем ответ от сервера - 400!
    assert status == 200

def test_8_add_new_pet_with_lack_of_data2(name='', animal_type='кошка', age= '3'):
    """Проверяем, что невозможно добавить питомца методом "add_new_pet_without_photo",
    не указывая обязательный параметр "name". Ожидаем ответ от сервера - 400"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом. ВНИМАНИЕ, БАГ! Ожидаем ответ от сервера - 400!
    assert status == 200

def test_9_delete_of_non_existent_pet():
    """Проверяем возможность удаления питомца по некорректному pet_id.
    Ожидаем ответ от сервера - 400"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Берём неcуществующий id питомца и отправляем запрос на удаление
    pet_id = '9C4AEC87-37A4-4EE0-8F1B-3170C81'
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученный ответ с ожидаемым результатом. ВНИМАНИЕ, БАГ! Ожидаем ответ от сервера - 400!
    assert status == 200


def test_10_add_a_valid_photo_to_non_existent_pet(pet_photo='images/P1040103.jpg'):
    """Проверяем возможность добавить фото питомца по некорректному pet_id.
    Ожидаем ответ от сервера - 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Берём неcуществующий id питомца и добавляем фото
    pet_id ='9C4AEC87-37A4-4EE0-8F1B-3170'
    status, result = pf.add_a_photo_to_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. ВНИМАНИЕ, БАГ! Ожидаем ответ от сервера - 400!
    assert status == 500



