#!/usr/bin/env python3
"""批量同步優化到所有 HTML 頁面"""
import re
from pathlib import Path

HTML_FILES = [
    Path("blog.html"), Path("404.html"),
    Path("kwun-tong.html"), Path("lam-tin.html"), 
    Path("tseung-kwan-o.html"), Path("kowloon-city.html"), Path("wong-tai-sin.html"),
] + list(Path("articles").glob("*.html"))

# 關鍵 CSS - 首屏必需樣式（從 tailwind.css 提取）
CRITICAL_CSS = r"""
  .fixed{position:fixed}.w-full{width:100%}.bg-white\/95{background-color:rgb(255 255 255 / 0.95)}.backdrop-blur-sm{backdrop-filter:blur(4px)}.shadow-md{box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1),0 2px 4px -2px rgb(0 0 0 / 0.1)}.z-50{z-index:50}.max-w-6xl{max-width:72rem}.mx-auto{margin-left:auto;margin-right:auto}.px-4{padding-left:1rem;padding-right:1rem}.flex{display:flex}.justify-between{justify-content:space-between}.items-center{align-items:center}.h-20{height:5rem}.flex-shrink-0{flex-shrink:0}.cursor-pointer{cursor:pointer}.text-2xl{font-size:1.5rem}.font-bold{font-weight:700}.text-emerald-800{color:rgb(6 95 70)}.tracking-wider{letter-spacing:0.05em}.border-2{border-width:2px}.border-emerald-800{border-color:rgb(6 95 70)}.p-1{padding:0.25rem}.rounded{border-radius:0.25rem}.ml-3{margin-left:0.75rem}.text-lg{font-size:1.125rem}.font-medium{font-weight:500}.text-gray-600{color:rgb(75 85 99)}.hidden{display:none}.sm\:block{display:block}.md\:flex{display:flex}.space-x-8>:not([hidden])~*{margin-left:2rem}.text-gray-600{color:rgb(75 85 99)}.hover\:text-emerald-700:hover{color:rgb(4 120 87)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.py-2{padding-top:0.5rem;padding-bottom:0.5rem}.bg-emerald-700{background-color:rgb(4 120 87)}.text-white{color:rgb(255 255 255)}.px-5{padding-left:1.25rem;padding-right:1.25rem}.rounded-full{border-radius:9999px}.hover\:bg-emerald-800:hover{background-color:rgb(6 95 70)}.shadow-lg{box-shadow:0 10px 15px -3px rgb(0 0 0 / 0.1),0 4px 6px -4px rgb(0 0 0 / 0.1)}.pulse-cta{animation:pulse-ring 2s infinite}@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(5,150,105,0.4)}70%{box-shadow:0 0 0 10px rgba(5,150,105,0)}100%{box-shadow:0 0 0 0 rgba(5,150,105,0)}}.md\:hidden{display:none}.block{display:block}.relative{position:relative}.pt-20{padding-top:5rem}.pb-16{padding-bottom:4rem}.md\:pt-32{padding-top:8rem}.md\:pb-24{padding-bottom:6rem}.flex{display:flex}.items-center{align-items:center}.min-h-\[80vh\]{min-height:80vh}.bg-stone-900{background-color:rgb(21 21 21)}.text-center{text-align:center}.text-white{color:rgb(255 255 255)}.text-4xl{font-size:2.25rem}.md\:text-5xl{font-size:3rem}.lg\:text-6xl{font-size:3.75rem}.font-bold{font-weight:700}.mb-6{margin-bottom:1.5rem}.text-lg{font-size:1.125rem}.md\:text-xl{font-size:1.25rem}.text-stone-200{color:rgb(231 229 228)}.max-w-lg{max-width:32rem}.leading-relaxed{line-height:1.625}.flex{display:flex}.flex-col{flex-direction:column}.items-center{align-items:center}.gap-4{gap:1rem}.bg-emerald-600{background-color:rgb(5 150 105)}.hover\:bg-emerald-700:hover{background-color:rgb(4 120 87)}.text-white{color:rgb(255 255 255)}.font-bold{font-weight:700}.py-3{padding-top:0.75rem;padding-bottom:0.75rem}.px-8{padding-left:2rem;padding-right:2rem}.rounded-full{border-radius:9999px}.shadow-xl{box-shadow:0 20px 25px -5px rgb(0 0 0 / 0.1),0 8px 10px -6px rgb(0 0 0 / 0.1)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.border-2{border-width:2px}.border-stone-300{border-color:rgb(214 211 209)}.hover\:bg-emerald-700:hover{background-color:rgb(4 120 87)}.hover\:border-emerald-700:hover{border-color:rgb(4 120 87)}.bg-stone-800{background-color:rgb(41 37 36)}.hover\:bg-stone-700:hover{background-color:rgb(68 64 60)}.fade-in{opacity:0;transform:translateY(20px);transition:opacity 0.6s ease,transform 0.6s ease}.fade-in.fade-visible{opacity:1;transform:translateY(0)}.faq-answer{max-height:0;opacity:0;overflow:hidden;transition:max-height 0.4s ease,opacity 0.3s ease}.faq-item.open .faq-answer{max-height:500px;opacity:1}.faq-icon{transition:transform 0.3s ease}.schedule-card{transition:opacity 0.3s ease}.bg-stone-50{background-color:rgb(250 250 249)}.py-20{padding-top:5rem;padding-bottom:5rem}.max-w-6xl{max-width:72rem}.mx-auto{margin-left:auto;margin-right:auto}.px-4{padding-left:1rem;padding-right:1rem}.text-3xl{font-size:1.875rem}.md\:text-4xl{font-size:2.25rem}.font-bold{font-weight:700}.text-gray-900{color:rgb(17 24 39)}.mb-4{margin-bottom:1rem}.text-gray-600{color:rgb(75 85 99)}.max-w-2xl{max-width:42rem}.mx-auto{margin-left:auto;margin-right:auto}.grid{display:grid}.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}.md\:grid-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.lg\:grid-cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}.gap-8{gap:2rem}.bg-white{background-color:rgb(255 255 255)}.p-8{padding:2rem}.rounded-2xl{border-radius:1rem}.shadow-sm{box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05)}.relative{position:relative}.absolute{position:absolute}.-top-4{top:-1rem}.left-8{left:2rem}.text-6xl{font-size:3.75rem}.text-emerald-200{color:rgb(167 243 208)}.font-serif{font-family:ui-serif,Georgia,Cambria,"Times New Roman",Times,serif}.text-gray-600{color:rgb(75 85 99)}.italic{font-style:italic}.mb-6{margin-bottom:1.5rem}.flex{display:flex}.items-center{align-items:center}.w-10{width:2.5rem}.h-10{height:2.5rem}.bg-emerald-100{background-color:rgb(209 250 229)}.rounded-full{border-radius:9999px}.flex{display:flex}.items-center{align-items:center}.justify-center{justify-content:center}.text-emerald-700{color:rgb(4 120 87)}.font-bold{font-weight:700}.mr-3{margin-right:0.75rem}.text-xs{font-size:0.75rem}.text-gray-500{color:rgb(107 114 128)}.flex{display:flex}.text-yellow-400{color:rgb(250 204 21)}.mt-4{margin-top:1rem}.space-x-1>:not([hidden])~*{margin-left:0.25rem}.w-4{width:1rem}.h-4{height:1rem}.fill-current{fill:currentColor}.bg-stone-100{background-color:rgb(245 245 244)}.py-20{padding-top:5rem;padding-bottom:5rem}.text-3xl{font-size:1.875rem}.md\:text-4xl{font-size:2.25rem}.font-bold{font-weight:700}.text-gray-900{color:rgb(17 24 39)}.mb-12{margin-bottom:3rem}.text-center{text-align:center}.text-gray-600{color:rgb(75 85 99)}.max-w-4xl{max-width:56rem}.mx-auto{margin-left:auto;margin-right:auto}.space-y-3>:not([hidden])~*{margin-top:0.75rem}.bg-stone-50{background-color:rgb(250 250 249)}.rounded-xl{border-radius:0.75rem}.border{border-width:1px}.border-stone-200{border-color:rgb(229 228 226)}.overflow-hidden{overflow:hidden}.fade-in{opacity:0;transform:translateY(20px);transition:opacity 0.6s ease,transform 0.6s ease}.faq-toggle{display:flex;align-items:center;justify-content:space-between;cursor:pointer}.w-full{width:100%}.text-left{text-align:left}.p-5{padding:1.25rem}.flex{display:flex}.items-center{align-items:center}.justify-between{justify-content:space-between}.hover\:bg-stone-100:hover{background-color:rgb(245 245 244)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.font-bold{font-weight:700}.text-gray-900{color:rgb(17 24 39)}.pr-4{padding-right:1rem}.w-5{width:1.25rem}.h-5{height:1.25rem}.text-emerald-600{color:rgb(5 150 105)}.flex-shrink-0{flex-shrink:0}.max-h-0{max-height:0}.opacity-0{opacity:0}.overflow-hidden{overflow:hidden}.max-h-\[500px\]{max-height:500px}.opacity-1{opacity:1}.px-5{padding-left:1.25rem;padding-right:1.25rem}.pb-5{padding-bottom:1.25rem}.text-gray-600{color:rgb(75 85 99)}.leading-relaxed{line-height:1.625}.inline-flex{display:inline-flex}.items-center{align-items:center}.text-emerald-700{color:rgb(4 120 87)}.hover\:text-emerald-800:hover{color:rgb(6 95 70)}.text-sm{font-size:0.875rem}.font-medium{font-weight:500}.mt-2{margin-top:0.5rem}.w-3{width:0.75rem}.h-3{height:0.75rem}.ml-1{margin-left:0.25rem}.grid{display:grid}.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}.md\:grid-cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}.gap-6{gap:1.5rem}.bg-white{background-color:rgb(255 255 255)}.rounded-2xl{border-radius:1rem}.shadow-sm{box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05)}.p-6{padding:1.5rem}.hover\:shadow-lg:hover{box-shadow:0 10px 15px -3px rgb(0 0 0 / 0.1),0 4px 6px -4px rgb(0 0 0 / 0.1)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.group{cursor:pointer}.inline-block{display:inline-block}.py-0\.5{padding-top:0.125rem;padding-bottom:0.125rem}.px-2{padding-left:0.5rem;padding-right:0.5rem}.rounded-full{border-radius:9999px}.bg-emerald-100{background-color:rgb(209 250 229)}.text-emerald-800{color:rgb(6 95 70)}.text-xs{font-size:0.75rem}.font-medium{font-weight:500}.mb-3{margin-bottom:0.75rem}.text-lg{font-size:1.125rem}.font-bold{font-weight:700}.text-gray-900{color:rgb(17 24 39)}.group-hover\:text-emerald-700:hover{color:rgb(4 120 87)}.text-gray-600{color:rgb(75 85 99)}.text-sm{font-size:0.875rem}.mb-3{margin-bottom:0.75rem}.text-emerald-700{color:rgb(4 120 87)}.font-medium{font-weight:500}.inline-flex{display:inline-flex}.items-center{align-items:center}.w-3{width:0.75rem}.h-3{height:0.75rem}.ml-1{margin-left:0.25rem}.text-center{text-align:center}.mt-10{margin-top:2.5rem}.inline-flex{display:inline-flex}.items-center{align-items:center}.bg-emerald-700{background-color:rgb(4 120 87)}.text-white{color:rgb(255 255 255)}.px-8{padding-left:2rem;padding-right:2rem}.py-3{padding-top:0.75rem;padding-bottom:0.75rem}.rounded-full{border-radius:9999px}.hover\:bg-emerald-800:hover{background-color:rgb(6 95 70)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.font-bold{font-weight:700}.bg-stone-900{background-color:rgb(21 21 21)}.text-stone-300{color:rgb(214 211 209)}.py-16{padding-top:4rem;padding-bottom:4rem}.max-w-6xl{max-width:72rem}.mx-auto{margin-left:auto;margin-right:auto}.px-4{padding-left:1rem;padding-right:1rem}.grid{display:grid}.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}.md\:grid-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.gap-12{gap:3rem}.items-center{align-items:center}.text-3xl{font-size:1.875rem}.font-bold{font-weight:700}.text-white{color:rgb(255 255 255)}.mb-4{margin-bottom:1rem}.text-lg{font-size:1.125rem}.space-y-4>:not([hidden])~*{margin-top:1rem}.flex{display:flex}.items-center{align-items:center}.w-6{width:1.5rem}.h-6{height:1.5rem}.text-emerald-500{color:rgb(16 185 129)}.text-xl{font-size:1.25rem}.font-bold{font-weight:700}.text-white{color:rgb(255 255 255)}.bg-white\/5{background-color:rgb(255 255 255 / 0.05)}.p-8{padding:2rem}.rounded-2xl{border-radius:1rem}.border{border-width:1px}.border-white\/10{border-color:rgb(255 255 255 / 0.1)}.text-xl{font-size:1.25rem}.font-bold{font-weight:700}.text-white{color:rgb(255 255 255)}.mb-4{margin-bottom:1rem}.space-y-4>:not([hidden])~*{margin-top:1rem}.block{display:block}.text-sm{font-size:0.875rem}.mb-1{margin-bottom:0.25rem}.w-full{width:100%}.bg-stone-800{background-color:rgb(41 37 36)}.border{border-width:1px}.border-stone-700{border-color:rgb(68 64 60)}.rounded{border-radius:0.25rem}.p-3{padding:0.75rem}.text-white{color:rgb(255 255 255)}.focus\:outline-none:focus{outline:2px solid transparent;outline-offset:2px}.focus\:border-emerald-500:focus{border-color:rgb(16 185 129)}.placeholder\:text-stone-400::placeholder{color:rgb(168 162 158)}.w-full{width:100%}.bg-emerald-600{background-color:rgb(5 150 105)}.hover\:bg-emerald-700:hover{background-color:rgb(4 120 87)}.text-white{color:rgb(255 255 255)}.font-bold{font-weight:700}.py-3{padding-top:0.75rem;padding-bottom:0.75rem}.rounded{border-radius:0.25rem}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.border-t{border-top-width:1px}.border-stone-800{border-color:rgb(41 37 36)}.mt-12{margin-top:3rem}.pt-8{padding-top:2rem}.text-center{text-align:center}.text-sm{font-size:0.875rem}.text-stone-500{color:rgb(107 114 128)}.fixed{position:fixed}.bottom-6{bottom:1.5rem}.right-6{right:1.5rem}.bg-green-500{background-color:rgb(34 197 94)}.hover\:bg-green-600:hover{background-color:rgb(22 163 74)}.text-white{color:rgb(255 255 255)}.p-4{padding:1rem}.rounded-full{border-radius:9999px}.shadow-2xl{box-shadow:0 25px 50px -12px rgb(0 0 0 / 0.25)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.transform{transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.hover\:scale-110:hover{transform:scale(1.1)}.z-50{z-index:50}.flex{display:flex}.items-center{align-items:center}.gap-2{gap:0.5rem}.group{cursor:pointer}.w-7{width:1.75rem}.h-7{height:1.75rem}.max-w-0{max-width:0}.overflow-hidden{overflow:hidden}.group-hover\:max-w-xs:hover{max-width:20rem}.transition-all{transition-property:all}.duration-300{transition-duration:300ms}.ease-in-out{transition-timing-function:cubic-bezier(0.4,0,0.2,1)}.whitespace-nowrap{white-space:nowrap}.font-bold{font-weight:700}.fixed{position:fixed}.bottom-6{bottom:1.5rem}.left-6{left:1.5rem}.bg-emerald-700{background-color:rgb(4 120 87)}.hover\:bg-emerald-800:hover{background-color:rgb(6 95 70)}.text-white{color:rgb(255 255 255)}.p-3{padding:0.75rem}.rounded-full{border-radius:9999px}.shadow-2xl{box-shadow:0 25px 50px -12px rgb(0 0 0 / 0.25)}.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke}.transform{transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.hover\:scale-110:hover{transform:scale(1.1)}.z-50{z-index:50}.opacity-0{opacity:0}.pointer-events-none{pointer-events:none}.w-6{width:1.5rem}.h-6{height:1.5rem}.
        /* Site-specific styles */
        html { scroll-behavior: smooth; }
        .fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
        .fade-in.fade-visible { opacity: 1; transform: translateY(0); }
        .faq-answer { max-height: 0; opacity: 0; overflow: hidden; transition: max-height 0.4s ease, opacity 0.3s ease; }
        .faq-item.open .faq-answer { max-height: 500px; opacity: 1; }
        .faq-icon { transition: transform 0.3s ease; }
        .schedule-card { transition: opacity 0.3s ease; }
        @keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(5,150,105,0.4); } 70% { box-shadow: 0 0 0 10px rgba(5,150,105,0); } 100% { box-shadow: 0 0 0 0 rgba(5,150,105,0); } }
        .pulse-cta { animation: pulse-ring 2s infinite; }
        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            body { background: #1c1917; color: #e7e5e4; }
            .bg-white, .bg-stone-50, .bg-stone-100 { background-color: #292524; }
            .bg-white\/95 { background-color: rgba(28,25,23,0.95); }
            .text-gray-900, .text-gray-800 { color: #e7e5e4; }
            .text-gray-600, .text-gray-500 { color: #a8a29e; }
            .border-stone-200, .border-stone-300 { border-color: #44403c; }
            .shadow-lg, .shadow-sm, .shadow-xl, .shadow-2xl { box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
            .bg-emerald-50 { background-color: #064e3b; }
            .bg-stone-200 { background-color: #44403c; }
        }
"""

