#!/usr/bin/env python3
"""
Fix master quote template in articles - replace with unique topic-relevant quotes per article.
"""

import re
import os
from pathlib import Path

# Per-article quotes to use (83 entries)
master_quote = {
    'tai-chi-beginner-guide': '「我教了三十多年太極，發現很多初學者最大的問題不是學會不會，而是太心急。」林燦平師傅說，「太極拳是一輩子的功夫，不要急著學完整套拳。先把基本功練好，每一個動作做到位，比學十套拳都有用。」',
    'tai-chi-history-origin': '「太極拳的歷史比我教拳的時間還要長得多。」林師傅說，「但無論哪個流派，基本功都是一樣的。站樁、放鬆、以腰為軸——這些是所有太極的根基。」',
    'tai-chi-vs-qigong-difference': '「經常有學生問我：師傅，學太極好還是學氣功好？」林師傅說，「我的答案是：兩樣都學。太極拳本身就有氣功的元素，兩者相輔相成。」',
    'tai-chi-24-forms-overview': '「二十四式是最適合初學者的套路。」林師傅說，「動作精簡，但每一式都是太極的精髓。學完整套，大約五至八分鐘，但足以鍛鍊全身。」',
    'yang-style-tai-chi-introduction': '「楊氏太極是世界上最流行的太極流派。」林師傅說，「動作舒展優美，速度均勻，適合任何年齡。我教的就是楊氏太極。」',
    'tai-chi-equipment-needed': '「初學者不需要買任何特殊裝備。」林師傅說，「穿舒適的衣服和鞋子來上課就可以了。等確定有興趣，再考慮購買太極服。」',
    'best-time-practice-tai-chi': '「晨練和晚練各有好处。」林師傅說，「早上練習可以喚醒身體，晚上練習可以舒緩一天的疲勞。選擇適合自己作息的时间最重要。」',
    'tai-chi-breathing-techniques': '「呼吸是太極的靈魂。」林師傅說，「初學者不要刻意控制呼吸，讓它自然就好。等動作熟練了，呼吸自然會配合動作。」',
    'common-tai-chi-mistakes': '「初學者最常犯的錯誤是用力過度。」林師傅說，「太極拳講究『鬆』，不是軟弱無力，而是去除所有不必要的緊張。」',
    'how-to-choose-tai-chi-class': '「選擇太極班，最重要的是看師傅的教學風格。」林師傅說，「好的師傅會耐心細緻，每個動作都會親自示範。歡迎先來觀課，满意才報名。」',
    'tai-chi-terminology-guide': '「術語只是參考，重要的是身體感受。」林師傅說，「『鬆』、『沉肩墜肘』、『含胸拔背』——這些要求要在練習中慢慢體會。」',
    'tai-chi-age-guide': '「太極拳適合任何年齡。」林師傅說，「六歲到九十歲都可以學，只是練習的方式和強度需要調整。」',
    'tai-chi-morning-routine': '「早上練習太極，最好先站樁三分鐘。」林師傅說，「讓身體慢慢覺醒，然後再做套路，這樣的效果最好。」',
    'tai-chi-neck-pain-relief': '「肩頸痛是辦公室人士的常見問題。」林師傅說，「太極拳的『沉肩墜肘』要求本身，就是對肩頸最好的治療。」',
    'tai-chi-lower-back-pain': '「腰背痛患者練太極，要特別注意動作幅度。」林師傅說，「以舒適為原則，不要勉強。循序漸進，很快就會見到效果。」',
    'tai-chi-frozen-shoulder': '「五十肩患者可以練太極拳，但要避免急性發炎時過度練習。」林師傅說，「緩解期通過太極的緩慢動作，可以逐步恢復肩關節的活動範圍。」',
    'tai-chi-knee-pain': '「膝蓋痛患者最擔心蹲下去的動作。」林師傅說，「其實只要膝蓋不超過腳尖，半蹲姿勢反而能強化膝蓋周圍的肌肉，保護膝關節。」',
    'tai-chi-sciatica': '「坐骨神經痛患者练习太極拳，要特別注意腰部的旋轉幅度。」林師傅說，「以不疼痛為原則，急性期應先就醫。」',
    'tai-chi-carpal-tunnel': '「手腕問題的患者练习太極拳，手腕一定要放鬆。」林師傅說，「『掤』的手法要求手臂呈弧形、手腕放鬆，能有效緩解手腕的緊張。」',
    'tai-chi-posture-correction': '「練習太極拳三個月，很多學員的姿勢都會自然改善。」林師傅說，「『虛領頂勁』、『含胸拔背』這些要求，不知不覺就矫正了駝背和寒背。」',
    'tai-chi-headache-relief': '「緊張性頭痛的根源是頭部和頸部肌肉長期緊張。」林師傅說，「太極拳的全身放鬆要求，能從根源上緩解這種緊張。」',
    'tai-chi-arthritis': '「美國關節炎基金會將太極拳列為最適合關節炎患者的運動。」林師傅說，「我有很多長者學員，練習太極拳後關節疼痛明顯減輕。」',
    'tai-chi-digital-neck': '「『手機頸』是低頭族的常見問題。」林師傅說，「『虛領頂勁』要求頭頂如懸絲，長期練習能糾正頭部前傾的姿勢。」',
    'tai-chi-muscle-tension': '「現代人壓力大，全身肌肉長期緊繃。」林師傅說，「太極拳的『鬆』字功，是對抗緊張的最好方法。」',
    'tai-chi-sports-injury': '「運動創傷後的康復，選擇太極拳這種溫和運動最穩妥。」林師傅說，「但一定要在師傅指導下進行，確保動作不會對受傷部位造成額外壓力。」',
    'tai-chi-fibromyalgia': '「纖維肌痛症患者練習太極拳，要以舒適為原則。」林師傅說，「低強度、不會加重疼痛的運動，反而能改善整體症狀。」',
    'tai-chi-fall-prevention': '「哈佛醫學院研究發現，練習太極拳的長者跌倒風險降低了45%。」林師傅說，「我很多長者學員，練習後平衡能力明顯改善，走路也更穩了。」',
    'tai-chi-senior-balance': '「長者最重要的練習是站樁。」林師傅說，「每天站樁五至十分鐘，能有效強化下肢力量，改善平衡能力。」',
    'tai-chi-senior-memory': '「練習太極拳需要記憶套路順序，這對大腦是很好的訓練。」林師傅說，「我有些長者學員說，練了太極後記性都好了。」',
    'tai-chi-senior-social': '「太極班不只教太極，更是一個社交場所。」林師傅說，「很多長者學員在這裡認識了新朋友，生活變得更加充實。」',
    'tai-chi-senior-osteoporosis': '「太極拳是承重運動，能幫助維持骨密度。」林師傅說，「我建議長者每天都練習，哪怕只是站樁和簡單的動作。」',
    'tai-chi-senior-heart': '「美國心臟協會將太極拳列為適合心血管疾病患者的運動。」林師傅說，「太極拳是溫和的有氧運動，能提高心率但不會過度負荷心臟。」',
    'tai-chi-senior-diabetes': '「糖尿病患者练习太極拳，飯後一到兩小時最理想。」林師傅說，「運動能消耗葡萄糖，降低血糖水平。」',
    'tai-chi-senior-sleep': '「晚上練習太極拳特別有助於睡眠。」林師傅說，「我們的晚班（19:00-22:00）非常適合有睡眠問題的學員。」',
    'tai-chi-retirement-life': '「退休後練習太極拳，是豐富生活的好選擇。」林師傅說，「健康、社交、終身學習——太極拳一次過滿足這三個願望。」',
    'tai-chi-senior-flexibility': '「長者練習太極拳，關節的靈活性和活動範圍都會明顯改善。」林師傅說，「我建議每天花十至十五分鐘練習。」',
    'tai-chi-senior-depression': '「太極拳對抗抑鬱有三重作用：運動、冥想、社交。」林師傅說，「我有些學員本來很抑鬱，練習太極後整個人都開朗了。」',
    'tai-chi-senior-immunity': '「UCLA研究發現，練習太極拳的長者免疫力顯著高於不運動的對照組。」林師傅說，「每天練習太極拳，感冒都少了很多。」',
    'tai-chi-parkinson': '「《新英格蘭醫學雜誌》研究發現，太極拳對柏金遜症患者的平衡和姿勢穩定性有顯著改善。」林師傅說，「我有些柏金遜症學員，堅持練習後效果很好。」',
    'tai-chi-stress-relief': '「研究發現，練習太極拳八週後，皮質醇水平下降了25%。」林師傅說，「壓力大的上班族，最適合下班後來打太極。」',
    'tai-chi-anxiety': '「太極拳的深呼吸能激活迷走神經，減慢心率。」林師傅說，「這是對抗焦慮的生理機制，很有效。」',
    'tai-chi-meditation': '「太極拳被稱為『moving meditation』。」林師傅說，「在運動中保持專注和覺察，這就是動態的冥想。」',
    'tai-chi-sleep-quality': '「失眠困擾很多人，安眠藥只是治標不治本。」林師傅說，「晚間練習太極拳，能幫助入睡，提高睡眠質素。」',
    'tai-chi-mindfulness': '「練習太極拳的過程中，你就在練習正念。」林師傅說，「專注於動作和身體感覺，不評價、不判斷，這正是正念的核心。」',
    'tai-chi-emotional-balance': '「太極拳講究陰陽平衡，這也是情緒管理的智慧。」林師傅說，「激動的時候要冷靜，低落的時候要振作——太極教我們動態平衡。」',
    'tai-chi-confidence': '「掌握新技能是建立自信的最快方法。」林師傅說，「很多學員告訴我，學會太極拳後，整個人都自信了。」',
    'tai-chi-brain-health': '「練習太極拳時，身體和大腦同時運作，是很好的大腦訓練。」林師傅說，「每週練習兩到三次，能有效促進大腦健康。」',
    'tai-chi-burnout': '「職業倦怠是很多上班族的問題。」林師傅說，「下班後來太極班，能幫助你從工作模式切換到生活模式。」',
    'tai-chi-focus': '「專注於動作和呼吸，能訓練大腦的『注意力肌肉』。」林師傅說，「每天練習二十分鐘，專注力會明顯提升。」',
    'tai-chi-patience': '「太極拳教我們『慢』。」林師傅說，「在這個追求速度的時代，慢下來反而能做得更好。」',
    'tai-chi-depression': '「《JAMA Psychiatry》研究發現，太極拳對抑鬱症的改善效果與心理治療相當。」林師傅說，「但要注意，太極拳是輔助，不是替代治療。」',
    'tai-chi-sword-basics': '「太極劍要求手腕靈活運用。」林師傅說，「初學者先練好太極拳的基本功，再開始學習劍法。」',
    'tai-chi-fan-techniques': '「太極扇的開合動作能訓練手腕力量。」林師傅說，「開扇時要乾脆有力，『啪』的一聲要響亮。」',
    'tai-chi-broadsword': '「太極刀的動作雖然剛猛，但仍然需要太極拳的基本功作為支撐。」林師傅說，「建議先掌握太極拳套路，再學刀法。」',
    'tai-chi-cane': '「鞭桿的長度約等於前臂長度，便於攜帶。」林師傅說，「初學者可以先從鞭桿開始，接觸器械練習。」',
    'tai-chi-equipment-selection': '「購買器械之前，先諮詢師傅的意見。」林師傅說，「劍的重量、長度、材質都要適合自己。」',
    'tai-chi-sword-health': '「太極劍要求身體挺拔，能改善姿勢。」林師傅說，「學習劍的套路能刺激大腦，增強記憶力。」',
    'tai-chi-fan-performance': '「太極扇表演時，眼神要跟隨扇子的方向。」林師傅說，「動作的節奏要有對比，開扇時快，收扇時慢。」',
    'tai-chi-weapons-history': '「這些器械雖然現在主要用於健身，但它們的武術含義仍然存在。」林師傅說，「了解歷史，能幫助你更好地理解動作。」',
    'tai-chi-sword-forms': '「三十二式太極劍是最標準的太極劍套路。」林師傅說，「每一個動作都有其獨特的劍法和含義。」',
    'tai-chi-fan-health-benefits': '「太極扇的開合動作比太極拳更有力度，能提高心率。」林師傅說，「這是很好的心肺鍛鍊。」',
    'tai-chi-cane-elderly': '「鞭桿既是練習器械，也可以作為日常行走的拐杖。」林師傅說，「一舉兩得，非常實用。」',
    'tai-chi-weapons-comparison': '「太極劍追求優雅，太極刀強調力量，太極扇注重趣味性。」林師傅說，「初學者可以先從太極扇開始，比較容易上手。」',
    'tai-chi-equipment-maintenance': '「正確的保養能讓器械使用多年。」林師傅說，「劍和刀要防鏽，扇子要避免受潮，鞭桿要定期上油。」',
    'qigong-beginners-guide': '「氣功的動作通常比太極拳更簡單，更適合初學者。」林師傅說，「建議從八段錦開始，這是最普及的氣功。」',
    'baduanjin-eight-brocades': '「八段錦有八百多年歷史，是最古老的氣功之一。」林師傅說，「全套只需十至十五分鐘，動作簡單但功效顯著。」',
    'zhan-zhuang-standing-meditation': '「站樁是太極拳的基本功，也是最有效的入門練習。」林師傅說，「初學者從三分鐘開始，逐步增加到十五分鐘。」',
    'qigong-immunity': '「練習氣功八週後，免疫細胞活性會顯著提高。」林師傅說，「我建議每天練習十五到二十分鐘。」',
    'qigong-digestion': '「飯後一小時練習氣功，能幫助消化。」林師傅說，「但要避免飯後立即劇烈運動。」',
    'qigong-energy': '「練習氣功後，白天的精力會明顯提升。」林師傅說，「早晨練習十至十五分鐘，能為一整天注入活力。」',
    'qigong-vs-yoga': '「氣功和瑜伽都有益健康，只是哲學基礎和練習方式不同。」林師傅說，「選擇哪一個，取決於個人喜好。」',
    'qigong-meditation': '「氣功練習中，身體運動和呼吸調節都是為了達到心靈的平靜。」林師傅說，「這是動態的冥想。」',
    'qigong-breathing': '「初學者從腹式呼吸開始，這是最自然的呼吸方式。」林師傅說，「熟練後可以嘗試逆腹式呼吸。」',
    'qigong-five-animals': '「五禽戲模仿虎、鹿、熊、猿、鳥五種動物的動作。」林師傅說，「每種動物對應不同的臟腑和經絡。」',
    'qigong-meridians': '「氣功的動作能拉伸經絡，促進氣血運行。」林師傅說，「定期練習，能保持經絡暢通。」',
    'qigong-morning-routine': '「早晨練習氣功，最好在空氣清新的環境中進行。」林師傅說，「空腹練習效果更好。」',
    'student-story-anxiety': '「看到學員的轉變，是我最有成就感的時刻。」林師傅說，「焦慮症學員堅持練習後，整個人都放鬆了。」',
    'student-story-beginner-60': '「六十歲開始學太極，一點都不晚。」林師傅說，「我的學員中，很多都是退休後才開始學的。」',
    'student-story-chronic-pain': '「慢性痛症患者練習太極拳，要以舒適為原則。」林師傅說，「循序漸進，不要勉强，很快就能見到效果。」',
    'student-story-community': '「太極班是一個温暖的社區。」林師傅說，「學員們互相鼓勵，一起進步，這是最珍貴的。」',
    'student-story-family': '「一家人一起練習太極拳，效果最好。」林師傅說，「有些家庭全家一起來，氣氛特別好。」',
    'student-story-it-professional': '「IT從業員的肩頸問題很常見。」林師傅說，「太極拳的『沉肩墜肘』要求，能有效緩解這些問題。」',
    'student-story-office-worker': '「辦公室一族的肩頸痛和腰背痛，都可以通過太極拳改善。」林師傅說，「關鍵是堅持練習。」',
    'student-story-retiree': '「退休後學太極拳，生活變得更加充實。」林師傅說，「太極班也是結交朋友的好地方。」',
    'student-story-senior-balance': '「長者最擔心跌倒。」林師傅說，「練習太極拳後，平衡能力明顯改善，走路也更穩了。」',
    'student-story-stress-relief': '「很多金融從業員工作壓力大，來學太極拳後減壓效果很好。」林師傅說，「放工後打太極，比去健身房更有效。」',
    'student-story-transformation': '「看到學員的轉變，是我的最大動力。」林師傅說，「堅持練習三個月，身體和心態都會有明顯改善。」',
    'student-story-weight-loss': '「練習太極拳配合均衡飲食，是健康的減肥方法。」林師傅說，「太極拳不是劇烈運動，但堅持下來效果很好。」',
}

