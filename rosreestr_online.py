import requests

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
				  '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'.encode('UTF-8'),
	'Content-Type': 'application/json',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

api_adres = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000'
api_cadnum = 'https://rosreestr.gov.ru/api/online/fir_objects/'
api_objectId = 'https://rosreestr.gov.ru/api/online/fir_object/'


def getUrl(street, house, building, apartment):
	if building != 'None':
		if apartment != 'None':
			url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
				f'regionId=132431000000&street={street}&house={house}&building={building}&apartment={apartment}'
		else:
			url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
				f'regionId=132431000000&street={street}&house={house}&building={building}'
	else:
		if apartment != 'None':
			url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
				f'regionId=132431000000&street={street}&house={house}&apartment={apartment}'
		else:
			url = f'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&' \
				f'regionId=132431000000&street={street}&house={house}'
	return url


def getCadNumByAdress(type_street, street, house, building, apartment):
	url = getUrl(street, house, building, apartment)
	print(url)
	try:
		cadNum_list = []
		response = requests.get(url, headers=headers, verify="CertBundle.pem")
		for el in response.json():
			cadNum = el.get('objectCn')
			if cadNum not in cadNum_list and cadNum != None:
				cadNum_list.append(cadNum)
				print(cadNum)
		print(cadNum_list)
	except:
		print('Error!!!')

	# for el in response.json():
	# 	print(el.get('objectCn'))

	return


def getCadNumParcel(type_street, street, house):
	# url = 'https://rosreestr.ru/fir_lite_rest/api/gkn/address/' \
	# 	  'fir_objects?macroRegionId=132000000000&regionId=132431000000&street=' + str(street) + '&house=' + str(house)
	url = 'https://rosreestr.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=' + str(
		street) + '&house=' + str(house)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	# print(r.json())
	cadNumParcel = []
	for a in r.json():
		if a.get("objectType") == "parcel":
			_type_street = a.get("street")
			index = _type_street.find("|")
			_type_street = _type_street[index + 1:]
			cadnum = a.get("objectCn")
			if getRemoved(cadnum) == 0 and normalizationTypeStreet(type_street) == normalizationTypeStreet(
					_type_street):
				cadNumParcel.append(cadnum)
	return cadNumParcel
