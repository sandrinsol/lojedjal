// Starts the gb-gbc-gba-test MCP server and calls its tools on SEPTEM:
// load_rom, run_sequence (title -> walk), check (hardware rules), describe.
import path from 'node:path';
import { createRequire } from 'node:module';
const harness = process.env.GBTEST_HARNESS ?? '/home/user/sandrinsol/gb-gbc-gba-test-mcp/harness';
const require = createRequire(path.join(harness, 'package.json'));
const { Client } = await import(require.resolve('@modelcontextprotocol/sdk/client/index.js'));
const { StdioClientTransport } = await import(require.resolve('@modelcontextprotocol/sdk/client/stdio.js'));
const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));

const transport = new StdioClientTransport({
  command: 'node', args: [path.join(harness, 'mcp-server.mjs')],
  env: { ...process.env, GBTEST_ROOT: root },
});
const client = new Client({ name: 'septem-tests', version: '1.0.0' });
await client.connect(transport);
const text = (r) => r.content.filter((c) => c.type === 'text').map((c) => c.text).join('\n');
const call = async (name, args = {}) => {
  const r = await client.callTool({ name, arguments: args });
  console.log(`--- ${name}${r.isError ? ' (error)' : ''}\n${text(r)}`);
  return r;
};
await call('load_rom', { path: 'septem.gba' });
await call('run_sequence', { steps: [{ wait: 60 }, { tap: 'START' }, { wait: 30 }, { tap: 'UP' }, { wait: 20 }, { tap: 'UP' }, { wait: 20 }] });
await call('check', { frames: 600 });
await call('describe', { io: true });
await client.close();
