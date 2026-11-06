# Teles Ads

## One-line director

Use `/director what if Modi became president of the USA` for a researched story, original character-specific jokes, a timed shot script and a video made in a selected style. The [director skill](.claude/skills/teles-director/SKILL.md) researches both the person's own humor and public jokes, then chooses one of the reference styles below. See the [worked script](examples/director/modi-us-president/SCRIPT.md), [source ledger](examples/director/modi-us-president/RESEARCH.md) and [open-source research](docs/DIRECTOR_OPEN_SOURCE.md). The example is explicitly fictional satire.

Use one command to match a **specific supplied video**, then give a new topic. Ten primary commands map one-to-one to the ten original supplied clips. Two additional commands use distinct, short segments of videos 04 and 05. The new `/documentary` command maps to the separately supplied snakebite explainer. All thirteen video-style skills and the director skill live in `.claude/skills/`; the slash commands live in `.claude/commands/`.

| Command | Video-number alias | Exact reference treatment | Source |
|---|---|---|---|
| `/fireline` | `/ref01` | Fire escape reenactment | [video 01](examples/reference-videos/source-01.mp4) |
| `/papertrail` | `/ref02` | Ukiyo-e process breakdown | [video 02](examples/reference-videos/source-02.mp4) |
| `/petalpress` | `/ref03` | Vintage tulip tutorial | [video 03](examples/reference-videos/source-03.mp4) |
| `/bodyatlas` | `/ref04` | Octopus infographic tutorial | [video 04](examples/reference-videos/source-04.mp4) |
| `/sagacut` | `/ref05` | Viking parchment documentary | [video 05](examples/reference-videos/source-05.mp4) |
| `/medarchive` | `/ref06` | Fleming fifteen-second archive | [video 06](examples/reference-videos/source-06.mp4) |
| `/inkcase` | `/ref07` | Illustrated moral casefile | [video 07](examples/reference-videos/source-07.mp4) |
| `/zackd` | `/ref08` | Sears-style kinetic 3D history | [video 08](examples/reference-videos/source-08.mp4) |
| `/realcase` | `/ref09` | Poisoned-drink 3D reconstruction | [video 09](examples/reference-videos/source-09.mp4) |
| `/rainmyth` | `/ref10` | Kuchisake-onna comic 3D short | [video 10](examples/reference-videos/source-10.mp4) |
| `/labnote` | — | Fact-card opening of video 04 | [video 04](examples/reference-videos/source-04.mp4) |
| `/pulpchronicle` | — | Reversal passage of video 05 | [video 05](examples/reference-videos/source-05.mp4) |
| `/documentary` | — | Hindi/Hinglish cinematic illustrated evidence explainer | [snakebite video](examples/documentary/reference/snakebite-source.mp4) |

Example: `/zackd why I'm afraid` uses the 3D characters, red/black kinetic type and comparison-to-insight rhythm of video 08. The **subject and words are new**. For a direct numbered request, `/ref08 why I'm afraid` routes to the same skill.

Each skill has a source-specific timed beat map, image and type rules, voice and sound behavior, and a worked example. The original twelve examples are in [examples/styles](examples/styles/). The [documentary example](examples/documentary/README.md) includes the original clip, three-second reference sheet, 14 full-size screenshots, a design specification, a complete Hiroshima/Nagasaki script and shot score, and a [rendered China–India example](examples/documentary/china-india-growth/README.md) with a 35-shot edit and source capture. Use `/documentary what happened in Japan why USA nuke him` as a one-line input pattern; the agent researches the precise question and makes a new video in that style. The [source map](examples/SOURCE_MAP.md) links the original ten filenames to numbered files; [sixteen-frame sheets](examples/style-atlas/) and [machine transcripts](examples/TRANSCRIPTS.json) support their analysis. Check exact transcript words and factual claims before publication.

## Production rule

Record the script first. Put each image and caption on the phrase it explains; leave a silent gap only when the story calls for one. Watch and listen to the entire draft, fix weak motion and competing background sound, then export the final. Reference frames are for analysis and are not production assets.

The original Arc Lab Series engine, lessons and Day 23 example remain in this repo. Its original series workflow is separate from these reference-specific commands.
