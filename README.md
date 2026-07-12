# 林燦平太極學會

> 油塘太極班招生 | 教授太極拳、刀、劍、扇、鞭桿 | 歡迎任何年齡及初學者

**Live Site**: https://lamtaichi.pages.dev/

---

## 目錄

- [關於](#關於)
- [網站功能](#網站功能)
- [SEO 架構](#seo-架構)
- [內容策略](#內容策略)
- [專案結構](#專案結構)
- [技術棧](#技術棧)
- [部署方式](#部署方式)
- [內容生成工具](#內容生成工具)
- [SEO 檢查清單](#seo-檢查清單)
- [未來規劃](#未來規劃)

---

## 關於

**林燦平太極學會** 是位於香港油塘的太極拳教學機構，由林燦平師傅主理。網站為純靜態 HTML 單頁應用，旨在透過完善的 SEO 策略和內容架構，將線上流量轉化為實體課程的真實學生。

### 課程資訊

| 項目 | 詳情 |
|---|---|
| **師傅** | 林燦平（30+ 年習武經驗） |
| **流派** | 楊氏太極拳 |
| **地點** | 小童群益會賽馬會油塘青少年綜合服務中心前空地 |
| **教授項目** | 太極拳、太極刀、太極劍、太極扇、鞭桿 |
| **適合對象** | 任何年齡、初學者至進階 |
| **報名方式** | 即場報名 / WhatsApp 6098 5742 / 致電查詢 |

### 上課時間

| 日期 | 早班 | 晚班 |
|---|---|---|
| 星期一、三、五、六、日 | 09:00 - 13:00 | 19:00 - 22:00 |
| 星期二、四 | 10:00 - 13:00 | 19:00 - 22:00 |

---

## 網站功能

### 首頁 (index.html)

| Section | 功能 |
|---|---|
| **Hero** | 全螢幕背景圖、招生標題、雙 CTA（致電 / 查看時間） |
| **關於師傅** | 師傅照片、30+ 年經驗徽章、課程特色 |
| **信任徽章** | 30+ 年經驗 / 200+ 學員 / 7 天課程 / 5 星滿意度 |
| **太極益處** | 三大益處卡片（全面鍛鍊、舒緩壓力、適合任何年齡） |
| **課程介紹** | 三張課程卡片（太極拳班、太極器械班、報名查詢） |
| **收費詳情** | 拳術班 / 器械班收費資訊 + WhatsApp 查詢 CTA |
| **上課地點** | 詳細地址、動態時間表過濾（全部/早上班/晚上班）、Google Maps 嵌入 |
| **學員見證** | 三位學員真實分享（會計師、退休人士、IT 從業員） |
| **常見問題** | 手風琴折疊 FAQ（5 題），每題附「閱讀更多」連結到博客文章 |
| **服務地區** | 5 張地區登陸頁連結（觀塘、藍田、將軍澳、九龍城、黃大仙） |
| **養生專欄精選** | 3 篇精選博客文章推薦 + 「查看更多」按鈕 |
| **頁尾 CTA** | 聯絡資訊 + WhatsApp 查詢表單（提交後跳轉 WhatsApp） |
| **浮動 WhatsApp** | 右下角固定按鈕，hover 展開文字 |

### 博客系統 (blog.html)

- **100 篇文章**，8 大分類
- **全文搜尋**：即時搜尋標題、摘要、標籤
- **分類篩選**：8 個分類按鈕，顯示文章數量
- **排序功能**：最受歡迎 / 最新 / A-Z
- **標籤點擊**：點擊文章標籤即時篩選

### 文章頁面 (articles/*.html)

每篇文章包含：
- 麵包屑導航（首頁 > 養生專欄 > 分類 > 文章）
- 分類標籤 + 關鍵字標籤
- 社交分享按鈕（WhatsApp / Facebook / 複製連結）
- H2/H3 結構化標題
- 列表或表格（Featured Snippet 優化）
- 「林師傅點評」第一人稱教學實例模組
- 3 篇相關文章推薦
- WhatsApp 查詢 CTA

### 地區登陸頁 (5 張)

針對不同地區的 Programmatic SEO 登陸頁：
- `kwun-tong.html` — 觀塘太極班
- `lam-tin.html` — 藍田太極班
- `tseung-kwan-o.html` — 將軍澳太極班
- `kowloon-city.html` — 九龍城太極班
- `wong-tai-sin.html` — 黃大仙太極班

每張頁面包含：地區優化標題、交通指引、地區常見問題、地區間互相連結。

### 404 頁面 (404.html)

自訂錯誤頁，包含熱門文章推薦和地區連結，減少跳出率。

---

## SEO 架構

### On-Page SEO

| 元素 | 實作 |
|---|---|
| **Meta Title** | 含地區、服務、痛點關鍵字（< 60 字元） |
| **Meta Description** | 含地點、服務、CTA、WhatsApp 號碼 |
| **Meta Keywords** | 12 個目標關鍵字 |
| **Canonical URL** | 所有頁面設定 |
| **Open Graph** | Facebook 分享優化（title, description, image, locale） |
| **Twitter Cards** | Twitter 分享優化 |
| **Robots Meta** | index, follow |
| **圖片 Alt** | 所有圖片含關鍵字描述 |

### Schema Markup (JSON-LD)

| Schema 類型 | 位置 | 內容 |
|---|---|---|
| **SportsActivityLocation** | index.html | 名稱、電話、地址、經緯度、營業時間、價格範圍 |
| **FAQPage** | index.html | 4 個常見問題及答案 |
| **Article** | 每篇文章 | 標題、作者、發佈日期、修改日期 |
| **BreadcrumbList** | 每篇文章 | 4 層麵包屑結構 |
| **LocalBusiness** | index.html | AggregateRating + 3 個 Review |
| **LocalBusiness** | 地區頁 | 含 serviceArea 字段 |

### 動態 URL 系統

所有頁面在 `<head>` 最頂部注入動態腳本，頁面載入時自動替換：
- canonical URL → `window.location.origin + pathname`
- og:url → 當前頁面 URL
- og:image / twitter:image → 當前域名 + `/class.png`
- 所有 JSON-LD Schema 內的 URL → 當前域名

確保部署到任何域名時，分享連結和 SEO 標籤都正確。

### 內部連結網絡

```
index.html ──→ 5 張地區頁 + 6 篇精選文章 + Benefits 區 3 篇文章連結
    │
    ├──→ blog.html ──→ 100 篇文章
    │       │
    │       └──→ 5 張地區頁（頁尾）
    │
    └──→ 404.html ──→ 6 篇熱門文章 + 5 張地區頁

每篇文章 ──→ ../index.html + ../blog.html + 3 篇相關文章
地區頁 ──→ 互相連結 (4/4) + index.html + blog.html
```

**零孤立頁面** — 每個頁面至少有 3 個入站連結。

### Sitemap & Robots

- **sitemap.xml**: 108 個 URL（1 首頁 + 1 博客 + 1 404 + 5 地區 + 100 文章）
- **robots.txt**: 允許所有爬蟲，指向 sitemap.xml

---

## 內容策略

### 文章分類（100 篇）

| 分類 | 文章數 | 類型 | 平均字數 |
|---|---|---|---|
| 太極入門 | 13 | 4 Pillar + 9 Cluster | ~1,600 |
| 肩頸腰背 | 13 | 1 Pillar + 12 Cluster | ~1,450 |
| 長者健康 | 13 | 1 Pillar + 12 Cluster | ~1,450 |
| 心理健康 | 12 | 2 Pillar + 10 Cluster | ~1,450 |
| 器械教學 | 13 | 2 Pillar + 11 Cluster | ~1,450 |
| 養生氣功 | 12 | 2 Pillar + 10 Cluster | ~1,450 |
| 太極文化 | 12 | 3 Pillar + 9 Cluster | ~1,500 |
| 學員故事 | 12 | 0 Pillar + 12 Cluster | ~1,400 |

### Pillar vs Cluster

| 類型 | 字數目標 | 目的 | 數量 |
|---|---|---|---|
| **Pillar Content** | 1,500 - 2,500 字 | 建立網域權威，涵蓋廣泛主題 | 18 篇 |
| **Cluster Content** | 800 - 1,200 字 | 解答特定長尾關鍵字問題 | 82 篇 |

### SEO 內容黃金規則

1. **結構化語法**：H1 → H2 → H3 層級分明，每篇包含列表或表格
2. **語義實體 (Entity-Based SEO)**：每類文章融入 10 個 LSI 關鍵字
3. **E-E-A-T**：每篇固定「林師傅點評」第一人稱教學實例模組
4. **內部連結閉環**：Cluster → Pillar → 首頁 CTA
5. **Featured Snippet 優化**：列表和表格結構，增加被選為精選摘要的機率

---

## 專案結構

```
taichimaster/
├── index.html                  # 首頁（677+ 行，12 個 section）
├── blog.html                   # 博客索引（搜尋 + 分類 + 排序）
├── 404.html                    # 自訂錯誤頁
├── sitemap.xml                 # 108 個 URL 索引
├── robots.txt                  # 爬蟲控制
├── favicon.png                 # 網站圖標（32x32）
├── apple-touch-icon.png        # iOS 觸摸圖標（180x180）
│
├── 地區登陸頁 (5)
│   ├── kwun-tong.html          # 觀塘太極班
│   ├── lam-tin.html            # 藍田太極班
│   ├── tseung-kwan-o.html      # 將軍澳太極班
│   ├── kowloon-city.html       # 九龍城太極班
│   └── wong-tai-sin.html       # 黃大仙太極班
│
├── articles/                   # 100 篇博客文章
│   ├── tai-chi-beginner-guide.html
│   ├── tai-chi-neck-pain-relief.html
│   ├── ... (共 100 篇)
│   └── student-story-transformation.html
│
├── 圖片 (5)
│   ├── class.png               # Hero 背景圖
│   ├── solo.jpg                # 師傅照片
│   ├── class_hall.jpg          # 上課環境
│   ├── class_8year.JPG         # 器械班上課實況
│   └── solo2.jpg               # 師傅示範器械
│
├── 生成工具 (5)
│   ├── generate_blog.py        # 100 篇文章 + blog.html 生成器
│   ├── gen_regions.py          # 5 張地區登陸頁生成器
│   ├── upgrade_content.py      # 內容結構升級工具
│   ├── fix_duplicates.py       # 消除重複內容工具
│   └── fix_meta_descriptions.py # 擴展 meta description 至 60-80 字
│
├── .article_classification.json # Pillar/Cluster 分類配置
├── opencode.jsonc              # OpenCode 配置
└── README.md                   # 本文件
```

---

## 技術棧

| 技術 | 用途 |
|---|---|
| **HTML5** | 語義化結構（nav, header, section, article, footer） |
| **Tailwind CSS (CDN)** | 響應式樣式設計 |
| **Lucide Icons (CDN)** | 矢量圖標 |
| **Vanilla JavaScript** | 手機選單、手風琴 FAQ、時間表過濾、Intersection Observer 動畫、滾動高亮、返回頂部、分享按鈕、動態 URL 替換 |
| **Python 3** | 內容生成工具 |
| **Cloudflare Pages** | 靜態網站託管 |

### 前端互動功能

| 功能 | 技術 |
|---|---|
| 手機版選單 | 純 JS toggle |
| 手風琴 FAQ | CSS max-height transition + JS |
| 時間表過濾 | JS data-filter 屬性切換 |
| 滾動淡入動畫 | Intersection Observer API |
| 導航滾動高亮 | Intersection Observer (scroll spy) |
| 返回頂部按鈕 | scroll event + smooth scroll |
| CTA Pulse 動畫 | CSS @keyframes |
| 分享按鈕 | 動態 URL + Clipboard API |
| 博客搜尋 | 即時 JavaScript 過濾 |
| 博客排序 | 按 viewWeight / ID / 字母排序 |
| 動態 URL 替換 | IIFE 在 `<head>` 最早執行 |

---

## 部署方式

### Cloudflare Pages（目前）

網站已部署至 Cloudflare Pages，自動從 `main` 分支部署：

```
https://lamtaichi.pages.dev/
```

### 自訂域名

網站支援任何域名部署。所有 URL 在頁面載入時動態替換為當前域名，包括：
- canonical URL
- Open Graph URL
- 圖片 URL
- 所有 JSON-LD Schema URL

部署到其他域名時，只需：
1. 將檔案上傳到新域名的伺服器
2. 更新 DNS 設定
3. 無需修改任何 HTML 內容

### 本地開發

```bash
# 克隆專案
git clone https://github.com/ashashash001001-stack/taichimaster.git
cd taichimaster

# 本地預覽（任何 HTTP 伺服器）
python3 -m http.server 8000
# 訪問 http://localhost:8000
```

---

## 內容生成工具

### generate_blog.py

生成 100 篇博客文章和 blog.html 索引頁。

```bash
python3 generate_blog.py
```

**輸出**：
- `articles/*.html` — 100 篇獨立文章
- `blog.html` — 博客索引頁（含搜尋、分類、排序）

### gen_regions.py

生成 5 張地區登陸頁。

```bash
python3 gen_regions.py
```

**輸出**：
- `kwun-tong.html`, `lam-tin.html`, `tseung-kwan-o.html`, `kowloon-city.html`, `wong-tai-sin.html`

### upgrade_content.py

將現有文章升級為 SEO 最佳實踐結構（H2/H3、列表、表格、林師傅點評）。

```bash
python3 upgrade_content.py
```

### fix_duplicates.py

消除模板生成的重複 H2 內容，為每篇文章生成獨一無二的描述。

```bash
python3 fix_duplicates.py
```

### fix_meta_descriptions.py

將所有 100 篇文章的 meta description 擴展至 60-80 中文字元，確保每篇文章都有獨特、相關的描述。

```bash
python3 fix_meta_descriptions.py
```

---

## 變現

### Google AdSense

網站已部署 `ads.txt` 檔案，支援 Google AdSense 廣告變現。

---

## SEO 檢查清單

### 已完成 ✅

- [x] Meta Title（含地區、服務、痛點，< 60 字元）
- [x] Meta Description（含地點、服務、CTA，60-80 中文字元）
- [x] Meta Keywords（12 個關鍵字）
- [x] Canonical URL（所有頁面）
- [x] Open Graph 標籤（Facebook 分享）
- [x] Twitter Card 標籤
- [x] Robots meta（index, follow）
- [x] LocalBusiness Schema（SportsActivityLocation）
- [x] FAQPage Schema（4 個問題）
- [x] Article Schema（100 篇文章）
- [x] BreadcrumbList Schema（100 篇文章）
- [x] Review Schema（3 個學員見證 + AggregateRating）
- [x] 圖片 Alt 標籤（5 張圖片，關鍵字優化）
- [x] WhatsApp 預填訊息連結
- [x] 地區關鍵字植入（油塘、觀塘、將軍澳、東九龍）
- [x] sitemap.xml（108 個 URL）
- [x] robots.txt
- [x] 404 自訂錯誤頁
- [x] Favicon + Apple Touch Icon
- [x] 圖片 lazy loading
- [x] 5 張地區登陸頁（Programmatic SEO）
- [x] 100 篇博客文章（8 分類，Pillar + Cluster）
- [x] 手風琴 FAQ
- [x] 動態時間表過濾
- [x] Intersection Observer 微互動
- [x] 收費資訊區塊
- [x] 信任徽章區塊
- [x] 頁尾表單 → WhatsApp 跳轉
- [x] 導航滾動高亮 + 返回頂部
- [x] 精選文章推薦
- [x] 社交分享按鈕（WhatsApp/Facebook/複製）
- [x] 麵包屑導航（100 篇文章）
- [x] 相關文章推薦（100 篇文章）
- [x] 內部連結網絡（零孤立頁面）
- [x] 動態 URL 系統（多域名支援）
- [x] GA4 追蹤代碼（placeholder）
- [x] GSC 驗證準備（placeholder）
- [x] Copyright 2026

### 待完成（需手動操作）

- [ ] **Google Analytics 4** — 替換 `G-XXXXXXXXXX` 為真實 Measurement ID
- [ ] **Google Search Console** — 加入驗證 meta tag 並提交 sitemap
- [ ] **Google Business Profile** — 註冊商家檔案
- [ ] **圖片 WebP 轉換** — 將 5 張原始圖片轉換為 WebP 格式
- [ ] **真實收費資訊** — 替換「歡迎查詢」為實際價格

---

## 未來規劃

### Phase 1 — 基礎優化（已完成）
- 技術 SEO 基礎設施
- 內容架構（100 篇文章）
- UX/UI 重構
- 內部連結網絡

### Phase 2 — 外部 SEO
- Google Business Profile 註冊和優化
- Google Reviews 累積策略
- 外部連結建設（本地目錄、媒體報導）

### Phase 3 — 內容擴展
- 新增「太極與都市病」系列文章
- 影片內容（YouTube 嵌入）
- 學員見證影片

### Phase 4 — 進階功能
- 線上報名表單
- 課程預約系統
- 學員進度追蹤

---

## 授權

© 2026 林燦平太極學會. All Rights Reserved.
