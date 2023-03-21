/*
 * Teensy MTP CLI
 * 
 * Code should be uploaded to the teensy to interface with companion CLI python script. It can also intereact with any software
 * with serial terminal
 * 
 */
#include <SD.h>
#include <SPI.h>

// change this to match your SD shield or module;
// Arduino Ethernet shield: pin 4
// Adafruit SD shields and modules: pin 10
// Sparkfun SD shield: pin 8
// Teensy audio board: pin 10
// Teensy 3.5 & 3.6 & 4.1 on-board: BUILTIN_SDCARD
// Wiz820+SD board: pin 4
// Teensy 2.0: pin 0
// Teensy++ 2.0: pin 20
const int chipSelect = BUILTIN_SDCARD;

// Command list
// 1  - List all file on SD card
// 2  - Copy file with name

/*
 * TODO:
 *  delete specific files
 *  delete all
 */

String file_name;

void setup() {
  Serial.begin(115200);
//  while (!Serial){
//    ;
//  }

  // Initializing SD card
  Serial.print("Initializing SD card..........");
  delay(1000);
  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("done.");
}

void loop() {
  // Awaits command from Serial
  if (Serial.available() > 0) {
    // read the incoming byte:
    uint8_t inByte = Serial.read();
    if (inByte > 0){
        // If received list_all command
        if (inByte == 49){
          delay(10);
          list_all();
        }
        //If received cp command
        
        else if (inByte == 50){
          // Parse file name and check if exist. Send ack or error byte accordingly
          delay(10);
          file_name = Serial.readString();
          File myFile = SD.open(file_name.c_str());
          if (myFile){
            Serial.print("0");
            while(myFile.available()){
              //Send file content over serial
              Serial.write(myFile.read());

              // Implemented flow control. Only needed because python base host using pyserial has small buffer
              if (Serial.available()){
                if (Serial.read() == 56){
                  while (1){
                    if (Serial.read() == 57){
                      break;  
                    }
                  }
                }
              }
            }
            myFile.close();
            // Send EOF sequence for host to know when file is finished
            Serial.write(0xAA);
            Serial.write(0xBB);
            Serial.write(0xCC);
          }
          // Error if file does not esixt
          else{
            Serial.print("1");
          }
        }
          
        else if (inByte == 51){
          delay(10);
          file_name = Serial.readString();
          if (file_name == "all"){
            delete_all();
            
          }
          else{
            SD.remove(file_name.c_str());
            }
          
        }

        else {;}
      }
    }
  }


void delete_all(){
  File root = SD.open("/");
  while(true){
    File cur_file = root.openNextFile();
    if (!cur_file) {
        break;
      }
    String cur_name = cur_file.name();
    cur_file.close();
    SD.remove(cur_name.c_str());
  }
}

// Copy from listfile example from Arduino SD library
void list_all(){
  File root = SD.open("/");
  printDirectory(root, 0);
  root.close();
}

void printDirectory(File dir, int numSpaces) {
   while(true) {
     File entry = dir.openNextFile();
     if (! entry) {
       //Serial.println("** no more files **");
       break;
     }
     printSpaces(numSpaces);
     if (entry.name()[0] == '.'){
      continue;
     }
     Serial.print(entry.name());
     if (entry.isDirectory()) {
       Serial.println("/");
       printDirectory(entry, numSpaces+2);
     } else {
       // files have sizes, directories do not
       int n = log10f(entry.size());
       if (n < 0) n = 10;
       if (n > 10) n = 10;
       printSpaces(50 - numSpaces - strlen(entry.name()) - n);
       Serial.print("  ");
       Serial.print(entry.size(), DEC);
       Serial.println();
     }
     entry.close();
   }
}

void printSpaces(int num) {
  for (int i=0; i < num; i++) {
    Serial.print(" ");
  }
}
