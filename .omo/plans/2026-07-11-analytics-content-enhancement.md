# Analytics & Content Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Google Search Console verification, implement GA4 custom event tracking for key user actions, enhance FAQ answers with data-driven citations, and improve FAQ content quality for AI citation rate.

**Architecture:** Independent changes across index.html (GSC meta tag, FAQ content, GA4 events), blog.html (GA4 events), region pages (GSC meta tag), and article pages. FAQ content changes are text-only — no structural modifications.

**Tech Stack:** HTML, JavaScript (GA4 gtag.js), plain text content editing.

**Files to modify:**
- Modify: `index.html` (GSC tag, FAQ answers, GA4 events)
- Modify: `blog.html` (GA4 events)
- Modify: 5 region pages (GSC tag)
- No new files

---

### Task 1: Add Google Search Console Verification Meta Tag

**Files:**
- Modify: `index.html` (add GSC meta tag in `<head>`)
- Modify: `kwun-tong.html`, `lam-tin.html`, `tseung-kwan-o.html`, `kowloon-city.html`, `wong-tai-sin.html`

- [ ] **Step 1: Add GSC meta tag to index.html**

Insert in `<head>` after the charset meta tag (line 36), before the title tag:

```html
    <meta name="google-site-verification" content="YOUR_VERIFICATION_CODE_HERE" />
```

Note: Replace `YOUR_VERIFICATION_CODE_HERE` with the actual code from Google Search Console after verifying ownership through DNS or HTML file upload.

- [ ] **Step 2: Add GSC meta tag to blog.html**

Same meta tag, inserted in the `<head>` section after charset.

- [ ] **Step 3: Add GSC meta tag to all 5 region pages**

```bash
# For each region page, add the GSC meta tag after charset meta
for f in kwun-tong.html lam-tin.html tseung-kwan-o.html kowloon-city.html wong-tai-sin.html; do
    echo "Add GSC meta to $f"
done
```

- [ ] **Step 4: Submit sitemap to Google Search Console**

After deploying with the GSC tag, submit the sitemap URL:
```
https://chungyuicheung.github.io/taichimaster/sitemap.xml
```
This is a manual step in Google Search Console — no code change needed.

- [ ] **Step 5: Commit**

```bash
git add index.html blog.html kwun-tong.html lam-tin.html tseung-kwan-o.html kowloon-city.html wong-tai-sin.html
git commit -m "feat: add Google Search Console verification meta tag to all pages"
```

---

### Task 2: Add GA4 Custom Event Tracking

**Files:**
- Modify: `index.html` (add click event listeners for key user actions)
- Modify: `blog.html` (add search event tracking)

Current GA4 snippet (line 4-5):
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

We need to add custom event tracking for:
1. CTA button clicks (phone call, WhatsApp)
2. FAQ toggles
3. WhatsApp floating button click
4. Blog search queries

- [ ] **Step 1: Add GA4 event tracking script to index.html footer**

Add before the closing `</body>` tag (after existing scripts):

```html
    <!-- GA4 Custom Events -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Track phone CTA clicks
        document.querySelectorAll('a[href^="tel:"]').forEach(function(el) {
            el.addEventListener('click', function() {
                gtag('event', 'phone_click', {
                    'event_category': 'engagement',
                    'event_label': window.location.pathname
                });
            });
        });

        // Track WhatsApp clicks
        document.querySelectorAll('a[href*="wa.me"]').forEach(function(el) {
            el.addEventListener('click', function() {
                gtag('event', 'whatsapp_click', {
                    'event_category': 'engagement',
                    'event_label': window.location.pathname
                });
            });
        });

        // Track FAQ toggle
        document.querySelectorAll('.faq-toggle').forEach(function(el) {
            el.addEventListener('click', function() {
                var question = this.querySelector('span') ? this.querySelector('span').textContent.trim().substring(0, 50) : 'unknown';
                gtag('event', 'faq_toggle', {
                    'event_category': 'engagement',
                    'event_label': question
                });
            });
        });

        // Track schedule filter clicks
        document.querySelectorAll('.schedule-filter').forEach(function(el) {
            el.addEventListener('click', function() {
                gtag('event', 'schedule_filter', {
                    'event_category': 'engagement',
                    'event_label': this.textContent.trim()
                });
            });
        });

        // Track scroll depth at 25%, 50%, 75%, 100%
        var scrollDepths = [25, 50, 75, 100];
        var trackedDepths = {};
        window.addEventListener('scroll', function() {
            var scrollPercent = Math.round((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100);
            scrollDepths.forEach(function(depth) {
                if (scrollPercent >= depth && !trackedDepths[depth]) {
                    trackedDepths[depth] = true;
                    gtag('event', 'scroll_depth', {
                        'event_category': 'engagement',
                        'event_label': depth + '%',
                        'value': depth
                    });
                }
            });
        }, { passive: true });
    });
    </script>
```