REPLACEMENTS = [
    # 1. 移除 Tailwind CDN preconnect
    (r'<link rel="preconnect" href="https://cdn\.tailwindcss\.com" crossorigin>\s*', ''),
    (r'<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*', ''),
    
    # 2. 替換 CSS 載入方式 - 關鍵 CSS 內聯 + 異步載入
    (r'<link rel="preload" href="css/tailwind\.css" as="style">\s*<link rel="stylesheet" href="css/tailwind\.css">', 
     f'<style>\n{CRITICAL_CSS}\n</style>\n<link rel="preload" href="css/tailwind.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="css/tailwind.css"></noscript>'),
    
    # 3. 替換 Lucide CDN 為本地
    (r'<script src="https://unpkg\.com/lucide@latest"><\/script>\s*<script>\s*lucide\.createIcons\(\);\s*<\/script>', 
     '<script src="js/icons.js"></script>'),
    
    # 4. 圖片路徑更新 (images/ 目錄)
    (r'src="class_hall\.jpg"', 'src="images/class_hall.jpg"'),
    (r'src="class_8year\.JPG"', 'src="images/class_8year.JPG"'),
    (r'src="solo2\.jpg"', 'src="images/solo2.jpg"'),
    (r'src="solo\.jpg"', 'src="images/solo.jpg"'),
    (r'src="class\.png"', 'src="images/class.png"'),
    (r'src="class\.webp"', 'src="images/class.webp"'),
    (r'src="solo\.webp"', 'src="images/solo.webp"'),
    (r'src="class_hall\.webp"', 'src="images/class_hall.webp"'),
    (r'src="class_8year\.webp"', 'src="images/class_8year.webp"'),
    (r'src="solo2\.webp"', 'src="images/solo2.webp"'),
]

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    for pattern, repl in REPLACEMENTS:
        content = re.sub(pattern, repl, content)
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    print("Processing HTML files...")
    updated = 0
    for html_file in HTML_FILES:
        if process_file(html_file):
            print(f"✅ Updated: {html_file}")
            updated += 1
        else:
            print(f"⏭️  No changes: {html_file}")
    print(f"\nDone! Updated {updated} files.")

if __name__ == "__main__":
    main()