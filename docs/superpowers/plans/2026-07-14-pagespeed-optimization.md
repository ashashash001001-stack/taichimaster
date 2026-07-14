# PageSpeed Insights 效能優化實施計劃

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 PageSpeed Performance 分數從 60 提升至 85+，主要解決 Lucide CDN 阻塞、圖片未優化、CSS/JS 阻塞渲染問題

**Architecture:** 靜態 HTML + Tailwind CSS (CDN) + Lucide Icons (CDN) + Vanilla JS。優化策略：移除第三方阻塞資源、轉為本地/內聯、圖片 WebP 化、關鍵 CSS 內聯

**Tech Stack:** HTML5, Tailwind CSS, Lucide Icons (SVG), Vanilla JS, Python (生成腳本)

---

## 📁 檔案變更映射

| 檔案 | 類型 | 責任 |
|------|------|------|
| `index.html` | Modify | 主頁 - Lucide 替換、圖片優化、CSS/JS 優化 |
| `blog.html` | Modify | 博客首頁 - 同步修復 |
| `*.html` (5 region + 100 articles) | Modify | 所有 HTML - 統一 Lucide SVG 替換、圖片 WebP、CSS 優化 |
| `css/tailwind.css` | Create | 本地編譯 Tailwind CSS（替代 CDN） |
| `js/icons.js` | Create | 內聯 SVG 圖標系統（替代 Lucide CDN） |
| `images/*.webp` | Create | 5 張圖片轉 WebP 格式 |
| `generate_icons.py` | Create | Lucide → 內聯 SVG 轉換腳本 |
| `optimize_images.py` | Create | 圖片批量 WebP 轉換腳本 |

---

## 🎯 任務分解

### Task 1: 建立本地 Tailwind CSS（移除 CDN 阻塞）

**Files:**
- Create: `css/tailwind.css`
- Modify: `index.html:222-227`, `blog.html`, all region pages, all article pages

**Steps:**

- [ ] **Step 1: 安裝並編譯 Tailwind**

```bash
# 安裝
npm init -y
npm install -D tailwindcss@latest
npx tailwindcss init
```

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "*.html",
    "articles/*.html",
  ],
  theme: { extend: {} },
  plugins: [],
}
```

```bash
# 編譯生產版本
npx tailwindcss -i ./css/input.css -o ./css/tailwind.css --minify
```

```css
/* css/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 2: 修改 index.html 移除 CDN，改用本地 CSS**

```html
<!-- 刪除以下行 (index.html:222-227) -->
<!-- <link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin> -->
<!-- <link rel="preconnect" href="https://unpkg.com" crossorigin> -->
<!-- <link rel="preload" href="css/tailwind.css" as="style"> -->
<!-- <link rel="stylesheet" href="css/tailwind.css"> -->
<!-- <style> ... </style> -->

<!-- 替換為：關鍵 CSS 內聯 + 非關鍵 CSS 異步載入 -->
<style>
  /* 關鍵 CSS - 首屏必需樣式 (從 tailwind.css 提取關鍵部分) */
  .fixed{position:fixed}.w-full{width:100%}.bg-white\/95{background-color:rgb(255 255 255 / 0.95)}...
  /* 這裡放入首屏渲染必需的 CSS，約 3-5KB */
</style>
<link rel="preload" href="css/tailwind.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="css/tailwind.css"></noscript>
```

- [ ] **Step 3: 同步修改 blog.html、5 個地區頁、100 篇文章**

使用 Python 腳本批量替換（見 Task 5）

- [ ] **Step 4: 驗證無樣式缺失**

```bash
# 本地預覽檢查
python3 -m http.server 8000
# 打開 http://localhost:8000 檢查首屏、導航、Hero、FAQ 等關鍵區塊
```

- [ ] **Step 5: Commit**

```bash
git add css/tailwind.css css/input.css tailwind.config.js index.html blog.html *.html
git commit -m "perf: replace Tailwind CDN with local compiled CSS + critical CSS inline"
```

---

### Task 2: 替換 Lucide CDN 為內聯 SVG 系統（解決 790ms 阻塞）

**Files:**
- Create: `js/icons.js` (SVG 圖標注冊表 + 渲染函數)
- Modify: `index.html:912-916`, all HTML files
- Create: `scripts/generate_icons.py` (提取用到的 Lucide 圖標)

**掃描所有 HTML 找出使用的 Lucide 圖標：**
- `menu`, `x` (導航)
- `phone` (電話)
- `users`, `award`, `map-pin` (信任徽章)
- `chevron-right` × 多處 (課程列表、服務地區)
- `star` (評價)
- `calendar`, `clock` (時間表)
- `arrow-right` (文章卡片、CTA)
- `message-circle` (WhatsApp 浮動按鈕)
- `chevron-up` (返回頂部)
- `chevron-down` (FAQ)
- `map-pin`, `message-circle` (頁尾)

共 **14 個唯一圖標**

- [ ] **Step 1: 建立圖標生成腳本**

```python
# scripts/generate_icons.py
import requests
import re

