from tabulate import tabulate
import random
import binascii




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