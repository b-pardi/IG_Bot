from botImports import *
from topSecretNoNoZone import *

"""
Small tests for various parts of the bot
NOT NEEDED FOR OPERATION
"""

if __name__ == '__main__':
    print("Gathering users from 'notfollowingback.txt'...")
    f = open("notfollowingback.txt", 'r+')
    profiles = []
    index = 0
    for line in f:
        profiles.append(index)
        profiles.append(line.strip())
        index += 1


    for name in profiles:
        print(name)
        time.sleep(0.1)

"""
Currently this prints alternating the numbers and names
fix that so it prints 0user 1anotheruser etc
then in loop that searches for user strip the first char (the number)
"""