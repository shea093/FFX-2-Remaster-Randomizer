mys = "Not found!"
mys = mys.replace("Nota", "aaaa")
print(len(mys))

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