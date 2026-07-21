#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const target = process.argv[2];
const resaveAll = process.argv.includes('--all');

if (!target) {
  console.error('Usage: node save_playground_blocks.js <file.md> [--all]');
  process.exit(2);
}

if (!fs.existsSync(target)) {
  console.error(`File not found: ${target}`);
  process.exit(2);
}

let text = fs.readFileSync(target, 'utf8');
const titleBase = path.basename(target, '.md');

const blockPattern = /<!-- \[▶ 在线演示\]\(https:\/\/infrad\.shopee\.io\/playground\/\?agent_code_id=(TBD|\d+)\) -->\n\s*```react\n([\s\S]*?)\n```/g;
const matches = [...text.matchAll(blockPattern)].filter((match) => resaveAll || match[1] === 'TBD');

if (matches.length === 0) {
  console.log('No Playground blocks to save.');
  process.exit(0);
}

async function saveBlock(code, index) {
  const response = await fetch('https://infrad.shopee.io/apis/faas/agent-code/save', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ code, title: `${titleBase}_${index + 1}` }),
  });
  const raw = await response.text();
  if (!response.ok) {
    throw new Error(`Save failed (${response.status}): ${raw.slice(0, 300)}`);
  }
  const json = JSON.parse(raw);
  const id = json?.data?.id || json?.data?.agent_code_id || json?.id || json?.agent_code_id;
  if (!id) {
    throw new Error(`Save response did not contain id: ${raw.slice(0, 300)}`);
  }
  return String(id);
}

(async () => {
  const replacements = new Map();
  for (let i = 0; i < matches.length; i += 1) {
    const match = matches[i];
    const id = await saveBlock(match[2], i);
    replacements.set(match.index, {
      original: match[0],
      updated: match[0].replace(/agent_code_id=(TBD|\d+)/, `agent_code_id=${id}`),
      id,
    });
    console.log(`${i + 1}/${matches.length}: ${id}`);
  }

  text = text.replace(blockPattern, (full, id, code, offset) => {
    const item = replacements.get(offset);
    return item ? item.updated : full;
  });

  fs.writeFileSync(target, text);
})();
