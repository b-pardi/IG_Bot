#from botImports import *
from topSecretNoNoZone import *
import re
import time

"""
Small tests for various parts of the bot
NOT NEEDED FOR OPERATION
"""

if __name__ == '__main__':

    iteration = []
    time_taken = []
    for i in range(0,100):
        start_time = time.time()
        time.sleep(float(i)/(350))
        end_time = time.time()
        iteration.append(i)
        time_taken.append(end_time - start_time)
        

    data = (iteration, time_taken)
    #print(data)

    with open ("time_data.txt", "w") as time_file:
        for point in iteration:
            time_file.write(f"{iteration[point-1]}, {time_taken[point-1]}\n")
        time_file.write("******\n")
        for point in iteration:
            time_file.write(f"{iteration[point-1]}\n")
        time_file.write("------\n")
        for point in iteration:
            time_file.write(f"{time_taken[point-1]}\n")



    #input("\n\npress enter to exit")
    quit()