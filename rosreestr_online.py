import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'.encode('UTF-8'),
    'Content-Type': 'application/json',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

api_adres = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000'
api_cadnum = 'https://rosreestr.gov.ru/api/online/fir_objects/'
api_objectId = 'https://rosreestr.gov.ru/api/online/fir_object/'


def getObjectType(objectId):
    url = f'https://rosreestr.gov.ru/api/online/fir_object/{objectId}'
    try:
        r = requests.get(url, headers=headers, verify="CertBundle.pem")
        # objectTypes = []
        print("Результат по запросу id", r.json())
        # for el in r.json():
        #     print(el)
        #     objectType = el.get("objectId")
        #     objectTypes.append(objectType)
        #     # if "_" in objectIds:
        #     #     objectId = objectIds
        #     # else:
        #     #     objectId = "objectId отсутстует"
        objectTypes = "dsv"
        return objectTypes
    except:
        print('Error!!! Нет объекта с таким Id')
    # return objectTypes

def getObjectId(cadNum):
    url = f'https://rosreestr.gov.ru/api/online/fir_objects/{cadNum}'
    try:
        r = requests.get(url, headers=headers, verify="CertBundle.pem")
        objectIds = []
        for el in r.json():
            objectId = el.get("objectId")
            objectIds.append(objectId)
            # if "_" in objectIds:
            #     objectId = objectIds
            # else:
            #     objectId = "objectId отсутстует"
        return objectIds
    except:
        print('Error!!! Нет объекта с таким кадастровым номером')
    return objectId
	# for i in el:
	# 	objectIds = el.get("objectId")
	# 	if "_" in objectIds:
	# 		objectId = objectIds
	# 	else:
	# 		objectId = "objectId отсутстует"
    objectId = "5"
    return objectId
def normalizationTypeStreet(type_street):
	type_ulicas = ["ул", "улица", "у", ]
	type_proezd = ["проезд", "пр-д", "пр"]
	type_pereulok = ["пер", "пер-к", "переулок"]
	type_prospect = ["пр-т", "п-кт", "проспект", "пр-кт"]

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
        print(new_house)
        houses.append(new_house)
    for house in houses:
        url = getUrl(street, house, building, apartment)
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
        print(url)
        try:
            response = requests.get(url, headers=headers, verify="CertBundle.pem")
            for el in response.json():
                cadNum = el.get('objectCn')
                if cadNum not in cadNumbers and cadNum != None:  # Исключаем дубли
                    objects = getObjectByCadNum(cadNum)
                    if checkTypeStreet(objects, type_street): # Исключаем ошибку в типе улицы
                        cadNumbers.append(cadNum)
        except:
            print("нет такого адреса")
            continue
    return cadNumbers

