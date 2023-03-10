import serial
import subprocess
import os
import time

# Clear the terminal to make it nicer
subprocess.run("clear",shell = True)

# Prepare the teensy for MTP
print ("Preparing teensy")
teensy_mtp_hex_file_name = 'teensy_mtp.ino.TEENSY41.hex'
cur_dir = os.getcwd()
teensy_mtp_hex_path = cur_dir + '/teensy_mtp/'
os.chdir(teensy_mtp_hex_path)
teensy_upload_mtp_str = "teensy_loader_cli --mcu=TEENSY41 -w -s " + teensy_mtp_hex_file_name
#upload_stat = subprocess.run(teensy_upload_mtp_str,shell = True)
#while(upload_stat.returncode == 1):
#    print ("Upload failed. Retrying")
#    upload_stat = subprocess.run(teensy_upload_mtp_str,shell = True)
#print ("MTP Code uploaded")
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
    # Readin a cmd from terminal
    cmd = input("cmd: ")
    cmd_array = cmd.split()

    # Exit command
    if (cmd_array[0] == "quit"):
        try:
            teensy_ser.close()
            exit()
        except:
            exit()

    # Clear terminal command
    elif (cmd_array[0] == "clear"):
        subprocess.run("clear",shell = True)

    # Print help options
    elif (cmd_array[0] == "help"):
        print (help_str)

    # Begin serial connection with Teensy
    elif (cmd_array[0] == "connect"):
        try:
            teensy_port = cmd_array[1]
        except:
            teensy_port = "/dev/ttyACM0"
        try:
            teensy_baud = int(cmd_array[2])
        except:
            teensy_baud = 115200 
        try:
            teensy_ser = serial.Serial(teensy_port, teensy_baud, timeout = 5)
            teensy_ser.reset_input_buffer()
        except:
            print ("Connection failed. Retry with different port or baudrate")

    # List all file on the SD card
    elif (cmd_array[0] == "ls"):
        teensy_ser.write(bytes('1'.encode('utf-8')))
        time.sleep (0.1)
        print(teensy_ser.read(teensy_ser.in_waiting).decode())

    # Send a string to the teensy. for debugging only
    elif (cmd_array[0] == "send"):
        teensy_ser.write(bytes(cmd_array[1].encode('utf-8')))
        time.sleep(0.1)
        while (teensy_ser.in_waiting>0):
            print(teensy_ser.read())

    # Command to copy file from SD card to specified path
    # cp file_to_copy /destination/path/on/computer/
    elif (cmd_array[0] == "cp"):
        try:
            output_file = cmd_array[2] + cmd_array[1]
            teensy_ser.write(bytes('2'.encode('utf-8')))
            time.sleep(0.1)
            teensy_ser.write(bytes(cmd_array[1].encode('utf-8')))
            time.sleep(5)
            file_search_stat = teensy_ser.read(teensy_ser.in_waiting).decode()
            if (file_search_stat == "1"):
                print("File does not exist")
            elif (file_search_state == "0"):
                file_copy_completed == 0
                with open(output_file, mode=w) as f:
                    while file_copy_completed == 0:
                        inByte = teensy_ser.read()
                        if (int(inByte) == '-1'):
                            break
                        else:
                            f.write(inByte)
        except:
            print ('Invalid cp command')

    # Manually reset the input buffer from serial port. for Debugging
    elif (cmd_array[0] == "reset_buffer"):
        try:
            teensy_ser.reset_input_buffer()
        except:
            print ("port not opened")

    else:
        print ('Invalid command')
