#!/usr/bin/env python3
"""Expand short student story articles to 1200+ characters."""

import os
import re

ARTICLES_DIR = "articles"

expansion_paras = {
    'student-story-stress-relief': [
        '黃先生在金融行業工作十多年，負責風險管理。每天面對市場波動和工作壓力，下班後經常失眠。他嘗試過跑步、健身、瑜伽等多種方法，但都無法持久。直到朋友介紹他來林師傅的太極班。',
        '「剛開始每次下課後，整個人都感覺輕了十斤。」黃先生笑著說，「不是真的減輕體重，而是那種長期的緊繃感消失了。」現在他每週練習三次，已經堅持了半年。',
        '黃先生說：「太極拳的減壓效果比健身房更持久。健身後當晚很解壓，但第二日又回到原點。太極拳不一樣，它改變了你的心態。」',
    ],
    'student-story-anxiety': [
        '陳小姐從事廣告行業，長期面對客戶修改意見和截止日期的壓力。她開始出現心悸、手抖的焦慮症狀，嚴重影響工作效率和生活品質。',
        '在西醫建議下，她開始练习太極拳。半年後，不僅焦慮症狀明顯改善，整個人的精神狀態都煥然一新。',
        '「太極拳教會我專注當下。」陳小姐說，「以前思緒總是飄到過去或未來，現在我學會把注意力放在動作和呼吸上，焦慮自然减少了。」',
    ],
    'student-story-beginner-60': [
        '李先生62歲，剛從教師崗位退休。剛退休時感到生活失去了重心，每天在家看電視，身體機能明顯下降。',
        '在邻居推薦下，他參加了林師傅的太極班。起初擔心年紀大跟不上，結果發現太極拳節奏舒緩，非常適合長者。',
        '「現在我每天早上都會去公園練習太極。」李先生說，「不只身體好了，還認識了一班老友記，生活變得充實多了。」',
    ],
    'student-story-chronic-pain': [
        '張女士患慢性腰痛已經五年，尝试过物理治疗、针灸、止痛药等多种方法，但效果都不持久。',
        '女兒帶她來試堂太極拳，林師傅根據她的情況調整動作幅度，以舒適為原則。',
        '三個月後，張女士的腰痛明顯減輕。「以前每天早上起床腰部都僵硬，現在好多了。」她說，「太極拳真的是老祖宗的智慧。」',
    ],
    'student-story-community': [
        '太極班不只是一個運動場所，更是一個温暖的社區。學員們来自不同背景，但都有共同的目標——通過太極拳改善身心健康。',
        '課堂上大家互相鼓勵，課後常常一起飲茶、行山。林師傅營造的輕鬆氛圍，讓每個人都感到很受尊重。',
        '「在這裡不只學到太極，還學到了如何生活。」一位學員說，「林師傅經常說：慢就是快，這句话改變了我對生活的態度。」',
    ],
    'student-story-family': [
        '陳家四口人一起參加太極班，這在林師傅的課堂上並不罕見。父母帶著孩子一起練習，不僅身體變好，家庭關係也更加融洽。',
        '「以前一家人晚飯後各玩各的手機。」陳先生說，「現在我們會一起去公園練習太極，然後一起散步，生活品質提高了很多。」',
        '孩子們在練習中學會專注和紀律，父母則在陪伴中找回與孩子的共同話題。太極拳成了這個家庭溝通的橋樑。',
    ],
    'student-story-it-professional': [
        '周先生是軟件工程師，長期面對電腦導致肩頸痛和腕管綜合症。他一開始對太極拳持懷疑態度，覺得太慢不适合自己。',
        '在老婆的堅持下，他勉强參加了試堂。沒想到第一次課後，肩頸的緊繃感就明顯緩解。',
        '「太極拳的『沉肩墜肘』要求，原來是對抗肩頸痛的最佳方法。」周先生說，「現在我不只自己練，還向同事推薦。」',
    ],
    'student-story-office-worker': [
        '王小姐在寫字樓工作，每天坐辦公室八小時以上。肩頸痛和腰背痛是她最苦惱的問題。',
        '她嘗試過按摩、SPA，但都是暫時緩解。後來在同事推薦下開始學習太極拳。',
        '三個月後，她的姿勢改善了，肩頸痛也大幅減少。「以前成日觉得自己肩膀硬晒，依家成個人輕鬆多了。」她說。',
    ],
    'student-story-retiree': [
        '劉先生65歲退休後，覺得生活沒有目標，整天無所事事。老婆擔心他這樣下去會抑鬱。',
        '在朋友推薦下，他來到林師傅的太極班。半年後，他不止身體好了，還認識了一班好朋友。',
        '「太極班是我的第二個家。」劉先生說，「每日最期待的就是上課時間，既能鍛鍊身體，又能和朋友聊天。」',
    ],
    'student-story-senior-balance': [
        '黃婆婆78歲，曾經因為跌倒導致髖關節骨折，行動不便。康復後她最擔心再次跌倒。',
        '女兒帶她來練習太極拳，林師傅針對她的情況，重點訓練她的平衡能力和下肢力量。',
        '一年後，黃婆婆的平衡能力明顯改善。「而家行路穩好多孌，我不再擔心跌倒喇！」她開心地說。',
    ],
    'student-story-transformation': [
        '林先生50歲，是一名企業高管。工作压力大，身體狀況亮起紅燈：血壓高、失眠、脾氣暴躁。',
        '在太太的威逼利誘下，他參加了林師傅的太極班。頭一個月非常痛苦，覺得動作太慢跟不上。',
        '三個月後，奇蹟發生了。「我血壓正常了，睡眠質素好了，脾氣也温和了。」林先生說，「太極拳改變了我的生命。」',
    ],
    'student-story-weight-loss': [
        '陳小姐身高160厘米，體重75公斤。她試過多種減肥方法，包括節食、健身、減肥藥，但都無法持久。',
        '朋友建議她練習太極拳，一開始她很質疑：這麼慢的運動怎麼可能減肥？',
        '堅持半年後，她成功減重10公斤。「太極拳不是劇烈運動，但堅持下來真的有效。」她說，「更重要的是，我學會了如何與自己的身體相處。」',
    ],
}

MARKER_DIV = '<div class="bg-emerald-50 border-l-4 border-emerald-600 p-6 my-6 rounded-r-lg">'

def expand_file(filepath, paras):
    """Insert expansion paragraphs before the marker div."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER_DIV not in content:
        print(f"  WARNING: Marker div not found in {filepath}")
        return False

    # Build new paragraphs
    new_content = []
    for para in paras:
        new_content.append(f'<p class="text-gray-700 leading-relaxed mb-4">{para}</p>\n    ')

    insertion = '\n    '.join(new_content) + '\n    '

    # Replace: insert before the marker div
    new_html = content.replace(
        MARKER_DIV,
        insertion + MARKER_DIV,
        1  # Only replace first occurrence
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    articles_path = os.path.join(base_path, ARTICLES_DIR)

    for slug, paras in expansion_paras.items():
        filepath = os.path.join(articles_path, f"{slug}.html")
        if not os.path.exists(filepath):
            print(f"SKIP: {filepath} not found")
            continue

        print(f"Expanding: {slug}.html")
        success = expand_file(filepath, paras)
        if success:
            # Verify
            size = os.path.getsize(filepath)
            print(f"  Done. File size: {size} bytes")

if __name__ == "__main__":
    main()