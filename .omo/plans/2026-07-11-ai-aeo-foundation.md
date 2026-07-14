# AI/AEO Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the AI/AEO foundation for 林燦平太極學會 by creating llms.txt, pricing.md, upgrading robots.txt with AI crawler strategy, and adding _headers for caching policy.

**Architecture:** Four independent static files at the site root. llms.txt provides an AI-agent-readable site index. pricing.md provides AI-readable pricing info. robots.txt controls crawler access. _headers sets HTTP cache headers for GitHub Pages.

**Tech Stack:** Plain text/markdown files, static HTML site root.

**Files to create/modify:**
- Create: `llms.txt`
- Create: `pricing.md`
- Modify: `robots.txt`
- Create: `_headers`

---

### Task 1: Create llms.txt

**Files:**
- Create: `llms.txt`

- [ ] **Step 1: Write the llms.txt file**

The llms.txt should follow the llms.txt standard: a brief site description, then categorized URL listings with descriptions. No tests needed — this is a static data file.

```markdown
# 林燦平太極學會 | Lam Chan Ping Tai Chi Club
> 油塘太極班招生 | 教授太極拳、刀、劍、扇、鞭桿 | 歡迎任何年齡及初學者

## 核心頁面
- https://chungyuicheung.github.io/taichimaster/：首頁，包含課程介紹、收費、時間表、學員見證、常見問題
- https://chungyuicheung.github.io/taichimaster/blog.html：養生專欄，100 篇太極健康知識文章
- https://chungyuicheung.github.io/taichimaster/404.html：自訂錯誤頁，包含熱門文章推薦

## 地區登陸頁
- https://chungyuicheung.github.io/taichimaster/kwun-tong.html：觀塘太極班資訊
- https://chungyuicheung.github.io/taichimaster/lam-tin.html：藍田太極班資訊
- https://chungyuicheung.github.io/taichimaster/tseung-kwan-o.html：將軍澳太極班資訊
- https://chungyuicheung.github.io/taichimaster/kowloon-city.html：九龍城太極班資訊
- https://chungyuicheung.github.io/taichimaster/wong-tai-sin.html：黃大仙太極班資訊

## 文章分類

### 太極入門（13 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-beginner-guide.html：太極拳入門指南，初學者必讀的 10 個基本概念
- https://chungyuicheung.github.io/taichimaster/articles/yang-style-tai-chi-introduction.html：楊氏太極拳介紹，最流行的太極流派
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-vs-qigong-difference.html：太極拳與氣功的分別
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-equipment-needed.html：學太極需要買什麼裝備？初學者裝備指南
- https://chungyuicheung.github.io/taichimaster/articles/best-time-practice-tai-chi.html：什麼時候練太極最好？晨練 vs 晚練
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-breathing-techniques.html：太極拳呼吸法教學，腹式呼吸的正確方法
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-24-forms-overview.html：二十四式簡化太極拳，每一式詳細解說
- https://chungyuicheung.github.io/taichimaster/articles/common-tai-chi-mistakes.html：初學太極常見的 8 個錯誤及改正方法
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-terminology-guide.html：太極拳常用術語解釋
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-etiquette.html：太極拳課堂禮儀與傳統
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-age-guide.html：不同年齡學太極的注意事項
- https://chungyuicheung.github.io/taichimaster/articles/how-to-choose-tai-chi-class.html：如何選擇適合自己的太極班
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-morning-routine.html：清晨太極養生習慣養成指南

### 肩頸腰背（13 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-neck-pain-relief.html：太極拳如何舒緩肩頸痛？辦公室人士救星
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-lower-back-pain.html：太極拳改善腰背痛，科學實證方法
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-digital-neck.html：低頭族救星，太極拳改善數位頸
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-frozen-shoulder.html：太極拳幫助改善五十肩
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-carpal-tunnel.html：太極拳對腕管綜合症的幫助
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-knee-pain.html：太極拳與膝蓋健康，正確練習避免受傷
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sciatica.html：太極拳改善坐骨神經痛
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-headache-relief.html：太極拳緩解緊張性頭痛
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-muscle-tension.html：太極拳釋放全身肌肉緊繃
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-posture-correction.html：太極拳矯正不良姿勢
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sports-injury.html：太極拳幫助運動傷害康復
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-fibromyalgia.html：太極拳對纖維肌痛的緩解作用
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-arthritis.html：太極拳改善關節炎的科學依據

### 長者健康（13 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-fall-prevention.html：太極拳預防長者跌倒，科學證實有效方法
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-balance.html：太極拳改善長者平衡能力
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-flexibility.html：太極拳提升長者柔韌性
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-heart.html：太極拳對長者心血管健康的好處
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-immunity.html：太極拳增強長者免疫力
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-memory.html：太極拳改善長者記憶力
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-sleep.html：太極拳改善長者睡眠品質
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-osteoporosis.html：太極拳預防骨質疏鬆
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-diabetes.html：太極拳對長者糖尿病的輔助治療
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-depression.html：太極拳改善長者抑鬱情緒
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-social.html：太極拳豐富長者社交生活
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-cane-elderly.html：長者用太極拐杖的好處
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-retirement-life.html：退休後學太極，開啟健康第二人生

### 心理健康（12 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-stress-relief.html：太極拳減壓科學，如何釋放都市壓力
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-anxiety.html：太極拳緩解焦慮症
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-depression.html：太極拳改善抑鬱症
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sleep-quality.html：太極拳提升睡眠品質
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-meditation.html：太極拳與靜坐冥想
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-mindfulness.html：太極拳與正念練習
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-emotional-balance.html：太極拳調節情緒平衡
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-brain-health.html：太極拳促進大腦健康
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-focus.html：太極拳提升專注力
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-confidence.html：太極拳建立自信心
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-burnout.html：太極拳對抗工作倦怠
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-patience.html：從太極拳學習耐心

### 器械教學（13 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sword-basics.html：太極劍入門，初學者必知基礎知識
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sword-forms.html：太極劍基本套路教學
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-sword-health.html：太極劍的健康益處
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-broadsword.html：太極刀入門教學
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-fan-techniques.html：太極扇基本技法
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-fan-health-benefits.html：太極扇的健康益處
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-fan-performance.html：太極扇表演技巧
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-cane.html：太極拐杖用法教學
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-weapons-comparison.html：太極器械比較，刀劍扇鞭桿特點
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-weapons-history.html：太極器械的歷史淵源
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-equipment-selection.html：如何選擇太極器械
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-equipment-maintenance.html：太極器械保養指南
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-martial-arts.html：太極拳的武術應用

### 養生氣功（12 篇）
- https://chungyuicheung.github.io/taichimaster/articles/qigong-beginners-guide.html：氣功入門，初學者必知基礎知識
- https://chungyuicheung.github.io/taichimaster/articles/qigong-breathing.html：氣功呼吸法教學
- https://chungyuicheung.github.io/taichimaster/articles/qigong-meditation.html：氣功冥想入門
- https://chungyuicheung.github.io/taichimaster/articles/qigong-energy.html：氣功與能量養生
- https://chungyuicheung.github.io/taichimaster/articles/qigong-immunity.html：氣功增強免疫力
- https://chungyuicheung.github.io/taichimaster/articles/qigong-digestion.html：氣功改善腸胃消化
- https://chungyuicheung.github.io/taichimaster/articles/qigong-meridians.html：氣功與經絡養生
- https://chungyuicheung.github.io/taichimaster/articles/qigong-five-animals.html：五禽戲入門教學
- https://chungyuicheung.github.io/taichimaster/articles/qigong-morning-routine.html：清晨氣功養生流程
- https://chungyuicheung.github.io/taichimaster/articles/qigong-vs-yoga.html：氣功與瑜伽的分別
- https://chungyuicheung.github.io/taichimaster/articles/baduanjin-eight-brocades.html：八段錦完整教學
- https://chungyuicheung.github.io/taichimaster/articles/zhan-zhuang-standing-meditation.html：站樁功入門指南

### 太極文化（12 篇）
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-history-origin.html：太極拳的歷史起源
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-yin-yang-philosophy.html：太極拳與陰陽哲學
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-taoism.html：太極拳與道家思想
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-five-elements.html：太極拳與五行學說
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-chinese-medicine.html：太極拳與中醫養生理論
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-modern-science.html：太極拳的現代科學研究
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-global-spread.html：太極拳的全球傳播
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-hong-kong.html：香港太極拳發展史
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-famous-masters.html：太極拳著名大師介紹
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-unesco.html：太極拳入選聯合國非物質文化遺產
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-meditation-zen.html：太極拳與禪修
- https://chungyuicheung.github.io/taichimaster/articles/tai-chi-senior-health-complete-guide.html：長者太極拳完全指南

### 學員故事（12 篇）
- https://chungyuicheung.github.io/taichimaster/articles/student-story-stress-relief.html：金融業黃先生透過太極拳減壓
- https://chungyuicheung.github.io/taichimaster/articles/student-story-anxiety.html：廣告業陳小姐透過太極拳改善焦慮
- https://chungyuicheung.github.io/taichimaster/articles/student-story-beginner-60.html：62 歲退休教師重拾生活重心
- https://chungyuicheung.github.io/taichimaster/articles/student-story-chronic-pain.html：慢性腰痛患者的康復之路
- https://chungyuicheung.github.io/taichimaster/articles/student-story-community.html：太極班社區溫暖故事
- https://chungyuicheung.github.io/taichimaster/articles/student-story-family.html：一家四口一起練習太極
- https://chungyuicheung.github.io/taichimaster/articles/student-story-it-professional.html：IT 工程師改善肩頸痛
- https://chungyuicheung.github.io/taichimaster/articles/student-story-office-worker.html：寫字樓員工改善腰背痛
- https://chungyuicheung.github.io/taichimaster/articles/student-story-retiree.html：65 歲退休人士找到生活目標
- https://chungyuicheung.github.io/taichimaster/articles/student-story-senior-balance.html：78 歲婆婆預防跌倒
- https://chungyuicheung.github.io/taichimaster/articles/student-story-transformation.html：50 歲企業高管的健康轉變
- https://chungyuicheung.github.io/taichimaster/articles/student-story-weight-loss.html：太極拳減重成功案例

## 收費資訊
收費請致電或 WhatsApp 6098 5742 查詢。歡迎即場試堂，滿意才報名。
按月收費，設有太極拳班及器械班。
```

