from tabulate import tabulate
import random
import binascii
import services

a = services.convert_gamevariable_to_reversed_hex(43,bytecount=1)
b = services.convert_gamevariable_to_reversed_hex(183,bytecount=1)
c = services.convert_gamevariable_to_reversed_hex(103,bytecount=1)
print(a,b,c)

str1 = '30 31 32 33 34 35 36 37 38 39 20 21 E2 80 9D 23 24 25 26 E2 80 99 28 29 2A 2B 2C 2D 2E 2F 3A 3B 3C 3D 3E 3F 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F E2 80 98 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D'
str2 = str1.split()
str3 = '0123456789 !”#$%&’()*+,-./:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_‘abcdefghijklmnopqrstuvwxyz{|}~·【】♪♥ “”— ¡↑↓←→¨«º '
str4 = []
for char in str3:
    str4.append(char)
print(str2)
print(str4)
print(len(str2),len(str4))
dict_str = ""

for index, h in enumerate(str2):
    dict_str = dict_str + "'" + str(hex(index+48)[2:])+ "' : '" + str(str4[index])  + "', "

dict_test = {
    '30' : '0', '31' : '1', '32' : '2', '33' : '3', '34' : '4', '35' : '5', '36' : '6', '37' : '7', '38' : '8',
    '39' : '9', '20' : ' ', '21' : '!', '9D' : '.', '23' : '#', '24' : '$', '25' : '%',
    '26' : '&', '99' : '™', '28' : '(', '29' : ')', '2A' : '*', '2B' : '+', '2C' : ',',
    '2D' : '-', '2E' : '.', '2F' : '/', '3A' : ':', '3B' : ';', '3C' : '<', '3D' : '=', '3E' : '>', '3F' : '?',
    '41' : 'A', '42' : 'B', '43' : 'C', '44' : 'D', '45' : 'E', '46' : 'F', '47' : 'G', '48' : 'H', '49' : 'I',
    '4A' : 'J', '4B' : 'K', '4C' : 'L', '4D' : 'M', '4E' : 'N', '4F' : 'O', '50' : 'P', '51' : 'Q', '52' : 'R',
    '53' : 'S', '54' : 'T', '55' : 'U', '56' : 'V', '57' : 'W', '58' : 'X', '59' : 'Y', '5A' : 'Z', '5B' : '[',
    '5C' : '/', '5D' : ']', '5E' : '^', '5F' : '_', 'E2' : 'â', '80' : '€', '98' : '˜', '61' : 'a', '62' : 'b',
    '63' : 'c', '64' : 'd', '65' : 'e', '66' : 'f', '67' : 'g', '68' : 'h', '69' : 'i', '6A' : 'j', '6B' : 'k',
    '6C' : 'l', '6D' : 'm', '6E' : 'n', '6F' : 'o', '70' : 'p', '71' : 'q', '72' : 'r', '73' : 's', '74' : 't',
    '75' : 'u', '76' : 'v', '77' : 'w', '78' : 'x', '79' : 'y', '7A' : 'z', '7B' : '{', '7C' : '|', '7D' : '}',
}

print(dict_str)

maxy = 255
c = "64 82 74 3A 70 7D 3A 78 83 74 7C 48"
c_list = []
for char in c:
    if char == " ":
        appendy = c[0:2]
        c_list.append(appendy)
        c = c[3:]
c_list.append(c)
print(c_list)
hex_nums = ['64', '82', '74', '3A', '70', '7D', '3A', '78', '83', '74', '7C', '48']
final_num = 0
for hex_num in hex_nums:
    final_num = final_num + int(hex_num,16)
print(hex(final_num))
print(final_num)


# print(float("0." + str(1)))
# #[lv x 0.1] + [(lv / 1B ) + 0C] - [lv^2] / 16[Constant] / C8 / 04
# #[lv x 0.A] + [(lv / B ) + C] - [lv^2] / 16[Constant] / D / E
# def luck_formula(A: int, B: int, C: int, D: int, E: int):
#     table = []
#     temp_list = []
#     count = 0
#     for level in range (1,100):
#         a_frac = A / 10
#         part1 = level * a_frac
#         part2 = (level / B) + C
#         part3 = level**2
#         formula_result = part1 + part2 - part3 / 16 / D / E
#         formula_output = str(level) + ". " + str(formula_result)
#         if count == 4:
#             temp_list.append(formula_output)
#             table.append(temp_list)
#             count = 0
#             temp_list = []
#         else:
#             count = count + 1
#             temp_list.append(formula_output)
#     print(tabulate(table))
#     print(table)
#         #print(str(level) + ". " + str((formula_result)))
# luck_formula(1, 27, 12, 200, 4)
#

# from itertools import permutations
#
# HP = 555555
# MP = 999
# LV = 99
# STR = 234
# MAG = 23
# DEF = 237
# MDEF = 81
# AGL = 255
# ACC = 99
# EVA = 1
# LUCK = 173
#
# stat_list = [HP,MP,LV,STR,DEF,MAG,MDEF,AGL,ACC,EVA,LUCK]
# hex_stat_str = ""
# hex_array_test = []
# count = 0
# for stat in stat_list:
#     count = count + 1
#     num = ""
#     if len(str(hex(stat)[2:])) == 1:
#         num = "0" + str(hex(stat)[2:])
#     elif len(str(hex(stat)[2:])) == 3:
#         temp = "00000" + str(hex(stat)[2:])
#         num = temp[6:8] + "0" + temp[5] + "0000"
#     elif len(str(hex(stat)[2:])) == 5:
#         temp = "000" + str(hex(stat)[2:])
#         print(temp)
#         num = temp[6:8] + temp[4:6] + temp[2:4] + temp[0:2]
#     else:
#         num = str(hex(stat)[2:])
#     if count == 1 or count == 2:
#         if len(num) == 2:
#             num = num + "000000"
#         if len(num) == 4:
#             num = num + "0000"
#     hex_array_test.append(num)
#     hex_stat_str = hex_stat_str + num   # Append
#
# print("\n")
# print(stat_list)
# print(hex_stat_str.upper())
# message = hex_stat_str.upper()
# new_message = ""
# for i in range(1,len(message)):
#     if i % 2 == 0:
#         new_message = new_message + " " + message[i-2:i]
# new_message = new_message[1:]
# print(len(hex_stat_str))
# print(new_message)
# print(hex_array_test)