const { Client } = require("@gradio/client");

async function checkSpace(spaceId) {
  try {
    console.log(`\nChecking ${spaceId}...`);
    const client = await Client.connect(spaceId);
    console.log(`Connected!`);
    
    // View the API
    const api = await client.view_api();
    
    // Find predict/generate endpoints
    if (api && api.named_endpoints) {
      for (const [name, info] of Object.entries(api.named_endpoints)) {
        console.log(`  Endpoint: ${name}`);
        if (info.parameters) {
          console.log(`    Parameters:`);
          for (const param of info.parameters) {
            console.log(`      - ${param.parameter_name || param.name}: ${param.type}`);
          }
        }
      }
    }
    
    return api;
  } catch (e) {
    console.log(`Failed: ${e.message}`);
    return null;
  }
}

async function main() {
  const spaces = [
    "kevinwang676/SadTalker",
    "John6666/SadTalker",
    "ALIKABALAH/SadTalker-API",
  ];
  
  for (const space of spaces) {
    await checkSpace(space);
  }
}

main().catch(console.error);
