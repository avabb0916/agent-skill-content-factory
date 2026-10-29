"""用标准库 unittest 跑质检脚本（不依赖 pytest）"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import qc_article  # noqa: E402


class QcTest(unittest.TestCase):
    def test_frontmatter(self):
        fm, body = qc_article.parse_frontmatter('---\ntitle: A\n---\nbody')
        self.assertEqual(fm['title'], 'A')
        self.assertIn('body', body)

    def test_detect_banned(self):
        res = qc_article.check(os.path.join(ROOT, 'tests', 'fixtures', 'bad.md'))
        codes = [i['code'] for i in res['issues']]
        self.assertIn('banned-words', codes)
        self.assertFalse(res['ok'])

    def test_good_has_no_banned(self):
        res = qc_article.check(os.path.join(ROOT, 'examples', 'good-article.md'))
        codes = [i['code'] for i in res['issues']]
        self.assertNotIn('banned-words', codes)


if __name__ == '__main__':
    unittest.main()
