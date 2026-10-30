// Dumps each BG layer via the MCP view_vram tool to tests/out/layers_*.png.
import path from 'node:path';
import { writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
const harness = process.env.GBTEST_HARNESS ?? '/home/user/sandrinsol/gb-gbc-gba-test-mcp/harness';
const require = createRequire(path.join(harness, 'package.json'));
const { Client } = await import(require.resolve('@modelcontextprotocol/sdk/client/index.js'));
const { StdioClientTransport } = await import(require.resolve('@modelcontextprotocol/sdk/client/stdio.js'));
const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));
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
