const { spawn } = require("child_process");
const Alumni = require("./api/models/alumni/alumni");

const driver = () => {
  const dataSet = [];

  const python = spawn("python", ["./bot/app.py"]);

  python.stdout.on("data", (data) => {
    console.log("Pipe data from python script ...");
    dataSet.push(data);
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}\n`);
    
    for(alumnus in dataSet){
        try {
            // Check if alumnus already exists
            const alumnus = await Alumni.findOne({
              linkedIn: alumnus.linkedIn,
            });
        
            if (alumnus) {
              continue;
            }
        
            const newAlumnus = new Alumni({
              ...alumnus,
            });
        
            await newAlumnus.save();
            console.log({
              message: "Alumnus uploaded successfully",
              success: true,
            });
          } catch (err) {
            console.log({
              message: "Unable to upload alumnus",
              success: false,
            });
          }
    }

  });
};

module.expots = { driver };
