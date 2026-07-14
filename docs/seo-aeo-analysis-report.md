# HEIC Converter — SEO & AI/AEO 完整分析報告

> 分析日期：2026-07-11
> 分析對象：https://heicconverter.com（Next.js 14 靜態網站）

---

## 目錄

1. [技術 SEO 基礎架構](#1-技術-seo-基礎架構)
2. [On-Page SEO](#2-on-page-seo)
3. [結構化資料 (JSON-LD Schema)](#3-結構化資料-json-ld-schema)
4. [國際化 SEO (i18n + hreflang)](#4-國際化-seo-i18n--hreflang)
5. [AI / AEO (Answer Engine Optimization)](#5-ai--aeo-answer-engine-optimization)
6. [內容策略與主題集群](#6-內容策略與主題集群)
7. [效能與技術 SEO](#7-效能與技術-seo)
8. [PWA 與使用者體驗](#8-pwa-與使用者體驗)
9. [分析與監控](#9-分析與監控)
10. [可複製的 SEO 行動清單](#10-可複製的-seo-行動清單)

---

## 1. 技術 SEO 基礎架構

### 1.1 Next.js 14 App Router + Static Export

| 做法 | 說明 | SEO 價值 |
|------|------|----------|
| `output: 'export'` 靜態導出 | 所有頁面預渲染為靜態 HTML，無需伺服器端渲染 | 搜尋引擎直接讀取完整 HTML，無需執行 JS 才能看到內容 |
| `generateStaticParams` | 所有 locale 頁面在 build 時預先生成 | 每個頁面都有獨立的靜態 HTML 檔案，搜尋引擎可直接索引 |
| `dynamicParams = false` | Blog 文章只允許預定義的 slug | 防止軟 404 頁面被索引 |
| `force-static` on sitemap | Sitemap 在 build 時靜態生成 | 減少伺服器負載，確保 sitemap 始終可用 |

**值得複製的做法：**
- ✅ **Static Export** — 所有頁面預渲染為靜態 HTML，搜尋引擎直接讀取完整內容
- ✅ **`dynamicParams = false`** — 防止未定義的 URL 被索引（軟 404）
- ✅ **`force-static`** — Sitemap 在 build 時靜態生成

---

## 2. On-Page SEO

### 2.1 Meta Tags 架構

**根佈局 (`src/app/layout.tsx`)**：
- `title.template: "%s | HEIC Converter"` — 所有子頁面自動附加品牌名稱
- `metadataBase` 設定為 `https://heicconverter.com` — 所有相對 URL 自動解析
- `manifest` 指向 PWA manifest
- Open Graph (og:title, og:description, og:type, og:image) — 社交分享優化
- Twitter Card (summary_large_image) — Twitter 分享優化
- Google Search Console 驗證標籤
- Google AdSense publisher ID
- theme-color

**Locale 佈局 (`[locale]/layout.tsx`)**：
- 每個 locale 頁面有獨立的 `generateMetadata`，讀取 `getTranslations('seo')` 取得 locale 感知的 title/description
- 每個 locale 頁面有獨立的 canonical URL
- 每個 locale 頁面有完整的 hreflang alternates

**工具頁面 (e.g. heic-to-png/page.tsx)**：
- 每個工具頁面有獨立的 `generateMetadata`，讀取 `getTranslations('tools.{toolKey}')` 取得 locale 感知的 title/description
- 每個工具頁面有獨立的 canonical URL + hreflang alternates

**Blog 文章頁面**：
- 動態 `generateMetadata` 讀取文章 title/description
- 完整的 hreflang alternates

### 值得複製的做法：
- ✅ **Title template** — `%s | HEIC Converter` 確保品牌一致性
- ✅ **metadataBase** — 設定基礎 URL，所有相對路徑自動解析
- ✅ **每個頁面獨立 generateMetadata** — 非共用預設值
- ✅ **async generateMetadata** — 支援 i18n 動態讀取翻譯
- ✅ **canonical URL** — 每個頁面都有獨立的 canonical
- ✅ **OG + Twitter Card** — 社交分享優化
- ✅ **Google Search Console 驗證** — 根佈局直接嵌入

---

## 3. 結構化資料 (JSON-LD Schema)

這是本專案最強的部分之一，多層次 Schema 覆蓋：

### 3.1 Organization Schema（根佈局）
```json
{
  "@type": "Organization",
  "name": "HEIC Converter",
  "url": "https://heicconverter.com",
  "logo": "https://heicconverter.com/icons/icon-192.svg",
  "description": "Free online HEIC/HEIF image converter...",
  "foundingDate": "2026-06-24",
  "sameAs": ["https://github.com/chungyuicheung/heic-converter"]
}
```
- 全站所有頁面都繼承此 Schema
- 包含 foundingDate、sameAs（GitHub）等豐富屬性

### 3.2 FAQPage Schema（工具頁面 + 首頁 + Blog）
- 每個工具頁面透過 `FaqJsonLd` 注入 FAQPage Schema
- 首頁也有 FAQPage Schema
- Blog 文章可選注入 FAQPage（3 篇高價值文章已配置）
- FAQ 答案包含具體數據與引用（提升 AI 引用率）

### 3.3 HowTo Schema（工具頁面）
- 每個工具頁面透過 `HowToJsonLd` 注入 HowTo Schema
- 包含 step-by-step 轉換流程（3 步驟）
- 包含 name + description

### 3.4 BlogPosting Schema（Blog 文章）
- 每篇 Blog 文章透過 `BlogArticleJsonLd` 注入 BlogPosting Schema
- 包含 headline、description、image、datePublished、dateModified、author、publisher、keywords、mainEntityOfPage

### 3.5 WebApplication Schema（SeoHead 元件）
- 舊版工具頁面使用 WebApplication Schema
- 包含 applicationCategory、operatingSystem、offers（price: 0）

### 值得複製的做法：
- ✅ **多層次 Schema 覆蓋** — Organization（全站）+ FAQPage + HowTo + BlogPosting + WebApplication
- ✅ **FAQ 答案含具體數據** — 提升 AI 引用率（+37-40% citation 提升，Princeton 研究）
- ✅ **Blog 文章可選 FAQ Schema** — 高價值文章額外注入 FAQPage
- ✅ **HowTo Schema 含 step-by-step** — 適合語音搜尋和精選摘要
- ✅ **BlogPosting 含完整作者/發布者/日期/關鍵詞**

---

## 4. 國際化 SEO (i18n + hreflang)

### 4.1 多語言架構
- **11 種語言**：en, zh-TW, id, th, vi, pt-BR, es, ko, ja, fr, de
- **`app/[locale]/` 目錄結構** — 每個語言有獨立的 URL 路徑
- **`localePrefix: 'always'`** — URL 永遠包含 locale 前綴（如 `/en/heic-to-png`）
- **Locale 檢測**：Cookie → navigator.languages → 英文預設

### 4.2 hreflang 實現
- `getHreflangAlternates()` 為每個路徑生成所有 11 種語言的 hreflang 標籤
- 包含 `x-default` 回退到英文
- 每個頁面的 `generateMetadata` 都注入完整的 alternates

### 4.3 Sitemap 多語言覆蓋
- 動態 `sitemap.ts` 包含：
  - 根首頁 + 所有 locale 首頁
  - 所有工具頁面（非 locale + locale 前綴）
  - Blog 索引頁（所有 locale）
  - Blog 文章（所有 locale × 所有 slug）
- 每個條目有 `lastModified`、`changeFrequency`、`priority`

### 4.4 重定向策略
- **Cloudflare Edge Redirects** (`_redirects`)：6 條根路徑 → `/en/` 301 永久重定向
- **JS 重定向**：根首頁 `/` 根據瀏覽器語言檢測重定向
- **根級頁面**：每個工具頁面在根級有 `RedirectPageMeta` 組件（meta refresh + canonical + noindex）
- **Blog 根級**：`redirect-client.tsx` 處理 blog slug 重定向

### 值得複製的做法：
- ✅ **11 種語言的完整 hreflang** — 每個頁面都有所有語言的替代連結
- ✅ **x-default 回退** — 確保搜尋引擎知道預設語言
- ✅ **301 重定向** — Cloudflare Edge 層級，非 JS 重定向
- ✅ **Locale 檢測優先級** — Cookie > 瀏覽器偏好 > 預設
- ✅ **Sitemap 覆蓋所有 locale × 所有頁面** — 無遺漏

---

## 5. AI / AEO (Answer Engine Optimization)

這是本專案最突出的部分，針對 AI 搜尋引擎（ChatGPT、Perplexity、Claude、Gemini）做了大量優化：

### 5.1 llms.txt（核心 AI SEO 資產）
- 完整的 `llms.txt` 檔案，包含所有工具頁面和 Blog 文章的 11 種語言 URL
- 按分類組織：Tool Pages / Batch Converter / Format Converters / Blog Articles
- 每個條目有描述文字，幫助 AI 理解內容
- 標註 `100% free` 關鍵資訊
- 列出所有支援語言

### 5.2 robots.txt AI Crawler 策略
```
User-agent: GPTBot → Allow
User-agent: ChatGPT-User → Allow
User-agent: PerplexityBot → Allow
User-agent: ClaudeBot → Allow
User-agent: anthropic-ai → Allow
User-agent: Google-Extended → Allow
User-agent: CCBot → Disallow  (封鎖訓練爬蟲)
```
- 明確允許所有主要 AI 搜尋引擎爬蟲
- 封鎖 CCBot（Common Crawl，純訓練用途）
- 包含 Sitemap 連結

### 5.3 llms.txt（核心 AI SEO 資產）
- 完整的 `llms.txt` 檔案，包含所有頁面的 11 種語言 URL
- 按分類組織（Tool Pages / Batch Converter / Format Converters / Blog Articles）
- 每個條目有描述文字
- 標註 `100% free` 關鍵資訊
- 列出所有支援語言
- `_headers` 中設定 `llms.txt` 不緩存，確保 AI 爬蟲取得最新內容

### 5.4 pricing.md（AI Agent 可讀定價文件）
- 明確宣告 `$0 / forever`
- 無帳戶、無上傳限制、無水印
- 純客戶端處理
- AI Agent 可直接讀取並引用

### 5.5 robots.txt AI Crawler 策略
- 明確允許 GPTBot、ChatGPT-User、PerplexityBot、ClaudeBot、anthropic-ai、Google-Extended
- 封鎖 CCBot（Common Crawl，純訓練用途）
- 包含 Sitemap 連結

### 5.6 FAQ 答案數據化（GEO 優化）
- FAQ 答案包含具體統計數據與引用
- 引用 ISO 規範標準與 SSIM/DSSIM 壓縮研究數據
- Princeton 研究顯示此做法可提升 +37-40% AI citation 率

### 5.7 Blog FAQPage Schema
- 3 篇高價值 Blog 文章配置 FAQ Schema
- 增強 AI Agent 答案提取能力

### 值得複製的做法：
- ✅ **llms.txt** — 完整的 AI Agent 可讀索引，按分類組織
- ✅ **pricing.md** — AI Agent 可讀定價文件
- ✅ **robots.txt AI Crawler 策略** — 允許 AI 搜尋引擎，封鎖純訓練爬蟲
- ✅ **FAQ 答案數據化** — 引用具體數據和標準，提升 AI 引用率
- ✅ **llms.txt 不緩存** — `_headers` 設定 no-cache
- ✅ **Blog FAQPage Schema** — 高價值文章額外注入 FAQ Schema

---

## 6. 內容策略與主題集群

### 6.1 關鍵詞落地頁策略
- 6 個工具頁面，每個針對特定關鍵詞：
  - `/heic-to-png` → "HEIC to PNG converter"
  - `/heic-to-jpeg` → "HEIC to JPEG converter"
  - `/heic-to-webp` → "HEIC to WebP converter"
  - `/heic-to-bmp` → "HEIC to BMP converter"
  - `/convert-heic` → "HEIC converter"
  - `/batch-convert-heic` → "batch HEIC converter"
- 每個頁面有獨立的 h1、subheadline、keywords、FAQ、formatInfo、comparisonTable

### 6.2 Blog 主題集群
- 27 篇 Blog 文章，分為三大類：
  - **Format Comparisons**（5 篇）：HEIC vs JPEG/PNG/WebP/HEIF
  - **How-To Guides**（10 篇）：Windows、iPhone、Mac、PC、Email、Batch
  - **Technical Guides**（12 篇）：格式解析、品質分析、檔案大小比較
- 文章之間有 `relatedSlugs` 交叉連結
- Blog 文章底部有 Related Articles 推薦

### 6.3 內部連結策略
- Header 導航包含所有工具頁面 + Blog
- SeoPageWrapper 底部有 "Also Available" 交叉連結區塊
- Blog 文章底部有 Related Articles
- Blog 文章底部有 CTA 連結回轉換工具
- 所有連結使用 locale-aware `Link` 組件

### 值得複製的做法：
- ✅ **每個格式有獨立落地頁** — 針對長尾關鍵詞
- ✅ **Blog 文章分主題集群** — Format Comparisons / How-To / Technical
- ✅ **文章間交叉連結** — `relatedSlugs` 機制
- ✅ **工具頁面間交叉連結** — "Also Available" 區塊
- ✅ **Blog → 工具 CTA** — 文章底部引導回轉換工具
- ✅ **locale-aware 內部連結** — 跨語言導航正確

---

## 7. 效能與技術 SEO

### 7.1 靜態導出 + CDN
- `output: 'export'` — 所有頁面預渲染為靜態 HTML
- Cloudflare Pages CDN 部署 — 全球邊緣節點
- `_headers` 設定靜態資源 1 年快取（`max-age=31536000, immutable`）

### 7.2 PWA 支援
- Service Worker（stale-while-revalidate 策略）
- Manifest（192px/512px 圖標、theme-color、standalone display）
- 離線頁面（`offline.html`）
- 可安裝到桌面

### 7.3 圖片優化
- `images: { unoptimized: true }` — 靜態導出不需要 Next.js 圖片優化
- OG 圖片（1200×630）— 社交分享
- PWA 圖標（192×192, 512×512）

### 7.4 快取策略
- `_headers` 設定靜態資源 1 年快取（`max-age=31536000, immutable`）
- `llms.txt` 不緩存（`no-cache, no-store, must-revalidate`）
- Cloudflare Pages CDN 邊緣快取

### 值得複製的做法：
- ✅ **靜態導出** — 所有頁面預渲染，無需 JS 執行
- ✅ **CDN 快取** — 靜態資源 1 年不可變快取
- ✅ **PWA 離線支援** — 提升使用者體驗和留存率
- ✅ **OG 圖片** — 1200×630 標準尺寸

---

## 8. PWA 與使用者體驗

### 8.1 PWA 功能
- Manifest（name、short_name、description、icons、display、theme_color）
- Service Worker（stale-while-revalidate 策略）
- 離線頁面（`offline.html`）
- 可安裝到桌面

### 8.2 使用者體驗 SEO 信號
- 響應式設計（Tailwind CSS）
- 深色模式支援
- 鍵盤無障礙（DropZone Enter/Space、aria-pressed）
- 即時轉換進度條
- 無需註冊/登入

### 值得複製的做法：
- ✅ **PWA 離線支援** — 提升使用者體驗和留存率
- ✅ **響應式設計** — 行動端 SEO 友好
- ✅ **深色模式** — 使用者體驗加分
- ✅ **無障礙標籤** — aria-label、aria-current、aria-pressed

---

## 9. 分析與監控

### 9.1 Google Analytics 4
- GA4 Measurement ID 配置
- 自訂事件追蹤：
  - `file_upload` — 檔案上傳
  - `format_change` — 格式切換
  - `conversion` — 轉換完成（含 format/quality/mode）
  - `download` — 下載（含 mode/count/format）
  - `cancel_all` — 取消
- `strategy="lazyOnload"` — 不阻塞頁面載入

### 9.2 Google AdSense
- 自動廣告腳本
- 響應式橫幅廣告位
- 底部廣告位
- `ads.txt` 驗證文件
- `lazyOnload` 策略

### 值得複製的做法：
- ✅ **GA4 自訂事件追蹤** — 追蹤使用者行為（上傳、轉換、下載）
- ✅ **lazyOnload 策略** — 第三方腳本不阻塞頁面載入
- ✅ **ads.txt** — AdSense 驗證文件
- ✅ **GA4 + AdSense 分離** — 各自獨立元件，可獨立控制

---

## 10. 可複製的 SEO 行動清單

以下是你可以直接複製到另一個網站的 SEO 行動清單，按優先級排列：

### 🔴 P0 — 必須做（立即見效）

| # | 項目 | 做法 |
|---|------|------|
| 1 | **metadataBase** | 設定 `metadataBase: new URL('https://yoursite.com')` |
| 2 | **Title template** | `title: { template: "%s \| Brand Name", default: "..." }` |
| 3 | **每個頁面獨立 generateMetadata** | 不要共用預設值，每個頁面有獨立的 title/description |
| 4 | **Canonical URL** | 每個頁面設定 canonical，避免重複內容 |
| 5 | **Open Graph + Twitter Card** | og:title, og:description, og:image, twitter:card |
| 6 | **robots.txt** | 允許 AI 爬蟲（GPTBot, ClaudeBot, PerplexityBot），封鎖純訓練爬蟲 |
| 7 | **Sitemap** | 動態生成，包含所有頁面 + 多語言版本 |
| 8 | **Google Search Console** | 驗證標籤嵌入根佈局 |
| 9 | **metadataBase** | 設定基礎 URL |
| 10 | **Canonical URL** | 每個頁面獨立 canonical |

### 🟡 P1 — 強烈建議（中高影響）

| # | 項目 | 做法 |
|---|------|------|
| 11 | **JSON-LD Organization Schema** | 全站注入 Organization（name/url/logo/description/sameAs） |
| 12 | **JSON-LD FAQPage Schema** | 每個有 FAQ 的頁面注入 FAQPage |
| 13 | **JSON-LD HowTo Schema** | 工具頁面注入 HowTo（step-by-step） |
| 14 | **JSON-LD BlogPosting Schema** | 每篇 Blog 文章注入 BlogPosting（含 author/publisher/date） |
| 15 | **llms.txt** | 建立 AI Agent 可讀的網站索引 |
| 16 | **pricing.md** | 建立 AI Agent 可讀的定價文件 |
| 17 | **robots.txt AI 策略** | 允許 AI 爬蟲，封鎖純訓練爬蟲 |
| 18 | **hreflang 完整實現** | 每個頁面有所有語言的 alternates |
| 19 | **Sitemap 多語言覆蓋** | 所有 locale × 所有頁面 |
| 20 | **301 重定向** | 根路徑 → locale 前綴路徑 |

### 🟡 P1 — 強烈建議（中高影響）

| # | 項目 | 做法 |
|---|------|------|
| 21 | **JSON-LD Organization Schema** | 全站注入 Organization（name/url/logo/sameAs） |
| 22 | **JSON-LD FAQPage Schema** | 每個有 FAQ 的頁面注入 FAQPage |
| 23 | **JSON-LD HowTo Schema** | 工具頁面注入 HowTo（step-by-step） |
| 24 | **JSON-LD BlogPosting Schema** | 每篇 Blog 文章注入 BlogPosting |
| 25 | **llms.txt** | 建立 AI Agent 可讀的網站索引 |
| 26 | **pricing.md** | 建立 AI Agent 可讀的定價文件 |
| 27 | **FAQ 答案數據化** | 引用具體數據和標準，提升 AI 引用率 |
| 28 | **關鍵詞落地頁策略** | 每個主要關鍵詞有獨立落地頁 |
| 29 | **Blog 主題集群** | 文章分主題集群，交叉連結 |
| 30 | **內部連結網路** | Header + "Also Available" + Related Articles + CTA |

### 🟢 P2 — 建議做（中等影響）

| # | 項目 | 做法 |
|---|------|------|
| 31 | **GA4 自訂事件追蹤** | 追蹤上傳/轉換/下載/取消等使用者行為 |
| 32 | **PWA Manifest** | name/short_name/description/icons/display/theme_color |
| 33 | **Service Worker** | stale-while-revalidate 快取策略 |
| 34 | **離線頁面** | offline.html |
| 35 | **ads.txt** | AdSense 驗證文件 |
| 36 | **301 重定向** | 舊路徑 → 新路徑，保留 SEO 權重 |
| 37 | **Locale 檢測優先級** | Cookie > 瀏覽器偏好 > 預設 |
| 38 | **async generateMetadata** | 支援 i18n 動態讀取 |
| 39 | **GA4 自訂事件** | 追蹤使用者行為（上傳/轉換/下載/取消） |
| 40 | **第三方腳本 lazyOnload** | 不阻塞頁面載入 |

### 🟢 P2 — 建議做（中等影響）

| # | 項目 | 做法 |
|---|------|------|
| 41 | **PWA Manifest** | name/short_name/description/icons/display/theme_color |
| 42 | **Service Worker** | stale-while-revalidate 快取策略 |
| 43 | **離線頁面** | offline.html |
| 44 | **ads.txt** | AdSense 驗證文件 |
| 45 | **301 重定向** | 舊路徑 → 新路徑，保留 SEO 權重 |
| 46 | **GA4 自訂事件** | 追蹤使用者行為（上傳/轉換/下載/取消） |
| 47 | **第三方腳本 lazyOnload** | 不阻塞頁面載入 |
| 48 | **靜態資源 1 年快取** | `max-age=31536000, immutable` |
| 49 | **響應式設計** | 行動端 SEO 友好 |
| 50 | **深色模式** | 使用者體驗加分 |

---

## 總結：這個專案最值得複製的 5 件事

1. **多層次 JSON-LD Schema** — Organization + FAQPage + HowTo + BlogPosting，覆蓋所有頁面類型
2. **llms.txt + pricing.md + robots.txt AI 策略** — 完整的 AI/AEO 三件套
3. **11 種語言的完整 i18n SEO** — hreflang + sitemap + 301 重定向
4. **FAQ 答案數據化** — 引用具體數據和標準，提升 AI 引用率
5. **主題集群 + 內部連結** — 工具頁面 + Blog 文章 + "Also Available" + Related Articles

這個專案的 SEO 做得非常全面，從技術基礎到 AI/AEO 前沿都有覆蓋。你可以直接拿這份報告當作 checklist，逐項檢查你的另一個網站，把缺失的部分補上。</think>

<｜DSML｜tool_calls>
<｜DSML｜invoke name="write">
<｜DSML｜parameter name="filePath" string="true">/Users/bubu/Documents/Github/heic-converter/docs/seo-aeo-analysis-report.md