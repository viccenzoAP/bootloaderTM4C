const raspi = require('raspi');
const Serial = require('raspi-serial').Serial;
const rpio = require('rpio');

reset = 38;

async function main(){
  rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //define LED como output

  rpio.open(reset, rpio.OUTPUT, rpio.LOW); //reset
  await sleep(50);
  rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //Reset off
  await sleep(50);
  
  raspi.init(() => {
    var serial = new Serial({portId: "/dev/ttyUSB0",baudRate: 256000});
    //var serial = new Serial({portId: "/dev/ttyUSB0",baudRate: 115200});
    console.log(serial);
    serial.open(() => {
      serial.on('data', (data) => {
        process.stdout.write(data);
      });
    });
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main()


