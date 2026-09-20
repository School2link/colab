const { Client } = require("@gradio/client");
const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

const SADTALKER_SPACE = "John6666/SadTalker";

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith("https") ? https : http;
    proto.get(url, { headers: { "User-Agent": "Mozilla/5.0" } }, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        downloadFile(response.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      if (response.statusCode !== 200) {
        reject(new Error("HTTP " + response.statusCode));
        return;
      }
      const file = fs.createWriteStream(dest);
      response.pipe(file);
      file.on("finish", () => {
        file.close();
        resolve();
      });
    }).on("error", (err) => {
      reject(err);
    });
  });
}

async function generateTalkingHead(imagePath, audioPath, outputPath) {
  console.log("\n[generate-avatar] Starting talking head generation...");
  console.log("  Image: " + imagePath);
  console.log("  Audio: " + audioPath);
  console.log("  Output: " + outputPath + "\n");

  if (!fs.existsSync(imagePath)) {
    throw new Error("Image not found: " + imagePath);
  }
  if (!fs.existsSync(audioPath)) {
    throw new Error("Audio not found: " + audioPath);
  }

  console.log("[1/4] Connecting to " + SADTALKER_SPACE + "...");
  const client = await Client.connect(SADTALKER_SPACE);
  console.log("  Connected!\n");

  console.log("[2/4] Preparing files...");
  const imageBuffer = fs.readFileSync(imagePath);
  const audioBuffer = fs.readFileSync(audioPath);

  const imageFile = new File([imageBuffer], path.basename(imagePath), { type: "image/png" });
  const audioFile = new File([audioBuffer], path.basename(audioPath), { type: "audio/wav" });
  console.log("  Files ready!\n");

  console.log("[3/4] Generating talking head (this may take 30-120s)...");
  console.log("  Please wait...");

  const result = await client.predict("/test", {
    source_image: imageFile,
    driven_audio: audioFile,
    preprocess: "full",
    still_mode: false,
    use_enhancer: true,
    batch_size: 1,
    size: "256",
    pose_style: 0,
    facerender: "facevid2vid",
    exp_scale: 1.0,
    use_ref_video: false,
    ref_video: null,
    ref_info: "pose",
    use_idle_mode: false,
    length_of_audio: 0,
    use_blink: true,
  });

  console.log("  Generation complete!\n");

  console.log("[4/4] Saving output...");
  const output = result.data;
  console.log("  Raw result:", JSON.stringify(output, null, 2));

  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Handle the response structure
  let videoUrl = null;
  if (Array.isArray(output) && output.length > 0) {
    const first = output[0];
    if (first && typeof first === "object") {
      if (first.video && first.video.url) {
        videoUrl = first.video.url;
      } else if (first.url) {
        videoUrl = first.url;
      } else if (first.path) {
        videoUrl = first.path;
      }
    } else if (typeof first === "string" && first.startsWith("http")) {
      videoUrl = first;
    }
  } else if (typeof output === "string" && output.startsWith("http")) {
    videoUrl = output;
  }

  if (videoUrl) {
    console.log("  Downloading from: " + videoUrl);
    try {
      await downloadFile(videoUrl, outputPath);
      const stat = fs.statSync(outputPath);
      console.log("  Saved to " + outputPath + " (" + (stat.size / 1024 / 1024).toFixed(2) + " MB)");
    } catch (dlErr) {
      console.log("  Download failed: " + dlErr.message);
      console.log("\n  Please download manually from the URL above.");
    }
  } else {
    console.log("  Could not extract video URL from response.");
    console.log("  Please check the output manually.");
  }

  console.log("\n[generate-avatar] Done!\n");
  return outputPath;
}

const args = process.argv.slice(2);
const imageIdx = args.indexOf("--image");
const audioIdx = args.indexOf("--audio");
const outputIdx = args.indexOf("--output");

if (imageIdx === -1 || audioIdx === -1) {
  console.error("\nUsage: node scripts/generate-avatar.js --image <path> --audio <path> [--output <path>]\n");
  process.exit(1);
}

const imagePath = args[imageIdx + 1];
const audioPath = args[audioIdx + 1];
const outputPath = outputIdx !== -1 ? args[outputIdx + 1] : path.join("public", "assets", "talking-head.mp4");

generateTalkingHead(imagePath, audioPath, outputPath).catch((err) => {
  console.error("\n[generate-avatar] Error:", err.message);
  process.exit(1);
});