# Lucide 圖標名稱列表
ICONS = [
    "menu", "x", "phone", "users", "award", "map-pin",
    "chevron-right", "star", "calendar", "clock",
    "arrow-right", "message-circle", "chevron-up", "chevron-down"
]

def fetch_svg(name):
    url = f"https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    # 移除 width/height，添加 class 方便樣式控制
    svg = resp.text
    svg = re.sub(r'<svg([^>]*)>', r'<svg\1 class="lucide lucide-{name}">', svg)
    return svg

# 生成 JS 模組
output = "// Auto-generated from Lucide icons\nconst ICONS = {\n"
for name in ICONS:
    svg = fetch_svg(name)
    # escape for JS string
    svg_js = svg.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    output += f'  "{name}": `{svg_js}`,\n'
output += "};\n\n"
output += """
function createIcon(name, attrs = {}) {
  const svg = ICONS[name];
  if (!svg) return '';
  # 替換 class 支持自定義 class
  return svg.replace('<svg', `<svg ${Object.entries(attrs).map(([k,v])=>`${k}="${v}"`).join(' ')}`);
}

# 替換所有 data-lucide 元素
function initIcons() {
  document.querySelectorAll('[data-lucide]').forEach(el => {
    const name = el.getAttribute('data-lucide');
    const classes = el.className;
    const html = createIcon(name, { class: classes || 'lucide' });
    el.outerHTML = html;
  });
}

# DOM ready 時初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initIcons);
} else {
  initIcons();
}
"""
with open("js/icons.js", "w") as f:
    f.write(output)
print("Generated js/icons.js with", len(ICONS), "icons")
```

- [ ] **Step 2: 運行生成腳本**

```bash
python3 scripts/generate_icons.py
```

- [ ] **Step 3: 修改 index.html 替換 Lucide CDN**

```html
<!-- 刪除 (index.html:912-916) -->
<!-- <script src="https://unpkg.com/lucide@latest"></script> -->
<!-- <script>lucide.createIcons();</script> -->

