import os
import time
from datetime import datetime

def animation(trigger):
   try:
      while 1:
         curr_time = datetime.now().strftime("%H:%M:%S")    
         curr_time_list = curr_time.split(":")
         
         if (trigger==curr_time):
            break

         string = f"""
--------------
|{curr_time_list[0]}|:|{curr_time_list[1]}|:|{curr_time_list[2]}|
--------------
"""
         os.system('cls')

         print(string, flush=True, end='')
         time.sleep(1)

      print("wakey wakey, IT'S TIME TO GET UP")
      
   except KeyboardInterrupt:
      print("exiting...")

user_input = input("Enter time [HH:MM:SS]: ")
animation(user_input)