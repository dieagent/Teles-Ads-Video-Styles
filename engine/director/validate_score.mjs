import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const file = process.argv[2];
if (!file) {
  console.error('Usage: node engine/director/validate_score.mjs <score.json>');
  process.exit(2);
}

const errors = [];
const warnings = [];
let score;
try { score = JSON.parse(fs.readFileSync(file, 'utf8')); }
catch (e) { console.error(`Cannot read score: ${e.message}`); process.exit(2); }

function need(ok, message) { if (!ok) errors.push(message); }
function filled(value) { return typeof value === 'string' && value.trim().length > 0; }
function uniqueIds(items, label) {
  const ids = new Set();
  for (const [i, item] of items.entries()) {
    need(filled(item?.id), `${label}[${i}] needs an id`);
    if (filled(item?.id)) {
      need(!ids.has(item.id), `Duplicate ${label} id: ${item.id}`);
      ids.add(item.id);
    }
  }
  return ids;
}

need(filled(score.title), 'title is required');
need(filled(score.premise), 'premise is required');
need(filled(score.style) && score.style !== 'teles-director', 'Choose one production style');
if (filled(score.style)) need(fs.existsSync(path.join(repo, '.claude/skills', score.style, 'SKILL.md')), `Unknown style: ${score.style}`);
need(filled(score.styleReason), 'Explain why the style fits');
need(Number.isFinite(score.targetSeconds) && score.targetSeconds > 0, 'targetSeconds must be positive');
if (score.fiction === true) need(filled(score.fictionLabel), 'Fiction needs a visible fictionLabel');
for (const field of ['goal', 'obstacle', 'turn', 'payoff']) need(filled(score.story?.[field]), `story.${field} is required`);

const sources = Array.isArray(score.sources) ? score.sources : [];
const jokes = Array.isArray(score.jokes) ? score.jokes : [];
const beats = Array.isArray(score.beats) ? score.beats : [];
need(sources.length > 0, 'Research source ledger is empty');
need(beats.length >= 3, 'At least setup, escalation and payoff beats are needed');
const sourceIds = uniqueIds(sources, 'sources');
const jokeIds = uniqueIds(jokes, 'jokes');
uniqueIds(beats, 'beats');

for (const [i, source] of sources.entries()) {
  need(['official','self_joke','public_joke','context'].includes(source.kind), `sources[${i}] has invalid kind`);
  need(filled(source.claim) && filled(source.use), `sources[${i}] needs claim and use`);
  try { const url = new URL(source.url); need(url.protocol === 'https:', `sources[${i}] URL must be HTTPS`); }
  catch { errors.push(`sources[${i}] needs a valid URL`); }
}
for (const [i, joke] of jokes.entries()) {
  need(filled(joke.setup) && filled(joke.originalPunch) && filled(joke.storyUse), `jokes[${i}] needs setup, originalPunch and storyUse`);
  need(Array.isArray(joke.sourceIds) && joke.sourceIds.length > 0, `jokes[${i}] needs sourceIds`);
  for (const id of joke.sourceIds || []) need(sourceIds.has(id), `jokes[${i}] references missing source ${id}`);
}

const acts = new Set();
let words = 0;
const locked = score.timing?.status === 'voice_locked';
need(['planned','voice_locked'].includes(score.timing?.status), 'timing.status must be planned or voice_locked');
if (locked) {
  need(filled(score.timing.voiceFile), 'voice_locked score needs timing.voiceFile');
  if (filled(score.timing.voiceFile)) need(fs.existsSync(path.resolve(path.dirname(file), score.timing.voiceFile)), 'timing.voiceFile does not exist');
}
for (const [i, beat] of beats.entries()) {
  need(['setup','escalation','payoff'].includes(beat.act), `beats[${i}] has invalid act`);
  acts.add(beat.act);
  for (const field of ['voice','visual','motion','caption','sound','purpose']) need(filled(beat[field]), `beats[${i}].${field} is required`);
  words += String(beat.voice || '').trim().split(/\s+/).filter(Boolean).length;
  for (const id of beat.sourceIds || []) need(sourceIds.has(id), `beats[${i}] references missing source ${id}`);
  for (const id of beat.jokeIds || []) need(jokeIds.has(id), `beats[${i}] references missing joke ${id}`);
  if (locked) {
    need(Number.isFinite(beat.start) && Number.isFinite(beat.end) && beat.end > beat.start, `beats[${i}] needs valid start/end`);
    const prior = beats[i - 1];
    if (i > 0 && Number.isFinite(prior.end) && Number.isFinite(beat.start)) {
      need(beat.start >= prior.end - 0.05, `beats[${i}] overlaps the previous voice beat`);
      const gap = beat.start - prior.end;
      if (gap > 0.5 && prior.intentionalSilence !== true) errors.push(`Unexplained ${gap.toFixed(2)}s voice gap before beats[${i}]`);
    }
  }
}
for (const act of ['setup','escalation','payoff']) need(acts.has(act), `Missing ${act} act`);
if (Number.isFinite(score.targetSeconds)) {
  const rate = words / score.targetSeconds;
  if (rate > 3.1) warnings.push(`Draft may be rushed: ${rate.toFixed(1)} words/s`);
  if (rate < 1.6) warnings.push(`Draft may have empty time: ${rate.toFixed(1)} words/s`);
}
if (locked && beats.length && Number.isFinite(beats.at(-1).end)) {
  if (Math.abs(beats.at(-1).end - score.targetSeconds) > 2) warnings.push('Locked voice duration differs from targetSeconds; update the target or ending');
}

for (const message of errors) console.error(`ERROR ${message}`);
for (const message of warnings) console.warn(`WARN  ${message}`);
console.log(`Director score: ${beats.length} beats, ${words} words, ${sources.length} sources, ${jokes.length} researched jokes`);
if (errors.length) process.exit(1);
console.log('Director score valid');
