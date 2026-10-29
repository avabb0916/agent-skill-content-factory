#!/usr/bin/env python3
"""长文质检（只依赖标准库）
用法: python3 qc_article.py article.md [--json]
退出码: 0 通过 / 1 有 error / 2 执行失败
"""
import json
import os
import re
import sys


def parse_frontmatter(raw):
    if not raw.startswith('---'):
        return {}, raw
    end = raw.find('\n---', 3)
    if end < 0:
        return {}, raw
    fm = {}
    for line in raw[3:end].splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm, raw[end + 4:]


def analyze(raw):
    fm, body = parse_frontmatter(raw)
    h1 = re.findall(r'^#\s+(.+)$', body, re.M)
    h2 = re.findall(r'^##\s+(.+)$', body, re.M)
    h3 = re.findall(r'^###\s+', body, re.M)
    imgs = [a or b for a, b in re.findall(r'!\[\[([^\]]+)\]\]|!\[[^\]]*\]\(([^)]+)\)', body)]
    plain = re.sub(r'!\[\[[^\]]+\]\]', '', body)
    plain = re.sub(r'```[\s\S]*?```', '', plain)
    chars = len(re.findall(r'[\u4e00-\u9fa5]', plain))
    words = chars + len(re.findall(r'\b[A-Za-z]{2,}\b', plain))
    return {
        'fm': fm,
        'h1': h1, 'h2': h2, 'h3': h3, 'images': imgs,
        'plain': plain, 'words': words,
        'tables': len(re.findall(r'^\|.+\|$', body, re.M)),
        'fences': body.count('```') // 2,
        'not_xy': len(re.findall(r'不是[^。，\n]{1,18}[，。]?\s*是', plain)),
    }


BANNED = ['TODO', '内部黑话', 'BIP']
RISK = ['成人', '赌博', '博彩', '盗版', '翻墙', '代注册', '荐股']
ABSOLUTE = ['全网第一', '100%有效', '永久有效', '保证赚钱']


def check(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    doc = analyze(open(path, encoding='utf-8').read())
    base = os.path.dirname(os.path.abspath(path))
    issues = []

    def add(level, code, msg):
        issues.append({'level': level, 'code': code, 'msg': msg})

    title = doc['fm'].get('title') or (doc['h1'][0] if doc['h1'] else '')
    if not title:
        add('error', 'title-required', '没有标题')
    if len(doc['h1']) > 1:
        add('error', 'single-h1', '一级标题 %d 个，只允许 1 个' % len(doc['h1']))
    if len(doc['h2']) < 5:
        add('warn', 'h2-min', '二级标题 %d 个，建议 ≥5' % len(doc['h2']))
    if doc['h3']:
        add('warn', 'no-h3', '三级标题 %d 个（多数平台不支持）' % len(doc['h3']))
    if doc['words'] < 2000:
        add('warn', 'word-min', '正文 %d 字/词，长文建议 ≥2000' % doc['words'])
    if doc['tables']:
        add('warn', 'no-table', '含 %d 行表格' % doc['tables'])
    if doc['fences']:
        add('warn', 'no-fence', '含 %d 个代码块' % doc['fences'])

    n = len(doc['images'])
    if n < 5:
        add('warn', 'image-min', '配图 %d 张，建议 ≥5' % n)
    if n > 9:
        add('warn', 'image-max', '配图 %d 张，建议 ≤9' % n)
    for p in doc['images']:
        full = p if os.path.isabs(p) else os.path.join(base, p)
        if not os.path.exists(full):
            add('error', 'image-exists', '配图不存在: %s' % p)

    cover = doc['fm'].get('cover_image')
    if cover:
        full = cover if os.path.isabs(cover) else os.path.join(base, cover)
        if not os.path.exists(full):
            add('error', 'cover-exists', '封面不存在: %s' % cover)

    if doc['not_xy'] > 3:
        add('warn', 'no-not-x-is-y', '「不是X，是Y」%d 次（AI 味强信号），建议 ≤3' % doc['not_xy'])
    tail = doc['plain'][-320:]
    if not re.search(r'留言|评论|告诉我|你怎么|你们的', tail):
        add('warn', 'cta-tail', '结尾没有提问/互动引导')

    long_paras = [p for p in doc['plain'].split('\n\n')
                  if len(re.findall(r'[\u4e00-\u9fa5]', p)) > 220]
    if long_paras:
        add('warn', 'long-paragraph', '%d 段超过 220 字' % len(long_paras))

    for w in BANNED:
        if w in doc['plain']:
            add('error', 'banned-words', '出现内部词: %s' % w)
    hit = [w for w in RISK if w in doc['plain']]
    if hit:
        add('warn', 'risk-words', '敏感词面: %s（换上位词更稳）' % '、'.join(hit))
    for w in ABSOLUTE:
        if w in doc['plain']:
            add('error', 'absolute-claim', '绝对化表述: %s' % w)

    for m in re.finditer(r'(\d+(?:[kK万])|\d+\s*(?:级别|量级))[^。]{0,12}(流量|收入|收益|转化)', doc['plain']):
        ctx = doc['plain'][max(0, m.start() - 40):m.end() + 60]
        if not re.search(r'未验证|样本|参考|大约|据说|有人报', ctx):
            add('warn', 'claim-number', '效果数字「%s」缺来源/样本说明' % m.group(0)[:20])

    errors = [i for i in issues if i['level'] == 'error']
    return {
        'ok': not errors,
        'file': os.path.basename(path),
        'title': title,
        'words': doc['words'],
        'h2': len(doc['h2']),
        'images': n,
        'issues': issues,
        'counts': {
            'error': len(errors),
            'warn': len([i for i in issues if i['level'] == 'warn']),
        },
    }


def main(argv):
    if len(argv) < 2:
        print('用法: python3 qc_article.py article.md [--json]')
        return 2
    path = argv[1]
    try:
        res = check(path)
    except Exception as e:  # noqa: BLE001
        print('检查失败:', e)
        return 2
    if '--json' in argv:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print('\n%s' % res['file'])
        print('  标题: %s' % (res['title'] or '(无)'))
        print('  字数: %d   二级标题: %d   配图: %d' % (res['words'], res['h2'], res['images']))
        for i in res['issues']:
            print('  [%s] %s: %s' % (i['level'], i['code'], i['msg']))
        print('\n  %d error / %d warn' % (res['counts']['error'], res['counts']['warn']))
        print('  结果:', '可以发（建议先处理 warn）' if res['ok'] else '不能发（先修 error）')
    return 0 if res['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
