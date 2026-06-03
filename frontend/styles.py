GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-primary: #050a15;
    --bg-secondary: #111827;
    --bg-card: #1a2332;
    --border: #1e3048;
    --border-hover: #3b82f6;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #3b82f6;
    --green: #10b981;
    --amber: #f59e0b;
    --red: #ef4444;
    --purple: #8b5cf6;
    --gradient-blue: linear-gradient(135deg, #3b82f6, #1d4ed8);
    --gradient-green: linear-gradient(135deg, #10b981, #059669);
    --shadow: 0 4px 24px rgba(0,0,0,0.3);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
.stApp { background: var(--bg-primary) !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0c1524 0%, #111827 100%) !important; border-right: 1px solid var(--border) !important; }
div[data-testid="stSidebarContent"] { background: transparent !important; }
header[data-testid="stHeader"] { background: transparent !important; }
div[data-testid="stToolbar"] { display: none !important; }

.main-header {
    background: linear-gradient(135deg, #0c1524 0%, #1a2744 50%, #0c1524 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px 48px;
    margin-bottom: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent 5%, #3b82f6 30%, #10b981 50%, #3b82f6 70%, transparent 95%);
    animation: shimmer 3s infinite;
}
@keyframes shimmer {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}
.main-header h1 {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa 0%, #34d399 50%, #60a5fa 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px;
    letter-spacing: -0.8px;
    animation: textGrad 4s linear infinite;
}
@keyframes textGrad {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.main-header p { color: #94a3b8; font-size: 13px; margin: 0; letter-spacing: 0.2px; }
.main-header .badge-row { display: flex; gap: 8px; justify-content: center; margin-top: 12px; }
.main-header .hbadge { 
    background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 500;
}

.kpi-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; margin: 20px 0 28px; }
@media (max-width: 900px) { .kpi-row { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 500px) { .kpi-row { grid-template-columns: repeat(2, 1fr); } }
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 14px;
    text-align: center;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute; bottom: 0; left: 20%; right: 20%;
    height: 2px; border-radius: 2px;
    background: var(--accent);
    opacity: 0;
    transition: opacity 0.25s;
}
.kpi-card:hover { border-color: var(--border-hover); transform: translateY(-3px); box-shadow: 0 8px 30px rgba(59,130,246,0.15); }
.kpi-card:hover::after { opacity: 1; }
.kpi-value { font-size: 28px; font-weight: 800; color: var(--text-primary); line-height: 1.1; }
.kpi-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 8px; font-weight: 600; }
.kpi-delta { font-size: 11px; margin-top: 6px; font-weight: 500; padding: 2px 8px; border-radius: 10px; display: inline-block; }
.kpi-delta.up { color: #34d399; background: rgba(16,185,129,0.1); }
.kpi-delta.down { color: #f87171; background: rgba(239,68,68,0.1); }

.section-title {
    font-size: 11px; font-weight: 700; color: var(--text-primary);
    margin: 24px 0 14px; padding: 8px 14px;
    background: var(--bg-secondary);
    border-radius: 8px;
    border-left: 3px solid var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.sensor-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    transition: all 0.25s;
}
.sensor-card:hover { border-color: var(--border-hover); box-shadow: 0 4px 20px rgba(59,130,246,0.08); }
.sensor-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(30,48,72,0.5); }
.sensor-row:last-child { border: none; }
.sensor-key { color: var(--text-muted); font-size: 12px; font-weight: 500; }
.sensor-val { color: var(--text-primary); font-size: 12px; font-weight: 600; }

.alert-card {
    background: linear-gradient(135deg, #1a0a0a, #2d1111);
    border: 1px solid #7f1d1d;
    border-radius: 14px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(239,68,68,0.1);
}
.alert-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ef4444, #f59e0b, #ef4444);
    animation: alertPulse 2s infinite;
}
@keyframes alertPulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }

.stTabs [data-baseweb="tab-list"] { background: rgba(17,24,39,0.8); border-radius: 12px; padding: 4px; gap: 2px; border: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-size: 12px; font-weight: 600; letter-spacing: 0.2px; color: #94a3b8 !important; padding: 8px 16px !important; }
.stTabs [data-baseweb="tab"]:hover { color: #e2e8f0 !important; background: rgba(59,130,246,0.08) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(59,130,246,0.15) !important; color: #60a5fa !important; border-bottom: none !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: transparent !important; }
.stTabs [data-baseweb="tab-border"] { background-color: transparent !important; }

.badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; }
.badge-ok { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.badge-warn { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-crit { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }

.park-name { font-size: 14px; font-weight: 700; color: var(--text-primary); }

/* Override Streamlit default widget colors */
.stSelectbox [data-baseweb="select"] { background: var(--bg-card) !important; border-color: var(--border) !important; }
.stSelectbox [data-baseweb="select"]:hover { border-color: var(--border-hover) !important; }
button[data-testid="baseButton-primary"] { background: linear-gradient(135deg, #3b82f6, #2563eb) !important; border: none !important; font-weight: 600 !important; border-radius: 10px !important; }
button[data-testid="baseButton-primary"]:hover { background: linear-gradient(135deg, #60a5fa, #3b82f6) !important; }
button[data-testid="baseButton-secondary"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; color: #e2e8f0 !important; border-radius: 10px !important; }
button[data-testid="baseButton-secondary"]:hover { border-color: var(--border-hover) !important; }
div[data-testid="stMetric"] { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 16px !important; }
div[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 800 !important; }
div[data-testid="stExpander"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }
div[data-testid="stStatus"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }

/* Remove any colored underlines/highlights from tabs */
.stTabs [role="tabpanel"] { border: none !important; }

.footer {
    text-align: center; margin-top: 40px; padding: 20px;
    border-top: 1px solid var(--border); color: var(--text-muted); font-size: 11px;
}

/* Text Input & Radio styling */
div[data-testid="stTextInput"] input { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; color: var(--text-primary) !important; }
div[data-testid="stTextInput"] input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important; }
div[data-testid="stRadio"] label { color: var(--text-secondary) !important; font-size: 12px !important; }
div[data-testid="stRadio"] [data-baseweb="radio"] { margin-bottom: 4px; }

/* Progress bar */
div[data-testid="stProgress"] > div > div { background: var(--accent) !important; border-radius: 6px !important; }
div[data-testid="stProgress"] { background: var(--bg-secondary) !important; border-radius: 6px !important; }

/* Caption & info boxes */
div[data-testid="stCaptionContainer"] { color: var(--text-muted) !important; }
div.stAlert { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }
</style>
"""
