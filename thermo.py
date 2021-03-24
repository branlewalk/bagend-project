# import os
import glob
import time


# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')


def read_temp_raw(device_folder):
    f = open(device_folder + '/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_folder):
    lines = read_temp_raw(device_folder)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_folder)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def read_sensor():
    thermo = 0
    sensors = []
    for device_folder in device_folders:
        sensors.append(read_temp(device_folder))
        thermo += 1
    return sensors


# while True:
#     thermo = 1
#     for device_folder in device_folders:
#         temps = read_temp(device_folder)
#         print("Thermocouple: " + str(thermo) + " " + str(temps[0]) + "C " + str(temps[1]) + "F.")
#         thermo += 1
#     time.sleep(1)
