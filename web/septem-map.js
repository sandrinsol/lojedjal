// SEPTEM map text <-> ROM map block. Shared by editor.html and index.html.
//
// Map text: one row per line, 8..32 rows of 8..32 cells.
//   #  wall   W  wall with a lancet window   .  floor   M  monk   ^ > v <  start + facing
// ROM block (see tools/build_map.py): "SEPTMAP1", width, height, start_x,
// start_y, facing, 3 pad bytes, then 32*32 cell bytes.
(function (global) {
  const MAGIC = 'SEPTMAP1';
  const MAX = 32;
  const MIN = 8;
  const FACING = '^>v<';
  const STORAGE_KEY = 'septem.map';

  /** Text -> { width, height, cells: string[] rows ('#','W','.'), start: {x, y, facing} }. */
  function parse(text) {
    const rows = text.replace(/\r/g, '').split('\n').map((r) => r.trimEnd()).filter((r) => r.length);
    if (rows.length < MIN || rows.length > MAX) throw new Error(`${rows.length} rows: a map has ${MIN} to ${MAX} rows`);
    const width = rows[0].length;
    if (width < MIN || width > MAX) throw new Error(`Width ${width}: a map is ${MIN} to ${MAX} cells wide`);
    let start = null;
    const cells = rows.map((row, y) => {
      if (row.length !== width) throw new Error(`Row ${y + 1} is ${row.length} wide, expected ${width}`);
      return [...row].map((ch, x) => {
        if (FACING.includes(ch)) {
          if (start) throw new Error('More than one start (^ > v <)');
          start = { x, y, facing: FACING.indexOf(ch) };
          return '.';
        }
        if (!'#W.M'.includes(ch)) throw new Error(`Unknown cell "${ch}" at row ${y + 1}, column ${x + 1}`);
        return ch;
      }).join('');
    });
    if (!start) throw new Error('No start: mark it with ^ > v or <');
    return { width, height: rows.length, cells, start };
  }

  function serialize(map) {
    return map.cells.map((row, y) => [...row].map((ch, x) =>
      (x === map.start.x && y === map.start.y ? FACING[map.start.facing] : ch)).join('')).join('\n');
  }

  function findBlock(rom) {
    const m = [...MAGIC].map((c) => c.charCodeAt(0));
    outer: for (let i = 0; i + 16 + MAX * MAX <= rom.length; i += 4) {
      for (let k = 0; k < 8; k++) if (rom[i + k] !== m[k]) continue outer;
      return i;
    }
    return -1;
  }

  function readBlock(rom) {
    const at = findBlock(rom);
    if (at < 0) throw new Error('This ROM has no SEPTEM map block');
    const width = rom[at + 8], height = rom[at + 9];
    const cells = [];
    for (let y = 0; y < height; y++) {
      let row = '';
      for (let x = 0; x < width; x++) row += String.fromCharCode(rom[at + 16 + y * width + x]);
      cells.push(row);
    }
    return { width, height, cells, start: { x: rom[at + 10], y: rom[at + 11], facing: rom[at + 12] & 3 } };
  }

  /** Returns a patched copy of the ROM bytes. */
  function patch(rom, map) {
    const out = new Uint8Array(rom);
    const at = findBlock(out);
    if (at < 0) throw new Error('This ROM has no SEPTEM map block');
    out.set([map.width, map.height, map.start.x, map.start.y, map.start.facing], at + 8);
    out.fill(0x23, at + 16, at + 16 + MAX * MAX);
    map.cells.forEach((row, y) => {
      for (let x = 0; x < map.width; x++) out[at + 16 + y * map.width + x] = row.charCodeAt(x);
    });
    return out;
  }

  function loadSaved() {
    try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
  }

  function save(text) {
    try { localStorage.setItem(STORAGE_KEY, text); return true; } catch { return false; }
  }

  global.SeptemMap = { parse, serialize, findBlock, readBlock, patch, loadSaved, save, MAX, MIN, FACING };
})(window);