- [ ] **Step 2: Verify the file is valid**

```bash
head -5 llms.txt && wc -l llms.txt
```
Expected: First 5 lines show the header. Total lines should be substantial (~200+).

- [ ] **Step 3: Commit**

```bash
git add llms.txt
git commit -m "feat: add llms.txt for AI/AEO - site index for AI crawlers"
```

---

### Task 2: Create pricing.md

**Files:**
- Create: `pricing.md`

- [ ] **Step 1: Write the pricing.md file**

An AI-agent-readable pricing document. Clear, structured, no filler.

```markdown
# 收費資訊 | Pricing

**林燦平太極學會** | Lam Chan Ping Tai Chi Club

最後更新：2026-07-11

---

## 課程收費

### 太極拳班
- 按月收費，歡迎 WhatsAapp 6098 5742 查詢最新價格
- 包含基本樁功、步法、傳統太極拳套路
- 適合任何年齡及初學者

### 太極器械班
- 按月收費，歡迎 WhatsApp 6098 5742 查詢最新價格
- 包含太極刀、太極劍、太極扇、鞭桿
- 適合已掌握基本拳法的學員

---

## 報名方式
1. **即場報名**：直接在上課時間到小童群益會前空地
2. **電話查詢**：致電 6098 5742
3. **WhatsApp**：https://wa.me/85260985742

## 上課時間
- 星期一、三、五、六、日：早上 09:00 - 下午 01:00
- 星期二、四：早上 10:00 - 下午 01:00
- 每日：晚上 07:00 - 晚上 10:00

## 地點
香港油塘小童群益會賽馬會油塘青少年綜合服務中心前空地

## 備註
- 歡迎隨時親臨觀課，滿意才報名
- 零基礎可旁聽，無需預約
- 首堂可免費試玩
```

