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
quit_help_str = "quit - \n    exit application\n\n"
clear_help_str = "clear - \n    clear terminal\n\n"
help_help_str =  "help - \n    show options\n\n"
copy_help_str = "cp file_to_copy /destination/path/on/computer/ - \n    copy specific file from SD to specified location on computer(requires all arguments)\n\n"
ls_help_str = "ls - \n    list all files on the SD card\n\n"
connect_help_str = "connect PORT BAUDRATE - \n    PORT - serial port after /dev/. Default is /dev/ttyAMC0\n    BAURATE - Default is 115200\n\n"
del_help_str = "rm file_to_delete/all - \n    delete a specific file or delete all content\n\n"
help_str = "Teensy MTP host application command list:\n\n" + connect_help_str +ls_help_str + copy_help_str + del_help_str +clear_help_str + quit_help_str + help_help_str
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
            teensy_port = "/dev/" + cmd_array[1]
        except:
            teensy_port = "/dev/ttyACM0"
        try:
            teensy_baud = int(cmd_array[2])
        except:
            teensy_baud = 115200 
        try:
            teensy_ser = serial.Serial(teensy_port, teensy_baud ,timeout = 5)
            teensy_ser.reset_input_buffer()
        except:
            print ("Connection failed. Retry with different port or baudrate")

    # List all file on the SD card
    elif (cmd_array[0] == "ls"):
        try:
            teensy_ser.reset_input_buffer()
            teensy_ser.write(bytes('1'.encode('utf-8')))
            time.sleep (0.1)
            print(teensy_ser.read(teensy_ser.in_waiting).decode())
        except:
            print ("No device connected")

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
            teensy_ser.reset_input_buffer()
            output_file = cmd_array[2] + cmd_array[1]
            # Send CP command
            teensy_ser.write(bytes('2'.encode('utf-8')))
            time.sleep(0.1)
            # Send file name
            teensy_ser.write(bytes(cmd_array[1].encode('utf-8')))
            time.sleep(0.1)
            # Check if file exists
            file_search_stat = teensy_ser.read().decode()
            if (file_search_stat == "1"):
                print("File does not exist")
            elif (file_search_stat == "0"):
                print ("Copying file")
                file_copy_completed = False
                end_file_pos = 0
                flow_stopped = False
                with open(output_file, mode='wb') as f:
                    while not file_copy_completed:
                        # Flow control because pyserial buffer is small
                        if teensy_ser.in_waiting > 2000 and not flow_stopped:
                            teensy_ser.write(bytes('8'.encode('utf-8')))
                            flow_stopped = True
                        if teensy_ser.in_waiting < 100 and flow_stopped:
                            teensy_ser.write(bytes('9'.encode('utf-8')))
                            flow_stopped = False
                        inByte = teensy_ser.read()
                        # Check for EOF sequence
                        if end_file_pos == 0 and inByte == b'\xaa':
                            end_file_pos = 1
                        elif end_file_pos == 1 and inByte == b'\xbb':
                            end_file_pos = 2
                        elif end_file_pos == 2 and inByte == b'\xcc':
                            file_copy_completed = True
                        else:
                            end_file_pos = 0
                        f.write(inByte)
                    f.seek(-3, os.SEEK_END)
                    f.truncate()
                    print("Done")
        except Exception as e:
            print (e)
            print ('Invalid cp command')
    elif (cmd_array[0] == "rm"):
        try:
            del_promtp = "Are you sure you want to delete " + cmd_array[1] + "? [y/n]   "
            del_confirm = input(del_promtp)
            if del_confirm == "y":
                teensy_ser.write(bytes('3'.encode('utf-8')))
                time.sleep(0.1)
                # Send file name
                teensy_ser.write(bytes(cmd_array[1].encode('utf-8')))
                time.sleep(0.1)
        except Exception as e:
            print (e)

    # Manually reset the input buffer from serial port. for Debugging
    elif (cmd_array[0] == "reset_buffer"):
        try:
            teensy_ser.reset_input_buffer()
        except:
            print ("port not opened")

    else:
        print ('Invalid command')
