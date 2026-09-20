const { Client } = require("@gradio/client");

async function findSpace() {
  const spaces = [
    "yakadanda/sadtalker",
    "DjT3ng/SadTalker",
    "Tonyassi/SadTalker"
  ];
  
  for (const space of spaces) {
    try {
      console.log(`Trying ${space}...`);
      const client = await Client.connect(space);
      console.log(`Connected to ${space}!`);
      const api = await client.view_api();
      console.log(JSON.stringify(api, null, 2));
      return;
    } catch (e) {
      console.log(`Failed: ${e.message}`);
    }
  }
}

findSpace();
