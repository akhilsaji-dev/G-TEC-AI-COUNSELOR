# ============================================================
# G-TEC AI Counselor — Django Integration
# ============================================================
# Files:
#   counselor/views.py
#   counselor/urls.py
#   counselor/ai_handler.py
#   myproject/urls.py (root, add one line)
# ============================================================


# ── counselor/ai_handler.py ──────────────────────────────────
"""
Handles AI response generation.
Uses Anthropic Claude if API key is set,
otherwise falls back to a smart rule-based engine.
"""

import re
from django.conf import settings

SYSTEM_PROMPT = """You are the G-TEC AI Counselor — a warm, knowledgeable, and professional career advisor
for a leading tech training institute in India called G-TEC.

Your role:
- Help students choose the right course based on their interests, background, and goals
- Explain career paths, salary ranges, and market demand clearly
- Be concise but thorough — use structured formatting with headers, bullet points, and bold text
- Always use Markdown formatting in your response (headings, bullets, bold, italic, code)
- Be encouraging and supportive; students may feel uncertain

Available courses at G-TEC:
- Python Full Stack (6 months, ₹25,000) — Django, React, REST API, PostgreSQL
- MERN Stack (6 months, ₹28,000) — MongoDB, Express, React, Node.js
- Flutter Development (4 months, ₹22,000) — Dart, Firebase, cross-platform mobile
- Data Analytics (3 months, ₹15,000) — SQL, Python, Power BI, Tableau
- AI & Machine Learning (8 months, ₹35,000) — TensorFlow, PyTorch, Scikit-learn
- UI/UX Design (3 months, ₹18,000) — Figma, Adobe XD, Prototyping
- Java Full Stack (6 months, ₹28,000) — Spring Boot, Hibernate, React, MySQL
- Cyber Security (5 months, ₹30,000) — Ethical hacking, Network security, Kali Linux
- Digital Marketing (2 months, ₹12,000) — SEO, Google Ads, Social Media
- Tally Prime (2 months, ₹8,000) — Accounting, GST, Payroll
- Graphic Design (3 months, ₹15,000) — Photoshop, Illustrator, CorelDRAW
- Power BI (2 months, ₹12,000) — DAX, Reports, Dashboards

Always end with a warm, encouraging closing line.
Format responses clearly with Markdown since the frontend renders HTML."""


# ── RULE-BASED FALLBACK ──────────────────────────────────────