- [ ] **Step 2: Verify the file**

```bash
head -5 pricing.md && wc -l pricing.md
```
Expected: Header lines visible. ~45 lines total.

- [ ] **Step 3: Commit**

```bash
git add pricing.md
git commit -m "feat: add pricing.md for AI/AEO - agent-readable pricing document"
```

---

### Task 3: Upgrade robots.txt with AI Crawler Strategy

**Files:**
- Modify: `robots.txt`

- [ ] **Step 1: Replace robots.txt content**

Current file:
```
User-agent: *
Allow: /

Sitemap: https://chungyuicheung.github.io/taichimaster/sitemap.xml
```

Replace with:

```
# AI Search Engine Crawlers - Allowed
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

# Training-only crawlers - Blocked
User-agent: CCBot
Disallow: /

# All other crawlers
User-agent: *
Allow: /

Sitemap: https://chungyuicheung.github.io/taichimaster/sitemap.xml
```

- [ ] **Step 2: Verify the file**

```bash
cat robots.txt
```
Expected: All 7 user-agent blocks visible with correct Allow/Disallow directives.

- [ ] **Step 3: Commit**

```bash
git add robots.txt
git commit -m "feat: upgrade robots.txt with AI crawler strategy - allow AI crawlers, block CCBot"
```

---

