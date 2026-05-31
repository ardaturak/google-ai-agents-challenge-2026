"""Shared UI components used across all pages."""

import streamlit as st


def render_sidebar():
    """Render consistent sidebar across all pages."""
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:24px 0 12px;'>
            <div style='width:56px; height:56px; margin:0 auto 10px; background:linear-gradient(135deg,#3b82f6,#10b981); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:28px; box-shadow: 0 4px 15px rgba(59,130,246,0.3);'>💧</div>
            <h2 style='color:#f1f5f9; margin:0; font-size:18px; font-weight:800; letter-spacing:-0.5px;'>PRONUVE</h2>
            <p style='color:#64748b; font-size:10px; margin:4px 0 0; letter-spacing:1.5px; font-weight:600;'>WATER INTELLIGENCE</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**System Status**")
        st.markdown("""
        <div style='font-size:12px; line-height:2.2; color:#cbd5e1;'>
        🟢 Orchestrator<br>🟢 Data Pipeline (3)<br>🟢 Analysis Layer (5)<br>
        🟢 Anomaly Detection (5×)<br>🟢 Optimization (3)<br>🟢 Governance (2)<br>
        🟢 Report Generator<br>🟢 Alert Agent <small style='color:#4ade80;'>human-in-the-loop active</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**ADK Patterns**")
        st.markdown("""
        <div style='font-size:11px; color:#94a3b8; line-height:2;'>
        <span style='color:#4ade80;'>●</span> SequentialAgent ×3<br>
        <span style='color:#fbbf24;'>●</span> ParallelAgent ×3<br>
        <span style='color:#f87171;'>●</span> LoopAgent ×1<br>
        <span style='color:#d8b4fe;'>●</span> Human-in-Loop ×1
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**MCP Servers**")
        st.markdown("""
        <div style='font-size:11px; color:#94a3b8; line-height:2;'>
        📦 BigQuery<br>🛰️ Earth Engine<br>🌤️ Weather API<br>📧 Gmail API
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div style='text-align:center; color:#475569; font-size:10px; line-height:1.8;'>
        ProgenX + PRONUVE<br>METU • TÜBİTAK<br>
        <span style='color:#3b82f6;'>Google AI Agents Challenge 2026</span>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """Render consistent footer across all pages."""
    st.markdown("""
    <div class="footer">
        <strong>PRONUVE Water Intelligence</strong> — Built by ProgenX + PRONUVE<br>
        Google for Startups AI Agents Challenge 2026 • Track 1: Build<br>
        Powered by Google ADK • Gemini • Cloud Run • BigQuery • Earth Engine
    </div>
    """, unsafe_allow_html=True)
