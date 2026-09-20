#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const USAGE = `
Usage: node generate-talking-head.js [options]

Options:
  --image <path>     Path to portrait image (required for avatar generation)
  --audio <path>     Path to audio file (optional if using --text)
  --text <text>      Text with emotional tags for Bark TTS (optional if using --audio)
  --voice <preset>   Bark voice preset (default: v2/en_speaker_6)
  --prompt <text>    Text prompt to generate an image via SD 1.5
  --api <url>        Colab API URL from ngrok (or set COLAB_API_URL env var)
  --output <path>    Output path (default: public/assets/talking-head.mp4)
  --timeout <ms>     Request timeout in ms (default: 300000 = 5 min)
  --check            Check if the API server is reachable
  --help             Show this help message

Examples:
  # Generate from existing image + audio
  node scripts/generate-talking-head.js --image photo.png --audio voice.wav --api URL

  # Generate from image + text (Bark TTS generates audio)
  node scripts/generate-talking-head.js --image photo.png --text "MAN: [gasps] Wait!" --api URL

  # Generate avatar image from text prompt
  node scripts/generate-talking-head.js --prompt "professional African business owner, male, 30s" --api URL

  # Check API health
  node scripts/generate-talking-head.js --check --api URL
`;

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--image":
        opts.image = args[++i];
        break;
      case "--audio":
        opts.audio = args[++i];
        break;
      case "--text":
        opts.text = args[++i];
        break;
      case "--voice":
        opts.voice = args[++i];
        break;
      case "--prompt":
        opts.prompt = args[++i];
        break;
      case "--api":
        opts.apiUrl = args[++i];
        break;
      case "--output":
        opts.output = args[++i];
        break;
      case "--timeout":
        opts.timeout = parseInt(args[++i], 10);
        break;
      case "--check":
        opts.check = true;
        break;
      case "--help":
        console.log(USAGE);
        process.exit(0);
    }
  }
  return opts;
}

async function checkHealth(apiUrl) {
  console.log(`Checking API at ${apiUrl}...`);
  try {
    const res = await fetch(`${apiUrl}/health`);
    if (!res.ok) {
      console.error(`Server returned ${res.status}`);
      return false;
    }
    const data = await res.json();
    console.log(`Server OK - Models: ${data.models?.join(", ") || data.model || "unknown"}`);
    return true;
  } catch (err) {
    console.error(`Cannot reach server: ${err.message}`);
    return false;
  }
}

async function generateImage(opts) {
  const apiUrl = opts.apiUrl || process.env.COLAB_API_URL;
  if (!apiUrl) {
    console.error("Error: --api or COLAB_API_URL env var required");
    process.exit(1);
  }

  const prompt = opts.prompt;
  const outputPath = path.resolve(opts.output || `public/assets/generated-${Date.now()}.png`);
  const timeout = opts.timeout || 120000;

  console.log(`Prompt: "${prompt}"`);
  console.log(`API:    ${apiUrl}`);
  console.log(`Output: ${outputPath}`);
  console.log("");

  const boundary = `----Boundary${Date.now().toString(16)}`;

  const parts = [];
  parts.push(
    Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="text_prompt"\r\n\r\n${prompt}\r\n`
    )
  );
  parts.push(
    Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="width"\r\n\r\n512\r\n`
    )
  );
  parts.push(
    Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="height"\r\n\r\n512\r\n`
    )
  );
  parts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(parts);

  console.log("Generating image...");
  console.log("(This may take 10-30 seconds)");
  console.log("");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const startTime = Date.now();
    const res = await fetch(`${apiUrl}/generate-image`, {
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
      },
      body,
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`API error ${res.status}: ${errorText}`);
      process.exit(1);
    }

    const arrayBuf = await res.arrayBuffer();
    const imageBuffer = Buffer.from(arrayBuf);
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, imageBuffer);

    console.log(`Done! (${elapsed}s)`);
    console.log(`Output: ${outputPath}`);
    console.log(`Size:   ${(imageBuffer.length / 1024).toFixed(0)}KB`);
  } catch (err) {
    clearTimeout(timer);
    if (err.name === "AbortError") {
      console.error(`Request timed out after ${timeout / 1000}s`);
    } else {
      console.error(`Error: ${err.message}`);
    }
    process.exit(1);
  }
}