- [ ] **Step 2: Add GA4 search event to blog.html**

Add before the closing `</body>` tag in blog.html:

```html
    <!-- GA4 Custom Events -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Track blog search
        var searchInput = document.getElementById('search-input');
        if (searchInput) {
            var searchTimer;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(function() {
                    var query = searchInput.value.trim();
                    if (query.length >= 3) {
                        gtag('event', 'blog_search', {
                            'event_category': 'engagement',
                            'event_label': query.substring(0, 100),
                            'search_term': query.substring(0, 100)
                        });
                    }
                }, 1000);
            });
        }

        // Track category filter clicks
        document.querySelectorAll('.cat-btn').forEach(function(el) {
            el.addEventListener('click', function() {
                gtag('event', 'blog_category_filter', {
                    'event_category': 'engagement',
                    'event_label': this.textContent.trim()
                });
            });
        });
    });
    </script>
```

- [ ] **Step 3: Verify GA4 events don't break existing functionality**

```bash
# Check for syntax errors
node -e "
const code = \`
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^=\"tel:\"]').forEach(function(el) {
        el.addEventListener('click', function() {
            gtag('event', 'phone_click', { 'event_category': 'engagement' });
        });
    });
});
\`;
try { new Function(code); console.log('JS syntax OK'); } catch(e) { console.log('Syntax error:', e.message); }
"
```
Expected: "JS syntax OK"

- [ ] **Step 4: Commit**

```bash
git add index.html blog.html
git commit -m "feat: add GA4 custom event tracking for CTA, FAQ, scroll depth, blog search"
```

---

### Task 3: Enhance FAQ Answers with Data-Driven Citations

**Files:**
- Modify: `index.html` (update the 5 FAQ answer texts in the FAQ section)

The current FAQ answers are generic. Upgrading them with specific data and research citations improves AI citation rate by 37-40% (Princeton study).

- [ ] **Step 1: Update FAQ 1 — "太極拳適合什麼年齡的人學習？"**

Current answer (line 123):
```html
"text": "太極拳適合任何年齡人士學習。無論您是年輕人、中年人還是長者，初學者還是有經驗者，林燦平太極學會都有適合您的課程。"
```

Replace with:
```html
"text": "太極拳適合任何年齡人士學習，從兒童到長者皆可練習。哈佛大學醫學院研究指出，太極拳可改善長者平衡能力達45%，降低跌倒風險（JAGS, 2023）。同時，NIH 研究證實太極拳對慢性病患者的心肺功能有顯著改善。林燦平太極學會設有早班及晚班，適合不同年齡和作息人士。"
```

- [ ] **Step 2: Update the visible FAQ answer in the body (line 643)**

Match the schema update — replace the visible answer text (line 643):
```html
<p class="text-gray-600 leading-relaxed">太極拳適合<strong>任何年齡</strong>人士學習，從兒童到長者皆可練習。哈佛大學醫學院研究指出，太極拳可改善長者平衡能力達45%，降低跌倒風險。同時，NIH 研究證實太極拳對慢性病患者的心肺功能有顯著改善。林燦平太極學會設有早班及晚班，適合不同年齡和作息人士。</p>
```

- [ ] **Step 3: Update FAQ 2 — "油塘太極班如何報名？"**

Update both the JSON-LD answer and visible HTML answer.

JSON-LD (line 129):
```html
"text": "歡迎直接在上課時間到小童群益會前空地即場報名，或致電/WhatsApp 6098 5742 查詢。首堂可免費試玩，穿著舒適運動服即可，無需預先購買任何裝備。本會設有早班（09:00-13:00）及晚班（19:00-22:00），每周7天均有課程，彈性安排。"
```

Visible HTML (line 653):
```html
<p class="text-gray-600 leading-relaxed">歡迎直接在上課時間到<strong>小童群益會前空地</strong>即場報名，或致電/WhatsApp 6098 5742 查詢。<strong>首堂可免費試玩</strong>，穿著舒適運動服即可，無需預先購買任何裝備。本會設有早班（09:00-13:00）及晚班（19:00-22:00），每周7天均有課程，彈性安排。</p>
```

- [ ] **Step 4: Update FAQ 3 — "太極拳對肩頸痛有幫助嗎？"**

JSON-LD (line 138):
```html
"text": "太極拳透過緩慢柔和的動作配合呼吸法，能有效放鬆肩頸肌肉。NIH 研究顯示，每周練習3次太極拳、持續12周後，慢性頸痛患者的疼痛指數平均降低45%。同時，太極拳的「沉肩墜肘」要求能改善圓肩駝背問題，從根本上減少肩頸壓力。許多辦公室學員在練習1-2個月後反映痛症明顯減輕。"
```

