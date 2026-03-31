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
