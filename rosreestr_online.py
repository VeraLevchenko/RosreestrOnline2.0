import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'.encode('UTF-8'),
    'Content-Type': 'application/json',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def getObjectType(objectId):
            # официальный API Росреестра (неполные сведения)
    # url = f'https://rosreestr.gov.ru/api/online/fir_object/{objectId}'
            # НЕофициальный API Росреестра (более полные сведения и даты новее)
    url = f'http://rosreestr.ru/fir_lite_rest/api/gkn/fir_object/{objectId}'
    try:
        r = requests.get(url, headers=headers, verify="CertBundle.pem")
        objectData = r.json().get("objectData")
        objectType = objectData.get("objectType")
    except:
        # print('Error!!! Нет объекта с таким Id')
        r = 'Error!!! Нет объекта с таким Id'
    return objectData, objectType
def getObjectId(cadNum):
    # официальный API Росреестра для поиска ID
    url = f'https://rosreestr.gov.ru/api/online/fir_objects/{cadNum}'
    # НЕофициальный API Росреестра для поиска ID
    url2 = f'http://rosreestr.ru/fir_lite_rest/api/gkn/fir_objects/{cadNum}'
    try:
        # r = requests.get(url, headers=headers, verify="CertBundle.pem")
        r2 = requests.get(url2, headers=headers, verify="CertBundle.pem")
        # objectIds = []
        objectIds2 = []
        # for el in r.json():
        #     objectId = el.get("objectId")
        #     objectIds.append(objectId)

        for el2 in r2.json():
            objectId2 = el2.get("objectId")
            objectIds2.append(objectId2)
    except:
        print('Error!!! Нет объекта с таким кадастровым номером')
    # print("objectId официальные", objectIds)
    # print("objectId2 неофициальный", objectIds2)
    return objectIds2

def normalizationTypeStreet(type_street):
    type_ulicas = ["ул", "улица", "у", ]
    type_proezd = ["проезд", "пр-д", "пр"]
    type_pereulok = ["пер", "пер-к", "переулок"]
    type_prospect = ["пр-т", "п-кт", "проспект", "пр-кт"]
    type_shosse = ["шоссе", "ш", "ш.", "пр-кт"]

    type_street = type_street.replace(".", '')
    type_street = type_street.lower()
    if type_street in type_ulicas:
        type_street = "улица"
    if type_street in type_proezd:
        type_street = "проезд"
    if type_street in type_pereulok:
        type_street = "переулок"
    if type_street in type_prospect:
        type_street = "проспект"
    if type_street in type_shosse:
        type_street = "шоссе"
    return type_street


def checkTypeStreet(objects, type_street):
    for el in objects:
        street = el.get('street')
        index = street.find("|")
        _type_street = street[index + 1:]
        if normalizationTypeStreet(type_street) == normalizationTypeStreet(_type_street):
            check = True
        else:
            check = False
    return check

def getObjectByCadNum(cadNum):
    url = f'https://rosreestr.gov.ru/api/online/fir_objects/{cadNum}'
    try:
        objects = requests.get(url, headers=headers, verify="CertBundle.pem")

    except:
        print('Error!!! Нет объекта с таким кадастровым номером')
    return objects.json()

def getUrls(street, house, building, apartment):
    houses = [house]
    urls = []
    # Генерация адреса с тире и без тире в номере здания
    if str(house).isdigit():
        pass
    else:
        if "-" in house:
            houses.append(str(house.replace("-", '')))
        else:
            new_house = ''
            k = 0
            for el in house:
                if el.isdigit() or k == 1:
                    new_house = new_house + el
                else:
                    new_house = new_house + "-" + el
                    k = 1
            houses.append(new_house)
    for house in houses:
        url = getUrl(street, house, building, apartment)
        print(url)
        urls.append(url)
    return urls


def getUrl(street, house, building, apartment):
    if building != '':
        if apartment != '':
            url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
                  f'regionId=132431000000&street={street}&house={house}&building={building}&apartment={apartment}'
        else:
            url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
                  f'regionId=132431000000&street={street}&house={house}&building={building}'
    else:
        if apartment != '':
            url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
                  f'regionId=132431000000&street={street}&house={house}&apartment={apartment}'
        else:
            url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
                  f'regionId=132431000000&street={street}&house={house}'
    return url


def getByAdressCadNumbers(type_street, street, house, building, apartment):
    urls = getUrls(street, house, building, apartment)
    cadNumbers = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers, verify="CertBundle.pem")
            for el in response.json():
                cadNum = el.get('objectCn')
                if cadNum not in cadNumbers and cadNum != None  and len(cadNum) < 20:# Исключаем дубли и некорр кад ном
                    objects = getObjectByCadNum(cadNum)
                    if checkTypeStreet(objects, type_street): # Исключаем ошибку в типе улицы
                        cadNumbers.append(cadNum)
        except:
            print("нет такого адреса")
            continue
    return cadNumbers

