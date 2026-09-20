const { Client } = require("@gradio/client");
const fs = require("fs");
const path = require("path");

async function downloadFromSpace() {
  console.log("Connecting to akin23/SadTalker-API...");
  const client = await Client.connect("akin23/SadTalker-API");
  
  // Try to list files in the results directory
  try {
    console.log("Trying to access file via download...");
    // The file path from the response
    const filePath = "/home/user/app/results/video_20260918_164107.mp4";
    
    // Try different download methods
    const methods = [
      () => client.download(filePath, "public/assets/talking-head.mp4"),
      () => client.file(filePath),
      () => client.read(filePath),
    ];
    
    for (let i = 0; i < methods.length; i++) {
      try {
        console.log(`Trying method ${i + 1}...`);
        const result = await methods[i]();
        console.log(`Method ${i + 1} result:`, result);
        if (result) {
          if (Buffer.isBuffer(result)) {
            fs.writeFileSync("public/assets/talking-head.mp4", result);
            console.log("Saved buffer to file");
          } else if (typeof result === "string" && fs.existsSync(result)) {
            fs.copyFileSync(result, "public/assets/talking-head.mp4");
            console.log("Copied file");
          }
        }
      } catch (e) {
        console.log(`Method ${i + 1} failed: ${e.message}`);
      }
    }
  } catch (e) {
    console.log("Error:", e.message);
  }
}

downloadFromSpace().catch(console.error);
