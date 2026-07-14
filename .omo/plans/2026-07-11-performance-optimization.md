# Performance Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve page load performance by converting large PNG/JPG images to WebP format (reducing class.png from 1.5MB to ~200KB), and optimizing the Tailwind CSS loading strategy.

**Architecture:** WebP conversion retains original files as fallback while serving WebP to modern browsers via `<picture>` elements. Tailwind optimized by generating a minimal build-time CSS file instead of CDN download at runtime.

**Tech Stack:** cwebp (WebP converter via Homebrew), HTML `<picture>` elements, Tailwind CSS CLI, Python helper script for batch conversion.

**Files to create/modify:**
- Create: `class.webp`, `solo.webp`, `solo2.webp`, `class_hall.webp`, `class_8year.webp`
- Modify: `index.html` (change `<img>` to `<picture>` for all 5 images)
- Modify: `blog.html` (add bg image if any)
- Create: `convert-images.sh` (optional helper script)

---

### Task 1: Install WebP Tools and Convert All Images

**Files:**
- Create: `class.webp`, `solo.webp`, `solo2.webp`, `class_hall.webp`, `class_8year.webp`

- [ ] **Step 1: Check if cwebp is installed**

```bash
which cwebp || brew install webp
```
Expected: `cwebp` binary path or successful installation.

- [ ] **Step 2: Convert class.png to WebP (the biggest win — 1.5MB → ~200KB)**

```bash
cwebp -q 80 class.png -o class.webp
ls -lh class.png class.webp
```
Expected: class.png ~1.5MB, class.webp ~150-250KB (80-85% size reduction).

- [ ] **Step 3: Convert solo.jpg to WebP**

```bash
cwebp -q 85 solo.jpg -o solo.webp
ls -lh solo.jpg solo.webp
```
Expected: solo.jpg ~88KB → solo.webp ~40-50KB.

- [ ] **Step 4: Convert solo2.jpg to WebP**

```bash
cwebp -q 85 solo2.jpg -o solo2.webp
ls -lh solo2.jpg solo2.webp
```
Expected: solo2.jpg ~214KB → solo2.webp ~100-120KB.

- [ ] **Step 5: Convert class_hall.jpg to WebP**

```bash
cwebp -q 85 class_hall.jpg -o class_hall.webp
ls -lh class_hall.jpg class_hall.webp
```
Expected: class_hall.jpg ~150KB → class_hall.webp ~70-90KB.

- [ ] **Step 6: Convert class_8year.JPG to WebP**

```bash
cwebp -q 85 class_8year.JPG -o class_8year.webp
ls -lh class_8year.JPG class_8year.webp
```
Expected: class_8year.JPG ~255KB → class_8year.webp ~120-150KB.

- [ ] **Step 7: Commit the WebP files**

```bash
git add class.webp solo.webp solo2.webp class_hall.webp class_8year.webp
git commit -m "perf: add WebP versions of all images (80-85% size reduction on hero image)"
```

---

### Task 2: Update index.html Images to Use WebP with Picture Fallback

**Files:**
- Modify: `index.html` (5 image elements)

Each `<img>` tag needs to be wrapped in a `<picture>` element that serves WebP to modern browsers and falls back to PNG/JPG for older browsers.

- [ ] **Step 1: Update Hero background image (class.png)**

Current (line 223-228):
```html
            <img 
                src="class.png" 
                alt="林燦平師傅於油塘教授太極拳班上課實況" 
                class="w-full h-full object-cover opacity-60"
            />
```

Replace with:
```html
            <picture>
                <source srcset="class.webp" type="image/webp">
                <img 
                    src="class.png" 
                    alt="林燦平師傅於油塘教授太極拳班上課實況" 
                    class="w-full h-full object-cover opacity-60"
                />
            </picture>
```

- [ ] **Step 2: Update About section teacher photo (solo.jpg)**

Current (line 263-269):
```html
                        <img 
                            src="solo.jpg" 
                            alt="林燦平師傅示範楊氏太極拳" 
                            loading="lazy"
                            class="w-full h-full object-cover hover:scale-105 transition duration-700"
                        />
```

