import serial
import subprocess
import os

# Clear the terminal to make it nicer
subprocess.run("clear",shell = True)

# Prepare the teensy for MTP
print ("Preparing teensy")
teensy_mtp_hex_file_name = 'teensy_mtp.ino.TEENSY41.hex'
cur_dir = os.getcwd()
teensy_mtp_hex_path = cur_dir + '/teensy_mtp/'
os.chdir(teensy_mtp_hex_path)
teensy_upload_mtp_str = "teensy_loader_cli --mcu=TEENSY41 -w -s " + teensy_mtp_hex_file_name
upload_stat = subprocess.run(teensy_upload_mtp_str,shell = True)
while(upload_stat.returncode == 1):
    print ("Upload failed. Retrying")
    upload_stat = subprocess.run(teensy_upload_mtp_str,shell = True)
print ("MTP Code uploaded")
os.chdir(cur_dir)

# Teensy serial port parameters
teensy_port = "/dev/ttyACM0"
teensy_baud = 115200 

# Help menu
quit_help_str = "quit - exit application\n\n"
clear_help_str = "clear - clear terminal\n\n"
help_help_str =  "help - show options\n\n"
help_str = "Teensy MTP host application command list:\n\n" + clear_help_str + quit_help_str + help_help_str
print (help_str)



while (1):
    cmd = input("cmd: ")
    cmd_array = cmd.split()
    if (cmd_array[0] == "quit"):
        try:
            teensy_ser.close()
            exit()
        except:
            exit()
    elif (cmd_array[0] == "clear"):
        subprocess.run("clear",shell = True)
    elif (cmd_array[0] == "help"):
        print (help_str)
    elif (cmd_array[0] == "connect"):
        try:
            teensy_port = cmd_array[1]
        except:
            teensy_port = "/dev/ttyACM0"
        try:
            teensy_baud = int(cmd_array[2])
        except:
            teensy_baud = 115200 
        teensy_ser = serial.Serial(teensy_port, teensy_baud, timeout = 5)
        teensy_ser.reset_input_buffer()
    elif (cmd_array[0] == "ls"):
        teensy_ser.write(bytes('1'.encode('utf-8')))
        while (teensy_ser.in_waiting > 0):
            print(teensy_ser.read())
    else:
        print ('Invalid command')
