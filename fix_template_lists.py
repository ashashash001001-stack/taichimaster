#!/usr/bin/env python3
"""
Fix template <ul> list items in articles by replacing them with unique, topic-relevant content.
"""

import re
import os
from pathlib import Path

ARTICLES_DIR = Path("articles")

TEMPLATE_UL_RE = re.compile(
    r'<ul class="list-disc list-inside space-y-2 mb-4 text-gray-700">\s*'
    r'<li><strong>楊氏太極</strong>：太極練習中的重要元素，有助於全面提升身心健康。</li>\s*'
    r'<li><strong>陳氏太極</strong>：太極練習中的重要元素，有助於全面提升身心健康。</li>\s*'
    r'<li><strong>樁功</strong>：太極練習中的重要元素，有助於全面提升身心健康。</li>\s*'
    r'<li><strong>步法</strong>：太極練習中的重要元素，有助於全面提升身心健康。</li>\s*'
    r'<li><strong>呼吸法</strong>：太極練習中的重要元素，有助於全面提升身心健康。</li>\s*'
    r'</ul>'
)

unique_lists = {
    'tai-chi-beginner-guide': [
        ('放鬆身心', '太極拳講究「鬆」，去除多餘的緊張，而非軟弱無力'),
        ('保持中正', '脊柱正直，頭頂如懸絲，尾閭內收，確保氣血暢通'),
        ('呼吸自然', '初學時自然呼吸，熟練後配合腹式呼吸'),
        ('重心轉移', '每一步重心平穩轉移，如貓行步般輕盈'),
        ('圓活連貫', '所有動作走弧線，動作之間連貫不斷'),
    ],
    'tai-chi-vs-qigong-difference': [
        ('太極拳', '完整武術套路，動作連貫，有武術和養生雙重功能'),
        ('氣功', '注重內在能量培養，動作簡單甚至只需靜坐或站立'),
        ('共同點', '都強調放鬆身心和陰陽平衡，相輔相成'),
        ('初學者建議', '先從太極拳基本功開始，配合簡單的氣功練習'),
    ],
    'tai-chi-history-origin': [
        ('陳氏太極拳', '強調剛柔並濟、發力明顯，是太極拳的源頭'),
        ('楊氏太極拳', '動作柔和舒展，由楊露禪改良自陳氏太極拳'),
        ('全球傳播', '太極拳已傳播到全球150多個國家，超過3億人練習'),
        ('非物質文化遺產', '2020年被聯合國教科文組織列入非物質文化遺產'),
    ],
    'yang-style-tai-chi-introduction': [
        ('楊露禪', '1799-1872年，楊氏太極拳創始人'),
        ('動作特點', '舒展大方，速度均勻，剛柔相濟，姿勢優美'),
        ('主要套路', '二十四式簡化太極拳、四十二式、八十五式和一百零八式'),
        ('適合人群', '動作舒緩，適合任何年齡人士'),
    ],
    'tai-chi-equipment-needed': [
        ('衣服', '任何舒適、寬鬆、不妨礙活動的衣服都可以'),
        ('鞋子', '平底、薄底、柔軟的鞋子最適合'),
        ('太極服', '絲質或棉質，寬鬆舒適'),
        ('太極鞋', '薄底布鞋，有助於感受地面'),
    ],
    'qigong-beginners-guide': [
        ('調身', '氣功動作通常簡單舒緩，容易學習'),
        ('調息', '強調深呼吸，特別是腹式呼吸'),
        ('調心', '意念集中，排除雜念'),
        ('靜功', '靜坐、站樁為主'),
        ('動功', '八段錦、五禽戲、易筋經等'),
    ],
    'baduanjin-eight-brocades': [
        ('雙手托天', '理三焦，調節全身氣機'),
        ('左右開弓', '似射雕，疏肝理氣'),
        ('調理脾胃', '須單舉，促進消化功能'),
        ('五勞七傷', '往後瞧，疏通經絡'),
        ('背後七顛', '百病消，強身健體'),
    ],
}

FALLBACK_LIST = [
    ('基本原理', '陰陽平衡、以柔克剛，貫穿每一個動作'),
    ('練習要素', '放鬆、中正、以腰為軸、虛實分明'),
    ('身心益處', '改善姿勢、舒緩壓力、增強平衡能力'),
    ('入門建議', '先從站樁開始，逐步過渡到套路練習'),
]


def make_ul(items):
    """Generate HTML ul list from list of (term, desc) tuples."""
    return '<ul class="list-disc list-inside space-y-2 mb-4 text-gray-700">\n' + ''.join(
        f'    <li><strong>{term}</strong>：{desc}。</li>\n' for term, desc in items
    ) + '</ul>'


def get_slug(filename):
    """Extract slug from filename (e.g., 'tai-chi-beginner-guide' from 'tai-chi-beginner-guide.html')."""
    return filename.replace('.html', '')


def fix_article(filepath):
    """Fix template lists in a single article file."""
    slug = get_slug(filepath.name)
    content = filepath.read_text(encoding='utf-8')

    if TEMPLATE_UL_RE.search(content):
        items = unique_lists.get(slug, FALLBACK_LIST)
        new_ul = make_ul(items)
        new_content = TEMPLATE_UL_RE.sub(new_ul, content)
        filepath.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    fixed_count = 0
    for filepath in sorted(ARTICLES_DIR.glob("*.html")):
        if fix_article(filepath):
            print(f"Fixed: {filepath.name}")
            fixed_count += 1

    print(f"\nTotal files fixed: {fixed_count}")


if __name__ == "__main__":
    main()