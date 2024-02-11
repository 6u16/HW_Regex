#from pprint import pprint
from copy import deepcopy  # Копирвание без последующей ссылки на объект
import csv
import os
import re


# Домашнее задание к лекции 2.2 «Regular expressions»

# Сортируем ФИО
def name_sort(l_data):
    contacts_list_struct = deepcopy(l_data)
    l_lfs = []
    
    for i, elem in enumerate(contacts_list_struct):
        s_lfs = ''.join(elem[0])
        l_lfs = s_lfs.split()
        
        if len(l_lfs)<2:  # пверяем степень запонения даннми ФИО
            s_lfs = ''.join(elem[1])
            l_lfs.extend(s_lfs.split())
            
        if len(l_lfs)<3:
            s_lfs = ''.join(elem[2])
            l_lfs.extend(s_lfs.split())
            
        try:  # Тот случай если отсутствует элемент ФИО
            elem[0] = l_lfs[0]
            elem[1] = l_lfs[1]
            elem[2] = l_lfs[2]
        except Exception:
            print('low info')
        l_lfs = []
    return contacts_list_struct

# Форматирование телефонов (Regex)
def phone_regex(l_data):
    contacts_list_struct = deepcopy(l_data)
    pattern = r'(\+7|8)?\s*\((\d+)\)\s*(\d+)[\s-](\d+)[\s-](\d+)|(\d+)[\s]*(\d+)[\s-](\d+)[\s-](\d+)|(\+7)(\d+)|([\доб.\s*]\d+)'  # r - это чтобы питон не воспринимал \ как свою операцию
    
    for elem in contacts_list_struct:
        l_phone = re.findall(pattern, elem[-2])
        if l_phone:  # проверка на пустую строку в списке
            s_phone = ''.join(l_phone[0])  # соединяем данне в кортеже[0] - это телефон без добавочного номера, чтобы получить подряд цифры телефона
            
            if len(s_phone)>10 and s_phone[0] != '+' and s_phone[1] != '7':  # форматирум в +79999999999
                s_phone = f'+7{s_phone[1:]}'
            s_phone = f'+7({s_phone[2:5]}){s_phone[5:8]}-{s_phone[8:10]}-{s_phone[10:12]}'
            
            if len(l_phone)>1: # Если список содержит 2 элмента кортежа, то 2й это добавочный номер, плюсуем
                s_phone_ad = ''.join(l_phone[1])
                s_phone = f'{s_phone} доб.{s_phone_ad[1:]}' # какой то празитарный пробел вначале не берётся .strip()
            
            elem[-2] = s_phone
    return contacts_list_struct
            
# Cлияние одинаковых персон
def merge_fun(l_data):
    contacts_list_struct = deepcopy(l_data)
    l_dublicate = []
    
    for i, elem_01 in enumerate(contacts_list_struct):  # Сравниваем данные и извлекаем дубликаты с удалением из нашего списка
        for j, elem_02 in enumerate(contacts_list_struct):
            if i!=j:  # Без повтоений
                if elem_01[0] == elem_02[0] and elem_01[1] == elem_02[1] and elem_01[3] == elem_02[3]\
                    or elem_01[0] == elem_02[0] and elem_01[1] == elem_02[1] and elem_01[3] == '':  # Условие совпадения ФИО либо ФИ
                    l_dublicate.append(elem_02)  # Создаём список дубликатов
                    contacts_list_struct.pop(j)  # Удаляем дбликаты
    
    for i, elem_01 in enumerate(contacts_list_struct):  # Дополняем чистый список данными если какие то строки пусты
        for j, elem_02 in enumerate(l_dublicate):
            if elem_01[0] == elem_02[0] and elem_01[1] == elem_02[1]: # Проверка по ФИ
                for i_1, mrg_el in enumerate(elem_01):  # Проверяем на пустую строку
                    if mrg_el == '':
                        elem_01[i_1] = elem_02[i_1]  # Дополняем данные
    return contacts_list_struct
                    

if __name__=='__main__':

    file_path = os.path.join(os.getcwd(), 'data')
    
    with open(f'{file_path}\phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    header = contacts_list.pop(0)
    
    l_clean = name_sort(contacts_list)
    l_clean = phone_regex(l_clean)
    l_clean = merge_fun(l_clean)
    l_clean.insert(0, header)

    with open(f'{file_path}\phonebook.csv', 'w', newline='', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(l_clean)