async function generateAvatar(opts) {
  const apiUrl = opts.apiUrl || process.env.COLAB_API_URL;
  if (!apiUrl) {
    console.error("Error: --api or COLAB_API_URL env var required");
    process.exit(1);
  }

  const imagePath = path.resolve(opts.image);
  const audioPath = path.resolve(opts.audio);
  const outputPath = path.resolve(opts.output || "public/assets/talking-head.mp4");
  const timeout = opts.timeout || 300000;

  if (!fs.existsSync(imagePath)) {
    console.error(`Image not found: ${imagePath}`);
    process.exit(1);
  }
  if (!fs.existsSync(audioPath)) {
    console.error(`Audio not found: ${audioPath}`);
    process.exit(1);
  }

  console.log(`Image: ${imagePath} (${(fs.statSync(imagePath).size / 1024).toFixed(0)}KB)`);
  console.log(`Audio: ${audioPath} (${(fs.statSync(audioPath).size / 1024).toFixed(0)}KB)`);
  console.log(`API:   ${apiUrl}`);
  console.log(`Output: ${outputPath}`);
  console.log("");

  const imageBuffer = fs.readFileSync(imagePath);
  const audioBuffer = fs.readFileSync(audioPath);
  const boundary = `----Boundary${Date.now().toString(16)}`;

  const imageExt = path.extname(imagePath).slice(1) || "png";
  const audioExt = path.extname(audioPath).slice(1) || "wav";
  const imageMime = imageExt === "jpg" ? "image/jpeg" : `image/${imageExt}`;
  const audioMime = audioExt === "mp3" ? "audio/mpeg" : `audio/${audioExt}`;

  const parts = [];

  parts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="image"; filename="${path.basename(imagePath)}"\r\n` +
        `Content-Type: ${imageMime}\r\n\r\n`
    )
  );
  parts.push(imageBuffer);
  parts.push(Buffer.from(`\r\n--${boundary}\r\n`));

  parts.push(
    Buffer.from(
      `Content-Disposition: form-data; name="audio"; filename="${path.basename(audioPath)}"\r\n` +
        `Content-Type: ${audioMime}\r\n\r\n`
    )
  );
  parts.push(audioBuffer);
  parts.push(Buffer.from(`\r\n--${boundary}\r\n`));

  parts.push(
    Buffer.from(
      `Content-Disposition: form-data; name="refine_lips"\r\n\r\ntrue\r\n`
    )
  );
  parts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(parts);

  console.log("Generating talking head video...");
  console.log("(This may take 30-120 seconds depending on the model)");
  console.log("");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const startTime = Date.now();
    const res = await fetch(`${apiUrl}/generate-full`, {
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
      },
      body,
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`API error ${res.status}: ${errorText}`);
      process.exit(1);
    }

    const arrayBuf = await res.arrayBuffer();
    const videoBuffer = Buffer.from(arrayBuf);
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, videoBuffer);

    console.log(`Done! (${elapsed}s)`);
    console.log(`Output: ${outputPath}`);
    console.log(`Size:   ${(videoBuffer.length / 1024 / 1024).toFixed(1)}MB`);
    console.log("");
    console.log("Next step: Update your fako_video_data.json to reference this video:");
    console.log(`  "video": "${path.relative(process.cwd(), outputPath).replace(/\\/g, "/")}"`);
  } catch (err) {
    clearTimeout(timer);
    if (err.name === "AbortError") {
      console.error(`Request timed out after ${timeout / 1000}s`);
    } else {
      console.error(`Error: ${err.message}`);
    }
    process.exit(1);
  }
}

async function main() {
  const opts = parseArgs();

  if (opts.check) {
    const apiUrl = opts.apiUrl || process.env.COLAB_API_URL;
    if (!apiUrl) {
      console.error("Error: --api or COLAB_API_URL env var required");
      process.exit(1);
    }
    const ok = await checkHealth(apiUrl);
    process.exit(ok ? 0 : 1);
  }

  if (opts.prompt) {
    await generateImage(opts);
    return;
  }

  if (!opts.image) {
    console.error("Error: --image is required (or use --prompt to generate an image)");
    console.log(USAGE);
    process.exit(1);
  }

  if (!opts.audio && !opts.text) {
    console.error("Error: --audio or --text is required");
    console.log(USAGE);
    process.exit(1);
  }

  await generateAvatar(opts);
}

main();
