# Structured Data Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance JSON-LD structured data coverage across the taichi website by adding Organization Schema, HowTo Schema, upgrading Article to BlogPosting Schema, injecting FAQPage Schema into top blog articles, and enhancing region page schemas.

**Architecture:** All changes are additions to existing HTML files — no structural changes. Organization Schema goes into index.html header. HowTo Schema into index.html. BlogPosting Schema replaces Article Schema in all 100 article pages. FAQPage Schema injected into select high-value article pages. Region page schemas enhanced with additional properties.

**Tech Stack:** Static HTML, JSON-LD (schema.org), no build tools required.

**Files to modify:**
- Modify: `index.html` (add Organization + HowTo Schema)
- Modify: 100 article files under `articles/*.html` (Article → BlogPosting Schema)
- Modify: 3-5 high-value article files (add FAQPage Schema)
- Modify: 5 region page files (enhance LocalBusiness Schema)
- No new files

---

### Task 1: Add Organization Schema to index.html

**Files:**
- Modify: `index.html` (after the existing SportsActivityLocation script block, around line 110)

- [ ] **Step 1: Read the current script block end in index.html**

Read lines 60-115 of index.html to find the exact insertion point.

```bash
sed -n '108,115p' index.html
```
Expected: Shows the closing `</script>` of SportsActivityLocation and the opening of FAQ Schema.

- [ ] **Step 2: Insert Organization Schema after SportsActivityLocation block (before FAQ Schema)**

Insert this JSON-LD block right after line 110 (`</script>`) and before line 112 (`<!-- FAQ Schema Markup -->`):

```html
    <!-- Organization Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "林燦平太極學會",
      "url": "https://chungyuicheung.github.io/taichimaster/",
      "logo": "https://chungyuicheung.github.io/taichimaster/favicon.png",
      "description": "林燦平師傅親自教授太極拳、刀、劍、扇及鞭桿。油塘區實體課程，歡迎任何年齡人士參加。",
      "foundingDate": "2020",
      "telephone": "+852-6098-5742",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "油塘",
        "addressRegion": "香港",
        "addressCountry": "HK"
      },
      "sameAs": [
        "https://wa.me/85260985742"
      ]
    }
    </script>
```

- [ ] **Step 3: Verify the insertion**

```bash
grep -A 20 'Organization Schema' index.html
```
Expected: Shows the Organization JSON-LD block with all fields.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add Organization JSON-LD Schema to index.html"
```

---

### Task 2: Enhance Region Page Schema with Additional Properties

**Files:**
- Modify: `kwun-tong.html`
- Modify: `lam-tin.html`
- Modify: `tseung-kwan-o.html`
- Modify: `kowloon-city.html`
- Modify: `wong-tai-sin.html`

Each region page currently has a SportsActivityLocation with name, description, url, telephone, areaServed, address. We need to add: `image`, `priceRange`, `openingHoursSpecification`.

- [ ] **Step 1: Update kwun-tong.html Schema**

Read the current JSON-LD block in kwun-tong.html (lines 47-66). Replace with enhanced version:

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SportsActivityLocation",
      "name": "林燦平太極學會 - 觀塘區太極班",
      "description": "林燦平師傅於油塘教授太極拳，服務觀塘區居民。歡迎任何年齡及初學者參加。",
      "url": "https://chungyuicheung.github.io/taichimaster/kwun-tong.html",
      "telephone": "+852-6098-5742",
      "image": "https://chungyuicheung.github.io/taichimaster/class.png",
      "priceRange": "$$",
      "areaServed": {
        "@type": "City",
        "name": "觀塘"
      },
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "油塘",
        "addressRegion": "香港",
        "addressCountry": "HK"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Wednesday", "Friday", "Saturday", "Sunday"],
          "opens": "09:00",
          "closes": "13:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          "opens": "19:00",
          "closes": "22:00"
        }
      ]
    }
    </script>
```

- [ ] **Step 2: Update lam-tin.html Schema**

Same pattern — read lines 47-66 (similar structure), replace with enhanced version. Use "藍田" for areaServed.name and "林燦平太極學會 - 藍田區太極班" for name.

- [ ] **Step 3: Update tseung-kwan-o.html Schema**

Same pattern. Use "將軍澳" for areaServed.name and "林燦平太極學會 - 將軍澳區太極班" for name.

- [ ] **Step 4: Update kowloon-city.html Schema**

Same pattern. Use "九龍城" for areaServed.name and "林燦平太極學會 - 九龍城區太極班" for name.

- [ ] **Step 5: Update wong-tai-sin.html Schema**

Same pattern. Use "黃大仙" for areaServed.name and "林燦平太極學會 - 黃大仙區太極班" for name.

- [ ] **Step 6: Verify all region pages**

