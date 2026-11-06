import fs from 'node:fs';
import path from 'node:path';

const [input, output] = process.argv.slice(2);
if (!input || !output) {
  console.error('Usage: node engine/director/export_direction.mjs <score.json> <brief.md>');
  process.exit(2);
}
const score = JSON.parse(fs.readFileSync(input, 'utf8'));
const lines = [
  `# ${score.title}`,
  '',
  `Premise: ${score.premise}`,
  `Screen label: ${score.fiction ? score.fictionLabel : 'none'}`,
  `Target: ${score.targetSeconds} seconds, vertical unless the selected style specifies otherwise.`,
  `Style skill: .claude/skills/${score.style}/SKILL.md`,
  `Style reason: ${score.styleReason}`,
  '',
  '## Story',
  `Goal: ${score.story.goal}`,
  `Obstacle: ${score.story.obstacle}`,
  `Turn: ${score.story.turn}`,
  `Payoff: ${score.story.payoff}`,
  '',
  '## Locked creative direction',
  'Use the narration and beat order below as authored. Follow the selected Teles Ads style for composition, type, motion and sound. Make original visuals. If a generator rewrites lines or changes the story, reject that draft and restore this score. Time the final cut from the recorded voice.',
  '',
];
for (const beat of score.beats) {
  lines.push(`### ${beat.id} — ${beat.act}`, `Voice: ${beat.voice}`, `Visual: ${beat.visual}`, `Motion: ${beat.motion}`, `Caption: ${beat.caption}`, `Sound: ${beat.sound}`, `Purpose: ${beat.purpose}`, '');
}
lines.push('## Research anchors', ...score.sources.map(s => `- ${s.id}: ${s.claim} (${s.url})`), '');
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, lines.join('\n'), 'utf8');
console.log(output);
