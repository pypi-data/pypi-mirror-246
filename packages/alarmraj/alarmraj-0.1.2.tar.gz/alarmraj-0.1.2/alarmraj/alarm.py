import pkg_resources
from datetime import datetime
from playsound import playsound
import os, sys, time

audio_path = "alarmraj/assets/a1.mp3"

def path_convertor(audio_path):
    return pkg_resources.resource_filename(audio_path)

def main():
    user_input = input("Enter time [HH:MM:SS]: ")

    try:
        while 1:
            curr_time = datetime.now().strftime("%H:%M:%S")    
            curr_time_list = curr_time.split(":")
            
            if (user_input==curr_time):
                break

            string = f"""--------------
|{curr_time_list[0]}|:|{curr_time_list[1]}|:|{curr_time_list[2]}|
--------------
"""
            os.system('cls')
            print(string, flush=True, end='')
            time.sleep(1)
            
        print("wakey wakey, IT'S TIME TO GET UP")
        audio_path = path_convertor(audio_path)
        playsound(audio_path)
        
    except KeyboardInterrupt:
        print("exiting...")

if __name__ == "__main__":
    main()