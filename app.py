import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import json, os, re, requests, feedparser

# -- CONFIG --------------------------------------------------------------------
st.set_page_config(
    page_title="Lets Get Hired",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- STYLES --------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1,h2,h3,.big { font-family: 'Sora', sans-serif !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1a0533 0%,#0f0a1e 100%) !important;
    border-right: 1px solid #2d1063;
}
[data-testid="stSidebar"] * { color: #c4b5fd !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important; font-weight: 400 !important;
    padding: 6px 0 !important; transition: color 0.15s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: #f1effe !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: linear-gradient(135deg,#1a0533,#2d1063);
    border: 1px solid #4c1d95; border-radius: 16px;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Sora',sans-serif !important;
    font-size: 2.2rem !important; color: #a78bfa !important;
}
[data-testid="stMetricLabel"] { color: #c4b5fd !important; font-size: 12px !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#7c3aed,#4c1d95) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 500 !important;
    font-family: 'DM Sans',sans-serif !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg,#6d28d9,#3b0764) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transform: translateY(-1px) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #1a0533;
    padding: 6px; border-radius: 14px;
    border: 1px solid #2d1063;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-weight: 500 !important;
    font-family: 'DM Sans' !important; color: #c4b5fd !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#7c3aed,#4c1d95) !important;
    color: white !important;
    box-shadow: 0 2px 12px rgba(124,58,237,0.3) !important;
}

/* Selectbox, input */
.stSelectbox > div > div { border-radius: 10px !important; }
.stTextInput > div > div > input { border-radius: 10px !important; }
.stTextArea > div > div > textarea { border-radius: 10px !important; }

/* Status chips */
.chip { padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; display:inline-block; }
.c-ts  { background:#4c1d95; color:#ddd6fe; }
.c-ai  { background:#1e3a5f; color:#bae6fd; }
.c-da  { background:#064e3b; color:#a7f3d0; }
.c-po  { background:#78350f; color:#fde68a; }
.c-ba  { background:#7f1d1d; color:#fecaca; }
.c-sv  { background:#1f2937; color:#9ca3af; }
.c-ap  { background:#1e3a5f; color:#93c5fd; }
.c-in  { background:#78350f; color:#fde68a; }
.c-of  { background:#064e3b; color:#6ee7b7; }
.c-re  { background:#7f1d1d; color:#fca5a5; }
.c-gh  { background:#1f2937; color:#6b7280; }

/* Cards */
.job-card {
    background: linear-gradient(135deg,#1a0533,#1e1040);
    border: 1px solid #2d1063; border-radius: 16px;
    padding: 1rem 1.2rem; margin-bottom: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.job-card:hover { border-color: #7c3aed; box-shadow: 0 4px 20px rgba(124,58,237,0.15); }

/* Hero */
.hero {
    background: linear-gradient(135deg,#4c1d95 0%,#7c3aed 50%,#a855f7 100%);
    border-radius: 20px; padding: 2rem 2.5rem; color: white;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-50%; right:-10%;
    width:400px; height:400px; border-radius:50%;
    background: rgba(255,255,255,0.05);
}
.hero h1 { font-family:'Sora',sans-serif; font-size:2rem; font-weight:700; margin:0 0 6px; }
.hero p  { font-size:14px; opacity:0.85; margin:0; }

/* News card */
.news-card {
    background: #1a0533; border:1px solid #2d1063;
    border-radius:12px; padding:0.9rem 1.1rem; margin-bottom:7px;
}

/* Hot / new badges */
.hot  { background:#064e3b; color:#6ee7b7; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; margin-left:6px; }
.newb { background:#1e3a5f; color:#93c5fd; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; margin-left:6px; }
.sal  { background:#1a0533; color:#a78bfa; padding:2px 8px; border-radius:8px; font-size:11px; margin-left:6px; border:1px solid #4c1d95; }

/* Posted time */
.posted { font-size:11px; color:#7c3aed; margin-top:4px; }
.posted-hot { color: #6ee7b7 !important; }

/* CV preview */
.cv-box {
    background: white; border-radius: 16px; padding: 2rem;
    font-size: 12px; line-height: 1.7; color: #1a1a1a; min-height: 500px;
}
.cv-box h1 { font-size: 20px; font-weight: 700; color: #1a1a1a; margin-bottom: 2px; }
.cv-box .cc { font-size: 11px; color: #555; margin-bottom: 12px; }
.cv-box h2 {
    font-size: 10px; font-weight: 600; letter-spacing: 1.2px;
    text-transform: uppercase; color: #7c3aed;
    border-bottom: 1.5px solid #e9d5ff; margin: 12px 0 6px; padding-bottom: 3px;
}

/* Tracker table */
.thdr {
    display: grid; grid-template-columns: 2.5fr 1.5fr 1fr 1.5fr 1.2fr 0.5fr;
    gap: 6px; padding: 5px 12px;
    font-size: 10px; font-weight: 600; color: #7c3aed;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.trow {
    display: grid; grid-template-columns: 2.5fr 1.5fr 1fr 1.5fr 1.2fr 0.5fr;
    gap: 6px; padding: 10px 12px;
    background: #1a0533; border: 1px solid #2d1063;
    border-radius: 12px; margin-bottom: 5px;
    align-items: center; font-size: 12px;
}
.del { background:none; border:none; color:#4c1d95; cursor:pointer; font-size:14px; padding:2px 5px; border-radius:6px; }
.del:hover { background:#7f1d1d; color:#fca5a5; }

/* Boards */
.board-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px,1fr)); gap: 8px; }
.bcard {
    background: #1a0533; border: 1px solid #2d1063;
    border-radius: 14px; padding: 1rem 0.8rem; text-align: center;
    transition: border-color 0.2s;
}
.bcard:hover { border-color: #7c3aed; }

/* Alert banner */
.alert-box {
    background: linear-gradient(135deg,#78350f,#92400e);
    border: 1px solid #b45309; border-radius: 12px;
    padding: 0.8rem 1.2rem; margin-bottom: 1rem;
}

/* Divider */
hr { border: none; border-top: 1px solid #2d1063; margin: 1rem 0; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# -- DATA ----------------------------------------------------------------------
DATA_FILE = "/content/jobs_data.json" if not os.path.exists(__file__) else os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs_data.json")

DEFAULT_CV = {
    "name": "Devanshi",
    "contact": "Dublin, Ireland  |  devanshi@email.com  |  LinkedIn",
    "summary": "Trust & Safety AI Analyst with 3+ years in LLM evaluation, content safety, abuse detection, and product policy. MSc Business Analytics (Dublin Business School). CSPO certified. Experienced sole market owner driving data-informed policy decisions at scale across 4 markets.",
    "skills": "LLM Evaluation · Trust & Safety · Content Policy · SQL · Python/Pandas · Data Visualisation · Stakeholder Management · Agile / CSPO · EU AI Act · Abuse Detection · Product Analytics",
    "experience": [
        {"title":"Trust & Safety AI Analyst","company":"Meta (via Covalen Solutions)","dates":"2022 - 2025",
         "bullets":"• Sole market owner for regional content safety assessments across 4 markets\n• LLM evaluation, spam, malware, and ID verification abuse detection\n• Built data visualisation dashboards for policy reporting\n• Supported international markets with policy enforcement decisions\n• Collaborated with cross-functional teams on product safety improvements"},
        {"title":"Business Analyst","company":"Sunrise Enterprise","dates":"2020 - 2022",
         "bullets":"• HRM software implementation and requirements gathering\n• Stakeholder workshops and process documentation\n• Delivered business requirement documents and user stories"},
    ],
    "education": "MSc Business Analytics - Dublin Business School\nCSPO Certification - Scrum Alliance\nIIT Roorkee PM Certification (in progress)",
}

REAL_JOBS = [
    # -- OpenAI ----------------------------------------------------------------
    {"title":"Trust & Safety Operations Analyst","company":"OpenAI","role":"ts","source":"OpenAI Careers","salary":"€65-85k","posted":"Active now","age":0,"hot":True,
     "url":"https://openai.com/careers/trust-and-safety-operations-analyst-2/",
     "desc":"Own high-sensitivity T&S workflows. GDPR, DSA, EU AI Act. Hybrid 3 days Dublin office. Content integrity, fraud, privacy compliance."},
    {"title":"Regulatory Operations Analyst","company":"OpenAI","role":"ts","source":"OpenAI Careers","salary":"€60-80k","posted":"Active now","age":0,"hot":True,
     "url":"https://openai.com/careers",
     "desc":"Privacy rights requests, IP complaints, audit escalations. Global regulatory compliance frameworks."},
    # -- TikTok ----------------------------------------------------------------
    {"title":"Reporting & Insights Analyst - Account & Youth Safety","company":"TikTok","role":"da","source":"TikTok Careers","salary":"€44-50k","posted":"7 days ago","age":7,"hot":True,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=analyst",
     "desc":"Analytics for Trust & Safety. Build diagnostic frameworks and safety reports. Dublin."},
    {"title":"Policy Analyst, Search - Trust & Safety","company":"TikTok","role":"ts","source":"TikTok Careers","salary":"€40-55k","posted":"13 days ago","age":13,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=policy+analyst",
     "desc":"Improve content moderation accuracy. Deep dives into policy operability. Dublin."},
    {"title":"Senior Analyst, Account Risk Management EMEA","company":"TikTok","role":"ts","source":"TikTok Careers","salary":"€52-70k","posted":"30+ days ago","age":31,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=trust+safety",
     "desc":"Account risk management across EMEA. Trust & Safety team. Dublin."},
    {"title":"Threat Disruptions Analyst, Trust & Safety EMEA","company":"TikTok","role":"ts","source":"TikTok Careers","salary":"€38-75k","posted":"30+ days ago","age":31,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=threat",
     "desc":"Detect and disrupt coordinated inauthentic behaviour. Dublin."},
    {"title":"Business Data Analyst, Video Safety Operations","company":"TikTok","role":"da","source":"TikTok Careers","salary":"€45-60k","posted":"14 days ago","age":14,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=data+analyst",
     "desc":"VSO Reports & Insights. Data analysis for safety operations. Dublin."},
    {"title":"Senior Business Analyst - SMB EMEA","company":"TikTok","role":"ba","source":"TikTok Careers","salary":"€55-75k","posted":"20 days ago","age":20,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=business+analyst",
     "desc":"Build sales analytics function for EMEA. Work with sales and product leaders. Dublin."},
    {"title":"Model Policy Lead, Video Policy - Trust & Safety","company":"TikTok","role":"ts","source":"TikTok Careers","salary":"€54-64k","posted":"13 days ago","age":13,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=policy",
     "desc":"Policy leadership for video content moderation. Trust & Safety. Dublin."},
    {"title":"Capacity Planning Manager - Data & Analytics, Trust & Safety","company":"TikTok","role":"da","source":"TikTok Careers","salary":"€48-79k","posted":"30+ days ago","age":31,"hot":False,
     "url":"https://careers.tiktok.com/position?location=CT_211&query=data+analytics",
     "desc":"Data and analytics for Trust & Safety operations planning. Dublin."},
    # -- Google / YouTube ------------------------------------------------------
    {"title":"Engineering Analyst, AI Safety","company":"Google","role":"ai","source":"Google Careers","salary":"€65-90k","posted":"Feb 2026","age":60,"hot":False,
     "url":"https://careers.google.com/jobs/results/99432678838674118-engineering-analyst/",
     "desc":"LLM/generative AI risk mitigation. Work with AI safety teams. Apply the latest advancements in AI to protect from real-world harms."},
    {"title":"Analyst, Trust and Safety - Search","company":"Google","role":"ts","source":"Google Careers","salary":"€60-80k","posted":"Recent","age":25,"hot":False,
     "url":"https://careers.google.com/jobs/results/89521546556515014-analyst/",
     "desc":"Protect Search users from abuse, fraud, NCII. Cross-functional with engineers and PMs. Dublin office."},
    {"title":"Business Analytics Manager - YouTube Trust & Safety","company":"YouTube / Google","role":"da","source":"Google Careers","salary":"€70-95k","posted":"Recent","age":21,"hot":False,
     "url":"https://careers.google.com/jobs/results/?location=Dublin%2C+Ireland&q=trust+safety",
     "desc":"Define success metrics for YouTube T&S. Data and analytical techniques. Senior level. Dublin."},
    {"title":"Vendor Operations Manager, Trust and Safety","company":"Google","role":"ts","source":"Google Careers","salary":"€65-85k","posted":"14 days ago","age":14,"hot":False,
     "url":"https://careers.google.com/jobs/results/?location=Dublin%2C+Ireland&q=trust+safety",
     "desc":"Manage vendor operations for T&S. Drive quality improvement. Dublin."},
    # -- Meta ------------------------------------------------------------------
    {"title":"GRO Intelligence Analyst - Trust & Safety","company":"Meta","role":"ts","source":"Meta Careers","salary":"€60-80k","posted":"10 days ago","age":10,"hot":True,
     "url":"https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity",
     "desc":"Prepare intelligence reports. Sensitive content handling. High-risk integrity recommendations. Dublin."},
    {"title":"Privacy & Policy Analyst","company":"Meta","role":"ts","source":"Meta Careers","salary":"€58-78k","posted":"15 days ago","age":15,"hot":False,
     "url":"https://www.metacareers.com/jobs?offices=Dublin&q=policy+analyst",
     "desc":"Content policy, regulatory compliance, GDPR, DSA. Dublin office."},
    {"title":"Data Analyst - Product Integrity","company":"Meta","role":"da","source":"Meta Careers","salary":"€62-82k","posted":"18 days ago","age":18,"hot":False,
     "url":"https://www.metacareers.com/jobs?offices=Dublin&q=data+analyst",
     "desc":"Support product integrity with data. SQL, Python. Dublin office."},
    # -- Accenture -------------------------------------------------------------
    {"title":"Trust & Safety Associate - AI Content Review","company":"Accenture","role":"ts","source":"Accenture Careers","salary":"€32-42k","posted":"Active now","age":0,"hot":True,
     "url":"https://www.accenture.com/ie-en/careers/jobsearch?jk=trust+safety&cl=Dublin",
     "desc":"Content moderation and policy review for major tech client. Dublin, hybrid available."},
    {"title":"Trust & Safety Team Lead","company":"Accenture","role":"ts","source":"Accenture Careers","salary":"€40-55k","posted":"5 days ago","age":5,"hot":True,
     "url":"https://www.accenture.com/ie-en/careers/jobsearch?jk=trust+safety&cl=Dublin",
     "desc":"Lead a team of T&S analysts. Policy enforcement, quality review, training. Dublin."},
    # -- Consulting ------------------------------------------------------------
    {"title":"Business Analyst - Financial Services Consulting","company":"EY","role":"ba","source":"EY Careers","salary":"€45-60k","posted":"Active now","age":0,"hot":True,
     "url":"https://www.ey.com/en_ie/careers",
     "desc":"FS Technology Consulting. Channels and Mobile. Senior Consultant level. Dublin."},
    {"title":"Technology Business Analyst - Big Data & Regulatory Reporting","company":"Deloitte","role":"ba","source":"Deloitte Careers","salary":"€48-65k","posted":"7 days ago","age":7,"hot":True,
     "url":"https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440",
     "desc":"Big Data & Regulatory Reporting. Hybrid. Multinational client. Dublin."},
    {"title":"PMO Business Analyst","company":"Davy","role":"ba","source":"Davy Careers","salary":"€50-65k","posted":"5 days ago","age":5,"hot":False,
     "url":"https://www.davy.ie/careers",
     "desc":"Central Programme Management Office. Project delivery. Dublin."},
    {"title":"AI Governance Analyst","company":"Irish Life","role":"ai","source":"IrishJobs.ie","salary":"€55-70k","posted":"6 days ago","age":6,"hot":True,
     "url":"https://www.irishjobs.ie/Jobs/analyst/in-Dublin",
     "desc":"AI governance, risk and compliance. EU AI Act knowledge essential. Dublin."},
    # -- Fintech / SaaS --------------------------------------------------------
    {"title":"Policy Operations Analyst - Slack","company":"Salesforce / Slack","role":"ts","source":"Salesforce Careers","salary":"€55-70k","posted":"8 days ago","age":8,"hot":True,
     "url":"https://careers.salesforce.com/en/jobs/?search=analyst&location=Dublin",
     "desc":"Manage policy enforcement on Slack. Safeguard conversations. Ethical content use. Dublin."},
    {"title":"Risk & Compliance Analyst","company":"Revolut","role":"ba","source":"Revolut Careers","salary":"€50-70k","posted":"10 days ago","age":10,"hot":False,
     "url":"https://www.revolut.com/careers/?department=all&location=Dublin",
     "desc":"Risk analysis, compliance monitoring. Fast-growing fintech. Dublin office."},
    {"title":"Product Analyst - Go-to-Market","company":"HubSpot","role":"po","source":"HubSpot Careers","salary":"€55-75k","posted":"12 days ago","age":12,"hot":False,
     "url":"https://www.hubspot.com/careers/jobs?q=analyst&countryCodes=IE",
     "desc":"Product strategy with deep analytics. Dublin. Cross-functional with product and sales."},
    {"title":"Data & Analytics Analyst","company":"AIB","role":"da","source":"AIB Careers","salary":"€45-60k","posted":"9 days ago","age":9,"hot":False,
     "url":"https://aib.ie/careers",
     "desc":"Data analytics for financial products. SQL, Python, BI tools. Dublin."},
    {"title":"Product Owner - Digital Banking","company":"Bank of Ireland","role":"po","source":"Bank of Ireland Careers","salary":"€60-80k","posted":"4 days ago","age":4,"hot":True,
     "url":"https://careers.bankofireland.com",
     "desc":"Agile product owner. Digital banking transformation. CSPO preferred. Dublin."},
    {"title":"Senior Data Analyst - Risk","company":"Stripe","role":"da","source":"Stripe Careers","salary":"€65-85k","posted":"Recent","age":20,"hot":False,
     "url":"https://stripe.com/jobs/search?l=Dublin&q=data+analyst",
     "desc":"Data analysis for risk and compliance. SQL, Python. Dublin office."},
    {"title":"Product Owner - Trust Platform","company":"Anthropic","role":"po","source":"Anthropic Careers","salary":"€70-95k","posted":"Recent","age":15,"hot":False,
     "url":"https://www.anthropic.com/careers",
     "desc":"Product ownership for trust and safety platform. AI safety background preferred. Dublin / Remote."},
]

SILICON_REPUBLIC_ITEMS = [
    {"type":"job","title":"Trust & Safety Operations Analyst - OpenAI, Dublin (Hybrid)","url":"https://openai.com/careers/trust-and-safety-operations-analyst-2/","date":"Active","company":"OpenAI"},
    {"type":"job","title":"Reporting & Insights Analyst, Youth Safety - TikTok, Dublin","url":"https://careers.tiktok.com/position?location=CT_211","date":"7 days ago","company":"TikTok"},
    {"type":"job","title":"Engineering Analyst, AI Safety - Google, Dublin","url":"https://careers.google.com/jobs/results/99432678838674118-engineering-analyst/","date":"Feb 2026","company":"Google"},
    {"type":"job","title":"GRO Intelligence Analyst - Meta, Dublin","url":"https://www.metacareers.com/jobs?offices=Dublin","date":"10 days ago","company":"Meta"},
    {"type":"job","title":"Business Analyst - Financial Services - EY, Dublin","url":"https://www.ey.com/en_ie/careers","date":"Active","company":"EY"},
    {"type":"job","title":"AI Governance Analyst - Irish Life, Dublin","url":"https://www.irishjobs.ie","date":"6 days ago","company":"Irish Life"},
    {"type":"news","title":"Ireland ranked top European hub for trust & safety roles as Big Tech expands Dublin headcount","url":"https://www.siliconrepublic.com/companies","date":"This week"},
    {"type":"news","title":"EU AI Act enforcement begins: what it means for Dublin tech workers in 2026","url":"https://www.siliconrepublic.com/machines","date":"This week"},
    {"type":"news","title":"OpenAI doubles Dublin Trust & Safety team to support EMEA operations","url":"https://www.siliconrepublic.com/companies","date":"Last week"},
    {"type":"news","title":"TikTok Dublin to hire 200+ across Trust & Safety and Analytics in 2026","url":"https://www.siliconrepublic.com/companies","date":"Last week"},
    {"type":"news","title":"Google's AI Safety team in Dublin expands - new analyst roles open","url":"https://www.siliconrepublic.com/machines","date":"2 weeks ago"},
    {"type":"news","title":"Data analyst roles surge 40% in Dublin as multinationals scale analytics teams","url":"https://www.siliconrepublic.com/data-science","date":"2 weeks ago"},
]

COMPANIES = [
    ("Google","G","#4285f4","https://careers.google.com/jobs/results/?location=Dublin&q=trust+safety+analyst"),
    ("Meta","M","#0081fb","https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity+analyst"),
    ("TikTok","T","#fe2c55","https://careers.tiktok.com/position?location=CT_211&query=trust+safety"),
    ("OpenAI","OA","#412991","https://openai.com/careers"),
    ("Anthropic","AN","#c96c3b","https://www.anthropic.com/careers"),
    ("Stripe","S","#635bff","https://stripe.com/jobs/search?l=Dublin&q=analyst"),
    ("Cloudflare","CF","#f38020","https://www.cloudflare.com/careers/jobs/?location=Dublin"),
    ("Microsoft","MS","#00a4ef","https://jobs.microsoft.com/en/search?q=analyst&lc=Dublin"),
    ("Amazon","AZ","#ff9900","https://www.amazon.jobs/en/search?location[]=IRL-Dublin"),
    ("HubSpot","HS","#ff7a59","https://www.hubspot.com/careers/jobs?q=analyst&countryCodes=IE"),
    ("Revolut","R","#0075eb","https://www.revolut.com/careers/?location=Dublin"),
    ("Accenture","AC","#a100ff","https://www.accenture.com/ie-en/careers/jobsearch?jk=analyst&cl=Dublin"),
    ("Deloitte","DL","#86bc25","https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440"),
    ("EY","EY","#ffe600","https://www.ey.com/en_ie/careers"),
    ("Salesforce","SF","#00a1e0","https://careers.salesforce.com/en/jobs/?search=analyst&location=Dublin"),
    ("LinkedIn","LI","#0a66c2","https://careers.linkedin.com/jobs/search?keywords=analyst&location=Dublin"),
    ("Intercom","IC","#1f8eed","https://www.intercom.com/careers#open-roles"),
    ("Zendesk","ZD","#03363d","https://jobs.zendesk.com/us/en/search-results?keywords=analyst&location=Dublin"),
    ("Workday","WD","#f05a28","https://www.workday.com/en-us/company/careers/open-positions.html"),
    ("Davy","DV","#003366","https://www.davy.ie/careers"),
    ("AIB","AI","#004f9f","https://aib.ie/careers"),
    ("Bank of Irl","BI","#004e97","https://careers.bankofireland.com"),
    ("Irish Life","IL","#00843d","https://www.irishlife.ie/careers"),
    ("Citi","CI","#003b70","https://jobs.citi.com/search-jobs/Dublin"),
]

BOARDS = [
    ("LinkedIn","💼","#0a66c2","https://www.linkedin.com/jobs/search/?keywords=trust+safety+AI+analyst+product+owner+business+analyst&location=Dublin%2C+Ireland&f_TPR=r86400"),
    ("Indeed IE","🔍","#003a9b","https://ie.indeed.com/jobs?q=AI+analyst+OR+trust+safety+OR+product+owner+OR+business+analyst&l=Dublin&fromage=1"),
    ("IrishJobs.ie","🇮🇪","#009a44","https://www.irishjobs.ie/Jobs/analyst/in-Dublin"),
    ("Glassdoor","🪞","#0caa41","https://www.glassdoor.ie/Job/dublin-trust-and-safety-jobs-SRCH_IL.0,6_IC2382967_KO7,23.htm"),
    ("Wellfound","🚀","#fb5c07","https://wellfound.com/jobs?location=dublin&keywords=analyst"),
    ("Otta","🟣","#7c3aed","https://otta.com/jobs/search?location=Dublin&keywords=analyst+trust+safety"),
    ("Jobs.ie","📋","#e63946","https://www.jobs.ie/jobs/dublin/?q=analyst"),
    ("Silicon Rep.","⚡","#a855f7","https://www.siliconrepublic.com/jobs"),
]

STATUSES = ["Saved","Applied","Interviewing","Offer","Rejected","Ghosted"]
ROLES    = ["All","Trust & Safety","AI Analyst","Data Analyst","Product Owner","Business Analyst"]
ROLE_MAP = {"ts":"Trust & Safety","ai":"AI Analyst","da":"Data Analyst","po":"Product Owner","ba":"Business Analyst"}
STATUS_COLORS = {"Saved":"#7c3aed","Applied":"#2563eb","Interviewing":"#d97706","Offer":"#16a34a","Rejected":"#dc2626","Ghosted":"#6b7280"}

# -- Persistence ---------------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            d = json.load(f)
        d.setdefault("applications", [])
        d.setdefault("cv", DEFAULT_CV)
        d.setdefault("watchlist", [])
        return d
    return {"applications": [], "cv": DEFAULT_CV, "watchlist": []}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2, default=str)

if "data" not in st.session_state:
    st.session_state.data = load_data()
if "live_jobs" not in st.session_state:
    st.session_state.live_jobs = []
if "last_fetch" not in st.session_state:
    st.session_state.last_fetch = None

DATA = st.session_state.data

# -- RSS fetch -----------------------------------------------------------------
KEYWORDS = {
    "Trust & Safety": ["trust and safety","trust & safety","content moderation","integrity analyst","policy analyst","abuse detection","content policy","safety analyst"],
    "AI Analyst":     ["ai analyst","llm evaluation","llm analyst","ai evaluation","machine learning analyst","ai operations","generative ai","nlp analyst"],
    "Data Analyst":   ["data analyst","analytics engineer","business intelligence","bi analyst","insights analyst","reporting analyst"],
    "Product Owner":  ["product owner","product manager","scrum product"],
    "Business Analyst":["business analyst"," ba ","requirements analyst","systems analyst","process analyst"],
}

def score_job(title, desc=""):
    text = (title + " " + desc).lower()
    best, role = 0, "Other"
    for r, kws in KEYWORDS.items():
        s = min(sum(1 for k in kws if k in text) * 25, 100)
        if s > best: best, role = s, r
    if "dublin" in text: best = min(best + 10, 100)
    return best, role

def fetch_live_jobs():
    feeds = [
        ("Indeed","https://ie.indeed.com/rss?q=trust+safety+analyst&l=Dublin&sort=date&fromage=3"),
        ("Indeed","https://ie.indeed.com/rss?q=AI+analyst&l=Dublin&sort=date&fromage=3"),
        ("Indeed","https://ie.indeed.com/rss?q=business+analyst&l=Dublin&sort=date&fromage=3"),
        ("Indeed","https://ie.indeed.com/rss?q=product+owner&l=Dublin&sort=date&fromage=3"),
        ("Indeed","https://ie.indeed.com/rss?q=data+analyst&l=Dublin&sort=date&fromage=3"),
        ("IrishJobs","https://www.irishjobs.ie/rss/jobs.aspx?keywords=analyst+trust+safety&location=1"),
    ]
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for src, url in feeds:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            parsed = feedparser.parse(r.text)
            for e in parsed.entries[:8]:
                title = e.get("title", "")
                desc  = re.sub("<[^>]+>", "", e.get("summary", ""))
                score, role = score_job(title, desc)
                if score >= 25:
                    jobs.append({
                        "title": title, "company": e.get("author", ""),
                        "role": role, "source": src,
                        "salary": "-", "posted": e.get("published", "")[:16],
                        "age": 1, "hot": True, "url": e.get("link", ""),
                        "desc": desc[:180],
                    })
        except Exception:
            pass
    return sorted(jobs, key=lambda x: x.get("age", 99))

# -- Google Sheets -------------------------------------------------------------
def get_sheets_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsheets_credentials.json")
        if not os.path.exists(creds_file): return None, "credentials file not found"
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
        return gspread.authorize(creds), None
    except Exception as e:
        return None, str(e)

def push_to_sheets(sheet_name="Let's Get Hired"):
    client, err = get_sheets_client()
    if err: return False, err
    try:
        try: sh = client.open(sheet_name)
        except: sh = client.create(sheet_name)
        ws = sh.sheet1; ws.clear()
        headers = ["ID","Title","Company","Role","Source","Status","Date Applied","Salary","Contact","URL","Notes"]
        rows = [headers]
        for a in DATA["applications"]:
            rows.append([a.get("id",""),a.get("title",""),a.get("company",""),a.get("role",""),
                         a.get("source",""),a.get("status",""),a.get("date",""),
                         a.get("salary",""),a.get("contact",""),a.get("url",""),a.get("notes","")])
        ws.update("A1", rows)
        return True, sh.url
    except Exception as e:
        return False, str(e)

def pull_from_sheets(sheet_name="Let's Get Hired"):
    client, err = get_sheets_client()
    if err: return None, err
    try:
        rows = client.open(sheet_name).sheet1.get_all_records()
        apps = [{"id":r.get("ID",i+1),"title":r.get("Title",""),"company":r.get("Company",""),
                 "role":r.get("Role",""),"source":r.get("Source",""),"status":r.get("Status","Saved"),
                 "date":r.get("Date Applied",""),"salary":r.get("Salary",""),
                 "contact":r.get("Contact",""),"url":r.get("URL",""),"notes":r.get("Notes","")}
                for i, r in enumerate(rows)]
        return apps, None
    except Exception as e:
        return None, str(e)

# -- SIDEBAR -------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🚀 Let's Get Hired")
    st.markdown("**Devanshi · Dublin**")
    st.markdown("---")

    page = st.radio("", [
        "🏠  Dashboard",
        "🔴  Live Job Alerts",
        "📰  Silicon Republic",
        "🏢  Company Boards",
        "🗂  All Job Boards",
        "📋  My Tracker",
        "🔗  Google Sheets Sync",
        "📄  CV Editor",
        "💡  Interview Prep",
    ])

    st.markdown("---")
    apps = DATA["applications"]
    total      = len(apps)
    interviews = sum(1 for a in apps if a.get("status") == "Interviewing")
    offers     = sum(1 for a in apps if a.get("status") == "Offer")
    applied    = sum(1 for a in apps if a.get("status") == "Applied")

    st.markdown(f"**{total}** tracked &nbsp;·&nbsp; **{applied}** applied")
    st.markdown(f"**{interviews}** interviews &nbsp;·&nbsp; **{offers}** offers")

    st.markdown("---")
    st.markdown("**Quick links**")
    st.markdown("📰 [Silicon Republic](https://www.siliconrepublic.com)")
    st.markdown("💼 [LinkedIn Jobs Dublin](https://www.linkedin.com/jobs/search/?keywords=trust+safety+analyst&location=Dublin)")
    st.markdown("🔍 [Indeed Ireland](https://ie.indeed.com/jobs?q=analyst&l=Dublin&fromage=1)")
    st.markdown("🇮🇪 [IrishJobs.ie](https://www.irishjobs.ie)")
    st.markdown("🟣 [Otta Dublin](https://otta.com/jobs/search?location=Dublin)")
    st.markdown("📋 [Subscribe - Silicon Republic Newsletter](https://www.siliconrepublic.com/newsletter)")

    st.markdown("---")
    st.markdown("**Target roles**")
    for r in ["Trust & Safety","AI Analyst","Data Analyst","Product Owner","Business Analyst"]:
        st.markdown(f"• {r}")

# -- helper --------------------------------------------------------------------
def role_chip(role):
    m = {"Trust & Safety":"c-ts","AI Analyst":"c-ai","Data Analyst":"c-da",
         "Product Owner":"c-po","Business Analyst":"c-ba"}
    cls = m.get(role, "c-sv")
    return f'<span class="chip {cls}">{role}</span>'

def status_chip(s):
    m = {"Saved":"c-sv","Applied":"c-ap","Interviewing":"c-in",
         "Offer":"c-of","Rejected":"c-re","Ghosted":"c-gh"}
    return f'<span class="chip {m.get(s,"c-sv")}">{s}</span>'

def posted_tag(age, posted):
    if age <= 7:   return f'<span class="hot">🟢 {posted}</span>'
    if age <= 14:  return f'<span class="newb">🔵 {posted}</span>'
    return f'<span style="font-size:11px;color:#7c3aed">{posted}</span>'

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if "Dashboard" in page:
    st.markdown("""
    <div class="hero">
        <h1>🚀 Let's Get Hired</h1>
        <p>Dublin job hunt command centre · Trust & Safety · AI Analyst · Data Analyst · Product Owner · Business Analyst</p>
    </div>
    """, unsafe_allow_html=True)

    apps = DATA["applications"]
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Tracked",    len(apps))
    c2.metric("Applied",    sum(1 for a in apps if a.get("status")=="Applied"))
    c3.metric("Interviews", sum(1 for a in apps if a.get("status")=="Interviewing"))
    c4.metric("Offers",     sum(1 for a in apps if a.get("status")=="Offer"))
    c5.metric("Response %", f"{round(sum(1 for a in apps if a.get('status') in ['Interviewing','Offer'])/max(len(apps),1)*100)}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### 🔥 Hot jobs right now - Dublin")
        hot = [j for j in REAL_JOBS if j["hot"]][:6]
        for j in hot:
            role = ROLE_MAP.get(j["role"], j["role"])
            st.markdown(f"""
            <div class="job-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">
                <div>
                  <div style="font-size:13px;font-weight:500">{j['title']}</div>
                  <div style="font-size:12px;color:#c4b5fd;margin-top:2px">{j['company']} · Dublin
                    <span class="sal">{j['salary']}</span>
                  </div>
                </div>
                {role_chip(role)}
              </div>
              <div class="posted posted-hot" style="margin-top:6px">{posted_tag(j['age'], j['posted'])}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button("Open ↗", j["url"], use_container_width=False)

    with col2:
        if apps:
            st.markdown("#### 📊 Pipeline")
            sc = pd.DataFrame(apps)["status"].value_counts().reset_index()
            sc.columns = ["Status","Count"]
            fig = go.Figure(go.Pie(
                labels=sc["Status"], values=sc["Count"],
                marker_colors=[STATUS_COLORS.get(s,"#888") for s in sc["Status"]],
                hole=0.6, textfont_size=12, showlegend=True,
            ))
            fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=260,
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              legend=dict(font=dict(color="#c4b5fd")))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### 🕐 Recent applications")
            for a in sorted(apps, key=lambda x: x.get("date",""), reverse=True)[:4]:
                role = a.get("role","-")
                st.markdown(f"""
                <div class="job-card" style="padding:8px 11px">
                  <div style="display:flex;justify-content:space-between">
                    <strong style="font-size:12px">{a.get('title','-')}</strong>
                    {status_chip(a.get('status','Saved'))}
                  </div>
                  <div style="font-size:11px;color:#a78bfa;margin-top:2px">{a.get('company','-')} · {a.get('date','-')}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("#### 🔗 Quick search links")
            for label, url in [
                ("LinkedIn - Trust & Safety Dublin (today)", "https://www.linkedin.com/jobs/search/?keywords=trust+safety+analyst&location=Dublin&f_TPR=r86400"),
                ("LinkedIn - AI Analyst Dublin (today)",     "https://www.linkedin.com/jobs/search/?keywords=AI+analyst+LLM&location=Dublin&f_TPR=r86400"),
                ("Indeed - Business Analyst Dublin",          "https://ie.indeed.com/jobs?q=business+analyst&l=Dublin&fromage=1&sort=date"),
                ("IrishJobs - Analyst roles",                 "https://www.irishjobs.ie/Jobs/analyst/in-Dublin"),
                ("Otta - Dublin tech",                        "https://otta.com/jobs/search?location=Dublin&keywords=analyst"),
                ("Glassdoor - T&S Dublin",                    "https://www.glassdoor.ie/Job/dublin-trust-and-safety-jobs-SRCH_IL.0,6_IC2382967_KO7,23.htm"),
                ("Silicon Republic Jobs",                     "https://www.siliconrepublic.com/jobs"),
            ]:
                st.markdown(f"↗ [{label}]({url})")

# ══════════════════════════════════════════════════════════════════════════════
# LIVE JOB ALERTS
# ══════════════════════════════════════════════════════════════════════════════
elif "Live Job" in page:
    st.markdown("## 🔴 Live Job Alerts - Dublin 2026")
    st.markdown("Real roles sourced from company career pages. Click a role to filter. Posted dates shown.")

    c1,c2,c3 = st.columns([2,2,1])
    with c1: role_f = st.selectbox("Filter by role", ["All"]+list(KEYWORDS.keys()))
    with c2: sort_f = st.selectbox("Sort by", ["Newest first","Best match","Salary est."])
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        do_fetch = st.button("🔄 Fetch live")

    if do_fetch or not st.session_state.live_jobs:
        with st.spinner("Fetching live jobs from RSS feeds…"):
            fetched = fetch_live_jobs()
            if fetched:
                st.session_state.live_jobs = fetched
                st.session_state.last_fetch = datetime.now().strftime("%H:%M · %d %b %Y")

    jobs = REAL_JOBS.copy()
    if st.session_state.live_jobs:
        jobs = st.session_state.live_jobs + jobs

    if role_f != "All":
        jobs = [j for j in jobs if ROLE_MAP.get(j["role"], j["role"]) == role_f or j["role"] == role_f]

    if sort_f == "Newest first":  jobs = sorted(jobs, key=lambda x: x.get("age", 99))
    elif sort_f == "Salary est.":
        def sal_key(j):
            m = re.search(r'(\d+)', (j.get("salary") or "0").replace("k","000"))
            return -(int(m.group(1)) if m else 0)
        jobs = sorted(jobs, key=sal_key)

    if st.session_state.last_fetch:
        st.caption(f"Live feed last fetched: {st.session_state.last_fetch} · {len(jobs)} total roles")
    else:
        st.caption(f"{len(jobs)} roles from company career pages · Click 'Fetch live' for RSS updates")

    for j in jobs:
        role = ROLE_MAP.get(j["role"], j["role"])
        hot = j.get("age", 99) <= 7
        with st.expander(f"{'🟢 ' if hot else ''}{j['title']} - {j['company']}"):
            cc1, cc2, cc3 = st.columns([3,2,1])
            cc1.markdown(f"**{j['title']}**  \n{j['company']} · Dublin")
            cc2.markdown(f"{role_chip(role)} <span class='sal'>{j.get('salary','-')}</span>", unsafe_allow_html=True)
            cc3.markdown(f"[Open ↗]({j['url']})")
            st.markdown(f"<div class='posted'>{posted_tag(j.get('age',99), j.get('posted','-'))}</div>", unsafe_allow_html=True)
            if j.get("desc"):
                st.markdown(f"<div style='font-size:12px;color:#c4b5fd;margin-top:6px'>{j['desc']}</div>", unsafe_allow_html=True)
            if st.button("+ Add to tracker", key=f"add_{j['title'][:30]}_{j['company']}"):
                DATA["applications"].append({
                    "id": len(DATA["applications"])+1,
                    "title": j["title"], "company": j["company"],
                    "role": ROLE_MAP.get(j["role"], j["role"]),
                    "source": j["source"], "status": "Saved",
                    "date": str(date.today()), "salary": j.get("salary",""),
                    "url": j["url"], "notes": "", "contact": "",
                    "posted": j.get("posted",""),
                })
                save_data(DATA)
                st.success(f"✅ Added: {j['title']}")

# ══════════════════════════════════════════════════════════════════════════════
# SILICON REPUBLIC
# ══════════════════════════════════════════════════════════════════════════════
elif "Silicon" in page:
    st.markdown("## 📰 Silicon Republic")
    st.markdown("Irish tech news and Dublin job posts - your daily pulse.")

    tab_all, tab_jobs, tab_news = st.tabs(["All", "Jobs", "Tech News"])

    for tab, ftype in [(tab_all, None), (tab_jobs, "job"), (tab_news, "news")]:
        with tab:
            items = SILICON_REPUBLIC_ITEMS if not ftype else [i for i in SILICON_REPUBLIC_ITEMS if i["type"]==ftype]
            for item in items:
                badge_style = "background:#1e3a5f;color:#93c5fd" if item["type"]=="job" else "background:#2d1063;color:#c4b5fd"
                co = f" · {item.get('company','')}" if item.get("company") else ""
                st.markdown(f"""
                <div class="news-card">
                  <a href="{item['url']}" target="_blank"
                     style="font-size:13px;font-weight:500;color:#a78bfa;text-decoration:none">
                     {item['title']}</a>
                  <span style="{badge_style};padding:1px 8px;border-radius:8px;font-size:10px;
                               font-weight:500;margin-left:8px">{item['type']}</span>
                  <div style="font-size:11px;color:#7c3aed;margin-top:4px">
                    Silicon Republic{co} · {item['date']}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Direct sections")
    links = [
        ("🤖 AI & Machine Learning","https://www.siliconrepublic.com/machines"),
        ("💼 Jobs in Ireland","https://www.siliconrepublic.com/jobs"),
        ("🏢 Dublin tech companies","https://www.siliconrepublic.com/companies"),
        ("📊 Data & Analytics","https://www.siliconrepublic.com/data-science"),
        ("🔒 Cybersecurity","https://www.siliconrepublic.com/security"),
        ("📧 Newsletter signup","https://www.siliconrepublic.com/newsletter"),
    ]
    cols = st.columns(3)
    for i, (label, url) in enumerate(links):
        cols[i%3].markdown(f"↗ [{label}]({url})")

# ══════════════════════════════════════════════════════════════════════════════
# COMPANY BOARDS
# ══════════════════════════════════════════════════════════════════════════════
elif "Company" in page:
    st.markdown("## 🏢 Company Career Pages - Dublin")
    st.markdown("24 major employers with direct career page links.")

    search = st.text_input("🔍 Search companies", placeholder="e.g. Google, TikTok…")
    cos = [(n,e,c,u) for n,e,c,u in COMPANIES if not search or search.lower() in n.lower()]

    cols = st.columns(4)
    for i, (name, abbr, color, url) in enumerate(cos):
        with cols[i%4]:
            st.markdown(f"""
            <div class="bcard">
              <div style="width:36px;height:36px;border-radius:50%;background:{color}22;
                          color:{color};display:flex;align-items:center;justify-content:center;
                          font-weight:600;font-size:11px;margin:0 auto 5px">{abbr}</div>
              <div style="font-size:12px;font-weight:500;margin-bottom:6px">{name}</div>
              <a href="{url}" style="font-size:11px;background:#2d1063;color:#c4b5fd;
                                      padding:3px 10px;border-radius:8px;text-decoration:none;
                                      display:inline-block">Jobs ↗</a>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎯 Role-specific searches")
    role_searches = [
        ("Trust & Safety @ Google","https://careers.google.com/jobs/results/?location=Dublin&q=trust+safety"),
        ("Trust & Safety @ TikTok","https://careers.tiktok.com/position?location=CT_211&query=trust+safety"),
        ("Trust & Safety @ Meta","https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity"),
        ("Trust & Safety @ OpenAI","https://openai.com/careers"),
        ("AI Analyst @ Google","https://careers.google.com/jobs/results/?location=Dublin&q=AI+analyst"),
        ("AI Governance @ Irish Life","https://www.irishjobs.ie/Jobs/analyst/in-Dublin"),
        ("Data Analyst @ Stripe","https://stripe.com/jobs/search?l=Dublin&q=data+analyst"),
        ("Product Owner @ Bank of Ireland","https://careers.bankofireland.com"),
        ("Business Analyst @ EY","https://www.ey.com/en_ie/careers"),
        ("Business Analyst @ Deloitte","https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440"),
    ]
    c1,c2 = st.columns(2)
    for i,(label,url) in enumerate(role_searches):
        (c1 if i%2==0 else c2).markdown(f"↗ [{label}]({url})")

# ══════════════════════════════════════════════════════════════════════════════
# ALL JOB BOARDS
# ══════════════════════════════════════════════════════════════════════════════
elif "Job Boards" in page:
    st.markdown("## 🗂 All Job Boards")
    st.markdown("Every major platform pre-filtered for your Dublin roles.")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)
    for i,(name,emoji,color,url) in enumerate(BOARDS):
        with cols[i%4]:
            st.markdown(f"""
            <div class="bcard">
              <div style="font-size:20px;margin-bottom:4px">{emoji}</div>
              <div style="font-size:12px;font-weight:500;color:{color};margin-bottom:6px">{name}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button("Search ↗", url, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📣 Set up job alerts on each platform (do this once!)")
    tips = [
        ("LinkedIn",   "Search → click **'Set alert'** → daily email for new matches"),
        ("Indeed",     "Run search → scroll to bottom → **'Get new jobs for this search by email'**"),
        ("IrishJobs",  "Create account → save search → email on new postings"),
        ("Glassdoor",  "Search → **'Get email updates'** on results page"),
        ("Otta",       "Sign in → set preferences → automatic weekly digest"),
        ("Wellfound",  "Create profile → set role + location → automatic matches emailed"),
    ]
    for p, tip in tips:
        with st.expander(f"📣 {p}"):
            st.markdown(tip)

# ══════════════════════════════════════════════════════════════════════════════
# TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif "Tracker" in page:
    st.markdown("## 📋 My Application Tracker")

    with st.expander("➕ Log a new application", expanded=False):
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            new_title   = st.text_input("Job title *")
            new_company = st.text_input("Company *")
        with r1c2:
            new_role    = st.selectbox("Role type", ROLES[1:])
            new_source  = st.text_input("Source", placeholder="LinkedIn / Indeed / Company…")
        with r1c3:
            new_status  = st.selectbox("Status", STATUSES)
            new_date    = st.date_input("Date applied", value=date.today())
            new_posted  = st.text_input("Posted date / age", placeholder="e.g. 3 days ago")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            new_url     = st.text_input("Job URL")
            new_salary  = st.text_input("Salary", placeholder="e.g. €60-75k")
        with r2c2:
            new_contact = st.text_input("Contact name", placeholder="Recruiter / hiring manager")
            new_notes   = st.text_area("Notes", height=68, placeholder="Interview dates, follow-ups…")

        if st.button("💾 Save application"):
            if new_title and new_company:
                DATA["applications"].append({
                    "id":      len(DATA["applications"])+1,
                    "title":   new_title,  "company":  new_company,
                    "role":    new_role,   "source":   new_source,
                    "status":  new_status, "date":     str(new_date),
                    "posted":  new_posted, "salary":   new_salary,
                    "url":     new_url,    "contact":  new_contact,
                    "notes":   new_notes,
                })
                save_data(DATA)
                st.success(f"✅ Saved: {new_title} at {new_company}")
                st.rerun()
            else:
                st.error("Please fill in job title and company.")

    apps = DATA["applications"]
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total",        len(apps))
    c2.metric("Applied",      sum(1 for a in apps if a.get("status")=="Applied"))
    c3.metric("Interviewing", sum(1 for a in apps if a.get("status")=="Interviewing"))
    c4.metric("Offers",       sum(1 for a in apps if a.get("status")=="Offer"))
    c5.metric("Rejected",     sum(1 for a in apps if a.get("status")=="Rejected"))

    st.markdown("<br>", unsafe_allow_html=True)
    fc1,fc2,fc3 = st.columns(3)
    with fc1: f_s = st.selectbox("Status filter", ["All"]+STATUSES)
    with fc2: f_r = st.selectbox("Role filter",   ROLES)
    with fc3: f_q = st.text_input("Search", placeholder="company or title…")

    filtered = apps[:]
    if f_s != "All": filtered = [a for a in filtered if a.get("status")==f_s]
    if f_r != "All": filtered = [a for a in filtered if a.get("role")==f_r]
    if f_q:          filtered = [a for a in filtered if f_q.lower() in (a.get("title","")+a.get("company","")).lower()]

    if not filtered:
        st.info("No applications match your filter - log one above!")
    else:
        st.markdown('<div class="thdr"><span>Role / Company</span><span>Source · Posted</span><span>Applied</span><span>Status</span><span>Role</span><span></span></div>', unsafe_allow_html=True)
        for idx, a in enumerate(filtered):
            posted_str = f" · {a['posted']}" if a.get("posted") else ""
            st.markdown(f"""
            <div class="trow">
              <div>
                <strong style="font-size:12px">{a.get('title','-')}</strong><br>
                <span style="color:#a78bfa;font-size:11px">{a.get('company','-')}</span>
                {f'<span class="sal">{a["salary"]}</span>' if a.get("salary") else ''}
              </div>
              <div style="font-size:11px;color:#c4b5fd">{a.get('source','-')}{posted_str}</div>
              <div style="font-size:11px">{a.get('date','-')}</div>
              <div>{status_chip(a.get('status','Saved'))}</div>
              <div>{role_chip(a.get('role','-'))}</div>
              <div></div>
            </div>""", unsafe_allow_html=True)

            if a.get("notes") or a.get("contact") or a.get("url"):
                with st.expander(f"📝 {a.get('title','')} - notes"):
                    if a.get("contact"): st.markdown(f"👤 **Contact:** {a['contact']}")
                    if a.get("notes"):   st.markdown(a["notes"])
                    if a.get("url"):     st.markdown(f"[Open job posting ↗]({a['url']})")

            new_s = st.selectbox("", STATUSES,
                index=STATUSES.index(a.get("status","Saved")) if a.get("status") in STATUSES else 0,
                key=f"s_{a.get('id',idx)}", label_visibility="collapsed")
            if new_s != a.get("status"):
                for item in DATA["applications"]:
                    if item.get("id") == a.get("id"): item["status"] = new_s
                save_data(DATA)
                st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

    if apps:
        ec1, ec2 = st.columns(2)
        with ec1:
            df = pd.DataFrame(apps)
            st.download_button("📥 Export CSV", df.to_csv(index=False),
                               "lets_get_hired.csv", "text/csv", use_container_width=True)
        with ec2:
            if st.button("🗑 Clear all data", use_container_width=True):
                DATA["applications"] = []
                save_data(DATA)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# GOOGLE SHEETS SYNC
# ══════════════════════════════════════════════════════════════════════════════
elif "Sheets" in page:
    st.markdown("## 🔗 Google Sheets Sync")
    st.markdown("Two-way sync with your 'Let's Get Hired' Google Sheet.")

    with st.expander("📋 Setup instructions (one time)", expanded=True):
        st.markdown("""
**Step 1** - [console.cloud.google.com](https://console.cloud.google.com) → Create project → Enable **Google Sheets API** + **Google Drive API**

**Step 2** - IAM & Admin → Service Accounts → Create → Download JSON key

**Step 3** - Rename it `gsheets_credentials.json` → place it in your app folder

**Step 4** - Create a Google Sheet named **"Let's Get Hired"** → share it with the service account email (Editor access)

**Step 5** - Sync below!
        """)

    creds_ok = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsheets_credentials.json"))
    if creds_ok: st.success("✅ Credentials found!")
    else: st.warning("⚠️ `gsheets_credentials.json` not found - follow setup above.")

    sheet_name = st.text_input("Sheet name", value="Let's Get Hired")
    cp, pull = st.columns(2)

    with cp:
        st.markdown("#### ⬆️ Push to Google Sheets")
        st.markdown(f"Upload **{len(DATA['applications'])}** applications.")
        if st.button("Push → Sheets", disabled=not creds_ok):
            with st.spinner("Pushing…"):
                ok, result = push_to_sheets(sheet_name)
            if ok: st.success(f"✅ Done! [Open sheet]({result})")
            else:  st.error(f"❌ {result}")

    with pull:
        st.markdown("#### ⬇️ Pull from Google Sheets")
        st.markdown("Import from your Google Sheet.")
        if st.button("Pull ← Sheets", disabled=not creds_ok):
            with st.spinner("Pulling…"):
                pulled, err = pull_from_sheets(sheet_name)
            if pulled is not None:
                DATA["applications"] = pulled
                save_data(DATA)
                st.success(f"✅ Imported {len(pulled)} applications!")
                st.rerun()
            else:
                st.error(f"❌ {err}")

    st.markdown("---")
    st.markdown("#### 📥 Manual CSV export → import to Google Sheets")
    if DATA["applications"]:
        df = pd.DataFrame(DATA["applications"])
        st.download_button("📥 Download CSV", df.to_csv(index=False),
                           "lets_get_hired.csv", "text/csv", use_container_width=True)
        st.markdown("*In Google Sheets: File → Import → Upload this CSV*")

# ══════════════════════════════════════════════════════════════════════════════
# CV EDITOR
# ══════════════════════════════════════════════════════════════════════════════
elif "CV" in page:
    st.markdown("## 📄 CV Editor")
    st.markdown("Edit on the left - live preview on the right.")

    cv = DATA["cv"]
    col_edit, col_prev = st.columns([1, 1])

    with col_edit:
        cv["name"]    = st.text_input("Full name",    value=cv.get("name",""))
        cv["contact"] = st.text_input("Contact line", value=cv.get("contact",""))
        st.markdown("**Summary**")
        cv["summary"] = st.text_area("", value=cv.get("summary",""), height=110, label_visibility="collapsed")
        st.markdown("**Skills**")
        cv["skills"]  = st.text_area("", value=cv.get("skills",""),  height=75,  label_visibility="collapsed")
        st.markdown("**Experience**")
        exps = cv.get("experience",[])
        for i, exp in enumerate(exps):
            with st.expander(f"Role {i+1}: {exp.get('title','-')}", expanded=(i==0)):
                exps[i]["title"]   = st.text_input("Title",   value=exp.get("title",""),   key=f"t{i}")
                exps[i]["company"] = st.text_input("Company", value=exp.get("company",""), key=f"c{i}")
                exps[i]["dates"]   = st.text_input("Dates",   value=exp.get("dates",""),   key=f"d{i}")
                exps[i]["bullets"] = st.text_area("Bullets",  value=exp.get("bullets",""), key=f"b{i}", height=100)
        cv["experience"] = exps
        ca, cb = st.columns(2)
        with ca:
            if st.button("+ Add role"):
                cv["experience"].append({"title":"","company":"","dates":"","bullets":""})
                save_data(DATA); st.rerun()
        with cb:
            if len(exps) > 1 and st.button("− Remove last"):
                cv["experience"].pop()
                save_data(DATA); st.rerun()
        st.markdown("**Education**")
        cv["education"] = st.text_area("", value=cv.get("education",""), height=75, label_visibility="collapsed")
        if st.button("💾 Save CV"): DATA["cv"] = cv; save_data(DATA); st.success("CV saved!")

    with col_prev:
        st.markdown("**Preview**")
        exp_html = ""
        for exp in cv.get("experience",[]):
            bullets = "".join(f"<div style='margin:2px 0'>{b}</div>" for b in exp.get("bullets","").split("\n") if b.strip())
            exp_html += f"""<div style='margin-bottom:10px'>
                <div style='font-weight:600;font-size:12px'>{exp.get('title','')} - {exp.get('company','')}</div>
                <div style='font-size:10px;color:#888;margin-bottom:3px'>{exp.get('dates','')}</div>
                <div style='font-size:11px'>{bullets}</div></div>"""
        st.markdown(f"""
        <div class="cv-box">
          <h1>{cv.get('name','')}</h1>
          <div class="cc">{cv.get('contact','')}</div>
          <h2>Summary</h2>
          <p style='font-size:11px'>{cv.get('summary','')}</p>
          <h2>Skills</h2>
          <p style='font-size:11px'>{cv.get('skills','')}</p>
          <h2>Experience</h2>{exp_html}
          <h2>Education</h2>
          <p style='font-size:11px'>{cv.get('education','').replace(chr(10),'<br>')}</p>
        </div>""", unsafe_allow_html=True)

        plain = f"{cv.get('name','')}\n{cv.get('contact','')}\n\nSUMMARY\n{cv.get('summary','')}\n\nSKILLS\n{cv.get('skills','')}\n\nEXPERIENCE\n"
        plain += "\n\n".join(f"{e.get('title','')} - {e.get('company','')} ({e.get('dates','')})\n{e.get('bullets','')}" for e in cv.get("experience",[]))
        plain += f"\n\nEDUCATION\n{cv.get('education','')}"
        st.download_button("📥 Download CV (.txt)", plain, "devanshi_cv.txt", "text/plain", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW PREP
# ══════════════════════════════════════════════════════════════════════════════
elif "Interview" in page:
    st.markdown("## 💡 Interview Prep")
    st.markdown("STAR answers and key talking points tailored to your background.")

    company_tabs = st.tabs(["OpenAI","TikTok","Google","Meta","General T&S"])

    openai_q = [
        ("Tell me about yourself", "3+ years Trust & Safety at Meta via Covalen. Sole market owner. LLM evaluation, abuse detection, content policy. MSc Business Analytics. CSPO. Now seeking a permanent senior T&S role at an AI-first company like OpenAI."),
        ("Why OpenAI?", "Your T&S team is building safety infrastructure for the most consequential AI of our time. My LLM evaluation and content policy background maps directly - I understand both the technical side (how models fail) and the operational side (how to scale enforcement)."),
        ("Describe a complex T&S case you owned end to end", "Use the coordinated account network investigation - SQL analysis to identify signal, cross-team escalation, policy recommendation, enforcement action. Quantify the outcome."),
        ("How do you handle exposure to harmful content?", "Structured processing time, clear workflow compartmentalisation, team debriefs, and proactive wellbeing check-ins. Aware of vicarious trauma risk - I've operated in 24/7 environments."),
        ("What do you know about DSA/EU AI Act?", "DSA requires platforms to publish transparency reports, conduct risk assessments for VLOPs, and respond to regulator requests. EU AI Act classifies AI systems by risk - high-risk systems need conformity assessments. OpenAI's ChatGPT is a GPAI model under Article 51."),
    ]

    tiktok_q = [
        ("Why TikTok?", "TikTok has one of the most complex T&S environments - short-form video at scale, multilingual markets, live content, e-commerce. My EMEA market ownership and LLM evaluation experience is directly applicable."),
        ("How do you analyse safety data at scale?", "SQL for pattern detection, Python/Pandas for trend analysis, BI dashboards for stakeholder reporting. At Meta I built dashboards that tracked policy enforcement metrics across 4 markets."),
        ("Tell me about a policy you helped improve", "Describe identifying a gap in abuse detection logic through SQL analysis → proposed policy change → cross-functional review → A/B test → rollout. Focus on data-driven decision making."),
    ]

    google_q = [
        ("Tell me about yourself - ADI framing", "Frame yourself as a data analyst who specialises in trust signals. 'I've spent 3+ years using SQL and Python to identify coordinated account networks, abuse patterns, and policy violations at Meta. My work sits at the intersection of data analysis and integrity operations.'"),
        ("Walk me through a SQL analysis you did", "Coordinated account detection: GROUP BY device fingerprint, COUNT of accounts, suspicious temporal clustering. Found networks of fake accounts using shared infrastructure. Escalated to policy team."),
        ("How do you measure the impact of T&S work?", "Leading indicators: detection rate, false positive rate, escalation latency. Lagging: repeat violation rate, user harm reports. I built dashboards tracking all of these across markets."),
    ]

    meta_q = [
        ("You've worked for Meta before - what would you do differently?", "Focus more on proactive rather than reactive enforcement. Build better tooling for market owners. Invest in cross-market learning."),
        ("How do you prioritise across multiple markets?", "Risk-based scoring - severity × volume × regulatory exposure. Highest severity markets get immediate attention. I owned 4 markets and used a triage matrix to allocate effort."),
    ]

    general_q = [
        ("Why are you leaving / what happened?", "My contract with Covalen concluded as Meta consolidated its vendor operations. I'm now actively pursuing permanent senior roles in T&S and AI analysis where I can have long-term impact."),
        ("What's your biggest strength?", "Combining technical data skills with operational T&S judgment. I can write the SQL query AND translate the findings into a policy recommendation AND present it to stakeholders."),
        ("Where do you see yourself in 3 years?", "Senior T&S Analyst or AI Policy Manager at a major platform, owning a product area end-to-end and contributing to AI governance frameworks."),
    ]

    for tab, qs, company in zip(company_tabs,
                                 [openai_q, tiktok_q, google_q, meta_q, general_q],
                                 ["OpenAI","TikTok","Google","Meta","General"]):
        with tab:
            st.markdown(f"**Key talking points for {company} interviews**")
            for q, a in qs:
                with st.expander(f"❓ {q}"):
                    st.markdown(a)
                    st.markdown("---")
                    st.text_area("Your notes", key=f"{company}_{q[:20]}", height=80, placeholder="Add your own notes here…")

    st.markdown("---")
    st.markdown("#### 📌 STAR framework reminder")
    st.info("**Situation** → **Task** → **Action** → **Result** · Always end with a number or measurable outcome.")

    st.markdown("#### 🔑 Your unique selling points")
    st.markdown("""
- **Rare combination**: LLM evaluation + T&S operations + data analysis - very few people have all three
- **EMEA market ownership**: experience making autonomous policy decisions for a region
- **EU AI Act awareness**: directly relevant for OpenAI, Google, TikTok Dublin
- **MSc Business Analytics**: signals data fluency beyond just operations
- **CSPO**: product thinking on top of analyst skills
- **Multilingual market support**: demonstrates ability to work across cultures and contexts
    """)


   