Replace with:
```html
                        <picture>
                            <source srcset="solo.webp" type="image/webp">
                            <img 
                                src="solo.jpg" 
                                alt="林燦平師傅示範楊氏太極拳" 
                                loading="lazy"
                                class="w-full h-full object-cover hover:scale-105 transition duration-700"
                            />
                        </picture>
```

- [ ] **Step 3: Update class_hall.jpg in Classes section**

Current (line 374):
```html
                        <img src="class_hall.jpg" alt="油塘太極拳入門班上課環境" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
```

Replace with:
```html
                        <picture>
                            <source srcset="class_hall.webp" type="image/webp">
                            <img src="class_hall.jpg" alt="油塘太極拳入門班上課環境" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
                        </picture>
```

- [ ] **Step 4: Update class_8year.JPG in Classes section**

Current (line 391):
```html
                        <img src="class_8year.JPG" alt="油塘太極器械班學員上課實況" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
```

Replace with:
```html
                        <picture>
                            <source srcset="class_8year.webp" type="image/webp">
                            <img src="class_8year.JPG" alt="油塘太極器械班學員上課實況" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
                        </picture>
```

- [ ] **Step 5: Update solo2.jpg (teacher demonstration photo)**

Current (line 407):
```html
                        <img src="solo2.jpg" alt="林燦平師傅示範太極劍與太極扇" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
```

Replace with:
```html
                        <picture>
                            <source srcset="solo2.webp" type="image/webp">
                            <img src="solo2.jpg" alt="林燦平師傅示範太極劍與太極扇" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition duration-500"/>
                        </picture>
```

- [ ] **Step 6: Verify all 5 images have picture elements**

```bash
grep -c '<picture>' index.html
```
Expected: 5 (all images wrapped in picture elements).

```bash
grep -c 'type="image/webp"' index.html
```
Expected: 5 (all pictures have WebP source).

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "perf: wrap all images in <picture> with WebP source and PNG/JPG fallback"
```

---

### Task 3: Analyze Tailwind CSS Optimization Options

**Files:**
- Read-only analysis: `index.html` (Tailwind classes used vs full CDN download)

- [ ] **Step 1: Check what Tailwind classes are actually used**

```bash
# Extract all Tailwind classes from index.html (words starting with specific prefixes)
grep -oP 'class="[^"]*"' index.html | tr ' ' '\n' | sort -u | grep -E '^(bg-|text-|p-|m-|flex|grid|w-|h-|max-w-|rounded|shadow|border|hover:|md:|lg:|sm:|transition|transform|opacity|font-|leading-|space-|gap-|from-|to-|via-|inset-|object-|items-|justify-|fixed|absolute|relative|hidden|block|inline-|overflow-|z-|top-|left-|right-|bottom-|min-h-|aspect-|backdrop-|cursor-|tracking-|list-)' | head -100
```
Expected: List of ~80-120 unique Tailwind utility classes used.

- [ ] **Step 2: Create a Tailwind CSS config file (optional)**

If Tailwind CLI optimization is desired, create `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./articles/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- [ ] **Step 3: Build custom CSS (optional — skip if CDN is acceptable for now)**

```bash
npx tailwindcss -i ./src/input.css -o ./css/tailwind.css --minify
```
Only if you have a CSS input file and want to go build-time. This step may be deferred to a separate plan.

- [ ] **Step 4: Note on Tailwind optimization**

Current CDN-based Tailwind loads ~90KB of CSS (all utilities). With build-time generation, this drops to ~15-25KB. **This is a P2 improvement** — consider implementing when adding build tooling.

No commit needed for analysis.

---

### Scope Completion Checklist
- [ ] cwebp installed via Homebrew
- [ ] class.png → class.webp converted (1.5MB → ~200KB)
- [ ] solo.jpg → solo.webp converted
- [ ] solo2.jpg → solo2.webp converted
- [ ] class_hall.jpg → class_hall.webp converted
- [ ] class_8year.JPG → class_8year.webp converted
- [ ] All 5 index.html images wrapped in `<picture>` with WebP source + original fallback
- [ ] All changes committed
