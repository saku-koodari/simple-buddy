import unittest, sys, os
sys.path.insert(0, os.path.expanduser('~/.buddy'))

class TestPRNG(unittest.TestCase):
    def test_make_seed_is_deterministic(self):
        from buddy import make_seed
        self.assertEqual(make_seed('alice'), make_seed('alice'))

    def test_different_users_get_different_seeds(self):
        from buddy import make_seed
        self.assertNotEqual(make_seed('alice'), make_seed('bob'))

    def test_mulberry32_same_seed_same_sequence(self):
        from buddy import mulberry32
        r1 = mulberry32(42)
        r2 = mulberry32(42)
        self.assertEqual([r1() for _ in range(5)], [r2() for _ in range(5)])

    def test_mulberry32_output_in_range(self):
        from buddy import mulberry32
        rng = mulberry32(99)
        for _ in range(100):
            v = rng()
            self.assertGreaterEqual(v, 0.0)
            self.assertLess(v, 1.0)

class TestRoll(unittest.TestCase):
    def test_roll_companion_is_deterministic(self):
        from buddy import roll_companion
        self.assertEqual(roll_companion('testuser'), roll_companion('testuser'))

    def test_roll_companion_different_users_differ(self):
        from buddy import roll_companion
        self.assertNotEqual(roll_companion('alice'), roll_companion('bob'))

    def test_roll_companion_shape(self):
        from buddy import roll_companion, SPECIES, EYES, HATS, RARITIES, STAT_NAMES
        c = roll_companion('testuser')
        self.assertIn(c['rarity'], RARITIES)
        self.assertIn(c['species'], SPECIES)
        self.assertIn(c['eye'], EYES)
        self.assertIn(c['hat'], HATS)
        self.assertIsInstance(c['shiny'], bool)
        self.assertEqual(set(c['stats'].keys()), set(STAT_NAMES))

    def test_stats_in_range(self):
        from buddy import roll_companion
        c = roll_companion('testuser')
        for val in c['stats'].values():
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, 100)

    def test_common_has_no_hat(self):
        from buddy import roll_companion
        found = False
        for i in range(200):
            c = roll_companion(f'user{i}')
            if c['rarity'] == 'common':
                self.assertEqual(c['hat'], 'none')
                found = True
                break
        self.assertTrue(found, "Couldn't find a common-rarity user in 200 tries")

class TestName(unittest.TestCase):
    def test_roll_name_is_title_case(self):
        from buddy import roll_name
        name = roll_name()
        self.assertEqual(name, name.title())

    def test_roll_name_is_two_words(self):
        from buddy import roll_name
        name = roll_name()
        self.assertEqual(len(name.split()), 2)

    def test_roll_name_varies(self):
        from buddy import roll_name
        names = {roll_name() for _ in range(20)}
        self.assertGreater(len(names), 1)

class TestSprites(unittest.TestCase):
    def test_render_sprite_substitutes_eye(self):
        from buddy import render_sprite
        lines = render_sprite('duck', '·', 'none')
        joined = '\n'.join(lines)
        self.assertIn('·', joined)
        self.assertNotIn('{E}', joined)

    def test_render_sprite_applies_hat(self):
        from buddy import render_sprite
        lines = render_sprite('duck', '·', 'crown')
        self.assertIn('^^^', lines[0])

    def test_render_sprite_drops_blank_hat_slot(self):
        from buddy import render_sprite
        lines_no_hat = render_sprite('duck', '·', 'none')
        self.assertFalse(lines_no_hat[0].strip() == '')

    def test_all_species_render_without_error(self):
        from buddy import render_sprite, SPECIES
        for species in SPECIES:
            lines = render_sprite(species, '·', 'none')
            self.assertIsInstance(lines, list)
            self.assertGreater(len(lines), 0)

class TestRender(unittest.TestCase):
    def _make_companion(self, rarity='uncommon'):
        return {
            'rarity': rarity,
            'species': 'duck',
            'eye': '·',
            'hat': 'none',
            'shiny': False,
            'stats': {'DEBUGGING': 80, 'PATIENCE': 30, 'CHAOS': 50, 'WISDOM': 60, 'SNARK': 45},
        }

    def test_render_contains_name(self):
        from buddy import render
        out = render(self._make_companion(), 'Dusty Goose')
        self.assertIn('Dusty Goose', out)

    def test_render_contains_stars(self):
        from buddy import render
        out = render(self._make_companion('uncommon'), 'X')
        self.assertIn('★★', out)

    def test_render_contains_shiny_marker_when_shiny(self):
        from buddy import render
        c = self._make_companion()
        c['shiny'] = True
        out = render(c, 'X')
        self.assertIn('✨', out)

    def test_render_contains_all_stat_names(self):
        from buddy import render, STAT_NAMES
        out = render(self._make_companion(), 'X')
        for stat in STAT_NAMES:
            self.assertIn(stat, out)

    def test_render_bar_length(self):
        from buddy import _bar
        self.assertEqual(len(_bar(0)),   10)
        self.assertEqual(len(_bar(100)), 10)
        self.assertEqual(len(_bar(50)),  10)

if __name__ == '__main__':
    unittest.main()
