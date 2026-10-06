import unittest

from plagiarism_checker import PlagiarismChecker, ngrams, REFERENCE


class TestNgrams(unittest.TestCase):
    def test_ngram_count(self):
        self.assertEqual(ngrams("abcdef", n=3), ["abc", "bcd", "cde", "def"])

    def test_whitespace_removed(self):
        self.assertEqual(ngrams("a b c", n=2), ["ab", "bc"])


class TestPlagiarism(unittest.TestCase):
    def setUp(self):
        self.pc = PlagiarismChecker()

    def test_exact_copy_detected(self):
        # 直接复制参考库第一段
        text = REFERENCE["人工智能简介"]
        r = self.pc.check(text)
        self.assertEqual(r["best_match"], "人工智能简介")
        self.assertGreater(r["repetition_rate"], 0.9)

    def test_paraphrase_low(self):
        r = self.pc.check("今天我去超市买了水果和蔬菜，然后回家做饭。")
        self.assertLess(r["repetition_rate"], 0.3)

    def test_overlap_fragments_present(self):
        text = "人工智能是研究如何让计算机模拟人类智能的一门学科。"
        r = self.pc.check(text)
        self.assertTrue(len(r["overlaps"]) > 0)

    def test_empty(self):
        r = self.pc.check("")
        self.assertEqual(r["repetition_rate"], 0.0)
        self.assertIsNone(r["best_match"])

    def test_health_match(self):
        text = "保持健康需要规律运动和充足睡眠，多喝水少熬夜。"
        r = self.pc.check(text)
        self.assertEqual(r["best_match"], "健康生活")


if __name__ == "__main__":
    unittest.main()
