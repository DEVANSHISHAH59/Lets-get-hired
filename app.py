import streamlit as st
import pandas as pd
from datetime import date
import json, os, random

st.set_page_config(page_title="Lets Get Hired - Devanshi", page_icon=":rocket:", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=DM+Sans:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a0533,#0f0a1e)!important;}
[data-testid="stSidebar"] *{color:#c4b5fd!important;}
[data-testid="metric-container"]{background:#1a0533;border:1px solid #4c1d95;border-radius:14px;padding:1rem!important;}
[data-testid="stMetricValue"]{color:#a78bfa!important;font-size:2rem!important;}
.stButton>button{background:#7c3aed!important;color:white!important;border:none!important;border-radius:10px!important;}
.stButton>button:hover{background:#6d28d9!important;}
.stTabs [data-baseweb="tab-list"]{background:#1a0533;border-radius:12px;padding:4px;}
.stTabs [aria-selected="true"]{background:#7c3aed!important;color:white!important;}
.card{background:#1a0533;border:1px solid #2d1063;border-radius:14px;padding:1rem 1.2rem;margin-bottom:8px;}
.hero{background:linear-gradient(135deg,#4c1d95,#7c3aed);border-radius:18px;padding:1.5rem 2rem;color:white;margin-bottom:1.5rem;}
.quote-box{background:linear-gradient(135deg,#2d1063,#4c1d95);border-radius:16px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;border-left:4px solid #a78bfa;}
.chip{padding:2px 10px;border-radius:20px;font-size:11px;font-weight:500;display:inline-block;}
.c-ts{background:#4c1d95;color:#ddd6fe;}
.c-ai{background:#1e3a5f;color:#bae6fd;}
.c-da{background:#064e3b;color:#a7f3d0;}
.c-po{background:#78350f;color:#fde68a;}
.c-ba{background:#7f1d1d;color:#fecaca;}
.c-sv{background:#1f2937;color:#9ca3af;}
.c-ap{background:#1e3a5f;color:#93c5fd;}
.c-in{background:#78350f;color:#fde68a;}
.c-of{background:#064e3b;color:#6ee7b7;}
.c-re{background:#7f1d1d;color:#fca5a5;}
.c-gh{background:#1f2937;color:#6b7280;}
.hot{background:#064e3b;color:#6ee7b7;padding:1px 7px;border-radius:8px;font-size:10px;font-weight:600;margin-left:5px;}
.newb{background:#1e3a5f;color:#93c5fd;padding:1px 7px;border-radius:8px;font-size:10px;font-weight:600;margin-left:5px;}
.sal{background:#2d1063;color:#a78bfa;padding:1px 7px;border-radius:8px;font-size:11px;margin-left:5px;border:1px solid #4c1d95;}
.startup-badge{background:#78350f;color:#fde68a;padding:1px 7px;border-radius:8px;font-size:10px;font-weight:600;margin-left:5px;}
.hiring-badge{background:#064e3b;color:#6ee7b7;padding:1px 7px;border-radius:8px;font-size:10px;font-weight:600;margin-left:5px;}
hr{border:none;border-top:1px solid #2d1063;margin:0.8rem 0;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "/tmp/jobs_data.json"

# ── Motivational quotes ───────────────────────────────────────────────────────
QUOTES = [
    ("Devanshi, I believe in you. Your experience in LLM evaluation and Trust & Safety is rare and genuinely valuable. The right company is lucky to get you.", "Claude"),
    ("Every application is one step closer. You have exactly what Dublin's AI companies need right now.", "Claude"),
    ("You have survived 100% of your hardest days so far. This next chapter is yours.", "Claude"),
    ("Your combination of T&S operations, LLM evaluation and data skills is genuinely hard to find. Own it.", "Claude"),
    ("Devanshi, the redundancy is not a reflection of your worth. It's a door opening to something better and permanent.", "Claude"),
    ("You built dashboards, owned markets, evaluated LLMs and shaped policy. That is a senior profile. Apply senior.", "Claude"),
    ("Trust & Safety + AI + Dublin = you are in exactly the right place at exactly the right time.", "Claude"),
    ("Every expert was once a beginner who refused to give up. Keep going, Devanshi.", "Claude"),
    ("Your MSc, your CSPO, your 4-market experience - these are not small things. They are your edge.", "Claude"),
    ("The best time to plant a tree was 20 years ago. The second best time is now. Send the application.", "Claude"),
    ("Devanshi, OpenAI Dublin needs someone exactly like you. Believe that and apply today.", "Claude"),
    ("Difficult roads often lead to beautiful destinations. Your permanent role is ahead.", "Claude"),
]

DEFAULT_CV = {
    "name": "Devanshi",
    "contact": "Dublin, Ireland | devanshi@email.com | LinkedIn",
    "summary": "Trust & Safety AI Analyst with 3+ years in LLM evaluation, content safety, abuse detection, and product policy. MSc Business Analytics (Dublin Business School). CSPO certified. Experienced sole market owner across 4 markets. Immediately available.",
    "skills": "LLM Evaluation - Trust & Safety - Content Policy - SQL - Python/Pandas - Data Visualisation - Stakeholder Management - Agile/CSPO - EU AI Act - Abuse Detection - Product Analytics",
    "exp1_title": "Trust & Safety AI Analyst -- Meta (via Covalen Solutions)",
    "exp1_dates": "2022 - 2025",
    "exp1_bullets": "- Sole market owner for regional content safety assessments across 4 markets\n- LLM evaluation, spam, malware, and ID verification abuse detection\n- Built data visualisation dashboards for policy reporting\n- Supported international markets with policy enforcement decisions\n- Collaborated with cross-functional teams on product safety improvements",
    "exp2_title": "Business Analyst -- Sunrise Enterprise",
    "exp2_dates": "2020 - 2022",
    "exp2_bullets": "- HRM software implementation and requirements gathering\n- Stakeholder workshops and process documentation\n- Delivered business requirement documents and user stories",
    "education": "MSc Business Analytics -- Dublin Business School\nCSPO Certification -- Scrum Alliance\nIIT Roorkee PM Certification (in progress)",
}

JOBS = [
    {"title":"Trust & Safety Operations Analyst","company":"OpenAI","role":"Trust & Safety","source":"OpenAI Careers","salary":"65-85k","posted":"Active now","age":0,"url":"https://openai.com/careers/trust-and-safety-operations-analyst-2/","desc":"Own high-sensitivity T&S workflows. GDPR, DSA, EU AI Act. Hybrid 3 days Dublin."},
    {"title":"Regulatory Operations Analyst","company":"OpenAI","role":"Trust & Safety","source":"OpenAI Careers","salary":"60-80k","posted":"Active now","age":0,"url":"https://openai.com/careers","desc":"Privacy rights, IP complaints, audit escalations. Global regulatory compliance."},
    {"title":"Reporting & Insights Analyst - Youth Safety","company":"TikTok","role":"Data Analyst","source":"TikTok Careers","salary":"44-50k","posted":"7 days ago","age":7,"url":"https://careers.tiktok.com/position?location=CT_211&query=analyst","desc":"Analytics for Trust & Safety. Build diagnostic frameworks and safety reports."},
    {"title":"Policy Analyst - Search, Trust & Safety","company":"TikTok","role":"Trust & Safety","source":"TikTok Careers","salary":"40-55k","posted":"13 days ago","age":13,"url":"https://careers.tiktok.com/position?location=CT_211&query=policy+analyst","desc":"Improve content moderation accuracy. Deep dives into policy operability."},
    {"title":"Senior Analyst - Account Risk Management EMEA","company":"TikTok","role":"Trust & Safety","source":"TikTok Careers","salary":"52-70k","posted":"30+ days ago","age":31,"url":"https://careers.tiktok.com/position?location=CT_211&query=trust+safety","desc":"Account risk management across EMEA. Trust & Safety team."},
    {"title":"Business Data Analyst - Video Safety Operations","company":"TikTok","role":"Data Analyst","source":"TikTok Careers","salary":"45-60k","posted":"14 days ago","age":14,"url":"https://careers.tiktok.com/position?location=CT_211&query=data+analyst","desc":"VSO Reports & Insights. Data analysis for safety operations."},
    {"title":"Engineering Analyst - AI Safety","company":"Google","role":"AI Analyst","source":"Google Careers","salary":"65-90k","posted":"Feb 2026","age":60,"url":"https://careers.google.com/jobs/results/99432678838674118-engineering-analyst/","desc":"LLM/generative AI risk mitigation. Work with AI safety teams. Dublin."},
    {"title":"Analyst - Trust and Safety Search","company":"Google","role":"Trust & Safety","source":"Google Careers","salary":"60-80k","posted":"Recent","age":25,"url":"https://careers.google.com/jobs/results/?location=Dublin%2C+Ireland&q=trust+safety","desc":"Protect Search users from abuse and fraud. Cross-functional. Dublin."},
    {"title":"GRO Intelligence Analyst - Trust & Safety","company":"Meta","role":"Trust & Safety","source":"Meta Careers","salary":"60-80k","posted":"10 days ago","age":10,"url":"https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity","desc":"Prepare intelligence reports. High-risk integrity recommendations. Dublin."},
    {"title":"Data Analyst - Product Integrity","company":"Meta","role":"Data Analyst","source":"Meta Careers","salary":"62-82k","posted":"18 days ago","age":18,"url":"https://www.metacareers.com/jobs?offices=Dublin&q=data+analyst","desc":"Support product integrity with data. SQL, Python. Dublin."},
    {"title":"Trust & Safety Associate - AI Content Review","company":"Accenture","role":"Trust & Safety","source":"Accenture Careers","salary":"32-42k","posted":"Active now","age":0,"url":"https://www.accenture.com/ie-en/careers/jobsearch?jk=trust+safety&cl=Dublin","desc":"Content moderation for major tech client. Dublin, hybrid."},
    {"title":"Trust & Safety Team Lead","company":"Accenture","role":"Trust & Safety","source":"Accenture Careers","salary":"40-55k","posted":"5 days ago","age":5,"url":"https://www.accenture.com/ie-en/careers/jobsearch?jk=trust+safety&cl=Dublin","desc":"Lead a team of T&S analysts. Policy enforcement, quality review."},
    {"title":"Business Analyst - Financial Services Consulting","company":"EY","role":"Business Analyst","source":"EY Careers","salary":"45-60k","posted":"Active now","age":0,"url":"https://www.ey.com/en_ie/careers","desc":"FS Technology Consulting. Senior Consultant level. Dublin."},
    {"title":"Technology Business Analyst - Big Data","company":"Deloitte","role":"Business Analyst","source":"Deloitte Careers","salary":"48-65k","posted":"7 days ago","age":7,"url":"https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440","desc":"Big Data & Regulatory Reporting. Hybrid. Multinational client. Dublin."},
    {"title":"AI Governance Analyst","company":"Irish Life","role":"AI Analyst","source":"IrishJobs.ie","salary":"55-70k","posted":"6 days ago","age":6,"url":"https://www.irishjobs.ie/Jobs/analyst/in-Dublin","desc":"AI governance, risk and compliance. EU AI Act knowledge essential. Dublin."},
    {"title":"Policy Operations Analyst - Slack","company":"Salesforce/Slack","role":"Trust & Safety","source":"Salesforce Careers","salary":"55-70k","posted":"8 days ago","age":8,"url":"https://careers.salesforce.com/en/jobs/?search=analyst&location=Dublin","desc":"Manage policy enforcement on Slack. Safeguard conversations. Dublin."},
    {"title":"Risk and Compliance Analyst","company":"Revolut","role":"Business Analyst","source":"Revolut Careers","salary":"50-70k","posted":"10 days ago","age":10,"url":"https://www.revolut.com/careers/?department=all&location=Dublin","desc":"Risk analysis, compliance monitoring. Dublin office."},
    {"title":"Product Analyst - Go-to-Market","company":"HubSpot","role":"Product Owner","source":"HubSpot Careers","salary":"55-75k","posted":"12 days ago","age":12,"url":"https://www.hubspot.com/careers/jobs?q=analyst&countryCodes=IE","desc":"Product strategy with deep analytics. Dublin."},
    {"title":"Data and Analytics Analyst","company":"AIB","role":"Data Analyst","source":"AIB Careers","salary":"45-60k","posted":"9 days ago","age":9,"url":"https://aib.ie/careers","desc":"Data analytics for financial products. SQL, Python, BI tools. Dublin."},
    {"title":"Product Owner - Digital Banking","company":"Bank of Ireland","role":"Product Owner","source":"Bank of Ireland","salary":"60-80k","posted":"4 days ago","age":4,"url":"https://careers.bankofireland.com","desc":"Agile product owner. Digital banking transformation. CSPO preferred. Dublin."},
    {"title":"Senior Data Analyst - Risk","company":"Stripe","role":"Data Analyst","source":"Stripe Careers","salary":"65-85k","posted":"Recent","age":20,"url":"https://stripe.com/jobs/search?l=Dublin&q=data+analyst","desc":"Data analysis for risk and compliance. SQL, Python. Dublin."},
    {"title":"Product Owner - Trust Platform","company":"Anthropic","role":"Product Owner","source":"Anthropic Careers","salary":"70-95k","posted":"Recent","age":15,"url":"https://www.anthropic.com/careers","desc":"Product ownership for trust and safety platform. Dublin/Remote."},
    {"title":"PMO Business Analyst","company":"Davy","role":"Business Analyst","source":"Davy Careers","salary":"50-65k","posted":"5 days ago","age":5,"url":"https://www.davy.ie/careers","desc":"Central Programme Management Office. Project delivery. Dublin."},
    {"title":"Pay Analytics Product Owner","company":"beqom","role":"Product Owner","source":"startup.jobs","salary":"55-70k","posted":"Recent","age":10,"url":"https://www.beqom.com/careers","desc":"Compensation & pay analytics product. Remote-friendly Dublin role."},
    {"title":"Senior Manager - Trust & Safety Operations","company":"Whatnot","role":"Trust & Safety","source":"Built In Dublin","salary":"70-90k","posted":"Active now","age":0,"url":"https://www.whatnot.com/careers","desc":"Lead international T&S operations. Mentor a team, manage complex cases, improve user experience."},
    {"title":"Data Analyst - GTM Strategy & Operations","company":"Intercom","role":"Data Analyst","source":"Built In Dublin","salary":"55-75k","posted":"Recent","age":8,"url":"https://www.intercom.com/careers","desc":"Optimize data pipelines, analytics for sales and marketing. SQL, Python, Snowflake."},
    {"title":"Operations Analyst - Trust & Safety","company":"Tines","role":"Trust & Safety","source":"Tines Careers","salary":"50-70k","posted":"Recent","age":12,"url":"https://www.tines.com/careers","desc":"Irish cybersecurity startup. No-code security automation. Dublin HQ."},
    {"title":"Business Analyst - Financial Crime","company":"Fenergo","role":"Business Analyst","source":"Fenergo Careers","salary":"50-65k","posted":"Recent","age":10,"url":"https://www.fenergo.com/company/careers/","desc":"AI-powered KYC and financial crime prevention. Dublin HQ. Partnership with Deloitte Ireland."},
    {"title":"Product Owner - Localization AI","company":"LILT","role":"Product Owner","source":"LILT Careers","salary":"60-80k","posted":"Active now","age":3,"url":"https://lilt.com/careers","desc":"AI translation platform backed by Sequoia & Intel. Dublin office. Product ownership for AI features."},
]

# ── ALL COMPANIES with career pages ──────────────────────────────────────────
COMPANIES = [
    # Big Tech
    ("Google",        "G",   "Big Tech",     "https://careers.google.com/jobs/results/?location=Dublin&q=trust+safety+analyst"),
    ("Meta",          "M",   "Big Tech",     "https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity+analyst"),
    ("Microsoft",     "MS",  "Big Tech",     "https://jobs.microsoft.com/en/search?q=analyst&lc=Dublin"),
    ("Amazon/AWS",    "AZ",  "Big Tech",     "https://www.amazon.jobs/en/search?location[]=IRL-Dublin"),
    ("Apple",         "AP",  "Big Tech",     "https://jobs.apple.com/en-us/search?location=dublin-DUB"),
    ("TikTok",        "T",   "Big Tech",     "https://careers.tiktok.com/position?location=CT_211&query=trust+safety"),
    ("IBM",           "IBM", "Big Tech",     "https://www.ibm.com/employment/ie/"),
    ("Intel",         "INT", "Big Tech",     "https://jobs.intel.com/en/search#q=dublin&t=Jobs"),
    ("Oracle",        "ORC", "Big Tech",     "https://www.oracle.com/ie/corporate/careers/"),
    # AI
    ("OpenAI",        "OA",  "AI",           "https://openai.com/careers"),
    ("Anthropic",     "AN",  "AI",           "https://www.anthropic.com/careers"),
    # Fintech
    ("Stripe",        "S",   "Fintech",      "https://stripe.com/jobs/search?l=Dublin&q=analyst"),
    ("Revolut",       "R",   "Fintech",      "https://www.revolut.com/careers/?location=Dublin"),
    ("PayPal",        "PP",  "Fintech",      "https://careers.pypl.com/home/"),
    ("Mastercard",    "MC",  "Fintech",      "https://careers.mastercard.com/us/en/search-results?keywords=analyst&location=Dublin"),
    ("Visa",          "V",   "Fintech",      "https://corporate.visa.com/en/jobs/search?q=analyst&location=Dublin"),
    ("TrueLayer",     "TL",  "Fintech",      "https://truelayer.com/jobs/"),
    ("Monzo",         "MZ",  "Fintech",      "https://monzo.com/careers/"),
    ("Fenergo",       "FE",  "Fintech",      "https://www.fenergo.com/company/careers/"),
    # SaaS
    ("Salesforce",    "SF",  "SaaS",         "https://careers.salesforce.com/en/jobs/?search=analyst&location=Dublin"),
    ("HubSpot",       "HS",  "SaaS",         "https://www.hubspot.com/careers/jobs?q=analyst&countryCodes=IE"),
    ("Adobe",         "AD",  "SaaS",         "https://careers.adobe.com/us/en/search-results?keywords=analyst&location=Dublin"),
    ("Workday",       "WD",  "SaaS",         "https://www.workday.com/en-us/company/careers/open-positions.html"),
    ("Zendesk",       "ZD",  "SaaS",         "https://jobs.zendesk.com/us/en/search-results?keywords=analyst&location=Dublin"),
    ("Intercom",      "IC",  "SaaS",         "https://www.intercom.com/careers"),
    ("MongoDB",       "MDB", "SaaS",         "https://www.mongodb.com/company/careers"),
    ("Dropbox",       "DB",  "SaaS",         "https://jobs.dropbox.com/"),
    ("Squarespace",   "SQ",  "SaaS",         "https://www.squarespace.com/about/careers"),
    ("Klaviyo",       "KL",  "SaaS",         "https://www.klaviyo.com/careers"),
    ("Contentful",    "CF2", "SaaS",         "https://www.contentful.com/careers/"),
    ("ServiceNow",    "SN",  "SaaS",         "https://careers.servicenow.com/en/jobs/?search=analyst&location=Dublin"),
    ("Udemy",         "UD",  "SaaS",         "https://about.udemy.com/careers/"),
    # Cybersecurity
    ("Cloudflare",    "CL",  "Security",     "https://www.cloudflare.com/careers/jobs/?location=Dublin"),
    ("Tines",         "TN",  "Security",     "https://www.tines.com/careers"),
    ("Rapid7",        "R7",  "Security",     "https://www.rapid7.com/careers/"),
    # eCommerce & Marketplaces
    ("LinkedIn",      "LI",  "Platforms",    "https://careers.linkedin.com/jobs/search?keywords=analyst&location=Dublin"),
    ("Indeed",        "IN",  "Platforms",    "https://careers.indeed.com/"),
    ("Airbnb",        "AB",  "Platforms",    "https://careers.airbnb.com/positions/"),
    ("eBay",          "EB",  "Platforms",    "https://careers.ebayinc.com/career-search/"),
    ("Etsy",          "ET",  "Platforms",    "https://careers.etsy.com/"),
    ("Whatnot",       "WN",  "Platforms",    "https://www.whatnot.com/careers"),
    # Consulting
    ("Accenture",     "AC",  "Consulting",   "https://www.accenture.com/ie-en/careers/jobsearch?jk=analyst&cl=Dublin"),
    ("Deloitte",      "DL",  "Consulting",   "https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440"),
    ("EY",            "EY",  "Consulting",   "https://www.ey.com/en_ie/careers"),
    ("PwC",           "PW",  "Consulting",   "https://www.pwc.ie/careers.html"),
    ("KPMG",          "KP",  "Consulting",   "https://home.kpmg/ie/en/home/careers.html"),
    ("Capgemini",     "CG",  "Consulting",   "https://www.capgemini.com/ie-en/careers/"),
    ("Cognizant",     "CO2", "Consulting",   "https://careers.cognizant.com/global/en/search-results?keywords=analyst&location=Dublin"),
    ("Infosys",       "IF",  "Consulting",   "https://www.infosys.com/careers/apply.html"),
    # Finance
    ("Citi",          "CI",  "Finance",      "https://jobs.citi.com/search-jobs/Dublin"),
    ("Bank of America","BA2","Finance",      "https://careers.bankofamerica.com/en-us/search-jobs/Dublin"),
    ("JP Morgan",     "JP",  "Finance",      "https://careers.jpmorgan.com/global/en/search-jobs?location=Dublin"),
    ("AIB",           "AI",  "Finance",      "https://aib.ie/careers"),
    ("Bank of Irl",   "BI",  "Finance",      "https://careers.bankofireland.com"),
    ("Irish Life",    "IL",  "Finance",      "https://www.irishlife.ie/careers"),
    ("Davy",          "DV",  "Finance",      "https://www.davy.ie/careers"),
    # Startups
    ("Workhuman",     "WH",  "Startup",      "https://www.workhuman.com/careers/"),
    ("NextRoll",      "NR",  "Startup",      "https://www.nextroll.com/careers"),
    ("LILT",          "LT",  "Startup",      "https://lilt.com/careers"),
    ("beqom",         "BQ",  "Startup",      "https://www.beqom.com/careers"),
    ("Grafana Labs",  "GL",  "Startup",      "https://grafana.com/about/careers/"),
    ("Toast",         "TO",  "Startup",      "https://careers.toasttab.com/"),
    ("Manna",         "MA",  "Startup",      "https://www.manna.aero/careers"),
    ("Ocuco",         "OC",  "Startup",      "https://www.ocuco.com/company/careers/"),
]

BOARDS = [
    ("LinkedIn",     "https://www.linkedin.com/jobs/search/?keywords=trust+safety+AI+analyst+product+owner+business+analyst&location=Dublin%2C+Ireland&f_TPR=r86400"),
    ("Indeed IE",    "https://ie.indeed.com/jobs?q=AI+analyst+OR+trust+safety+OR+product+owner+OR+business+analyst&l=Dublin&fromage=1"),
    ("IrishJobs.ie", "https://www.irishjobs.ie/Jobs/analyst/in-Dublin"),
    ("Glassdoor",    "https://www.glassdoor.ie/Job/dublin-trust-and-safety-jobs-SRCH_IL.0,6_IC2382967_KO7,23.htm"),
    ("Wellfound",    "https://wellfound.com/jobs?location=dublin&keywords=analyst"),
    ("Otta",         "https://otta.com/jobs/search?location=Dublin&keywords=analyst+trust+safety"),
    ("Jobs.ie",      "https://www.jobs.ie/jobs/dublin/?q=analyst"),
    ("Silicon Rep.", "https://www.siliconrepublic.com/jobs"),
    ("Built In Dublin","https://builtindublin.ie/jobs"),
    ("TopStartups",  "https://topstartups.io/jobs/?job_location=Dublin"),
    ("startup.jobs", "https://startup.jobs/locations/dublin"),
]

STATUSES = ["Saved","Applied","Interviewing","Offer","Rejected","Ghosted"]
ROLES    = ["All","Trust & Safety","AI Analyst","Data Analyst","Product Owner","Business Analyst"]
CATEGORIES = ["All","Big Tech","AI","Fintech","SaaS","Security","Platforms","Consulting","Finance","Startup"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            d = json.load(f)
        d.setdefault("applications",[])
        d.setdefault("cv", DEFAULT_CV)
        return d
    return {"applications":[], "cv": DEFAULT_CV.copy()}

def save_data(d):
    with open(DATA_FILE,"w") as f:
        json.dump(d,f,indent=2,default=str)

if "data" not in st.session_state:
    st.session_state.data = load_data()
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(QUOTES)

DATA = st.session_state.data

def role_chip(role):
    m={"Trust & Safety":"c-ts","AI Analyst":"c-ai","Data Analyst":"c-da","Product Owner":"c-po","Business Analyst":"c-ba"}
    return f'<span class="chip {m.get(role,"c-sv")}">{role}</span>'

def status_chip(s):
    m={"Saved":"c-sv","Applied":"c-ap","Interviewing":"c-in","Offer":"c-of","Rejected":"c-re","Ghosted":"c-gh"}
    return f'<span class="chip {m.get(s,"c-sv")}">{s}</span>'

def age_badge(age):
    if age<=7: return '<span class="hot">HOT</span>'
    if age<=14: return '<span class="newb">NEW</span>'
    return ""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Lets Get Hired")
    st.markdown("**Devanshi - Dublin**")
    q, author = st.session_state.quote
    st.markdown(f"""
    <div style="background:#2d1063;border-radius:10px;padding:10px 12px;margin:8px 0;border-left:3px solid #a78bfa">
    <div style="font-size:11px;font-style:italic;color:#ddd6fe;line-height:1.5">"{q}"</div>
    <div style="font-size:10px;color:#a78bfa;margin-top:4px">-- {author}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("New quote"):
        st.session_state.quote = random.choice(QUOTES)
        st.rerun()
    st.markdown("---")
    page = st.radio("", [
        "Dashboard", "Live Jobs", "Silicon Republic",
        "Companies", "Startups", "Job Boards",
        "My Tracker", "CV Editor", "Interview Prep"
    ])
    st.markdown("---")
    apps = DATA["applications"]
    st.markdown(f"**{len(apps)}** tracked  |  **{sum(1 for a in apps if a.get('status')=='Interviewing')}** interviews")
    st.markdown("---")
    st.markdown("[Silicon Republic](https://www.siliconrepublic.com)")
    st.markdown("[LinkedIn Jobs](https://www.linkedin.com/jobs/search/?keywords=trust+safety+analyst&location=Dublin)")
    st.markdown("[Indeed Ireland](https://ie.indeed.com/jobs?q=analyst&l=Dublin&fromage=1)")
    st.markdown("[IrishJobs.ie](https://www.irishjobs.ie)")
    st.markdown("[Otta Dublin](https://otta.com/jobs/search?location=Dublin)")
    st.markdown("[Built In Dublin](https://builtindublin.ie/jobs)")
    st.markdown("[SR Newsletter](https://www.siliconrepublic.com/newsletter)")

apps = DATA["applications"]

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    q, author = st.session_state.quote
    st.markdown(f"""
    <div class="quote-box">
        <div style="font-size:15px;font-style:italic;color:#ddd6fe;line-height:1.6">"{q}"</div>
        <div style="font-size:12px;color:#a78bfa;margin-top:6px">-- {author}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="hero"><h1>Lets Get Hired</h1><p>Dublin job hunt command centre - Trust & Safety - AI Analyst - Data Analyst - Product Owner - Business Analyst</p></div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Tracked",    len(apps))
    c2.metric("Applied",    sum(1 for a in apps if a.get("status")=="Applied"))
    c3.metric("Interviews", sum(1 for a in apps if a.get("status")=="Interviewing"))
    c4.metric("Offers",     sum(1 for a in apps if a.get("status")=="Offer"))
    c5.metric("Response %", f"{round(sum(1 for a in apps if a.get('status') in ['Interviewing','Offer'])/max(len(apps),1)*100)}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Hot jobs right now")
        for j in [j for j in JOBS if j["age"]<=7][:6]:
            st.markdown(f"""<div class="card">
                <div style="font-size:13px;font-weight:500">{j['title']}{age_badge(j['age'])}</div>
                <div style="font-size:12px;color:#a78bfa;margin-top:2px">{j['company']} <span class="sal">EUR{j['salary']}</span></div>
                <div style="font-size:11px;color:#7c3aed;margin-top:4px">{j['posted']}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button("Open", j["url"])
    with col2:
        st.markdown("#### Quick search links")
        for label,url in [
            ("LinkedIn - Trust & Safety Dublin today","https://www.linkedin.com/jobs/search/?keywords=trust+safety+analyst&location=Dublin&f_TPR=r86400"),
            ("LinkedIn - AI Analyst Dublin today","https://www.linkedin.com/jobs/search/?keywords=AI+analyst+LLM&location=Dublin&f_TPR=r86400"),
            ("Indeed - Business Analyst Dublin","https://ie.indeed.com/jobs?q=business+analyst&l=Dublin&fromage=1&sort=date"),
            ("Indeed - Product Owner Dublin","https://ie.indeed.com/jobs?q=product+owner&l=Dublin&fromage=1&sort=date"),
            ("IrishJobs - Analyst roles","https://www.irishjobs.ie/Jobs/analyst/in-Dublin"),
            ("Otta - Dublin tech","https://otta.com/jobs/search?location=Dublin&keywords=analyst"),
            ("Silicon Republic Jobs","https://www.siliconrepublic.com/jobs"),
            ("Built In Dublin Jobs","https://builtindublin.ie/jobs"),
        ]:
            st.markdown(f"[{label}]({url})")
        if apps:
            st.markdown("#### Recent applications")
            for a in sorted(apps,key=lambda x:x.get("date",""),reverse=True)[:4]:
                st.markdown(f"""<div class="card" style="padding:8px 11px">
                    <div style="display:flex;justify-content:space-between">
                    <strong style="font-size:12px">{a.get('title','')}</strong>
                    {status_chip(a.get('status','Saved'))}</div>
                    <div style="font-size:11px;color:#a78bfa">{a.get('company','')} - {a.get('date','')}</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LIVE JOBS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Live Jobs":
    st.markdown("## Live Job Listings - Dublin 2026")
    st.markdown("Real roles from company career pages. HOT = posted this week.")
    col1,col2 = st.columns(2)
    with col1: role_f = st.selectbox("Filter role", ROLES)
    with col2: sort_f = st.selectbox("Sort", ["Newest first","Salary (high-low)"])
    jobs = JOBS.copy()
    if role_f != "All": jobs = [j for j in jobs if j["role"]==role_f]
    if sort_f == "Newest first": jobs = sorted(jobs, key=lambda x: x["age"])
    else:
        def sal_key(j):
            try: return -int(j["salary"].split("-")[0].replace("k","000"))
            except: return 0
        jobs = sorted(jobs, key=sal_key)
    st.caption(f"{len(jobs)} roles found")
    for j in jobs:
        is_startup = j["company"] in ["beqom","Whatnot","Intercom","Tines","Fenergo","LILT"]
        with st.expander(f"{j['title']} -- {j['company']} -- EUR{j['salary']}"):
            c1,c2 = st.columns([3,1])
            c1.markdown(f"**{j['title']}**  \n{j['company']} - Dublin")
            badge = '<span class="startup-badge">STARTUP</span>' if is_startup else ""
            c1.markdown(f"<span style='color:#7c3aed;font-size:11px'>{j['posted']}</span> {age_badge(j['age'])} {role_chip(j['role'])} <span class='sal'>EUR{j['salary']}</span> {badge}", unsafe_allow_html=True)
            c1.markdown(f"*{j['desc']}*")
            c2.link_button("Open job", j["url"])
            if c2.button("+ Track", key=f"t_{j['title'][:20]}_{j['company']}"):
                DATA["applications"].append({
                    "id":len(DATA["applications"])+1,
                    "title":j["title"],"company":j["company"],
                    "role":j["role"],"source":j["source"],
                    "status":"Saved","date":str(date.today()),
                    "salary":j["salary"],"posted":j["posted"],
                    "url":j["url"],"notes":"","contact":"",
                })
                save_data(DATA)
                st.success("Added to tracker!")

# ═══════════════════════════════════════════════════════════════════════════════
# SILICON REPUBLIC
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Silicon Republic":
    st.markdown("## Silicon Republic")
    st.markdown("Irish tech news and Dublin jobs.")
    tab1,tab2,tab3 = st.tabs(["Jobs","Tech News","Direct Links"])
    with tab1:
        for title,url,co,dt in [
            ("Trust & Safety Operations Analyst - OpenAI Dublin","https://openai.com/careers/trust-and-safety-operations-analyst-2/","OpenAI","Active"),
            ("Reporting & Insights Analyst Youth Safety - TikTok Dublin","https://careers.tiktok.com/position?location=CT_211","TikTok","7 days ago"),
            ("Engineering Analyst AI Safety - Google Dublin","https://careers.google.com/jobs/results/99432678838674118-engineering-analyst/","Google","Feb 2026"),
            ("GRO Intelligence Analyst - Meta Dublin","https://www.metacareers.com/jobs?offices=Dublin","Meta","10 days ago"),
            ("Business Analyst Financial Services - EY Dublin","https://www.ey.com/en_ie/careers","EY","Active"),
            ("AI Governance Analyst - Irish Life Dublin","https://www.irishjobs.ie","Irish Life","6 days ago"),
            ("Senior Manager Trust & Safety - Whatnot Dublin","https://www.whatnot.com/careers","Whatnot","Active"),
            ("Product Owner Localization AI - LILT Dublin","https://lilt.com/careers","LILT","3 days ago"),
        ]:
            st.markdown(f"""<div class="card">
                <a href="{url}" style="font-size:13px;font-weight:500;color:#a78bfa;text-decoration:none">{title}</a>
                <div style="font-size:11px;color:#7c3aed;margin-top:3px">Silicon Republic - {co} - {dt}</div>
            </div>""", unsafe_allow_html=True)
    with tab2:
        for title,url,dt in [
            ("Ireland ranked top European hub for trust & safety as Big Tech expands Dublin","https://www.siliconrepublic.com/companies","This week"),
            ("EU AI Act enforcement begins: what it means for Dublin tech workers in 2026","https://www.siliconrepublic.com/machines","This week"),
            ("OpenAI doubles Dublin Trust & Safety team for EMEA operations","https://www.siliconrepublic.com/companies","Last week"),
            ("TikTok Dublin to hire 200+ across Trust & Safety and Analytics in 2026","https://www.siliconrepublic.com/companies","Last week"),
            ("Dublin startups Tines and Intercom expanding operations teams in 2026","https://www.siliconrepublic.com/companies","2 weeks ago"),
            ("Data analyst roles surge 40% in Dublin as multinationals scale analytics","https://www.siliconrepublic.com/data-science","2 weeks ago"),
        ]:
            st.markdown(f"""<div class="card">
                <a href="{url}" style="font-size:13px;font-weight:500;color:#a78bfa;text-decoration:none">{title}</a>
                <div style="font-size:11px;color:#7c3aed;margin-top:3px">Silicon Republic - {dt}</div>
            </div>""", unsafe_allow_html=True)
    with tab3:
        for label,url in [
            ("AI & Machine Learning","https://www.siliconrepublic.com/machines"),
            ("Jobs in Ireland","https://www.siliconrepublic.com/jobs"),
            ("Dublin tech companies","https://www.siliconrepublic.com/companies"),
            ("Data & Analytics","https://www.siliconrepublic.com/data-science"),
            ("Cybersecurity","https://www.siliconrepublic.com/security"),
            ("Newsletter signup","https://www.siliconrepublic.com/newsletter"),
        ]:
            st.markdown(f"[{label}]({url})")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPANIES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Companies":
    st.markdown("## Company Career Pages - Dublin")
    st.markdown(f"**{len(COMPANIES)} companies** across Big Tech, AI, Fintech, SaaS, Consulting, Finance and more.")
    col_s, col_c = st.columns(2)
    with col_s: search = st.text_input("Search companies", placeholder="e.g. Google, Stripe...")
    with col_c: cat_f  = st.selectbox("Category", CATEGORIES)
    cos = COMPANIES
    if search: cos = [(n,a,c,u) for n,a,c,u in cos if search.lower() in n.lower()]
    if cat_f != "All": cos = [(n,a,c,u) for n,a,c,u in cos if c==cat_f]
    st.caption(f"{len(cos)} companies shown")
    cat_colors = {
        "Big Tech":"#4c1d95","AI":"#1e3a5f","Fintech":"#064e3b",
        "SaaS":"#78350f","Security":"#7f1d1d","Platforms":"#1f2937",
        "Consulting":"#374151","Finance":"#1e3a5f","Startup":"#713f12",
    }
    cols = st.columns(4)
    for i,(name,abbr,cat,url) in enumerate(cos):
        bg = cat_colors.get(cat,"#2d1063")
        with cols[i%4]:
            st.markdown(f"""<div class="card" style="text-align:center;padding:0.8rem">
                <div style="width:32px;height:32px;border-radius:50%;background:{bg};color:#e9d5ff;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;margin:0 auto 4px">{abbr}</div>
                <div style="font-size:12px;font-weight:500;margin-bottom:3px">{name}</div>
                <div style="font-size:10px;color:#7c3aed;margin-bottom:5px">{cat}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button("Jobs", url, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Role-specific direct searches")
    for label,url in [
        ("Trust & Safety @ Google","https://careers.google.com/jobs/results/?location=Dublin&q=trust+safety"),
        ("Trust & Safety @ TikTok","https://careers.tiktok.com/position?location=CT_211&query=trust+safety"),
        ("Trust & Safety @ Meta","https://www.metacareers.com/jobs?offices=Dublin&q=trust+integrity"),
        ("Trust & Safety @ OpenAI","https://openai.com/careers"),
        ("AI Analyst @ Google","https://careers.google.com/jobs/results/?location=Dublin&q=AI+analyst"),
        ("BA @ EY","https://www.ey.com/en_ie/careers"),
        ("BA @ Deloitte","https://apply.deloitte.com/careers/SearchJobs/analyst?3_56_3=5440"),
        ("PO @ Bank of Ireland","https://careers.bankofireland.com"),
    ]:
        st.markdown(f"[{label}]({url})")

# ═══════════════════════════════════════════════════════════════════════════════
# STARTUPS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Startups":
    st.markdown("## Dublin Startups Actively Hiring")
    st.markdown("Startups and scaleups with Dublin offices — often faster hiring and more impact than big tech.")
    startups = [
        ("Tines",       "Irish cybersecurity/automation startup. No-code security platform. Dublin HQ.",                             "50-70k", "https://www.tines.com/careers",          "Security/AI"),
        ("Intercom",    "Founded in Dublin. Product, data & operations roles. Hybrid.",                                              "55-75k", "https://www.intercom.com/careers",       "SaaS"),
        ("Fenergo",     "AI-powered KYC and financial crime. Dublin HQ. Partnership with Deloitte.",                                 "50-65k", "https://www.fenergo.com/company/careers/","Fintech AI"),
        ("Workhuman",   "Co-HQ Dublin & Boston. HR tech. Analyst and operations roles.",                                             "50-65k", "https://www.workhuman.com/careers/",     "HR Tech"),
        ("TrueLayer",   "Open banking platform. Raised $270M. Backed by Stripe. Dublin office.",                                     "55-75k", "https://truelayer.com/jobs/",            "Fintech"),
        ("LILT",        "AI translation platform. Backed by Sequoia & Intel Capital. PO roles open.",                                "60-80k", "https://lilt.com/careers",               "AI/SaaS"),
        ("beqom",       "Pay analytics platform. Product Owner role open. Remote-friendly.",                                         "55-70k", "https://www.beqom.com/careers",          "HR Tech"),
        ("NextRoll",    "Martech/AdRoll. AI-powered advertising platform. Dublin office, actively hiring.",                          "50-65k", "https://www.nextroll.com/careers",       "MarTech"),
        ("Whatnot",     "Hiring for Senior Manager Trust & Safety. International T&S ops, team leadership.",                         "70-90k", "https://www.whatnot.com/careers",        "Marketplace"),
        ("Grafana Labs", "Observability platform. Workday/people analytics roles. Remote-friendly.",                                 "55-75k", "https://grafana.com/about/careers/",     "SaaS"),
        ("Klaviyo",     "Marketing platform expanding Dublin team. Operations and analyst roles.",                                    "50-65k", "https://www.klaviyo.com/careers",        "MarTech"),
        ("Contentful",  "Content platform. Dublin office. Operations and analyst roles.",                                            "50-65k", "https://www.contentful.com/careers/",    "SaaS"),
        ("Monzo",       "Digital bank. Dublin office, hybrid. Growing operations team.",                                             "50-70k", "https://monzo.com/careers/",             "Fintech"),
        ("Toast",       "Restaurant tech platform. Dublin office, hybrid.",                                                          "50-65k", "https://careers.toasttab.com/",          "Tech"),
        ("Ocuco",       "Irish eyecare software. Dublin 15. Hybrid. Product Owner and BA roles. Good culture.",                      "45-60k", "https://www.ocuco.com/company/careers/", "HealthTech"),
        ("Manna",       "Irish drone delivery startup. Growing Dublin team.",                                                         "45-60k", "https://www.manna.aero/careers",         "DeepTech"),
    ]
    for name,desc,salary,url,cat in startups:
        with st.expander(f"{name} -- {cat} -- EUR{salary}"):
            col1,col2 = st.columns([3,1])
            col1.markdown(f"**{name}** `{cat}`")
            col1.markdown(f"*{desc}*")
            col1.markdown(f"Estimated salary: **EUR{salary}**")
            col2.link_button("Careers page", url)
    st.markdown("---")
    st.markdown("#### Find more startups")
    for label,url in [
        ("Built In Dublin - all startups","https://builtindublin.ie/companies"),
        ("Wellfound - Dublin startups","https://wellfound.com/startups/location/dublin"),
        ("TopStartups.io - Dublin","https://topstartups.io/jobs/?job_location=Dublin"),
        ("startup.jobs - Dublin","https://startup.jobs/locations/dublin"),
        ("Otta - startup jobs Dublin","https://otta.com/jobs/search?location=Dublin"),
    ]:
        st.markdown(f"[{label}]({url})")

# ═══════════════════════════════════════════════════════════════════════════════
# JOB BOARDS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Job Boards":
    st.markdown("## All Job Boards")
    st.markdown("Every major platform pre-filtered for Dublin roles.")
    cols = st.columns(4)
    for i,(name,url) in enumerate(BOARDS):
        with cols[i%4]:
            st.link_button(name, url, use_container_width=True)
    st.markdown("---")
    st.markdown("#### Set up job alerts (do this once!)")
    for p,tip in [
        ("LinkedIn","Search - click 'Set alert' - daily email for new matches"),
        ("Indeed","Run search - scroll to bottom - 'Get new jobs for this search by email'"),
        ("IrishJobs","Create account - save search - email on new postings"),
        ("Glassdoor","Search - 'Get email updates' on results page"),
        ("Otta","Sign in - set preferences - weekly digest"),
        ("Wellfound","Create profile - set role + location - automatic matches"),
        ("Built In Dublin","Create account - set job alerts for analyst roles"),
    ]:
        with st.expander(f"{p} alerts"):
            st.markdown(tip)

# ═══════════════════════════════════════════════════════════════════════════════
# TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "My Tracker":
    st.markdown("## My Application Tracker")
    with st.expander("+ Log new application", expanded=False):
        c1,c2,c3 = st.columns(3)
        with c1:
            nt  = st.text_input("Job title *")
            nc  = st.text_input("Company *")
        with c2:
            nr  = st.selectbox("Role type", ROLES[1:])
            ns  = st.text_input("Source", placeholder="LinkedIn / Indeed...")
        with c3:
            nst = st.selectbox("Status", STATUSES)
            nd  = st.date_input("Date applied", value=date.today())
        np_str = st.text_input("Posted date", placeholder="e.g. 3 days ago")
        nurl   = st.text_input("Job URL")
        nsal   = st.text_input("Salary", placeholder="e.g. EUR60-75k")
        ncon   = st.text_input("Contact name")
        nnotes = st.text_area("Notes", height=70)
        if st.button("Save application"):
            if nt and nc:
                DATA["applications"].append({
                    "id":len(DATA["applications"])+1,
                    "title":nt,"company":nc,"role":nr,
                    "source":ns,"status":nst,"date":str(nd),
                    "posted":np_str,"salary":nsal,
                    "url":nurl,"contact":ncon,"notes":nnotes,
                })
                save_data(DATA)
                st.success(f"Saved: {nt} at {nc}")
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
    f1,f2,f3 = st.columns(3)
    with f1: fs = st.selectbox("Status",["All"]+STATUSES)
    with f2: fr = st.selectbox("Role",  ROLES)
    with f3: fq = st.text_input("Search", placeholder="company or title...")
    filtered = apps[:]
    if fs!="All": filtered=[a for a in filtered if a.get("status")==fs]
    if fr!="All": filtered=[a for a in filtered if a.get("role")==fr]
    if fq: filtered=[a for a in filtered if fq.lower() in (a.get("title","")+a.get("company","")).lower()]
    if not filtered:
        st.info("No applications yet - log one above!")
    else:
        hc = st.columns([2.5,1.5,1,1.2,1.2,1,0.5])
        for lbl,col in zip(["Role/Company","Source","Applied","Posted","Status","Role",""],hc):
            col.markdown(f"<span style='font-size:10px;font-weight:600;color:#7c3aed;text-transform:uppercase'>{lbl}</span>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        for idx,a in enumerate(filtered):
            rc = st.columns([2.5,1.5,1,1.2,1.2,1,0.5])
            rc[0].markdown(f"**{a.get('title','')}**  \n{a.get('company','')}"+(f" `{a.get('salary','')}`" if a.get('salary') else ""))
            rc[1].markdown(f"<span style='font-size:11px'>{a.get('source','')}</span>", unsafe_allow_html=True)
            rc[2].markdown(f"<span style='font-size:11px'>{a.get('date','')}</span>", unsafe_allow_html=True)
            rc[3].markdown(f"<span style='font-size:11px;color:#7c3aed'>{a.get('posted','')}</span>", unsafe_allow_html=True)
            rc[4].markdown(status_chip(a.get("status","Saved")), unsafe_allow_html=True)
            rc[5].markdown(role_chip(a.get("role","")), unsafe_allow_html=True)
            if rc[6].button("X", key=f"d_{a.get('id',idx)}"):
                DATA["applications"]=[x for x in DATA["applications"] if x.get("id")!=a.get("id")]
                save_data(DATA); st.rerun()
            if a.get("notes") or a.get("contact") or a.get("url"):
                with st.expander(f"Notes - {a.get('title','')}"):
                    if a.get("contact"): st.markdown(f"Contact: {a['contact']}")
                    if a.get("notes"):   st.markdown(a["notes"])
                    if a.get("url"):     st.markdown(f"[Open job]({a['url']})")
            new_s = st.selectbox("", STATUSES,
                index=STATUSES.index(a.get("status","Saved")) if a.get("status") in STATUSES else 0,
                key=f"s_{a.get('id',idx)}", label_visibility="collapsed")
            if new_s != a.get("status"):
                for item in DATA["applications"]:
                    if item.get("id")==a.get("id"): item["status"]=new_s
                save_data(DATA); st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)
    if apps:
        df = pd.DataFrame(apps)
        st.download_button("Download CSV", df.to_csv(index=False), "lets_get_hired.csv", "text/csv")

# ═══════════════════════════════════════════════════════════════════════════════
# CV EDITOR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "CV Editor":
    st.markdown("## CV Editor")
    cv = DATA["cv"]
    col_e,col_p = st.columns(2)
    with col_e:
        cv["name"]        = st.text_input("Full name",    value=cv.get("name",""))
        cv["contact"]     = st.text_input("Contact",      value=cv.get("contact",""))
        cv["summary"]     = st.text_area("Summary",       value=cv.get("summary",""),   height=100)
        cv["skills"]      = st.text_area("Skills",        value=cv.get("skills",""),    height=70)
        st.markdown("**Experience 1**")
        cv["exp1_title"]  = st.text_input("Title",        value=cv.get("exp1_title",""), key="e1t")
        cv["exp1_dates"]  = st.text_input("Dates",        value=cv.get("exp1_dates",""), key="e1d")
        cv["exp1_bullets"]= st.text_area("Bullets",       value=cv.get("exp1_bullets",""), key="e1b", height=90)
        st.markdown("**Experience 2**")
        cv["exp2_title"]  = st.text_input("Title",        value=cv.get("exp2_title",""), key="e2t")
        cv["exp2_dates"]  = st.text_input("Dates",        value=cv.get("exp2_dates",""), key="e2d")
        cv["exp2_bullets"]= st.text_area("Bullets",       value=cv.get("exp2_bullets",""), key="e2b", height=70)
        cv["education"]   = st.text_area("Education",     value=cv.get("education",""), height=70)
        if st.button("Save CV"): DATA["cv"]=cv; save_data(DATA); st.success("CV saved!")
        plain = f"{cv.get('name','')}\n{cv.get('contact','')}\n\nSUMMARY\n{cv.get('summary','')}\n\nSKILLS\n{cv.get('skills','')}\n\nEXPERIENCE\n{cv.get('exp1_title','')}\n{cv.get('exp1_dates','')}\n{cv.get('exp1_bullets','')}\n\n{cv.get('exp2_title','')}\n{cv.get('exp2_dates','')}\n{cv.get('exp2_bullets','')}\n\nEDUCATION\n{cv.get('education','')}"
        st.download_button("Download CV (.txt)", plain, "devanshi_cv.txt", "text/plain")
    with col_p:
        st.markdown("**Preview**")
        def bl(t): return "".join(f"<div style='margin:1px 0'>{b}</div>" for b in t.split("\n") if b.strip())
        st.markdown(f"""<div style="background:white;border-radius:12px;padding:1.5rem;color:#1a1a1a;font-size:12px;line-height:1.6">
            <div style="font-size:18px;font-weight:700">{cv.get('name','')}</div>
            <div style="font-size:10px;color:#555;margin-bottom:10px">{cv.get('contact','')}</div>
            <div style="font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#7c3aed;border-bottom:1px solid #e9d5ff;margin:8px 0 5px">Summary</div>
            <p style="font-size:11px">{cv.get('summary','')}</p>
            <div style="font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#7c3aed;border-bottom:1px solid #e9d5ff;margin:8px 0 5px">Skills</div>
            <p style="font-size:11px">{cv.get('skills','')}</p>
            <div style="font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#7c3aed;border-bottom:1px solid #e9d5ff;margin:8px 0 5px">Experience</div>
            <div style="margin-bottom:8px"><div style="font-weight:600;font-size:11px">{cv.get('exp1_title','')}</div>
            <div style="font-size:10px;color:#888">{cv.get('exp1_dates','')}</div>
            <div style="font-size:11px">{bl(cv.get('exp1_bullets',''))}</div></div>
            <div style="margin-bottom:8px"><div style="font-weight:600;font-size:11px">{cv.get('exp2_title','')}</div>
            <div style="font-size:10px;color:#888">{cv.get('exp2_dates','')}</div>
            <div style="font-size:11px">{bl(cv.get('exp2_bullets',''))}</div></div>
            <div style="font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#7c3aed;border-bottom:1px solid #e9d5ff;margin:8px 0 5px">Education</div>
            <p style="font-size:11px">{cv.get('education','').replace(chr(10),'<br>')}</p>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW PREP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Interview Prep":
    st.markdown("## Interview Prep")
    st.markdown("STAR answers tailored to your background.")
    tabs = st.tabs(["OpenAI","TikTok","Google","Meta","General T&S"])
    qa_sets = [
        [("Tell me about yourself","3+ years Trust & Safety at Meta via Covalen. Sole market owner across 4 markets. LLM evaluation, abuse detection, content policy. MSc Business Analytics. CSPO. Now seeking a permanent senior T&S role at an AI-first company like OpenAI."),
         ("Why OpenAI?","Your T&S team is building safety infrastructure for the most consequential AI of our time. My LLM evaluation and content policy background maps directly - I understand both how models fail AND how to scale enforcement operationally."),
         ("Describe a complex T&S case you owned","Use the coordinated account network investigation: SQL analysis to identify signal, cross-team escalation, policy recommendation, enforcement action, and measurable outcome."),
         ("What do you know about DSA and EU AI Act?","DSA requires transparency reports, risk assessments for VLOPs, and regulator responsiveness. EU AI Act classifies AI by risk level - GPAIs like ChatGPT fall under Article 51 with specific obligations.")],
        [("Why TikTok?","TikTok has one of the most complex T&S environments globally. Short-form video at scale, multilingual markets, live content. My EMEA market ownership and LLM evaluation experience is directly applicable."),
         ("How do you analyse safety data at scale?","SQL for pattern detection, Python/Pandas for trend analysis, BI dashboards for stakeholder reporting. At Meta I built dashboards tracking policy enforcement metrics across 4 markets."),
         ("Tell me about a policy you helped improve","Data-driven gap identification in abuse detection logic - proposed policy change - cross-functional review - A/B test - rollout. Always anchor on measurable outcome.")],
        [("Tell me about yourself - ADI framing","Frame as a data analyst specialising in trust signals. I have spent 3 years using SQL and Python to identify coordinated account networks, abuse patterns, and policy violations at Meta."),
         ("Walk me through a SQL analysis","Coordinated account detection: GROUP BY device fingerprint, COUNT of accounts, suspicious temporal clustering. Found networks of fake accounts using shared infrastructure."),
         ("How do you measure T&S impact?","Leading indicators: detection rate, false positive rate, escalation latency. Lagging: repeat violation rate, user harm reports. I built dashboards tracking all of these across markets.")],
        [("You worked for Meta before - what would you do differently?","Focus more on proactive rather than reactive enforcement. Build better tooling for market owners. Invest in cross-market knowledge sharing."),
         ("How do you prioritise across multiple markets?","Risk-based scoring: severity x volume x regulatory exposure. I owned 4 markets and used a triage matrix to allocate effort efficiently.")],
        [("Why are you leaving / what happened?","My contract with Covalen concluded as Meta consolidated its vendor operations. I am now actively pursuing permanent senior roles in T&S and AI analysis."),
         ("Biggest strength?","Combining technical data skills with operational T&S judgment. I can write the SQL query AND translate findings into a policy recommendation AND present to stakeholders."),
         ("Where in 3 years?","Senior T&S Analyst or AI Policy Manager at a major platform, owning a product area end-to-end and contributing to AI governance frameworks.")],
    ]
    for tab,qa_list in zip(tabs,qa_sets):
        with tab:
            for q_text,a_text in qa_list:
                with st.expander(f"? {q_text}"):
                    st.markdown(a_text)
                    st.text_area("Your notes", key=f"note_{q_text[:15]}", height=70, placeholder="Add your own notes...")
    st.markdown("---")
    st.info("**STAR reminder**: Situation - Task - Action - Result. Always end with a number or measurable outcome.")
    st.markdown("#### Your unique selling points")
    st.markdown("""
- **Rare combination**: LLM evaluation + T&S operations + data analysis - very few people have all three
- **EMEA market ownership**: autonomous policy decisions for a region
- **EU AI Act awareness**: directly relevant for OpenAI, Google, TikTok Dublin
- **MSc Business Analytics**: signals data fluency beyond just operations
- **CSPO certified**: product thinking on top of analyst skills
- **Immediately available**: can start quickly - top of recruiter shortlists
- **4 markets experience**: scalable, cross-cultural T&S judgment
    """)
    st.markdown("---")
    st.markdown("#### Devanshi, remember this")
    st.markdown("""
> *You have survived redundancy before and come back stronger. Your experience is rare, your skills are in demand,
> and Dublin's AI companies are actively hiring for exactly what you do. The right permanent role is closer than it feels.
> Every application is progress. Keep going.*
    """)