<!-- 替換為：內聯 SVG 系統 -->
<script src="js/icons.js"></script>
```

- [ ] **Step 4: 同步修改所有 HTML 檔案** (見 Task 5 批量腳本)

- [ ] **Step 5: 驗證圖標正常顯示**

```bash
python3 -m http.server 8000
# 檢查導航選單、所有 chevron-right、星星、WhatsApp 按鈕、返回頂部等
```

- [ ] **Step 6: Commit**

```bash
git add js/icons.js scripts/generate_icons.py index.html blog.html *.html
git commit -m "perf: replace Lucide CDN with inline SVG icon system (saves 790ms blocking)"
```

---

### Task 3: 圖片優化 - WebP 轉換 + width/height + lazy loading 優化

**Files:**
- Create: `images/*.webp` (5 files)
- Modify: `index.html` (5 個 `<img>` 標籤)
- Create: `scripts/optimize_images.py`

**當前圖片：**
| 原文件 | 用途 | 建議尺寸 |
|--------|------|----------|
| `class.png` | Hero 背景 | 1920×1080 → 1200×800 |
| `solo.jpg` | 師傅照片 | 400×300 |
| `class_hall.jpg` | 上課環境 | 800×600 |
| `class_8year.JPG` | 器械班實況 | 800×600 |
| `solo2.jpg` | 師傅示範器械 | 400×300 |

- [ ] **Step 1: 建立批量優化腳本**

```python
# scripts/optimize_images.py
import subprocess
from pathlib import Path

INPUT_DIR = Path(".")
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

SPECS = {
    "class.png": {"width": 1200, "quality": 80},   # Hero 背景
    "solo.jpg": {"width": 400, "quality": 80},     # 師傅照片
    "class_hall.jpg": {"width": 800, "quality": 80}, # 上課環境
    "class_8year.JPG": {"width": 800, "quality": 80}, # 器械班
    "solo2.jpg": {"width": 400, "quality": 80},    # 師傅示範
}

for src_name, spec in SPECS.items():
    src = INPUT_DIR / src_name
    if not src.exists():
        print(f"⚠️  Missing: {src_name}")
        continue
    
    stem = src.stem
    out = OUTPUT_DIR / f"{stem}.webp"
    
    cmd = [
        "magick", str(src),
        "-resize", f"{spec['width']}x>",
        "-quality", str(spec['quality']),
        "-define", "webp:lossless=false",
        str(out)
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        size_kb = out.stat().st_size / 1024
        print(f"✅ {src_name} → {out.name} ({size_kb:.1f} KB)")
    else:
        print(f"❌ {src_name}: {result.stderr.decode()}")
```

- [ ] **Step 2: 安裝 ImageMagick 並運行**

```bash
brew install imagemagick  # macOS
# 或 apt-get install imagemagick

python3 scripts/optimize_images.py
```

- [ ] **Step 3: 更新 index.html 圖片引用**

```html
<!-- Hero 背景 (約第 300 行) -->
<!-- 修改前 -->
<!-- <img src="class_hall.jpg" alt="..." loading="lazy" class="w-full h-full object-cover"> -->

<!-- 修改後 -->
<picture>
  <source srcset="images/class_hall.webp" type="image/webp">
  <img src="images/class_hall.jpg" alt="油塘太極拳入門班上課環境" 
       width="800" height="600" loading="lazy" 
       class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
</picture>

<!-- 課程介紹區 (約第 462 行) -->
<picture>
  <source srcset="images/class_hall.webp" type="image/webp">
  <img src="images/class_hall.jpg" alt="油塘太極拳入門班上課環境" 
       width="800" height="600" loading="lazy" 
       class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
</picture>

<!-- 器械班區 (約第 482 行) -->
<picture>
  <source srcset="images/class_8year.webp" type="image/webp">
  <img src="images/class_8year.JPG" alt="油塘太極器械班學員上課實況" 
       width="800" height="600" loading="lazy" 
       class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
</picture>

<!-- 器械班區第2張 (約第 501 行) -->
<picture>
  <source srcset="images/solo2.webp" type="image/webp">
  <img src="images/solo2.jpg" alt="林燦平師傅示範太極劍與太極扇" 
       width="400" height="300" loading="lazy" 
       class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
</picture>

<!-- 師傅照片在 about 區塊也需更新 -->
```

- [ ] **Step 4: Hero 區背景圖優化 (CSS background-image)**

```html
<!-- 在 <style> 關鍵 CSS 中添加 -->
.hero-bg {
  background-image: url('images/class.webp');
  /* fallback */
  background-image: image-set(
    url('images/class.webp') type('image/webp'),
    url('class.png') type('image/png')
  );
}
```

- [ ] **Step 5: 驗證**

```bash
python3 -m http.server 8000
# 檢查 Network 面板：圖片應為 webp、尺寸正確、有 width/height
# 檢查 CLS：無版面跳動
```

- [ ] **Step 6: Commit**

```bash
git add images/*.webp scripts/optimize_images.py index.html
git commit -m "perf: optimize images to WebP + add width/height for CLS prevention"
```

---

### Task 4: 修復 Accessibility - Heading Order (h4 → h3)

**Files:**
- Modify: `index.html` (學員見證區塊)

**問題位置：** `index.html` 約第 668 行附近，見證卡片標題用了 `h4` 但上層無 `h2/h3`

- [ ] **Step 1: 定位並修復**

```html
<!-- 修改前 (見證卡片 1) -->
<div class="bg-white p-6 rounded-xl shadow-sm border border-stone-200">
  <div class="flex items-center mb-4">
    <div class="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center">
      <i data-lucide="user" class="w-5 h-5 text-emerald-600"></i>
    </div>
    <div class="ml-3">
      <h4 class="font-bold text-gray-900">林小姐 (35歲)</h4>  <!-- 問題在這 -->
      <p class="text-sm text-gray-500">會計師</p>
    </div>
  </div>
  ...
</div>

<!-- 修改後 -->
<div class="bg-white p-6 rounded-xl shadow-sm border border-stone-200">
  <div class="flex items-center mb-4">
    <div class="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center">
      <i data-lucide="user" class="w-5 h-5 text-emerald-600"></i>
    </div>
    <div class="ml-3">
      <h3 class="font-bold text-gray-900">林小姐 (35歲)</h3>  <!-- 改為 h3 -->
      <p class="text-sm text-gray-500">會計師</p>
    </div>
  </div>
  ...
</div>
```

同理修改另外 2 個見證卡片 (`張先生`, `Mike Wong`)

- [ ] **Step 2: 驗證無障礙樹狀結構**

```bash
# 使用 axe-core 或瀏覽器 DevTools Accessibility 面板檢查
npx @axe-core/cli http://localhost:8000
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "a11y: fix heading order in testimonials (h4 -> h3)"
```

---

### Task 5: 批量同步修改所有 HTML 頁面 (5 地區 + 100 文章 + blog + 404)

**Files:**
- Create: `scripts/sync_optimizations.py`
- Modify: `blog.html`, `kwun-tong.html`, `lam-tin.html`, `tseung-kwan-o.html`, `kowloon-city.html`, `wong-tai-sin.html`, `404.html`, `articles/*.html` (100 files)

- [ ] **Step 1: 編寫批量同步腳本**

```python
# scripts/sync_optimizations.py
import re
from pathlib import Path

HTML_FILES = [
    "blog.html", "404.html",
    "kwun-tong.html", "lam-tin.html", 
    "tseung-kwan-o.html", "kowloon-city.html", "wong-tai-sin.html",
] + list(Path("articles").glob("*.html"))

REPLACEMENTS = [
    # 1. 移除 Tailwind CDN preconnect
    (r'<link rel="preconnect" href="https://cdn\.tailwindcss\.com" crossorigin>\s*', ''),
    (r'<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*', ''),
    
    # 2. 替換 CSS 載入方式
    (r'<link rel="preload" href="css/tailwind\.css" as="style">\s*<link rel="stylesheet" href="css/tailwind\.css">', 
     '''<style>
  /* Critical CSS inline - 首屏必需樣式 */
  .fixed{position:fixed}.w-full{width:100%}.bg-white\\/95{background-color:rgb(255 255 255 / 0.95)}.backdrop-blur-sm{backdrop-filter:blur(4px)}.shadow-md{box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1),0 2px 4px -2px rgb(0 0 0 / 0.1)}.z-50{z-index:50}.max-w-6xl{max-width:72rem}.mx-auto{margin-left:auto;margin-right:auto}.px-4{padding-left:1rem;padding-right:1rem}.flex{display:flex}.justify-between{justify-content:space-between}.items-center{align-items:center}.h-20{height:5rem}.flex-shrink-0{flex-shrink:0}.cursor-pointer{cursor:pointer}.text-2xl{font-size:1.5rem}.font-bold{font-weight:700}.text-emerald-800{color:rgb(6 95 70)}.tracking-wider{letter-spacing:0.05em}.border-2{border-width:2px}.border-emerald-800{border-color:rgb(6 95 70)}.p-1{padding:0.25rem}.rounded{border-radius:0.25rem}.ml-3{margin-left:0.75rem}.text-lg{font-size:1.125rem}.font-medium{font-weight:500}.text-gray-600{color:rgb(75 85 99)}.hidden{display:none}.sm\\:block{display:block}.md\\:flex{display:flex}.space-x-8>:not([hidden])~*{margin-left:2rem}.text-gray-600{color:rgb(75 85 99)}.hover\\:text-emerald-700:hover{color:rgb(4 120 87)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.py-2{padding-top:0.5rem;padding-bottom:0.5rem}.bg-emerald-700{background-color:rgb(4 120 87)}.text-white{color:rgb(255 255 255)}.px-5{padding-left:1.25rem;padding-right:1.25rem}.rounded-full{border-radius:9999px}.hover\\:bg-emerald-800:hover{background-color:rgb(6 95 70)}.shadow-lg{box-shadow:0 10px 15px -3px rgb(0 0 0 / 0.1),0 4px 6px -4px rgb(0 0 0 / 0.1)}.pulse-cta{animation:pulse-ring 2s infinite}@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(5,150,105,0.4)}70%{box-shadow:0 0 0 10px rgba(5,150,105,0)}100%{box-shadow:0 0 0 0 rgba(5,150,105,0)}}.md\\:hidden{display:none}.block{display:block}
