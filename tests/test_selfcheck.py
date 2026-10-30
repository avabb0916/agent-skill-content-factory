import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import check_selfcheck  # noqa: E402


class SelfCheckTest(unittest.TestCase):
    def test_missing_file(self):
        self.assertEqual(check_selfcheck.main(['x', '/tmp/__nope__.md']), 2)

    def test_incomplete(self):
        p = '/tmp/_selfcheck_incomplete.md'
        open(p, 'w', encoding='utf-8').write('| 1 | a | ✅ |\n| 2 | b | ✅ |\n')
        self.assertEqual(check_selfcheck.main(['x', p]), 1)

    def test_complete(self):
        p = '/tmp/_selfcheck_ok.md'
        rows = '\n'.join('| %d | q | ✅ |' % i for i in range(1, 11))
        open(p, 'w', encoding='utf-8').write(rows)
        self.assertEqual(check_selfcheck.main(['x', p]), 0)


if __name__ == '__main__':
    unittest.main()