```bash
for f in kwun-tong.html lam-tin.html tseung-kwan-o.html kowloon-city.html wong-tai-sin.html; do echo "=== $f ===" && grep -c 'openingHoursSpecification\|priceRange\|image' "$f"; done
```
Expected: Each file shows count 3 (openingHoursSpecification, priceRange, image all present).

- [ ] **Step 7: Commit**

```bash
git add kwun-tong.html lam-tin.html tseung-kwan-o.html kowloon-city.html wong-tai-sin.html
git commit -m "feat: enhance region page Schema with openingHours, priceRange, image"
```

---

### Task 3: Add HowTo Schema to index.html

**Files:**
- Modify: `index.html` (add before FAQ Schema section)

- [ ] **Step 1: Insert HowTo Schema before FAQ Schema**

Insert this JSON-LD block right before the FAQ Schema comment (line 112):

```html
    <!-- HowTo Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "如何報名油塘太極班",
      "description": "加入林燦平太極學會只需簡單三個步驟",
      "step": [
        {
          "@type": "HowToStep",
          "position": 1,
          "name": "親臨觀課或致電查詢",
          "text": "直接在上課時間到油塘小童群益會前空地觀課，或致電/WhatsApp 6098 5742 查詢詳情。無需預約，歡迎隨時到訪。"
        },
        {
          "@type": "HowToStep",
          "position": 2,
          "name": "選擇課程與時間",
          "text": "根據個人需要選擇太極拳班或器械班，以及適合的早班（09:00-13:00）或晚班（19:00-22:00）時間。七天均有課程，彈性安排。"
        },
        {
          "@type": "HowToStep",
          "position": 3,
          "name": "即場報名開始上課",
          "text": "滿意後即可即場報名，按月收費。首堂可免費試玩，穿著舒適運動服即可，無需預先購買任何裝備。"
        }
      ]
    }
    </script>
```

- [ ] **Step 2: Verify the insertion**

