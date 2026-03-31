#!/usr/bin/env python3
import hashlib
import os
import random


# ─── PRNG ────────────────────────────────────────────────────────────────────

def _imul(a: int, b: int) -> int:
    """32-bit integer multiplication (mirrors JS Math.imul)."""
    return ((a & 0xFFFFFFFF) * (b & 0xFFFFFFFF)) & 0xFFFFFFFF


def mulberry32(seed: int):
    """Mulberry32 PRNG — returns a closure yielding floats in [0, 1)."""
    a = seed & 0xFFFFFFFF
    def rng() -> float:
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = _imul(a ^ (a >> 15), 1 | a)
        t = (t + _imul(t ^ (t >> 7), 61 | t)) ^ t
        t = t & 0xFFFFFFFF
        return (t ^ (t >> 14)) / 4294967296
    return rng


def make_seed(user: str) -> int:
    SALT = 'friend-2026-401'
    digest = hashlib.sha256((user + SALT).encode()).hexdigest()
    return int(digest[:8], 16)


# ─── ROLL TABLES ─────────────────────────────────────────────────────────────

SPECIES = [
    'duck', 'goose', 'blob', 'cat', 'dragon', 'octopus', 'owl', 'penguin',
    'turtle', 'snail', 'ghost', 'axolotl', 'capybara', 'cactus', 'robot',
    'rabbit', 'mushroom', 'chonk',
]

EYES = ['·', '✦', '×', '◉', '@', '°']

HATS = ['none', 'crown', 'tophat', 'propeller', 'halo', 'wizard', 'beanie', 'tinyduck']

RARITIES = ['common', 'uncommon', 'rare', 'epic', 'legendary']

RARITY_WEIGHTS = {'common': 60, 'uncommon': 25, 'rare': 10, 'epic': 4, 'legendary': 1}
RARITY_FLOOR   = {'common': 5, 'uncommon': 15, 'rare': 25, 'epic': 35, 'legendary': 50}
RARITY_STARS   = {'common': '★', 'uncommon': '★★', 'rare': '★★★', 'epic': '★★★★', 'legendary': '★★★★★'}

STAT_NAMES = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK']


def _pick(rng, lst: list):
    return lst[int(rng() * len(lst))]


def _roll_rarity(rng) -> str:
    roll = rng() * 100
    for r in RARITIES:
        roll -= RARITY_WEIGHTS[r]
        if roll < 0:
            return r
    return 'common'


def _roll_stats(rng, rarity: str) -> dict:
    floor = RARITY_FLOOR[rarity]
    peak = _pick(rng, STAT_NAMES)
    dump = peak
    while dump == peak:
        dump = _pick(rng, STAT_NAMES)
    stats = {}
    for name in STAT_NAMES:
        if name == peak:
            stats[name] = min(100, floor + 50 + int(rng() * 30))
        elif name == dump:
            stats[name] = max(1, floor - 10 + int(rng() * 15))
        else:
            stats[name] = floor + int(rng() * 40)
    return stats


def roll_companion(user: str) -> dict:
    """Deterministic companion roll from user string."""
    rng     = mulberry32(make_seed(user))
    rarity  = _roll_rarity(rng)
    species = _pick(rng, SPECIES)
    eye     = _pick(rng, EYES)
    hat     = 'none' if rarity == 'common' else _pick(rng, HATS)
    shiny   = rng() < 0.01
    stats   = _roll_stats(rng, rarity)
    return {
        'rarity': rarity, 'species': species, 'eye': eye,
        'hat': hat, 'shiny': shiny, 'stats': stats,
    }


# ─── NAME ────────────────────────────────────────────────────────────────────

ADJECTIVES = [
    'dusty', 'ancient', 'swift', 'tiny', 'cosmic', 'grumpy', 'fuzzy', 'silent',
    'brave', 'soggy', 'crispy', 'gentle', 'wild', 'sleepy', 'curious', 'mighty',
    'rusty', 'glowing', 'frozen', 'bouncy', 'sneaky', 'hollow', 'golden', 'mossy',
    'stormy', 'fluffy', 'gloomy', 'radiant', 'spiky', 'wandering', 'humble',
    'twitchy', 'serene', 'grizzled', 'damp', 'luminous', 'crinkled', 'bashful',
    'wobbly', 'brittle',
]

NOUNS = [
    'goose', 'pebble', 'claw', 'ember', 'mist', 'bramble', 'flicker', 'dusk',
    'twig', 'stone', 'shadow', 'ripple', 'hollow', 'spark', 'drift', 'burrow',
    'grove', 'tide', 'vale', 'flint', 'wisp', 'brook', 'fern', 'crater',
    'gust', 'knoll', 'marsh', 'peak', 'shard', 'thicket', 'vapor', 'haven',
    'ledge', 'cove', 'bloom', 'spore', 'frond', 'glow', 'shell', 'haze',
]


