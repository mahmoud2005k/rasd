import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from features import FEATURE_NAMES, MODEL_FEATURES, extract  # noqa: E402


class FeaturesTest(unittest.TestCase):
    def test_scheme_and_www_do_not_change_model_features(self):
        a, b = extract("https://www.google.com/search?q=1"), extract("google.com/search?q=1")
        diff = {k for k in a if a[k] != b[k]}
        self.assertEqual(diff, {"is_https"})
        self.assertNotIn("is_https", MODEL_FEATURES)

    def test_feature_count(self):
        self.assertEqual(len(FEATURE_NAMES), 37)
        self.assertEqual(len(MODEL_FEATURES), 36)

    def test_unicode_attacks_are_counted(self):
        self.assertEqual(extract("http://goo\u200bgle.com")["invisible_chars"], 1)
        self.assertEqual(extract("http://p\u0430ypal.com")["mixed_script"], 1)

    def test_garbage_input_does_not_crash(self):
        for s in ("", "   ", "////", "http://", "@@@", "http://[::1]:99999/x"):
            f = extract(s)
            self.assertEqual(set(f), set(FEATURE_NAMES))


if __name__ == "__main__":
    unittest.main()
