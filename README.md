# buddy

A terminal tamagotchi. Because a $380B company put one in their CLI and we thought: *yeah, we can do that in a weekend.*

```
     (\__/)
    ( @  @ )    Brittle Ledge
   =(  ..  )=   ★ common
    (")__(")

  DEBUGGING    ██████░░░░  56
  PATIENCE     ███░░░░░░░  30
  CHAOS        █░░░░░░░░░   7
  WISDOM       █░░░░░░░░░  10
  SNARK        ░░░░░░░░░░   2
```

## Usage

```bash
python3 buddy.py
```

That's it. That's the whole interface.

## How it works

Your companion is **deterministic** — seeded from your `$USER` and the salt `friend-2026-401` (shamelessly stolen from Anthropic's leaked source). Same machine, same species, same stats, forever. You rolled a rabbit? You're a rabbit person now. Deal with it.

The **name** is random every run, because persistence requires files and files require opinions and we had enough opinions already.

### The PRNG

Mulberry32. A tiny 32-bit seeded PRNG. We use it because the original source had this comment:

> *Mulberry32 — tiny seeded PRNG, good enough for picking ducks*

Good enough for picking ducks is good enough for us.

### Species (18 total)

duck · goose · blob · cat · dragon · octopus · owl · penguin · turtle · snail · ghost · axolotl · capybara · cactus · robot · rabbit · mushroom · **chonk**

### Rarity

| Rarity    | Odds  | Stars     |
|-----------|-------|-----------|
| common    | 60%   | ★         |
| uncommon  | 25%   | ★★        |
| rare      | 10%   | ★★★       |
| epic      |  4%   | ★★★★      |
| legendary |  1%   | ★★★★★     |

Common doesn't get a hat. Life is unfair.

### Stats

Five stats: **DEBUGGING**, **PATIENCE**, **CHAOS**, **WISDOM**, **SNARK**

One will be your peak. One will be your dump. The rest are vibes.
Higher rarity = higher floor. A legendary companion with SNARK 2 is still theoretically possible and we consider this a feature.

### Shiny

1% chance. You'll know it when you see it ✨. Or you won't, because you're common, and common doesn't get anything nice.

## Origin story

Anthropic shipped `claude-code` as an npm package. The package contained a `.map` file. The `.map` file contained their entire TypeScript source. Someone uploaded it to GitHub. The internet went through it.

Among the findings: a full tamagotchi system — 18 species, gacha rarities, hats, stats, a Mulberry32 PRNG seeded per user — gated behind a feature flag scheduled to drop April 1, 2026. The species names were hex-encoded (`export const duck = String.fromCharCode(0x64,0x75,0x63,0x6b)`) because one of them collides with an internal model codename and their own build scanner would have caught it.

They hex-encoded the word duck. To hide it from themselves.

This project is a Python port of that system. No React. No Ink. No `bun:bundle`. No 803,924-byte `main.tsx`. Just a single file and a PRNG that is, per the original source, *good enough for picking ducks.*

## Requirements

- Python 3 (pre-installed on macOS)
- A `$USER` environment variable
- Acceptance that you might be a common rabbit

## Files

```
~/.buddy/
├── buddy.py       # everything
├── test_buddy.py  # 21 tests, all passing
├── design.md      # spec, written before the code (shocking, we know)
├── plan.md        # implementation plan
└── README.md      # you are here
```

## Tests

```bash
python3 ~/.buddy/test_buddy.py -v
```

21 tests. They all pass. The original codebase had 460 eslint-disable comments. We have zero. We're not saying we're better, but we're saying we're better.

## Credits

This is a Python port of the `/buddy` system from Claude Code — an April 1, 2026 easter egg that shipped (unknowingly early) when Anthropic's full TypeScript source leaked via a `.map` file in their npm package.

The original source was reconstructed and published at:
**[github.com/Kuberwastaken/claude-code](https://github.com/Kuberwastaken/claude-code)**

All sprite art, PRNG logic, rarity weights, stat formulas, and the salt `friend-2026-401` are ported directly from that source. Credit where it's due: Anthropic built a surprisingly complete tamagotchi.

## License

The original salt is `friend-2026-401`. We kept it. Consider this a tribute.
