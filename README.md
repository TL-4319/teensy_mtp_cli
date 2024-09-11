# Teensy Media Transfer Protocol (MTP) Library
This library allows for working with micro SD card mounted on Teensy 4.1 through the USB connection. 

## Dependencies

* Python 3
* pySerial
* Teensyduino or Arduino IDE

## Teensy code
Before using MTP functionalities, one need to upload the embbeded code provided in ```/teensy_mtp/```. There are two files:

* ```/teensy_mtp/teensy_mtp.ino``` - can be used to upload the code from Arduino IDE
* ```/teensy_mtp/teensy_mtp.ino.TEENSY41.hex``` - compiled hex file for Teensy 4.1 that can be uploaded directly with Teensyduino 

## Host application

The library provide a sample python CLI application to interact with the Teensy for various operations such as

* list files
* copy files
* delete files

Enter "help" in command line after running python script to list all available commands.

## Usage note
Using the provide ```mtp_host.py``` might be slow. This is because the implemented MTP also support flow control where the host device can command the teensy to pause data transfer if the input buffer of the host device is near full to prevent buffer overflow. This is needed because in the current implementation on Linux, the PC serial inpt buffer is only 4096. Trial and error shows that it is more reliable to stop data transfer when the buffer is around 50% (2000 bytes) full which is somewhat inefficient. This will be a persistent issue unless there is a way for pySerial to increase the input buffer on Linux. Note: I have yet to test this on Windows and maybe the implementation there has a way to change buffer size.

The best hack around way to get data fast at the moment is to use [HTerm](https://www.der-hammer.info/pages/terminal.html) which is a serial monitor. It has a significantly greater buffer and was able to transfer logs from 10 minutes flights in seconds. To use HTerm with MTP, ensure that the MTP embedded code has been uploaded to the teensy and serial connection has been made between HTerm and the Teensy. Then in the "Input control" section, ensure input type is "ASC" for ASCII characters. You can send string "1" and should receive the list of file on the SD card. To transfer a file, first clear the received buffer. Then enter "2<FILE_NAME>". Once transfer is completed, one can just save the entire input buffer from HTerm to a file and it will be just like a typical ```*.bfs``` file. 
