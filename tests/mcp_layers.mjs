// Dumps each BG layer via the MCP view_vram tool to tests/out/layers_*.png.
import path from 'node:path';
import { harness, root } from '../tools/paths.mjs';
import { writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const require = createRequire(path.join(harness, 'package.json'));
const { Client } = await import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/index.js')).href);
const { StdioClientTransport } = await import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/stdio.js')).href);
const client = new Client({ name: 'septem-tests', version: '1.0.0' });
await client.connect(new StdioClientTransport({ command: 'node', args: [path.join(harness, 'mcp-server.mjs')], env: { ...process.env, GBTEST_ROOT: root } }));
await client.callTool({ name: 'load_rom', arguments: { path: 'septem.gba' } });
await client.callTool({ name: 'run_sequence', arguments: { steps: [{ wait: 60 }, { tap: 'START' }, { wait: 30 }, { tap: 'SELECT' }, { tap: 'SELECT' }, { wait: 10 }] } });
const r = await client.callTool({ name: 'view_vram', arguments: { what: 'layers' } });
let i = 0;
for (const c of r.content) {
  if (c.type === 'text') console.log(c.text);
  if (c.type === 'image') await writeFile(path.join(root, 'tests', 'out', `layers_${i++}.png`), Buffer.from(c.data, 'base64'));
}
await client.close();
