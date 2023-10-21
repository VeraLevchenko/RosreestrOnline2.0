
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
    df = pd.read_excel(filename, index_col=0, sheet_name='Sheet1')
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
    k = 2
    for i in range(0, k):
        rez = []
        print(f"{i}из{len(df.index)}")
        cadNumber = str(df.iloc[i]['CadNumbers'])
        if len(cadNumber) <= 23:
            print(cadNumber)
            objectIds2 = rosreestr_online.getObjectId(cadNumber)
            print("objectIds2", objectIds2)
            if len(objectIds2) > 0:
                objectDаta, objectType = rosreestr_online.getObjectType(objectIds2[0])
                objectName = objectDаta.get("objectName")
                removed = objectDаta.get("removed")
                print("objectName:", objectName)
                print("removed:", removed)
                rez.append(objectName)
                rez.append(removed)
            else:
                rez.append("Объект с таким адресом отсутствует на ГКУ")
        else:
            rez.append("Пропускаю")
        rezult.append(rez)
    blank = [i for i in range(1, 2)]
    print(blank)
    print(rezult)
    # df.insert(loc=len(df.columns), column='objectName', value=rezult)
    # df.to_excel(filename, index=False)


    end_time = time.time()  # время окончания выполнения
    execution_time = end_time - start_time  # вычисляем время выполнения
    print(f"Время выполнения программы: {execution_time} секунд")


if __name__ == '__main__':
    # for i in range(511, 512):
    filename = f'D:/No_cn_in_gar/результат простановки кадастровых/Помещения/sales_combined.xlsx'
    print(filename)
    getNumberMassiv(filename)