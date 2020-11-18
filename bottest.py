#from botImports import *
from topSecretNoNoZone import *
import re

"""
Small tests for various parts of the bot
NOT NEEDED FOR OPERATION
"""

if __name__ == '__main__':
    names_list = []
    with open ("notfollowingback.txt") as test_file:
        for line in test_file:
            names_list.append(line.strip())

    name_list = ['apple', 'orange', 'banana', 'strawberry', 'cantaloupe']

    for index, item in enumerate(names_list):
        if re.search("[z]", names_list[index]):
            #print(str(index) + ": " + item + "\n\t" + str(index+1) + ": " + names_list[index+1])
            print(str(index) + ": " + item + "\n\t" + str(index+1) + ": " + names_list[index+1])

    input("\n\npress enter to exit")
    quit()