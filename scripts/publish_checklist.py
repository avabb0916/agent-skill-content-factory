#!/usr/bin/env python3
"""发布前风险检查（只依赖标准库）
用法: python3 publish_checklist.py article.md
退出码: 0 无阻断 / 1 有必须处理项
"""
import re
import sys

RISK = {
    '敏感词面': ['成人', '赌博', '博彩', '盗版', '翻墙', '代注册', '网贷', '荐股'],
    '平台名单': ['Similarweb', 'Semrush', 'Ahrefs', 'Gumroad', 'OpenAI', 'ChatGPT', 'Shopify', 'Stripe'],
    '绝对化': ['全网第一', '100%有效', '永久有效', '保证赚钱'],
    '导流': ['微信', '加V', '私信领取', '扫码'],
}
BLOCKING = {'绝对化', '导流'}


def main(argv):
    if len(argv) < 2:
        print('用法: python3 publish_checklist.py article.md')
        return 2
    path = argv[1]
    try:
        txt = open(path, encoding='utf-8').read()
    except OSError as e:
        print('读取失败:', e)
        return 2

    blocking = 0
    for cat, words in RISK.items():
        hit = [w for w in words if w in txt]
        if not hit:
            continue
        level = 'ERROR' if cat in BLOCKING else 'warn'
        extra = '（即使出现在“排除”语境也可能被机器召回，换上位词）' if cat == '敏感词面' else ''
        print('  [%s] %s: %s%s' % (level, cat, '、'.join(hit), extra))
        if cat in BLOCKING:
            blocking += 1

    for m in re.finditer(r'(\d+(?:[kK万])|\d+\s*(?:级别|量级))[^。]{0,12}(流量|收入|收益|转化)', txt):
        ctx = txt[max(0, m.start() - 40):m.end() + 60]
        if not re.search(r'未验证|样本|参考|大约|据说|有人报', ctx):
            print('  [warn] 效果数字「%s」缺来源/样本说明' % m.group(0)[:20])

    print('风控检查:', '有必须处理项' if blocking else '无阻断项')
    return 1 if blocking else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