def roll_name() -> str:
    """Random name each run — uses system random, not the deterministic PRNG."""
    return f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}".title()


# ─── SPRITES ─────────────────────────────────────────────────────────────────

# Frame 0 only. {E} is substituted with the rolled eye character at render time.
SPRITES = {
    'duck':     ['            ', '    __      ', '  <({E} )___  ', '   (  ._>   ', '    `--´    '],
    'goose':    ['            ', '     ({E}>    ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
    'blob':     ['            ', '   .----.   ', '  ( {E}  {E} )  ', '  (      )  ', '   `----´   '],
    'cat':      ['            ', '   /\\_/\\    ', '  ( {E}   {E})  ', '  (  ω  )   ', '  (")_(")   '],
    'dragon':   ['            ', '  /^\\  /^\\  ', ' <  {E}  {E}  > ', ' (   ~~   ) ', '  `-vvvv-´  '],
    'octopus':  ['            ', '   .----.   ', '  ( {E}  {E} )  ', '  (______)  ', '  /\\/\\/\\/\\  '],
    'owl':      ['            ', '   /\\  /\\   ', '  (({E})({E}))  ', '  (  ><  )  ', '   `----´   '],
    'penguin':  ['            ', '  .---.     ', '  ({E}>{E})     ', ' /(   )\\    ', '  `---´     '],
    'turtle':   ['            ', '   _,--._   ', '  ( {E}  {E} )  ', ' /[______]\\ ', '  ``    ``  '],
    'snail':    ['            ', ' {E}    .--.  ', '  \\  ( @ )  ', '   \\_`--´   ', '  ~~~~~~~   '],
    'ghost':    ['            ', '   .----.   ', '  / {E}  {E} \\  ', '  |      |  ', '  ~`~``~`~  '],
    'axolotl':  ['            ', '}~(______)~{', '}~({E} .. {E})~{', '  ( .--. )  ', '  (_/  \\_)  '],
    'capybara': ['            ', '  n______n  ', ' ( {E}    {E} ) ', ' (   oo   ) ', '  `------´  '],
    'cactus':   ['            ', ' n  ____  n ', ' | |{E}  {E}| | ', ' |_|    |_| ', '   |    |   '],
    'robot':    ['            ', '   .[||].   ', '  [ {E}  {E} ]  ', '  [ ==== ]  ', '  `------´  '],
    'rabbit':   ['            ', '   (\\__/)   ', '  ( {E}  {E} )  ', ' =(  ..  )= ', '  (")__(")  '],
    'mushroom': ['            ', ' .-o-OO-o-. ', '(__________)', '   |{E}  {E}|   ', '   |____|   '],
    'chonk':    ['            ', '  /\\    /\\  ', ' ( {E}    {E} ) ', ' (   ..   ) ', '  `------´  '],
}

HAT_LINES = {
    'none':      '',
    'crown':     '   \\^^^/    ',
    'tophat':    '   [___]    ',
    'propeller': '    -+-     ',
    'halo':      '   (   )    ',
    'wizard':    '    /^\\     ',
    'beanie':    '   (___)    ',
    'tinyduck':  '    ,>      ',
}


def render_sprite(species: str, eye: str, hat: str) -> list:
    lines = [line.replace('{E}', eye) for line in SPRITES[species]]
    if hat != 'none' and not lines[0].strip():
        lines[0] = HAT_LINES[hat]
    if not lines[0].strip():
        lines = lines[1:]
    return lines


# ─── OUTPUT ──────────────────────────────────────────────────────────────────

RARITY_COLORS = {
    'common':    '\033[90m',
    'uncommon':  '\033[32m',
    'rare':      '\033[34m',
    'epic':      '\033[35m',
    'legendary': '\033[33m',
}
RESET = '\033[0m'


def _bar(value: int, width: int = 10) -> str:
    filled = round(value / 100 * width)
    return '█' * filled + '░' * (width - filled)


def render(companion: dict, name: str) -> str:
    rarity  = companion['rarity']
    color   = RARITY_COLORS[rarity]
    stars   = RARITY_STARS[rarity]
    shiny_s = ' ✨' if companion['shiny'] else ''

    sprite = render_sprite(companion['species'], companion['eye'], companion['hat'])

    info = [
        f"{color}{name}{RESET}",
        f"{color}{stars} {rarity}{shiny_s}{RESET}",
    ]

    mid = len(sprite) // 2
    out = []
    for i, line in enumerate(sprite):
        info_part = info[i - mid] if 0 <= (i - mid) < len(info) else ''
        out.append(f"  {line}  {info_part}")

    out.append('')

    for stat, val in companion['stats'].items():
        out.append(f"  {stat:<11}  {color}{_bar(val)}{RESET}  {val}")

    return '\n'.join(out)
