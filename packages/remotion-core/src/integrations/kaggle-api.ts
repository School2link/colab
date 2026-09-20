import fs from "fs";
import path from "path";

export interface KaggleApiOptions {
  apiUrl: string;
  imagePath: string;
  audioPath: string;
  outputPath?: string;
  timeoutMs?: number;
  refineLips?: boolean;
}

export interface KaggleApiResult {
  videoPath: string;
  fileSize: number;
}

export interface GenerateImageOptions {
  apiUrl: string;
  prompt: string;
  outputPath?: string;
  width?: number;
  height?: number;
  timeoutMs?: number;
}

export interface GenerateImageResult {
  imagePath: string;
  fileSize: number;
}

export interface GenerateBrollOptions {
  apiUrl: string;
  prompt: string;
  duration?: number;
  outputPath?: string;
  timeoutMs?: number;
}

export interface GenerateBrollResult {
  videoPath: string;
  fileSize: number;
}

export async function generateTalkingHeadKaggle(
  options: KaggleApiOptions
): Promise<KaggleApiResult> {
  const {
    apiUrl,
    imagePath,
    audioPath,
    outputPath,
    timeoutMs = 300000,
    refineLips = true,
  } = options;

  const resolvedImagePath = path.resolve(imagePath);
  const resolvedAudioPath = path.resolve(audioPath);

  if (!fs.existsSync(resolvedImagePath)) {
    throw new Error(`Image not found: ${resolvedImagePath}`);
  }
  if (!fs.existsSync(resolvedAudioPath)) {
    throw new Error(`Audio not found: ${resolvedAudioPath}`);
  }

  console.log(`[kaggle-api] Connecting to ${apiUrl}...`);

  const imageBuffer = fs.readFileSync(resolvedImagePath);
  const audioBuffer = fs.readFileSync(resolvedAudioPath);

  const boundary = `----FormBoundary${Date.now().toString(16)}`;

  const imageExt = path.extname(resolvedImagePath).slice(1) || "png";
  const audioExt = path.extname(resolvedAudioPath).slice(1) || "wav";
  const imageMime = imageExt === "jpg" ? "image/jpeg" : `image/${imageExt}`;
  const audioMime = audioExt === "mp3" ? "audio/mpeg" : `audio/${audioExt}`;

  const bodyParts: Buffer[] = [];

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="image"; filename="${path.basename(resolvedImagePath)}"\r\n` +
        `Content-Type: ${imageMime}\r\n\r\n`
    )
  );
  bodyParts.push(imageBuffer);
  bodyParts.push(Buffer.from(`\r\n`));

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="audio"; filename="${path.basename(resolvedAudioPath)}"\r\n` +
        `Content-Type: ${audioMime}\r\n\r\n`
    )
  );
  bodyParts.push(audioBuffer);
  bodyParts.push(Buffer.from(`\r\n`));

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="refine_lips"\r\n\r\n` +
        `${refineLips}\r\n`
    )
  );

  bodyParts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(bodyParts);

  console.log(`[kaggle-api] Sending image (${(imageBuffer.length / 1024).toFixed(0)}KB) + audio (${(audioBuffer.length / 1024).toFixed(0)}KB)...`);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${apiUrl}/generate-full`, {
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
      },
      body,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error ${response.status}: ${errorText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    const videoBuffer = Buffer.from(arrayBuffer);

    const resolvedOutputPath = outputPath
      ? path.resolve(outputPath)
      : path.resolve(
          "public/assets/talking-head.mp4"
        );

    const outputDir = path.dirname(resolvedOutputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(resolvedOutputPath, videoBuffer);

    console.log(`[kaggle-api] Video saved: ${resolvedOutputPath} (${(videoBuffer.length / 1024 / 1024).toFixed(1)}MB)`);

    return {
      videoPath: resolvedOutputPath,
      fileSize: videoBuffer.length,
    };
  } catch (err: any) {
    clearTimeout(timeout);
    if (err.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs / 1000}s`);
    }
    throw err;
  }
}

export async function generateImageKaggle(
  options: GenerateImageOptions
): Promise<GenerateImageResult> {
  const {
    apiUrl,
    prompt,
    outputPath,
    width = 512,
    height = 512,
    timeoutMs = 120000,
  } = options;

  console.log(`[kaggle-api] Generating image: "${prompt}"...`);

  const boundary = `----FormBoundary${Date.now().toString(16)}`;

  const bodyParts: Buffer[] = [];

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="text_prompt"\r\n\r\n` +
        `${prompt}\r\n`
    )
  );

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="width"\r\n\r\n` +
        `${width}\r\n`
    )
  );

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="height"\r\n\r\n` +
        `${height}\r\n`
    )
  );

  bodyParts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(bodyParts);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${apiUrl}/generate-image`, {
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
      },
      body,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error ${response.status}: ${errorText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    const imageBuffer = Buffer.from(arrayBuffer);

    const resolvedOutputPath = outputPath
      ? path.resolve(outputPath)
      : path.resolve(`public/assets/generated-${Date.now()}.png`);

    const outputDir = path.dirname(resolvedOutputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(resolvedOutputPath, imageBuffer);

    console.log(`[kaggle-api] Image saved: ${resolvedOutputPath} (${(imageBuffer.length / 1024).toFixed(0)}KB)`);

    return {
      imagePath: resolvedOutputPath,
      fileSize: imageBuffer.length,
    };
  } catch (err: any) {
    clearTimeout(timeout);
    if (err.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs / 1000}s`);
    }
    throw err;
  }
}

export async function generateBrollKaggle(
  options: GenerateBrollOptions
): Promise<GenerateBrollResult> {
  const {
    apiUrl,
    prompt,
    duration = 5,
    outputPath,
    timeoutMs = 300000,
  } = options;

  console.log(`[kaggle-api] Generating B-Roll: "${prompt}"...`);

  const boundary = `----FormBoundary${Date.now().toString(16)}`;

  const bodyParts: Buffer[] = [];

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="text_prompt"\r\n\r\n` +
        `${prompt}\r\n`
    )
  );

  bodyParts.push(
    Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="duration"\r\n\r\n` +
        `${duration}\r\n`
    )
  );

  bodyParts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(bodyParts);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${apiUrl}/generate-broll`, {
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
      },
      body,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error ${response.status}: ${errorText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    const videoBuffer = Buffer.from(arrayBuffer);

    const resolvedOutputPath = outputPath
      ? path.resolve(outputPath)
      : path.resolve(`public/assets/broll-${Date.now()}.mp4`);

    const outputDir = path.dirname(resolvedOutputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(resolvedOutputPath, videoBuffer);

    console.log(`[kaggle-api] B-Roll saved: ${resolvedOutputPath} (${(videoBuffer.length / 1024 / 1024).toFixed(1)}MB)`);

    return {
      videoPath: resolvedOutputPath,
      fileSize: videoBuffer.length,
    };
  } catch (err: any) {
    clearTimeout(timeout);
    if (err.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs / 1000}s`);
    }
    throw err;
  }
}

export async function checkKaggleHealth(apiUrl: string): Promise<boolean> {
  try {
    const response = await fetch(`${apiUrl}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "ok";
  } catch {
    return false;
  }
}
