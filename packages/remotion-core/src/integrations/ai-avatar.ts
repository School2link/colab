import { Client } from "@gradio/client";
import fs from "fs";
import path from "path";

const SADTALKER_SPACE = "akin23/SadTalker-API";

export interface AvatarOptions {
  imagePath: string;
  audioPath: string;
  preprocess?: "full" | "crop" | "resize";
  stillMode?: boolean;
  useEnhancer?: boolean;
}

export interface AvatarResult {
  videoPath: string;
}

export async function generateTalkingHead(
  options: AvatarOptions
): Promise<AvatarResult> {
  const {
    imagePath,
    audioPath,
    preprocess = "full",
    stillMode = false,
    useEnhancer = true,
  } = options;

  console.log(`[ai-avatar] Connecting to ${SADTALKER_SPACE}...`);
  const client = await Client.connect(SADTALKER_SPACE);

  console.log(`[ai-avatar] Uploading image: ${imagePath}`);
  const imageFile = new File(
    [fs.readFileSync(imagePath)],
    path.basename(imagePath),
    { type: "image/png" }
  );

  console.log(`[ai-avatar] Uploading audio: ${audioPath}`);
  const audioFile = new File(
    [fs.readFileSync(audioPath)],
    path.basename(audioPath),
    { type: "audio/wav" }
  );

  console.log(`[ai-avatar] Generating talking head (this may take 30-120s)...`);
  const result = await client.predict("/predict", {
    source_image: imageFile,
    driven_audio: audioFile,
  });

  console.log(`[ai-avatar] Generation complete!`);
  console.log(`[ai-avatar] Result:`, JSON.stringify(result.data, null, 2));

  return {
    videoPath: String(result.data),
  };
}