RULE_RESPONSES = {
    r'(beginner|start|no experience|fresher|zero|never|new to)': """
## 🌟 Best Courses for Beginners

Here are our most beginner-friendly options at G-TEC:

### 1. **Data Analytics** *(Most recommended to start)*
- No prior coding needed
- Learn Excel → SQL → Python → Power BI
- Duration: 3 months | Fee: ₹15,000
- Salary after placement: **₹3.5–7 LPA**

### 2. **UI/UX Design**
- Zero technical background needed
- Learn Figma, prototyping, and user research
- Duration: 3 months | Fee: ₹18,000
- Creative + logical — best of both worlds

### 3. **Python Full Stack**
- Starts from absolute basics
- By month 2, you'll build real web apps
- Duration: 6 months | Fee: ₹25,000
- Salary: **₹5–12 LPA**

> 💡 *My recommendation: Start with Data Analytics or UI/UX if you want quick results. Choose Python Full Stack if you're committed to software development.*

You've got this! Every expert was once a beginner. 🚀
""",

    r'(mern|react|node|javascript|js)': """
## ⚛️ MERN Stack vs Python Full Stack

Both are excellent choices — here's a clear breakdown:

| Feature | MERN Stack | Python Full Stack |
|---------|-----------|-----------------|
| Language | JavaScript | Python + JS |
| Best for | Startups, SPAs | Enterprise, APIs |
| Jobs | ₹6–14 LPA | ₹5–12 LPA |
| Duration | 6 months | 6 months |
| Difficulty | Medium | Medium-Easy |

### Why choose MERN?
- **One language (JS)** for both frontend and backend
- Massive demand at **funded startups and product companies**
- React is the #1 frontend framework globally

### Why choose Python Full Stack?
- Python is **easier to learn** for beginners
- Django is extremely powerful for **data-heavy applications**
- Better if you plan to move into **AI/ML later**

> 🎯 *If you're startup-focused and love JavaScript → MERN. If you want AI/ML as a future path → Python Full Stack.*

Feel free to ask more — we'll find the perfect fit for you! 😊
""",

    r'(data analytics|data analyst|power bi|tableau|excel|sql)': """
## 📊 Career in Data Analytics

Data Analytics is one of the **fastest-growing and most accessible** tech fields in 2025.

### What You'll Learn at G-TEC
1. **Excel** — Advanced formulas, pivot tables, dashboards
2. **SQL** — Queries, joins, stored procedures
3. **Python** — Pandas, NumPy, data wrangling
4. **Power BI** — Interactive reports and business dashboards
5. **Statistics** — Descriptive stats, hypothesis testing
6. **Tableau** — Data storytelling and visualisation

### Career Opportunities
- Data Analyst — **₹4–9 LPA**
- Business Analyst — **₹5–12 LPA**
- BI Analyst — **₹6–14 LPA**
- Product Analyst — **₹8–18 LPA**

### Is it right for you?
✅ You like working with numbers and patterns  
✅ You enjoy solving business problems  
✅ You want a quick path to employment (3 months)  
✅ No prior coding experience needed

> ⚡ *Duration: 3 months | Fee: ₹15,000 — Best ROI in our entire course catalogue.*

This field is **exploding** — every company needs data analysts now. 📈
""",

    r'(flutter|mobile|app|android|ios|dart)': """
## 📱 Flutter Development in 2026

Great question! Flutter is absolutely worth learning in 2026, and here's why:

### Flutter's Current Standing
- Used by **Google, BMW, eBay, Alibaba** in production
- **Cross-platform** — one codebase for Android + iOS + Web
- Dart language is clean, fast, and easy to pick up
- **#1 most used cross-platform framework** (Stack Overflow Survey 2024)

### What you'll build at G-TEC
- Full mobile apps with beautiful UI
- Firebase backend integration (auth, database, storage)
- State management (Riverpod / BLoC)
- API integration and deployment to Play Store / App Store

### Job Market
- Mobile Developer (Flutter): **₹5–11 LPA**
- Senior Flutter Dev: **₹12–22 LPA**
- Freelance: **₹500–2000/hr** (international clients)

### Duration & Fee
- 4 months | ₹22,000

> 🌟 *Flutter is one of the smartest niche skills to have in 2026. Less competition than web dev, excellent salary, and growing demand.*

You'd be making a very smart career move! 💪
""",

    r'(cyber|security|hacking|ethical|network|pentest)': """
## 🛡️ Cyber Security — Career & Scope

Cyber Security is one of the **highest-demand and highest-paying** tech fields globally.

### The Opportunity
- **3.5 million cybersecurity jobs** unfilled globally (2025)
- India needs **1 million+ cyber professionals** by 2026
- Every bank, hospital, and tech company is hiring

### What You'll Learn at G-TEC
1. **Network Fundamentals** — TCP/IP, DNS, firewalls
2. **Ethical Hacking** — Kali Linux, Metasploit, Burp Suite
3. **Web Application Security** — OWASP Top 10
4. **Penetration Testing** — Methodology, reporting
5. **Cryptography & Digital Forensics**
6. **Compliance** — ISO 27001, GDPR basics

### Career Paths & Salaries
- SOC Analyst — **₹4–8 LPA**
- Ethical Hacker — **₹6–15 LPA**
- Security Engineer — **₹10–25 LPA**
- CISO (10 yrs) — **₹40–80 LPA**

### Course Details
- Duration: 5 months | Fee: ₹30,000

> 🔐 *Cyber Security isn't just a job — it's a mission. You protect real people and organisations from real threats.*

An extraordinary career awaits you in this field! 🌐
""",

    r'(ai|machine learning|ml|deep learning|nlp|tensorflow|pytorch)': """
## 🤖 AI & Machine Learning — The Future is Now

AI & ML is the **most transformative and highest-paying** tech domain of this decade.

### Why AI/ML in 2025?
- **ChatGPT effect** — every company is integrating AI
- India's AI market growing at **45% CAGR**
- AI engineers among the **top 3 highest-paid** globally

### What You'll Learn at G-TEC
**Phase 1 — Python & Math Foundations**
- NumPy, Pandas, Matplotlib
- Linear Algebra, Statistics, Probability

**Phase 2 — Classical ML**
- Scikit-learn, Random Forest, XGBoost
- Feature engineering, model evaluation

**Phase 3 — Deep Learning**
- TensorFlow 2.x, Keras, PyTorch
- CNNs, RNNs, Transformers (basics)

**Phase 4 — Applied AI**
- NLP with HuggingFace, Computer Vision, LLM fine-tuning

### Salaries
- ML Engineer: **₹8–20 LPA**
- Data Scientist: **₹10–25 LPA**
- AI Researcher: **₹18–40 LPA**

### Pre-requisite
Basic Python helps. We build from the ground up.

- Duration: 8 months | Fee: ₹35,000

> 🧠 *You don't just learn ML at G-TEC — you become someone who can build the future.*

This is the most exciting field you can enter right now! ✨
""",
}

