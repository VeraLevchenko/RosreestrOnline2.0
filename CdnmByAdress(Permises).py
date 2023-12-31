# Программа берет данные из файла xlsx и возвращает кадастровые номера помещений
# 1. делает запрос в ЕГРН по адресу и возвращает перечень объектов с таким адресом
# 2. из перечня объектов выбираются кадастровые номера этих объектов
# 3. делает запрос в ЕГРН по данным кадастровым номерам и возвращает перечень Id ()
# 4. делает запрос в ЕГРН по данным ID и возвращает перечень объектов, который проверяется на, то что это помещение
# 5. Если помещение результат записывается в датафрэйм, затем в тот же файл


import rosreestr_online
import pandas as pd
import time

def getNumberMassiv(filename):
    start_time = time.time()  # время начала выполнения


#----------------------официальные API______________________________________________
    # url = 'https://rosreestr.gov.ru/api/online/fir_objects/42:30:0302016:242'
    # url = 'https://rosreestr.gov.ru/api/online/fir_object/142_469806'
                # Запрос по адресу чувствителен к тире. Поэтому запрашивать надо по всем возможным вариантам. К регистру не чуствителен
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Металлургов&house=25&apartment=129'
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Строителей&house=7&building=1'
    # url = 'https://rosreestr.gov.ru/api/online/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Франкфурта&house=9А'

#----------------------кодировка типов объектов--------------------------
    # 002001001000 / Земельный участок
    # 002001002000 / Здание
    # 002001003000 / Помещение
    # 002001004000 / Сооружение
    # 002001005000 / Объект незавершённого строительства
    # 002001006000 / Предприятие как имущественный комплекс
    # 002001008000 / Единый недвижимый комплекс
    # 002001009000 / Машино-место
    # 002001010000 / Иной объект недвижимости

    rezult = []
    df = pd.read_excel(filename, index_col=0, sheet_name='Лист1')
             # Сброс ограничений на количество выводимых рядов
    # pd.set_option('display.max_rows', 10)
            # отключаем перенос табл на другую строку
    pd.options.display.expand_frame_repr = False
            # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', 10)
            # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', 50)

    print(df.head(10))
    # len(df.index)

    for i in range(0, len(df.index)):
        print(f"{i}из{len(df.index)}")
        type_street = str(df.iloc[i]['street_abbr'])
        street = str(df.iloc[i]['street_fullname'])
        house = str(df.iloc[i]['house_fullname'])
        building = ''
        apartment = str(df.iloc[i]['appartment_number'])
        cadNumbers = rosreestr_online.getByAdressCadNumbers(type_street, street, house, building, apartment)
        rez = []
        if len(cadNumbers) != 0:
            for cadNumber in cadNumbers:
                objectIds, objectIds2 = rosreestr_online.getObjectId(cadNumber)
                if len(objectIds2) > 0:
                    objectDаta, objectType = rosreestr_online.getObjectType(objectIds2[0])
                    # print(objectType)
                    if objectType == '002001003000':
                        print("cadNumber = ", cadNumber)
                        print(objectType)
                        rez.append(cadNumber)
                else:
                    rez.append(cadNumber + "ID не найдено!!!!!!!!!!!!!")
        else:
            rez.append("Объект с таким адресом отсутствует на ГКУ")
        print(rez)
        rezult.append(rez)
    df.insert(loc=len(df.columns), column='CadNumbers', value=rezult)
    df.to_excel(filename, index=False)


    end_time = time.time()  # время окончания выполнения
    execution_time = end_time - start_time  # вычисляем время выполнения
    print(f"Время выполнения программы: {execution_time} секунд")


if __name__ == '__main__':
    for i in range(231, 276):
        filename = f'D:/No_cn_in_gar/результат простановки кадастровых/Massiv/{i}.xlsx'
        print(filename)
        getNumberMassiv(filename)