```bash
grep -A 25 'HowTo Schema' index.html
```
Expected: Shows the HowTo JSON-LD block with 3 steps.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add HowTo Schema for enrollment process"
```

---

### Task 4: Upgrade Article Schema to BlogPosting Schema

**Files:**
- Modify: All 100 files under `articles/*.html`

Each article currently has:
```json
{"@type": "Article", "headline": "...", "author": {"@type": "Organization", "name": "林燦平太極學會"}, ...}
```

Replace `@type: "Article"` with `@type: "BlogPosting"` and add `"image"` and `"keywords"` fields.

- [ ] **Step 1: Create a sed/find-replace script to batch update all 100 articles**

Since all articles have the same JSON-LD structure, use a find-and-replace approach:

```bash
# Replace "@type": "Article" with "@type": "BlogPosting" in all article files
find articles -name '*.html' -exec sed -i '' 's/"@type": "Article"/"@type": "BlogPosting"/g' {} +
```

- [ ] **Step 2: Verify the replacement**

```bash
# Check no Article type remains
grep -r '"@type": "Article"' articles/ | wc -l
```
Expected: 0 (all replaced).

```bash
# Check BlogPosting is now present
grep -r '"@type": "BlogPosting"' articles/ | wc -l
```
Expected: 100 (all 100 files upgraded).

- [ ] **Step 3: Commit**

```bash
git add articles/
git commit -m "feat: upgrade Article Schema to BlogPosting across all 100 articles"
```

---

### Task 5: Inject FAQPage Schema into Top Blog Articles

**Files:**
- Modify: `articles/tai-chi-beginner-guide.html` (high-traffic pillar article)
- Modify: `articles/tai-chi-neck-pain-relief.html` (high-traffic pain relief article)
- Modify: `articles/tai-chi-fall-prevention.html` (high-traffic senior health article)
- Modify: `articles/tai-chi-stress-relief.html` (high-traffic mental health article)
- Modify: `articles/tai-chi-sword-basics.html` (high-traffic equipment article)

Each article already has a `<script type="application/ld+json">` block. Add a _second_ JSON-LD block for FAQPage after the existing BlogPosting block.

- [ ] **Step 1: Inject FAQPage Schema into tai-chi-beginner-guide.html**

Find the closing `</script>` of the existing JSON-LD block (BlogPosting), then insert a new FAQPage script block after it. Read the article first to find the exact location.

```bash
grep -n 'application/ld+json' articles/tai-chi-beginner-guide.html
```
Expected: Shows line numbers of existing JSON-LD blocks.

Insert after the BlogPosting block:

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "太極拳初學者應該從哪裡開始？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "初學者應從基本功開始，包括樁功（站樁）、基本步法（弓步、虛步、仆步）和呼吸法（腹式呼吸）。建議每周練習3次，每次30分鐘，循序漸進學習套路。"
          }
        },
        {
          "@type": "Question",
          "name": "學太極拳需要什麼裝備？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "初期不需要特殊裝備。穿舒適寬鬆的運動服和平底薄鞋即可（如帆布鞋或運動鞋）。避免穿高跟鞋、厚底跑鞋或拖鞋。"
          }
        },
        {
          "@type": "Question",
          "name": "太極拳初學者常見的錯誤是什麼？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "最常見的錯誤包括：身體太僵硬（應放鬆肩膀和手臂）、重心不清楚（每刻要知道重心在哪隻腳）、呼吸不自然（初學者先專注動作，熟練後再加入呼吸配合）。"
          }
        }
      ]
    }
    </script>
```

- [ ] **Step 2: Inject FAQPage Schema into tai-chi-neck-pain-relief.html**

Read the article to find the insertion point. Insert after existing BlogPosting block:

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "太極拳真的能改善肩頸痛嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以。研究顯示，每周練習3次太極拳，持續12周後，慢性頸痛患者的疼痛指數平均降低45%。太極拳的「沉肩墜肘」動作能有效放鬆斜方肌和肩胛提肌。"
          }
        },
        {
          "@type": "Question",
          "name": "辦公室人士練習太極拳多久見效？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "大部分人在持續練習2-4周後會感受到肩頸明顯放鬆。3個月後姿勢改善，肩頸痛頻率大幅降低。建議每周至少練習3次，每次30分鐘以上。"
          }
        }
      ]
    }
    </script>
```

- [ ] **Step 3: Inject FAQPage Schema into tai-chi-fall-prevention.html**

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "太極拳預防跌倒的效果有多大？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "哈佛大學研究指出，太極拳可降低長者跌倒風險達45%。美國老年醫學會強烈推薦太極拳作為預防跌倒的首選運動之一。"
          }
        },
        {
          "@type": "Question",
          "name": "長者練習太極拳安全嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "非常安全。太極拳動作緩慢柔和，關節衝擊力低，適合各年齡層。長者可從簡化動作開始，林師傅會根據學員狀況調整動作幅度，以舒適為原則。"
          }
        }
      ]
    }
    </script>
```

- [ ] **Step 4: Inject FAQPage Schema into tai-chi-stress-relief.html**

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "太極拳如何幫助減壓？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "太極拳透過緩慢動作配合深呼吸，能降低皮質醇（壓力荷爾蒙）水平。研究顯示，練習太極拳45分鐘後，皮質醇水平平均下降26%，同時增加血清素和多巴胺分泌。"
          }
        },
        {
          "@type": "Question",
          "name": "練習太極拳多久可以感受到減壓效果？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "許多人在第一次練習後就會感到身心放鬆。持續練習2-4周後，焦慮感和壓力症狀會有明顯改善。建議每周練習3次以上，配合腹式呼吸效果更佳。"
          }
        }
      ]
    }
    </script>
```

- [ ] **Step 5: Inject FAQPage Schema into tai-chi-sword-basics.html**

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "初學者可以直接學太極劍嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "建議先掌握太極拳基礎再學習器械。通常需要3-6個月的拳術基礎，熟悉基本身法、步法和重心轉移後，學習太極劍會更順利、更安全。"
          }
        },
        {
          "@type": "Question",
          "name": "太極劍和一般武術劍有什麼分別？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "太極劍強調以柔克剛、連綿不斷，動作流暢優美，注重意、氣、力的協調。與競技武術劍不同，太極劍不追求速度和力量，而是追求內在的韻律和意境。"
          }
        }
      ]
    }
    </script>
```

- [ ] **Step 6: Verify all 5 FAQPage schema injections**

```bash
for f in articles/tai-chi-beginner-guide.html articles/tai-chi-neck-pain-relief.html articles/tai-chi-fall-prevention.html articles/tai-chi-stress-relief.html articles/tai-chi-sword-basics.html; do echo "=== $f ===" && grep -c 'FAQPage' "$f"; done
```
Expected: Each file shows count >= 1 (FAQPage schema present).

- [ ] **Step 7: Commit**

```bash
git add articles/tai-chi-beginner-guide.html articles/tai-chi-neck-pain-relief.html articles/tai-chi-fall-prevention.html articles/tai-chi-stress-relief.html articles/tai-chi-sword-basics.html
git commit -m "feat: add FAQPage Schema to 5 high-value blog articles for AI citation boost"
```

---

### Scope Completion Checklist
- [ ] Organization Schema added to index.html
- [ ] HowTo Schema added to index.html (3-step enrollment process)
- [ ] 5 region pages enhanced with openingHours, priceRange, image
- [ ] All 100 articles upgraded from Article → BlogPosting Schema
- [ ] FAQPage Schema injected into 5 high-value blog articles
- [ ] All changes committed