# Regex pattern to find the template block
template_pattern = re.compile(r'<div class="bg-emerald-50 border-l-4 border-emerald-600 p-6 my-6 rounded-r-lg">.*?</div>', re.DOTALL)

# New block template
new_block_template = '''<div class="bg-emerald-50 border-l-4 border-emerald-600 p-6 my-6 rounded-r-lg">
        <h3 class="text-lg font-bold text-emerald-800 mb-3 flex items-center">
            <span class="text-2xl mr-2">👨‍🏫</span>林師傅點評
        </h3>
        <p class="text-gray-700 leading-relaxed italic">{quote}</p>
    </div>'''


def process_article(file_path: Path) -> bool:
    """Process a single article file. Returns True if modified, False otherwise."""
    slug = file_path.stem

    if slug not in master_quote:
        return False

    content = file_path.read_text(encoding='utf-8')

    match = template_pattern.search(content)
    if not match:
        return False

    new_block = new_block_template.format(quote=master_quote[slug])
    new_content = template_pattern.sub(new_block, content, count=1)

    file_path.write_text(new_content, encoding='utf-8')
    return True


def main():
    articles_dir = Path('/Users/bubu/Documents/Github/taichimaster/articles')

    modified_count = 0
    skipped_count = 0

    for html_file in sorted(articles_dir.glob('*.html')):
        if process_article(html_file):
            print(f"✓ Updated: {html_file.name}")
            modified_count += 1
        else:
            slug = html_file.stem
            if slug in master_quote:
                print(f"✗ Skipped (no template found): {html_file.name}")
            skipped_count += 1

    print(f"\nSummary: {modified_count} articles updated, {skipped_count} skipped")


if __name__ == '__main__':
    main()