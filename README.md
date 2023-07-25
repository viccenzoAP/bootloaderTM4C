# TM4C boatloader

This code is used to create a boot partition that will perform ota as requested.

This code was developd for TI TM4C MCU family. However this was only tested at TM4C123BE6PM

This code was tested on a raspberry pi zero 2W over a USB to Serial adapter (/dev/ttyUSB0)

## Instalation process

* Install node, npm and python


* clone this repository
  ![image](https://github.com/viccenzoAP/bootloaderTM4C/assets/98824931/d531aebf-e98f-490f-9c17-7c81495a755c)
* Install npm packages inside the folder (sudo npm i)
  ![image](https://github.com/viccenzoAP/bootloaderTM4C/assets/98824931/1da3e95d-02d8-4468-afdb-86bc732a18af)
* save the firmware file inside the "data" folder and name the file "ota.bin"
  ![image](https://github.com/viccenzoAP/bootloaderTM4C/assets/98824931/daab0608-a12f-40ee-b0cb-a8e098930c51)
* Run the process with "sudo node index.js" command

## expected behavior

* the sistem will automaticaly restart and enter em boot mode (all led indication green)
* the sistem will perform a memory cleaning proceadure and, if successfull, all leds will turn off
* the system will request to write the bin file (first led will light up)
* the systemm will start the flashing procedure (seccond led will light up)
* the system will request the end of flashing procedure (third led will light up)
* If the procedure works correctly all led will blink 4 times and a restrat happends
* The new firmware shoud be loaded now and the procedure is complete
