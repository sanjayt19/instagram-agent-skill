# Paths

The skills reference five working files. Defaults assume a personal setup;
repoint them to wherever your project actually lives.

| file | default | what it is |
| --- | --- | --- |
| voice | `~/.claude/instagram/voice.md` | voice profile (or `templates/voice-brand.md` for a brand account) |
| swipe | `~/.claude/instagram/swipe.md` | `/ig-viral` output: what is working in the niche |
| log | `~/.claude/instagram/log.md` | post log: date, hook formula, first line |
| plan | `~/.claude/instagram/plan.md` | `/ig-plan` output: the week |
| drafts | `~/workspace/instagram/stories/` | `/ig-story --draft` renders |

To repoint: copy the template files to your project dir and tell the agent
the paths once per session, e.g. "voice is at `brand/ig-voice.md`, log at
`research/ig-log.md`". The agent then uses those paths everywhere the skill
says `~/.claude/instagram/`.

Or symlink once and forget it:

```bash
mkdir -p ~/.claude/instagram
ln -s /path/to/project/brand/ig-voice.md ~/.claude/instagram/voice.md
ln -s /path/to/project/research/ig-log.md ~/.claude/instagram/log.md
```