### Task 4: Create _headers for Caching Policy

**Files:**
- Create: `_headers`

- [ ] **Step 1: Write the _headers file**

GitHub Pages supports `_headers` for custom HTTP headers. This file:
1. Sets llms.txt to no-cache (AI crawlers always get fresh content)
2. Sets pricing.md to no-cache
3. Sets static assets to 1-year immutable cache
4. Sets HTML pages to 1-hour cache

```
# AI/AEO files - no cache (always serve latest)
/llms.txt
  Cache-Control: no-cache, no-store, must-revalidate

/pricing.md
  Cache-Control: no-cache, no-store, must-revalidate

# Static assets - 1 year immutable cache
/*.png
  Cache-Control: max-age=31536000, immutable

/*.jpg
  Cache-Control: max-age=31536000, immutable

/*.JPG
  Cache-Control: max-age=31536000, immutable

/*.ico
  Cache-Control: max-age=31536000, immutable

/*.svg
  Cache-Control: max-age=31536000, immutable

/*.webp
  Cache-Control: max-age=31536000, immutable

# HTML pages - short cache for content updates
/*.html
  Cache-Control: max-age=3600
```

- [ ] **Step 2: Verify the file**

```bash
cat _headers
```
Expected: All header rules shown correctly.

- [ ] **Step 3: Commit**

```bash
git add _headers
git commit -m "feat: add _headers with caching policy - llms.txt no-cache, static assets 1y immutable"
```

---

### Scope Completion Checklist
- [ ] llms.txt created with all 108 URLs organized by category + descriptions
- [ ] pricing.md created with clear fee structure
- [ ] robots.txt upgraded with AI crawler strategy (allow GPTBot/ClaudeBot/PerplexityBot, block CCBot)
- [ ] _headers created with llms.txt no-cache + static asset caching
- [ ] All 4 files committed
