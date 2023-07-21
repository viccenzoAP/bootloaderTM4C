const { exec } = require('child_process')
const path = require('path');
const rpio = require('rpio');

reset = 38;
bootLoaderStart = 40;

rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //define LED como output
rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.HIGH); //define LED como output

main();

async function main(){
    flash();
}

async function flash(){
    console.log("Start Flashing");
    await sleep(1000);
    console.log("Start BootMode");
    await otaMode();
    console.log('Start data transfer')
    await sleep(1000);

    var otaPath = path.join(__dirname, "data","ota.bin");
    console.log(otaPath);

    exec(`python3 main.py ${otaPath}`, (err, output) => {
        // once the command has completed, the callback function is called
        if (err) {
            // log and return if we encounter an error
            console.error("could not execute command: ", err)
            return
        }
        // log the output received from the command
        console.log("Output:\n", output)
        result = output.split('\n')
        if(result[result.length-1] == "Boot process was successfull"){
            console.log("the boot process was successfull");
        }else{
            console.log("the boot process failed");
        }
    });
}

async function otaMode(){
    rpio.open(reset, rpio.OUTPUT, rpio.LOW); //define LED como output
    await sleep(1000);
    rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.LOW); //define LED como output
    await sleep(1000);
    rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //define LED como output
    await sleep(1000);
    rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.HIGH); //define LED como output
    await sleep(1000);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}