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

if __name__ == '__main__':
    unittest.main()