DEFAULT_RESPONSE = """## 👋 I'm Here to Help!

Thank you for your question. I'd love to give you a personalised answer!

### What I can help you with:

- 📚 **Course recommendations** based on your background and goals
- 💰 **Salary insights** for each career path
- 🗺️ **Career roadmaps** — what to learn and in what order
- ⚖️ **Course comparisons** — e.g. Python vs MERN, UI/UX vs Graphic Design
- 🎯 **Industry trends** — what's in demand in 2025–2026
- ❓ **Eligibility & prerequisites** for each course

### Try asking something like:
- *"I'm a BCA graduate interested in data — what should I learn?"*
- *"Which course has the best placement in Kerala?"*
- *"Can I learn MERN without prior coding experience?"*

Our counselors are also available for a **free 1-on-1 consultation**. Just mention it and I'll connect you!

Looking forward to guiding you toward your best future. 🌟
"""


def get_rule_response(message: str) -> str | None:
    """Check rule-based responses. Returns None if no match."""
    message_lower = message.lower()
    for pattern, response in RULE_RESPONSES.items():
        if re.search(pattern, message_lower):
            return response.strip()
    return None


def get_ai_response(message: str) -> str:
    """
    Main response generator.
    1. Try Anthropic Claude API (if key available)
    2. Fall back to rule-based responses
    3. Final fallback to default message
    """
    # ── Try Anthropic API ──
    api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
    if api_key:
        try:
            import anthropic
            import markdown

            client = anthropic.Anthropic(api_key=api_key)
            result = client.messages.create(
                model='claude-sonnet-4-20250514',
                max_tokens=800,
                system=SYSTEM_PROMPT,
                messages=[{'role': 'user', 'content': message}]
            )
            raw_md = result.content[0].text
            # Convert Markdown → HTML for Django's |safe filter
            html = markdown.markdown(
                raw_md,
                extensions=['tables', 'fenced_code', 'nl2br']
            )
            return html
        except Exception as e:
            # Log in production; continue to fallback
            print(f"[G-TEC AI] Anthropic error: {e}")

    # ── Rule-based fallback ──
    import markdown
    rule_resp = get_rule_response(message)
    raw_md = rule_resp if rule_resp else DEFAULT_RESPONSE
    return markdown.markdown(raw_md, extensions=['tables', 'fenced_code', 'nl2br'])


# ── counselor/views.py ───────────────────────────────────────
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .ai_handler import get_ai_response


@csrf_protect
@require_http_methods(['GET', 'POST'])
def counselor_chat(request):
    """
    GET  → Show empty chat interface
    POST → Process user message, return AI response
    """
    context = {
        'user_message': '',
        'response': '',
        'error': '',
    }

    if request.method == 'POST':
        user_message = request.POST.get('user_message', '').strip()

        if not user_message:
            context['error'] = 'Please type a message before sending.'
        elif len(user_message) > 2000:
            context['error'] = 'Your message is too long. Please keep it under 2000 characters.'
        else:
            try:
                ai_response = get_ai_response(user_message)
                context['user_message'] = user_message
                context['response'] = ai_response
            except Exception as e:
                context['error'] = 'Something went wrong. Please try again in a moment.'
                print(f"[G-TEC AI] View error: {e}")

    return render(request, 'index.html', context)


# ── counselor/urls.py ────────────────────────────────────────
from django.urls import path
from . import views

app_name = 'counselor'

urlpatterns = [
    path('', views.counselor_chat, name='chat'),
]


# ── myproject/urls.py (root — add this) ─────────────────────
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('counselor.urls')),      # G-TEC chat at root
#     # ... your other apps
# ]


# ── requirements (add to requirements.txt) ──────────────────
# markdown==3.5.2        ← converts AI Markdown → HTML
# anthropic==0.17.0      ← optional, for Claude API


# ── settings.py (add these) ─────────────────────────────────
# from decouple import config
# ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')
# # Without API key: smart rule-based responses activate automatically


# ── .env file ───────────────────────────────────────────────
# ANTHROPIC_API_KEY=sk-ant-your-key-here   # Optional
# SECRET_KEY=your-django-secret-key
# DEBUG=True


# ── HOW TO RUN ───────────────────────────────────────────────
# pip install django markdown anthropic python-decouple
# python manage.py startapp counselor
# Copy views.py, urls.py, ai_handler.py into counselor/
# Copy index.html into templates/
# Add 'counselor' to INSTALLED_APPS in settings.py
# Add path to root urls.py
# python manage.py runserver
# Visit: http://127.0.0.1:8000/