</style>
<link rel="preload" href="css/tailwind.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="css/tailwind.css"></noscript>'''),

    # 3. 替換 Lucide CDN 為本地
    (r'<script src="https://unpkg\.com/lucide@latest"><\/script>\s*<script>\s*lucide\.createIcons\(\);\s*<\/script>', 
     '<script src="js/icons.js"></script>'),
    
    # 4. 圖片路徑更新 (假設圖片移至 images/ 目錄)
    (r'src="class_hall\.jpg"', 'src="images/class_hall.jpg"'),
    (r'src="class_8year\.JPG"', 'src="images/class_8year.JPG"'),
    (r'src="solo2\.jpg"', 'src="images/solo2.jpg"'),
    (r'src="solo\.jpg"', 'src="images/solo.jpg"'),
    (r'src="class\.png"', 'src="images/class.png"'),
]

for html_file in HTML_FILES:
    content = html_file.read_text(encoding='utf-8')
    original = content
    for pattern, repl in REPLACEMENTS:
        content = re.sub(pattern, repl, content)
    if content != original:
        html_file.write_text(content, encoding='utf-8')
        print(f"✅ Updated: {html_file}")
    else:
        print(f"⏭️  No changes: {html_file}")
```

- [ ] **Step 2: 運行腳本**

```bash
python3 scripts/sync_optimizations.py
```

- [ ] **Step 3: 手動檢查關鍵頁面**

```bash
# 檢查 blog.html、各地區頁、幾篇文章
python3 -m http.server 8000
# 打開 http://localhost:8000/blog.html 等
```

- [ ] **Step 4: Commit**

```bash
git add scripts/sync_optimizations.py blog.html *.html articles/*.html
git commit -m "perf: batch apply CSS/JS/icon optimizations to all pages"
```

---

### Task 6: 效能驗證與回歸測試

**Files:** 無新增檔案，僅驗證

- [ ] **Step 1: 本地 Lighthouse CI**

```bash
# 安裝
npm install -g @lhci/cli

# 建立 lighthouserc.json
cat > lighthouserc.json << 'EOF'
{
  "ci": {
    "collect": {
      "startServerCommand": "python3 -m http.server 8000",
      "url": ["http://localhost:8000/", "http://localhost:8000/blog.html"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.8 }],
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "categories:best-practices": ["error", { "minScore": 0.9 }],
        "categories:seo": ["error", { "minScore": 0.9 }]
      }
    }
  }
}
EOF

# 運行
lhci autorun
```

- [ ] **Step 2: 實測 PageSpeed Insights (部署後)**

```bash
# 部署到 Cloudflare Pages 後
# 訪問 https://pagespeed.web.dev/analysis/https-<your-domain>/
# 確認 Performance ≥ 85
```

- [ ] **Step 3: 核心指標檢查清單**

| 指標 | 目標 | 驗證方式 |
|------|------|----------|
| Performance Score | ≥ 85 | Lighthouse |
| LCP | < 2.5s | Lighthouse / Web Vitals |
| CLS | < 0.1 | Lighthouse / Layout Shift |
| TBT | < 200ms | Lighthouse |
| 無阻塞 JS | 0 | Network 面板 |
| 圖片 WebP | 100% | Network 面板 |
| 圖片 width/height | 100% | Elements 面板 |

- [ ] **Step 4: 功能回歸測試**

```bash
# 核心功能清單
□ 導航選單開關 (手機/桌面)
□ 平滑滾動錨點
□ FAQ 手風琴展開/關閉
□ 時間表篩選 (全部/早上/晚上)
□ 返回頂部按鈕
□ 滾動導航高亮
□ WhatsApp 浮動按鈕 hover 展開
□ 表單提交 → WhatsApp 跳轉
□ 所有 Lucide 圖標正常顯示
□ 深色模式正常
□ 響應式斷點正常
```

- [ ] **Step 5: Final Commit**

```bash
git add lighthouserc.json
git commit -m "ci: add Lighthouse CI config for performance regression testing"
```

---

## 📦 執行總覽

| 任務 | 預估時間 | 影響分數 | 優先級 |
|------|---------|---------|--------|
| Task 1: 本地 Tailwind + 關鍵 CSS | 30 min | +10-15 | 🔴 P0 |
| Task 2: Lucide → 內聯 SVG | 45 min | +15-20 | 🔴 P0 |
| Task 3: 圖片 WebP + width/height | 30 min | +5-10 | 🔴 P0 |
| Task 4: Heading Order 修復 | 10 min | +2 (a11y) | 🟡 P1 |
| Task 5: 批量同步所有頁面 | 20 min | 全站一致性 | 🔴 P0 |
| Task 6: 效能驗證 | 20 min | 驗收 | 🔴 P0 |

**總計：~2.5 小時**

---

## ✅ 驗收標準

部署後在 PageSpeed Insights 重測，需達到：

- [ ] **Performance ≥ 85** (現 60)
- [ ] **Accessibility ≥ 93** (現 93，不可倒退)
- [ ] **Best Practices = 100** (現 100)
- [ ] **SEO = 100** (現 100)
- [ ] **LCP < 2.5s**
- [ ] **CLS < 0.1**
- [ ] **無第三方阻塞資源** (Network 面板確認)
- [ ] **所有功能正常** (回歸測試通過)