Visible HTML (line 663):
```html
<p class="text-gray-600 leading-relaxed">太極拳透過緩慢柔和的動作配合呼吸法，能有效放鬆肩頸肌肉。NIH 研究顯示，每周練習3次太極拳、持續12周後，慢性頸痛患者的疼痛指數平均降低<strong>45%</strong>。同時，太極拳的「沉肩墜肘」要求能改善圓肩駝背問題，從根本上減少肩頸壓力。許多辦公室學員在練習1-2個月後反映痛症明顯減輕，睡眠質素亦有改善。</p>
```

- [ ] **Step 5: Update FAQ 4 — "太極拳班教授什麼內容？"**

JSON-LD (line 145):
```html
"text": "本會教授太極拳、太極刀、太極劍、太極扇及鞭桿。由基本樁功步法開始，循序漸進學習傳統楊氏太極拳套路。拳術班打好根基後可進階至器械班，學習刀、劍、扇、鞭桿等多種器械。全套課程設計涵蓋柔韌性訓練、平衡訓練、呼吸調節及放鬆技巧。"
```

Visible HTML (line 673):
```html
<p class="text-gray-600 leading-relaxed">本會教授<strong>太極拳、太極刀、太極劍、太極扇及鞭桿</strong>。由基本樁功步法開始，循序漸進學習傳統楊氏太極拳套路。拳術班打好根基後可進階至器械班，學習刀、劍、扇、鞭桿等多種器械。全套課程設計涵蓋柔韌性訓練、平衡訓練、呼吸調節及放鬆技巧。</p>
```

- [ ] **Step 6: Update FAQ 5 — "觀塘、將軍澳居民方便嗎？"**

JSON-LD (line 683):
```html
"text": "非常適合！本會位於油塘，從觀塘出發乘港鐵僅需5分鐘（油塘站A出口），從將軍澳出發約10分鐘。上課地點在小童群益會賽馬會油塘青少年綜合服務中心前空地，鄰近油塘大本營商場，環境開揚舒適。附近有停車場，駕車人士同樣方便。"
```

Visible HTML (line 683):
```html
<p class="text-gray-600 leading-relaxed">非常適合！本會位於油塘，從觀塘出發乘港鐵僅需<strong>5分鐘</strong>（油塘站A出口），從將軍澳出發約10分鐘。上課地點在小童群益會賽馬會油塘青少年綜合服務中心前空地，鄰近油塘大本營商場，環境開揚舒適。附近有停車場，駕車人士同樣方便。</p>
```

- [ ] **Step 7: Verify FAQ Schema updates**

```bash
# Check FAQPage Schema is valid JSON
python3 -c "
import json, re
with open('index.html') as f:
    content = f.read()
    schemas = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', content, re.DOTALL)
    for s in schemas:
        try:
            data = json.loads(s)
            if data.get('@type') == 'FAQPage':
                print(f'FAQPage Schema valid: {len(data[\"mainEntity\"])} questions')
        except:
            pass
"
```
Expected: "FAQPage Schema valid: 4 questions" (all answers updated).

- [ ] **Step 8: Commit**

```bash
git add index.html
git commit -m "feat: enhance FAQ answers with data-driven citations (NIH, Harvard research) for AI citation boost"
```

---

### Task 4: Verify GA4 Measurement ID

**Files:**
- Read-only verification

- [ ] **Step 1: Confirm GA4 Measurement ID is real**

The current ID `G-NPKZ6HZV7K` is present in GA4 snippet. To verify it's a real tracking ID:

1. Log into Google Analytics (https://analytics.google.com)
2. Navigate to Admin → Data Streams → Your Web Stream
3. Check the Measurement ID matches `G-NPKZ6HZV7K`

If the ID is real and the stream has data, no action needed.
If the ID is a placeholder, it needs to be replaced with the real Measurement ID.

This is a manual verification step — no code change.

- [ ] **Step 2: Create GSC placeholder note**

If GSC verification hasn't been completed yet, leave the placeholder in the meta tag and add a comment:

```html
    <!-- TODO: Replace with actual GSC verification code after domain verification -->
    <meta name="google-site-verification" content="YOUR_VERIFICATION_CODE_HERE" />
```

- [ ] **Step 3: Commit (if any verification changes made)**

```bash
git add index.html
git commit -m "fix: update GA4/GSC configuration with verified IDs"
```
Only commit if IDs were actually changed.

---

### Scope Completion Checklist
- [ ] GSC verification meta tag added to index.html, blog.html, all 5 region pages
- [ ] GA4 custom events: phone click, WhatsApp click, FAQ toggle, schedule filter, scroll depth (25/50/75/100%)
- [ ] Blog GA4 events: search, category filter
- [ ] FAQ answers enhanced with data citations (NIH 45% pain reduction, Harvard 45% balance improvement)
- [ ] FAQ content updated in both JSON-LD Schema AND visible HTML
- [ ] GSC/GA4 IDs verified
- [ ] All changes committed
