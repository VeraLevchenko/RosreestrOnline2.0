import rosreestr_online

if __name__ == '__main__':
#----------------------официальные API______________________________________________
    # url = 'https://rosreestr.gov.ru/api/online/fir_objects/42:30:0302016:242'
    # url = 'https://rosreestr.gov.ru/api/online/fir_object/142_469806'
                # Запрос по адресу чувствителен к тире. Поэтому запрашивать надо по всем возможным вариантам. К регистру не чуствителен
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Металлургов&house=25&apartment=129'
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Строителей&house=7&building=1'
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Франкфурта&house=9А'

    type_street = 'улица'
    street = 'Франкфурта'
    house = '9-А'
    building = ''
    apartment = ''
    cadNumbers = rosreestr_online.getByAdressCadNumbers(type_street, street, house, building, apartment)
    # print("C данным адресом найдены объекты с кадастровыми номерами: ", cadNumbers)
    for cadNumber in cadNumbers:
        objectIds = rosreestr_online.getObjectId(cadNumber)
        print("cadNumber = ", cadNumber)
        print("objectIds", objectIds)
        for objectId in objectIds:
            print("objectId", objectId)
            objectType = rosreestr_online.getObjectType(objectId)
            # print(objectType)

