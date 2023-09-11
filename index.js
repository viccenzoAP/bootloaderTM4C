const util = require('util');
const exec = util.promisify(require('child_process').exec);
const path = require('path');
const { stderr } = require('process');
const rpio = require('rpio');
const { Console } = require('console');

reset = 38;
bootLoaderStart = 40;

rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //define LED como output
rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.HIGH); //define LED como output

main();

success = 0
fail = 0

async function main(){
    result = await flash();
    if(result == 1){
            console.log("Boot successfull");
    }else{
        console.log("Boot failed");
    }
/*
    for(i=0;i<100;i++){
        console.log("Boot attempt: " + i)
        result = await flash();
        console.log(result);
        if(result == 1){
            console.log("Boot successfull");
            success++;
        }else{
            console.log("Boot failed");
            fail++;
        }
    }
    console.log("After 100 attempts the chip had booted " + success + " successfully and " + fail + " failed tries");
    */
}

async function flash(){
    console.log("Start BootMode");
    await otaMode();
    console.log('Start data transfer')

    var otaPath = path.join(__dirname, "data","ota.bin");
    //console.log(otaPath);
    try{
        //console.log(`python3 main.py ${otaPath}`);
        const { stdout, stderr } = await exec(`python3 main.py ${otaPath}`);
        // log the output received from the command
        console.log("Output:\n", stdout)
        result = stdout.split('\n')
        if(result[result.length-1] == "Boot process was successfull"){
            //console.log("the boot process was successfull");
            return 1
        }else{
            //console.log("the boot process failed");
            return 0;
        }
    }catch{
        console.log(stderr);
    }
    /*
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
            return 1
        }else{
            console.log("the boot process failed");
            return 0;
        }
    });*/
}

async function otaMode(){
    rpio.open(reset, rpio.OUTPUT, rpio.LOW); //reset
    await sleep(50);
    rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.LOW); //Boot
    await sleep(50);
    rpio.open(reset, rpio.OUTPUT, rpio.HIGH); //Reset off
    await sleep(50);
    rpio.open(bootLoaderStart, rpio.OUTPUT, rpio.HIGH); //boot off
    await sleep(50);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
