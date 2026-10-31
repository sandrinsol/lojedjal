// Where SEPTEM's tools find things. By default the gb-gbc-gba-test-mcp clone
// sits next to this repo:
//
//   your-folder/
//     lojedjal/               this repo
//     gb-gbc-gba-test-mcp/    https://github.com/sandrinsol/gb-gbc-gba-test-mcp
//
// GBTEST_REPO (the clone) or GBTEST_HARNESS (its harness folder) override it.
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));

export const harness = process.env.GBTEST_HARNESS ??
  path.join(process.env.GBTEST_REPO ?? path.join(root, '..', 'gb-gbc-gba-test-mcp'), 'harness');

/** Imports a module from the harness folder (works with Windows paths too). */
export function importHarness(file) {
  if (!existsSync(harness)) {
    throw new Error(`gb-gbc-gba-test-mcp not found at ${path.dirname(harness)}: clone it next to this repo or set GBTEST_REPO`);
  }
  return import(pathToFileURL(path.join(harness, file)).href);
}
