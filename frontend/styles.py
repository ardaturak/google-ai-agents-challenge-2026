GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #1e293b;
    --bg-card: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    --border: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-blue: #3b82f6;
    --accent-green: #22c55e;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --accent-purple: #a855f7;
}

.stApp { background-color: var(--bg-primary) !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important; }
div[data-testid="stSidebarContent"] { background: transparent !important; }

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 40px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #3b82f6, #22c55e, transparent);
}
.main-header h1 {
    font-size: 30px;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.main-header p { color: #94a3b8; font-size: 13px; margin: 0; letter-spacing: 0.3px; }

.kpi-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin: 16px 0 24px; }
.kpi-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
    transition: all 0.2s ease;
}
.kpi-card:hover { border-color: #3b82f6; transform: translateY(-2px); box-shadow: 0 4px 20px rgba(59,130,246,0.1); }
.kpi-value { font-size: 26px; font-weight: 700; color: #f1f5f9; line-height: 1.2; }
.kpi-label { font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px; }
.kpi-delta { font-size: 11px; margin-top: 4px; font-weight: 500; }
.kpi-delta.up { color: #4ade80; }
.kpi-delta.down { color: #f87171; }

.section-title {
    font-size: 15px; font-weight: 600; color: #e2e8f0;
    margin: 20px 0 12px; padding-left: 12px;
    border-left: 3px solid #3b82f6;
    letter-spacing: -0.2px;
}

.sensor-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px 20px;
    transition: border-color 0.2s;
}
.sensor-card:hover { border-color: #475569; }
.sensor-card .park-name { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 12px; }
.sensor-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #1e293b; }
.sensor-row:last-child { border: none; }
.sensor-key { color: #64748b; font-size: 12px; }
.sensor-val { color: #e2e8f0; font-size: 12px; font-weight: 500; }

.alert-card {
    background: linear-gradient(135deg, #1f0a0a, #2d0f0f);
    border: 1px solid #991b1b;
    border-radius: 12px;
    padding: 24px;
    position: relative;
    overflow: hidden;
}
.alert-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ef4444, #f59e0b, #ef4444);
}

.stTabs [data-baseweb="tab-list"] { background: #1e293b; border-radius: 10px; padding: 4px; gap: 2px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-size: 13px; font-weight: 500; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; }
.badge-ok { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-warn { background: #451a03; color: #fbbf24; border: 1px solid #92400e; }
.badge-crit { background: #450a0a; color: #f87171; border: 1px solid #991b1b; }

@media (max-width: 768px) {
    .kpi-row { grid-template-columns: repeat(3, 1fr); }
    .main-header h1 { font-size: 22px; }
}
@media (max-width: 480px) {
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""
