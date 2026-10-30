#!/usr/bin/env python3
"""检查 selfcheck.md 是否完成 10 问自查
用法: python3 check_selfcheck.py <selfcheck.md>
退出码: 0 通过 / 1 未完成 / 2 缺文件
"""
import os
import re
import sys


def main(argv):
    if len(argv) < 2:
        print('用法: python3 check_selfcheck.py selfcheck.md')
        return 2
    path = argv[1]
    if not os.path.exists(path):
        print('❌ 缺少自查文件:', path)
        print('   按 docs/SELFCHECK.md 的模板写 10 条，每条打 ✅')
        return 2
    text = open(path, encoding='utf-8').read()
    passed = len(re.findall(r'✅', text))
    rows = len(re.findall(r'^\|\s*\d+\s*\|', text, re.M))
    if passed < 10 or rows < 10:
        print('❌ 自查未完成：%d 条通过 / %d 行（需要 10 条都过）' % (passed, rows))
        return 1
    print('✅ 10 问自查已完成（%d 条通过）' % passed)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
