import os, re, io, calendar
from datetime import date, datetime
import requests, streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from db import (init_db, save_mood_log, save_manual_mood, MOOD_LABELS, MOOD_EMOJI,
                 get_mood_logs_for_month, get_user_mood_history,
                 get_all_employee_mood_logs, get_latest_mood_per_employee)
from recommendations import get_period_recommendation
from auth import (make_token, read_token, get_user, username_taken, create_user,
                   verify_user, set_password, check_pw, new_otp, save_otp, check_otp)
from email_utils import send_otp

st.set_page_config(page_title="MoodMentor", layout="wide")
BRAND_GREEN = "#1DBF73"
BRAND_GREEN_DARK = "#159c5e"
INK = "#1f2937"
MUTED = "#6b7280"
BG = "#f5f7f6"

st.markdown("""
<style>

/* Hide Streamlit UI */
[data-testid="stHeader"]{
    display:none;
}

[data-testid="stToolbar"]{
    display:none;
}

[data-testid="stDecoration"]{
    display:none;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Background */
.stApp{
    background:#FCFCFD;
}

/* Move content down */
.block-container{
    padding-top:0px !important;
}

/* Remove extra gap */
div[data-testid="stHorizontalBlock"]{
    align-items:center;
}

/* ==========================
Greeting Section
========================== */

.greeting-container{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:20px;
    padding:24px 30px;
    margin-bottom:25px;
    box-shadow:0 6px 20px rgba(0,0,0,.05);
}
.greeting-title{
    font-size:38px;
    font-weight:700;
    color:#111827;
    margin-bottom:6px;
}
.greeting-subtitle{
    font-size:18px;
    color:#64748B;
}
.datetime-box{
    display:flex;
    justify-content:flex-end;
    gap:30px;
    font-size:17px;
    color:#475569;
    font-weight:500;
    margin-top:12px;
}
.metric-card{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:22px;
    display:flex;
    align-items:center;
    gap:18px;
    box-shadow:0 5px 18px rgba(0,0,0,.05);
    transition:0.25s;
    min-height:115px;
}

.metric-card:hover{
    transform:translateY(-4px);
    box-shadow:0 15px 28px rgba(0,0,0,.08);
}

.metric-icon{
    width:68px;
    height:68px;
    border-radius:50%;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:34px;
    flex-shrink:0;
}

.metric-title{
    font-size:16px;
    color:#6B7280;
    font-weight:500;
}

.metric-value{
    font-size:34px;
    font-weight:700;
    color:#111827;
    margin-top:2px;
}

.metric-subtitle{
    margin-top:3px;
    font-size:15px;
    font-weight:500;
}

/* Mood picker buttons */
.st-key-mood_picker div.stButton > button {
    height: 88px;
    border-radius: 100px;
    border: 1px solid #E2E8F0;
    background: white;
    padding:0;
}

.st-key-mood_picker div.stButton > button p,
.st-key-mood_picker div.stButton > button span {
    font-size: 52px !important;
    line-height: 10 !important;
}

.st-key-mood_picker div.stButton > button[kind="primary"]{
    background:#EFF6FF;
    border:2px solid #2563EB;
}

.st-key-mood_picker div.stButton > button:hover{
    border-color:#2563EB;
}


/* How Do You Feel section — card wrapper */
.st-key-mood_section{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:20px;
    padding:24px 30px;
    margin-bottom:25px;
    box-shadow:0 6px 20px rgba(0,0,0,.05);
}

/* ==========================
Mood Calendar
========================== */
.st-key-mood_calendar_card{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:18px;
    padding:20px 22px 16px 22px;
    box-shadow:0 6px 18px rgba(0,0,0,.04);
    margin-bottom:25px;
}

.cal-title{
    font-size:22px;
    font-weight:700;
    color:#111827;
}
.cal-subtitle{
    font-size:14px;
    color:#9CA3AF;
    margin-top:2px;
}

/* Round arrow nav buttons */
.st-key-cal_nav div.stButton > button{
    width:32px;
    height:32px;
    border-radius:50%;
    border:1px solid #E2E8F0;
    background:white;
    color:#475569;
    padding:0;
    font-size:14px;
    line-height:1;
    min-height:32px;
}
.st-key-cal_nav div.stButton > button:hover{
    border-color:#2563EB;
    color:#2563EB;
}

.cal-weekday{
    text-align:center;
    font-size:12px;
    color:#9CA3AF;
    font-weight:600;
    margin-bottom:8px;
}

.cal-daycell{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:flex-start;
    padding:4px 0 10px 0;
    min-height:72px;
}
.cal-daynum{
    font-size:12px;
    color:#B0B7C3;
    margin-bottom:5px;
}
.cal-daynum.today{
    color:#111827;
    font-weight:700;
}
.cal-daynum.empty{
    color:transparent;
}
.cal-emoji-wrap{
    width:32px;
    height:32px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:15px;
}
.cal-emoji-wrap.today-ring{
    border:2px solid #22C55E;
}

.cal-legend{
    display:flex;
    gap:20px;
    flex-wrap:wrap;
    margin-top:16px;
    padding-top:14px;
    border-top:1px solid #F1F5F9;
}
.cal-legend-item{
    display:flex;
    align-items:center;
    gap:6px;
    font-size:13px;
    color:#475569;
}
.cal-legend-dot{
    width:9px;
    height:9px;
    border-radius:50%;
    display:inline-block;
}
/* ==========================
Mood Distribution
========================== */
.st-key-mood_dist_card{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:18px;
    padding:20px 22px;
    box-shadow:0 6px 18px rgba(0,0,0,.04);
    margin-bottom:25px;
    height:100%;
}

.dist-title{
    font-size:20px;
    font-weight:700;
    color:#111827;
    margin-bottom:14px;
}

.dist-legend{
    display:flex;
    flex-direction:column;
    gap:12px;
    justify-content:center;
    height:100%;
}
.dist-legend-item{
    display:flex;
    align-items:center;
    gap:10px;
    font-size:15px;
    color:#334155;
    font-weight:500;
}
.dist-legend-dot{
    width:11px;
    height:11px;
    border-radius:50%;
    display:inline-block;
    flex-shrink:0;
}

.dist-total{
    font-size:13px;
    color:#9CA3AF;
    margin-top:16px;
}
/* ==========================
Mood Trend
========================== */
.st-key-mood_trend_card{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:18px;
    padding:20px 24px 10px 24px;
    box-shadow:0 6px 18px rgba(0,0,0,.04);
    margin-bottom:25px;
}

.trend-title{
    font-size:20px;
    font-weight:700;
    color:#111827;
    margin-bottom:2px;
}
.trend-subtitle{
    font-size:14px;
    color:#9CA3AF;
    margin-bottom:6px;
}
/* ==========================
Tools Section
========================== */
.st-key-tools_section{
    background:white;
    border:1px solid #E8EDF5;
    border-radius:20px;
    padding:24px 30px;
    margin-bottom:25px;
    box-shadow:0 6px 20px rgba(0,0,0,.05);
}

.tools-header{
    display:flex;
    align-items:center;
    gap:10px;
    font-size:20px;
    font-weight:700;
    color:#111827;
    margin-bottom:18px;
}

.tool-card-inner{
    display:flex;
    align-items:center;
    gap:16px;
    padding:20px 22px;
    border-radius:16px;
    position:relative;
}
.tool-icon-box{
    width:46px;
    height:46px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    flex-shrink:0;
}
.tool-text{ flex:1; min-width:0; }
.tool-title{
    font-size:15px;
    font-weight:700;
    color:#111827;
}
.tool-subtitle{
    font-size:13px;
    color:#6B7280;
    margin-top:2px;
}
.tool-chevron{
    font-size:20px;
    color:#9CA3AF;
    flex-shrink:0;
}

/* Card wrappers — make them feel clickable */
.st-key-tool_card_journal, .st-key-tool_card_chat{
    position:relative;
    border-radius:16px;
    cursor:pointer;
    transition:.2s;
}
.st-key-tool_card_journal:hover, .st-key-tool_card_chat:hover{
    transform:translateY(-3px);
    box-shadow:0 12px 24px rgba(0,0,0,.08);
}

/* Invisible button overlaid on the whole card so any click on the
   card (icon, title, chevron, anywhere) triggers navigation */
.st-key-tool_card_journal div.stButton,
.st-key-tool_card_chat div.stButton{
    position:absolute;
    inset:0;
    z-index:5;
}
.st-key-tool_card_journal div.stButton > button,
.st-key-tool_card_chat div.stButton > button{
    width:100%;
    height:100%;
    opacity:0;
    cursor:pointer;
    border:none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ----------------------- */
/* LANDING PAGE */
/* ----------------------- */

.hero-bg{
    background:linear-gradient(180deg,#F8FBFF 0%,#FFFFFF 100%);
    padding:0px;
    margin-top:0px;
}

/* Landing page navbar */
.top-navbar{
    width:100%;
    height:78px;
    display:flex;
    align-items:center;
    background:white;
    border-bottom:1px solid #EEF2F7;
    padding:0 70px;
    box-sizing:border-box;
}

.logo{
    display:flex;
    align-items:center;
    gap:12px;
    font-size:34px;
    font-weight:800;
    color:#0F172A;
    white-space:nowrap;
}
.landing-nav-right{
    display:flex;
    align-items:center;
    gap:32px;
}

.nav-link{
    font-size:16px;
    font-weight:600;
    color:#475569;
    cursor:pointer;
    transition:.2s;
}

.nav-link:hover{
    color:#2563EB;
}

.login-placeholder{
    background:#2563EB;
    color:white;
    padding:11px 25px;
    border-radius:12px;
    font-size:16px;
    font-weight:600;
}
.logo span{
color:#22C55E;
}

.login-btn{
background:white;
color:#2563EB;
border:2px solid #2563EB;
padding:12px 26px;
border-radius:14px;
font-size:16px;
font-weight:600;
transition:.3s;
cursor:pointer;
}

.login-btn:hover{
background:#2563EB;
color:white;
}

.hero-section{
padding:70px 80px;
}

.badge{
display:inline-block;
background:#E8FFF4;
color:#16A34A;
padding:8px 18px;
border-radius:30px;
font-size:13px;
font-weight:700;
letter-spacing:.6px;
margin-bottom:25px;
}

.hero-title{
font-size:62px;
font-weight:800;
line-height:1.15;
color:#0F172A;
margin-bottom:25px;
}

.hero-title span{
color:#22C55E;
}

.hero-text{
font-size:20px;
line-height:1.8;
color:#64748B;
margin-bottom:35px;
}

.primary-btn{
display:inline-block;
background:#2563EB;
color:white;
padding:16px 32px;
border-radius:14px;
font-size:17px;
font-weight:700;
margin-right:20px;
text-decoration:none;
box-shadow:0 12px 30px rgba(37,99,235,.25);
transition:.3s;
}

.primary-btn:hover{
transform:translateY(-3px);
}

.secondary-btn{
display:inline-block;
padding:16px 32px;
border-radius:14px;
font-weight:700;
border:2px solid #2563EB;
color:#2563EB;
text-decoration:none;
background:white;
transition:.3s;
}

.secondary-btn:hover{
background:#EFF6FF;
}



}
/* ---------- Landing Hero Image ---------- */

.st-key-hero_image{
    height:100%;
    display:flex;
    align-items:stretch;
}

.st-key-hero_image img{
    width:100%;
    height:430px;
    object-fit:cover;
    object-position:center;
    border-radius:24px;
    display:block;
}
/* ---------------- FEATURES ---------------- */

.section-title{
text-align:center;
font-size:44px;
font-weight:800;
color:#0F172A;
margin-top:90px;
margin-bottom:12px;
}

.section-subtitle{
text-align:center;
font-size:18px;
color:#64748B;
margin-bottom:45px;
}

.feature-card{

background:white;

border-radius:22px;

padding:35px 25px;

text-align:center;

border:1px solid #EEF2F7;

box-shadow:0 12px 30px rgba(0,0,0,.05);

transition:.35s;

height:280px;

}

.feature-card:hover{

transform:translateY(-10px);

box-shadow:0 25px 50px rgba(0,0,0,.10);

}

.feature-icon{

font-size:48px;

margin-bottom:20px;

}

.feature-title{

font-size:22px;

font-weight:700;

margin-bottom:12px;

color:#111827;

}

.feature-text{

font-size:15px;

line-height:1.7;

color:#64748B;

}



/* ---------- Stats Container ---------- */

.stats-container{
    background:white;
    padding:35px 25px;
    margin-top:70px;
    border-radius:24px;
    border:1px solid #EEF2F7;
    box-shadow:0 10px 35px rgba(0,0,0,.05);
}

.stat{
    text-align:center;
}

.stat-number{
    font-size:42px;
    font-weight:800;
    color:#2563EB;
}

.stat-title{
    font-size:18px;
    font-weight:700;
    margin-top:8px;
    color:#111827;
}

.stat-sub{
    font-size:14px;
    color:#64748B;
    margin-top:6px;
}
.stat-item{

    text-align:center;

    position:relative;

}

.stat-divider{

    border-right:1px solid #EDF2F7;

}

.stat-icon{

    width:92px;

    height:92px;

    border-radius:50%;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:44px;

    margin:auto;

    margin-bottom:24px;

}

.st-key-stats_container{
    background:white;
    padding:35px 25px;
    margin-top:70px;
    border-radius:24px;
    border:1px solid #EEF2F7;
    box-shadow:0 10px 35px rgba(0,0,0,.05);
}
/* ---------- HOW IT WORKS ---------- */

.timeline-section{

margin-top:90px;

}

.timeline-card{

text-align:center;

padding:20px;

}

.timeline-icon{

width:95px;

height:95px;

margin:auto;

border-radius:50%;

display:flex;

align-items:center;

justify-content:center;

font-size:42px;

background:#F0FDF4;

box-shadow:0 8px 20px rgba(0,0,0,.05);

}

.timeline-number{

margin-top:15px;

width:32px;

height:32px;

margin-left:auto;

margin-right:auto;

background:#2563EB;

color:white;

border-radius:50%;

display:flex;

align-items:center;

justify-content:center;

font-weight:700;

}

.timeline-title{

font-size:20px;

font-weight:700;

margin-top:18px;

}

.timeline-text{

font-size:15px;

line-height:1.7;

margin-top:10px;

color:#64748B;

}

/* ---------- CTA ---------- */

.st-key-cta_container{
    margin-top:100px;
    padding:45px 50px;
    border-radius:30px;
    background:linear-gradient(135deg,#EEF6FF,#F7FFFC);
    border:1px solid #E2E8F0;
    box-shadow:0 20px 40px rgba(0,0,0,.05);
}

.cta-image img{
    width:100%;
    border-radius:20px;
    display:block;
}

.cta-title{
    font-size:48px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:18px;
}

.cta-text{
    font-size:19px;
    color:#64748B;
    line-height:1.8;
    margin-bottom:35px;
}

/* ---------- Footer ---------- */

.footer{

margin-top:80px;

padding:30px;

text-align:center;

color:#64748B;

font-size:15px;

border-top:1px solid #E5E7EB;

}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* =========================================================
   FULL SCREEN AUTHENTICATION BACKGROUND
   ========================================================= */

.auth-page{
    min-height:100vh;
    width:100%;
    margin:0 !important;
    padding:0 !important;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        linear-gradient(
            135deg,
            #5146E5 0%,
            #6754EA 38%,
            #B05BE0 72%,
            #D965B8 100%
        );

    box-sizing:border-box;
}

/* Make the whole Streamlit page use the auth gradient
   only when authentication page is visible */
.stApp:has(.auth-page){
    background:
        linear-gradient(
            135deg,
            #5146E5 0%,
            #6754EA 38%,
            #B05BE0 72%,
            #D965B8 100%
        ) !important;
}

/* Remove Streamlit's default spacing around authentication */
.stApp:has(.auth-page) .block-container{
    padding-top:0 !important;
    padding-bottom:0 !important;
    padding-left:0 !important;
    padding-right:0 !important;
    max-width:100% !important;
}

.auth-page [data-testid="column"]{
    padding:0 !important;
}


/* Remove Streamlit column spacing */
.auth-page [data-testid="column"]{
    padding:0 !important;
}


/* =========================================================
   LEFT SECTION
   ========================================================= */

.auth-left{
    height:620px;
    width:100%;

    background:
        radial-gradient(
            circle at 70% 20%,
            rgba(255,255,255,.14),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #6251E8 0%,
            #7557E8 42%,
            #C75BCB 100%
        );

    padding:55px 50px;
    position:relative;
    overflow:hidden;

    box-sizing:border-box;
    color:white;
}


/* Decorative glow */
.auth-left::before{
    content:"";
    position:absolute;

    width:360px;
    height:360px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(255,255,255,.13),
            transparent 70%
        );

    right:-100px;
    top:-120px;

    pointer-events:none;
}


/* Decorative lower glow */
.auth-left::after{
    content:"";

    position:absolute;

    width:420px;
    height:220px;

    left:-100px;
    bottom:-100px;

    border-radius:50%;

    background:
        radial-gradient(
            ellipse,
            rgba(255,140,170,.30),
            transparent 70%
        );

    pointer-events:none;
}


/* =========================================================
   LOGO
   ========================================================= */

.auth-logo{
    display:flex;
    align-items:center;
    gap:11px;

    position:relative;
    z-index:3;

    margin-bottom:65px;
}


.auth-logo-icon{
    width:48px;
    height:48px;

    border-radius:14px;

    background:rgba(255,255,255,.18);

    border:1px solid rgba(255,255,255,.25);

    display:flex;
    align-items:center;
    justify-content:center;

    color:white;
    font-size:25px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.12);
}


.auth-logo-text{
    font-size:28px;
    font-weight:800;

    color:white;

    letter-spacing:-.8px;
}


.auth-logo-text span{
    color:#FFE4F5;
}


/* =========================================================
   BADGE
   ========================================================= */

.auth-badge{
    display:inline-flex;
    align-items:center;

    padding:7px 15px;

    border-radius:25px;

    background:rgba(255,255,255,.16);

    border:1px solid rgba(255,255,255,.20);

    color:white;

    font-size:12px;
    font-weight:700;

    margin-bottom:20px;

    position:relative;
    z-index:3;
}


/* =========================================================
   LEFT HEADING
   ========================================================= */

.auth-heading{
    font-size:46px;
    line-height:1.12;

    font-weight:800;

    color:white;

    letter-spacing:-1.8px;

    position:relative;
    z-index:3;

    margin-bottom:17px;
}


.auth-heading span{
    color:#FFD4EC;
}


/* =========================================================
   LEFT DESCRIPTION
   ========================================================= */

.auth-description{
    max-width:500px;

    font-size:15px;
    line-height:1.65;

    color:rgba(255,255,255,.88);

    position:relative;
    z-index:3;

    margin-bottom:25px;
}


/* =========================================================
   FEATURES
   ========================================================= */

.auth-features{
    display:flex;

    gap:0;

    position:relative;
    z-index:3;

    margin-top:20px;
}


.auth-feature{
    width:25%;

    padding:0 14px;

    border-right:
        1px solid rgba(255,255,255,.22);

    box-sizing:border-box;
}


.auth-feature:first-child{
    padding-left:0;
}


.auth-feature:last-child{
    border-right:none;
}


.auth-feature-icon{
    width:42px;
    height:42px;

    border-radius:12px;

    display:flex;
    align-items:center;
    justify-content:center;

    font-size:20px;

    margin-bottom:9px;

    background:rgba(255,255,255,.18) !important;

    border:1px solid rgba(255,255,255,.15);
}


.auth-feature-title{
    color:white;

    font-size:13px;
    font-weight:800;

    margin-bottom:4px;
}


.auth-feature-text{
    color:rgba(255,255,255,.75);

    font-size:10px;

    line-height:1.45;
}


/* =========================================================
   LEFT IMAGE
   ========================================================= */

.auth-visual{
    display:none;
}


/* Hide quote because reference has a clean lower area */
.auth-quote{
    display:none;
}


/* =========================================================
   RIGHT AUTHENTICATION WHITE CONTAINER
   ========================================================= */

.auth-right{
    width:100%;

    height:620px;
    min-height:620px;
    max-height:620px;

    background:#FFFFFF;

    border-radius:28px;

    padding:45px 50px;

    box-sizing:border-box;

    box-shadow:
        0 20px 50px rgba(40,20,90,.16);

    border:1px solid rgba(255,255,255,.75);

    position:relative;
    z-index:5;
}
/* Real Streamlit container for the white auth box */
.st-key-auth_right_container{
    width:100% !important;

    height:620px !important;
    min-height:620px !important;
    max-height:620px !important;

    background:#FFFFFF !important;

    border-radius:28px !important;

    padding:45px 50px !important;

    box-sizing:border-box !important;

    box-shadow:
        0 20px 50px rgba(40,20,90,.16) !important;

    border:1px solid rgba(255,255,255,.8) !important;

    display:flex !important;
    align-items:flex-start !important;
    justify-content:flex-start !important;
}

/* Inner login content */
.st-key-auth_card_container{
    width:100% !important;
    max-width:430px !important;

    margin:0 auto !important;

    background:transparent !important;

    padding:0 !important;
}
/* =========================================================
   AUTH CONTENT
   ========================================================= */

.auth-card-new{
    width:100%;
    max-width:330px;

    background:transparent;

    border:none;

    border-radius:0;

    padding:0;

    box-shadow:none;

    box-sizing:border-box;
}


/* =========================================================
   AUTH ILLUSTRATION
   ========================================================= */

/*
   Keep the existing content but make it
   very small and clean like the reference.
*/

.auth-card-illustration{
    width:100%;
    height:35px;

    background:transparent;

    display:flex;
    align-items:center;
    justify-content:center;

    margin-bottom:5px;

    overflow:hidden;
}


.auth-card-illustration::before{
    content:"🧠";

    font-size:27px;

    letter-spacing:0;

    filter:none;
}


/* =========================================================
   AUTH TITLE
   ========================================================= */

.auth-title{
    text-align:center;

    font-size:16px;

    font-weight:700;

    color:#6954C8;

    text-transform:uppercase;

    letter-spacing:.4px;

    margin-bottom:22px;
}


.auth-subtitle{
    text-align:center;

    color:#8B8FA3;

    font-size:12px;

    margin-bottom:20px;
}


/* =========================================================
   LABELS
   ========================================================= */

.auth-card-new label{
    color:#73758A !important;

    font-size:11px !important;

    font-weight:600 !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

.auth-card-new div[data-baseweb="input"]{
    border:none !important;

    border-radius:20px !important;

    background:#F0ECFF !important;

    min-height:34px;

    box-shadow:none !important;
}


.auth-card-new div[data-baseweb="input"]:focus-within{
    border:1px solid #8A62E8 !important;

    box-shadow:
        0 0 0 2px rgba(138,98,232,.10) !important;
}


.auth-card-new input{
    font-size:12px !important;

    color:#4C4A62 !important;
}


/* =========================================================
   PRIMARY BUTTON
   ========================================================= */

.auth-card-new button[kind="primary"]{
    min-height:38px !important;

    border-radius:20px !important;

    border:none !important;

    background:
        linear-gradient(
            90deg,
            #D75BB8,
            #8A5BE8
        ) !important;

    color:white !important;

    font-size:12px !important;

    font-weight:700 !important;

    box-shadow:
        0 7px 18px rgba(130,80,220,.22);

    transition:.25s ease;
}


.auth-card-new button[kind="primary"]:hover{
    transform:translateY(-2px);

    box-shadow:
        0 10px 22px rgba(130,80,220,.30);
}


/* =========================================================
   SECONDARY BUTTONS
   ========================================================= */

.auth-card-new button[kind="secondary"]{
    border-radius:20px !important;

    border:1px solid #E7E2F5 !important;

    background:white !important;

    color:#756E8D !important;

    font-weight:600 !important;
}


/* =========================================================
   LINKS
   ========================================================= */

.auth-links{
    display:flex;

    justify-content:space-between;
    align-items:center;

    margin-top:8px;
    margin-bottom:12px;

    font-size:10px;

    color:#9A9AA8;
}


.auth-forgot{
    color:#9B55D9;

    font-weight:600;
}


/* =========================================================
   DIVIDER
   ========================================================= */

.auth-divider{
    display:flex;

    align-items:center;

    gap:8px;

    margin:16px 0 12px;

    color:#AAA9B5;

    font-size:10px;
}


.auth-divider::before,
.auth-divider::after{
    content:"";

    flex:1;

    height:1px;

    background:#E9E7EF;
}


/* =========================================================
   SOCIAL BUTTONS
   ========================================================= */

.social-row{
    display:flex;

    gap:8px;

    margin-bottom:15px;
}


.social-btn{
    flex:1;

    height:34px;

    border:1px solid #E8E5F0;

    border-radius:18px;

    background:white;

    display:flex;

    align-items:center;
    justify-content:center;

    gap:6px;

    color:#77758A;

    font-size:10px;

    font-weight:600;
}


/* =========================================================
   BOTTOM SIGNUP
   ========================================================= */

.auth-bottom{
    text-align:center;

    color:#9695A3;

    font-size:10px;

    margin-top:12px;
}


.auth-bottom span{
    color:#9B55D9;

    font-weight:700;
}


/* =========================================================
   SECURITY
   ========================================================= */

.auth-security{
    max-width:330px;

    margin-top:10px;

    padding:8px 12px;

    border:none;

    border-radius:10px;

    background:#FAF9FD;

    text-align:center;

    color:#AAA8B6;

    font-size:9px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width:1000px){

    .auth-left{
        height:500px !important;
        min-height:500px !important;
    }

    .auth-right{
        height:500px !important;
        min-height:500px !important;
    }

    .st-key-auth_right_container{
        height:500px !important;
        min-height:500px !important;
        max-height:500px !important;
        padding:35px 30px !important;
    }

    .auth-heading{
        font-size:38px;
    }

    .auth-feature{
        padding:0 8px;
    }
}


@media (max-width:750px){

    .auth-page{
        min-height:100vh;

        padding:0 !important;

        align-items:flex-start;
    }

    .auth-left{
        height:auto;
        min-height:400px;

        padding:35px 28px;
    }

    .auth-right{
        height:auto;
        min-height:430px;

        padding:35px 25px;
    }

    .auth-logo{
        margin-bottom:35px;
    }

    .auth-heading{
        font-size:34px;
    }

    .auth-features{
        display:none;
    }
}

/* =========================================================
   REFERENCE-STYLE AUTHENTICATION CARD
   ========================================================= */

/* Full page purple/pink background */
.stApp:has(.st-key-auth_page_container){
    background:
        linear-gradient(
            135deg,
            #5146E5 0%,
            #6754EA 38%,
            #B05BE0 72%,
            #D965B8 100%
        ) !important;
}

/* Center the authentication card */
.st-key-auth_page_container{
    width:100% !important;
    max-width:1060px !important;

    height:620px !important;
    min-height:620px !important;

    margin:0 auto !important;
    padding:0 !important;

    background:transparent !important;

    border-radius:8px !important;

    overflow:hidden !important;

    box-shadow:
        0 22px 55px rgba(30,15,80,.28) !important;
}

/* Remove Streamlit column padding */
.st-key-auth_page_container [data-testid="column"]{
    padding:0 !important;
}

/* LEFT SIDE */
.st-key-auth_page_container .auth-left{
    height:620px !important;
    min-height:620px !important;

    width:100% !important;

    padding:55px 42px !important;

    box-sizing:border-box !important;

    border-radius:8px 0 0 8px !important;

    background:
        radial-gradient(
            circle at 75% 20%,
            rgba(255,255,255,.14),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #6251E8 0%,
            #7557E8 42%,
            #C75BCB 100%
        ) !important;
}

/* RIGHT SIDE */
.st-key-auth_page_container .st-key-auth_right_container{
    height:620px !important;
    min-height:620px !important;
    max-height:620px !important;

    width:100% !important;

    padding:55px 50px !important;

    box-sizing:border-box !important;

    border-radius:0 8px 8px 0 !important;

    background:#FFFFFF !important;

    border:none !important;

    box-shadow:none !important;

    display:flex !important;

    align-items:flex-start !important;

    justify-content:flex-start !important;
}

/* Login content should stay toward the left side
   of the white panel */
.st-key-auth_page_container .st-key-auth_card_container{
    width:100% !important;

    max-width:330px !important;

    margin:35px auto 0 auto !important;

    padding:0 !important;

    background:transparent !important;
}

/* Normal left-aligned authentication writing */
.st-key-auth_page_container .auth-title{
    text-align:left !important;
}

.st-key-auth_page_container .auth-subtitle{
    text-align:left !important;
}

/* Keep small illustration aligned normally */
.st-key-auth_page_container .auth-card-illustration{
    justify-content:flex-start !important;
}

/* Smaller heading to match reference */
.st-key-auth_page_container .auth-title{
    font-size:17px !important;
    margin-bottom:10px !important;
}

.st-key-auth_page_container .auth-subtitle{
    font-size:12px !important;
    margin-bottom:22px !important;
}

/* Form inputs */
.st-key-auth_page_container .auth-card-new div[data-baseweb="input"]{
    min-height:36px !important;
}

/* Login button */
.st-key-auth_page_container .auth-card-new button[kind="primary"]{
    min-height:38px !important;
}

/* Responsive */
@media (max-width:1000px){

    .st-key-auth_page_container{
        max-width:94% !important;
        height:auto !important;
        min-height:0 !important;
    }

    .st-key-auth_page_container .auth-left,
    .st-key-auth_page_container .st-key-auth_right_container{
        height:560px !important;
        min-height:560px !important;
    }
}

@media (max-width:750px){

    .st-key-auth_page_container{
        max-width:94% !important;
        height:auto !important;
    }

    .st-key-auth_page_container .auth-left{
        height:auto !important;
        min-height:430px !important;

        border-radius:8px 8px 0 0 !important;
    }

    .st-key-auth_page_container .st-key-auth_right_container{
        height:auto !important;
        min-height:500px !important;

        border-radius:0 0 8px 8px !important;
    }
}
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


MOOD_STYLE = {
    "Happy":   {"emoji": MOOD_EMOJI["Happy"],   "color": "#2ecc71"},
    "Neutral": {"emoji": MOOD_EMOJI["Neutral"], "color": "#3498db"},
    "Sad":     {"emoji": MOOD_EMOJI["Sad"],     "color": "#e67e22"},
    "Stress":  {"emoji": MOOD_EMOJI["Stress"],  "color": "#f1c40f"},
    "Angry":   {"emoji": MOOD_EMOJI["Angry"],   "color": "#e74c3c"},
    "Fear":    {"emoji": MOOD_EMOJI["Fear"],    "color": "#9b59b6"},
}
def style_for(label):
    return MOOD_STYLE.get(label, {"emoji": "", "color": "#bdbdbd"})

MOOD_TO_NUM = {"Happy": 2, "Neutral": 0, "Sad": -1, "Stress": -1, "Angry": -2, "Fear": -2}



def donut_chart(counts: dict, size=2.6):
    labels, values, colors = [], [], []
    for k, v in counts.items():
        if v > 0:
            labels.append(k); values.append(v)
            colors.append(style_for(k)["color"])
    if not values:
        return None
    fig, ax = plt.subplots(figsize=(size, size))
    ax.pie(
        values, colors=colors, startangle=90,
        wedgeprops=dict(width=0.42, edgecolor="white"),
        autopct="%1.0f%%", pctdistance=0.78,
        textprops={"color": "white", "fontsize": 11, "fontweight": "bold"},
    )
    ax.set(aspect="equal")
    fig.patch.set_alpha(0.0)
    return fig
def trend_chart(trend: dict, size=(9, 3.3)):
    if not trend:
        return None
    dates = list(trend.keys())
    values = list(trend.values())
    x = range(len(dates))

    fig, ax = plt.subplots(figsize=size)

    ax.plot(x, values, color="#22C55E", linewidth=2.5, zorder=3)
    ax.fill_between(x, values, -2, color="#22C55E", alpha=0.12, zorder=1)
    ax.scatter(x, values, s=70, facecolors="white", edgecolors="#22C55E",
               linewidths=2.2, zorder=4)

    ax.set_ylim(-2, 2)
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_yticklabels(["-2", "-1", "0", "+1", "+2"], color="#9CA3AF", fontsize=10)

    ax.set_xticks(list(x))
    ax.set_xticklabels(dates, color="#9CA3AF", fontsize=10)

    ax.grid(axis="y", color="#EEF1F4", linewidth=1, zorder=0)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")
    fig.tight_layout()
    return fig
def metric_card(title, value, subtitle, icon, bg, color):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon" style="background:{bg};color:{color};">
            {icon}
        </div>
        <div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle" style="color:{color};">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def build_pdf_report(username, start_d, end_d, entries, recommendation_text):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=48, bottomMargin=48)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("MoodMentor Wellness Report", styles["Title"]))
    story.append(Paragraph(f"{username} &nbsp;|&nbsp; {start_d} to {end_d}", styles["Normal"]))
    story.append(Spacer(1, 16))

    counts = {}
    for h in entries:
        counts[h["sentiment"]] = counts.get(h["sentiment"], 0) + 1
    summary_line = ", ".join(f"{k}: {v}" for k, v in counts.items())
    story.append(Paragraph("Mood summary", styles["Heading2"]))
    story.append(Paragraph(f"{len(entries)} entries logged. {summary_line}.", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recommendation", styles["Heading2"]))
    story.append(Paragraph(recommendation_text, styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Entries", styles["Heading2"]))
    table_data = [["Date", "Time", "Mood", "Emotion", "Confidence", "Source"]]
    for h in sorted(entries, key=lambda r: r["created_at"], reverse=True):
        table_data.append([
            str(h["mood_date"]),
            h["created_at"].strftime("%H:%M"),
            h["sentiment"] or "\u2014",
            h.get("emotion") or "\u2014",
            f"{h['confidence']:.0%}" if h.get("confidence") is not None else "\u2014",
            h["source"],
        ])
    tbl = Table(table_data, repeatRows=1, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1DBF73")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7f6")]),
    ]))
    story.append(tbl)

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()




@st.cache_resource
def setup(): init_db()
setup()

if "page" not in st.session_state: st.session_state.page = "welcome"
if "show_auth_panel" not in st.session_state: st.session_state.show_auth_panel = False
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login"
if "token" not in st.session_state: st.session_state.token = None
if "email" not in st.session_state: st.session_state.email = None
if "tool_page" not in st.session_state:
    st.session_state.tool_page = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "cal_year" not in st.session_state: st.session_state.cal_year = date.today().year
if "cal_month" not in st.session_state: st.session_state.cal_month = date.today().month
if "today_mood_saved" not in st.session_state: st.session_state.today_mood_saved = False
if "nav" not in st.session_state: st.session_state.nav = "Dashboard"

def goto_auth(mode): st.session_state.auth_mode = mode; st.rerun()

def valid_pw(pw):
    return len(pw) >= 8 and re.search(r"[A-Za-z]", pw) and re.search(r"[0-9]", pw)


if st.session_state.token:
    user = read_token(st.session_state.token)
    if user:
        role = user.get("role", "employee")
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        col1, col2 = st.columns([2,2])
        with col1:
            st.markdown(
            """
            <h2 style="
                color:#2563EB;
                font-weight:700;
                margin-top:5px;
                margin-bottom:0;">
                🧠 Mood Mentor
            </h2>
            """,
            unsafe_allow_html=True)
        with col2:
            if role == "employee":
                selected = option_menu(
                menu_title=None,
                options=["Dashboard","Profile","Logout"],
                icons=["house-fill","person","box-arrow-right"],
                menu_icon="",
                orientation="horizontal",
                default_index=0 if st.session_state.nav=="Dashboard" else 1,
                styles={
                "container":{
                    "padding":"0!important",
                    "background-color":"transparent",
                },
                "icon":{
                    "color":"#475569",
                    "font-size":"18px",
                },
                "nav-link":{
                    "font-size":"17px",
                    "font-weight":"600",
                    "color":"#334155",
                    "padding":"14px 25px",
                    "margin":"0px 8px",
                    "border-radius":"14px",
                    "--hover-color":"#EFF6FF",
                },
                "nav-link-selected":{
                    "background-color":"#2563EB",
                    "color":"white",
                    "box-shadow":"0 8px 18px rgba(37,99,235,.25)",
                },
                }
            )

            
            # Handle navbar selection
            if selected != st.session_state.nav:
                st.session_state.nav = selected

                # Only clear tool page when user actually changes navbar
                if selected in ["Dashboard", "Profile"]:
                    st.session_state.tool_page = None

                if selected == "Logout":
                    st.session_state.token = None
                    st.session_state.page = "welcome"
                    st.rerun()

        st.markdown("""
        <div style="
            background:white;
            padding:10px 30px;
            border-radius:22px;
            border:1px solid #E8EDF5;
            box-shadow:0 8px 25px rgba(0,0,0,.05);
            margin-bottom:20px;
            display:flex;
            align-items:center;
            justify-content:space-between;
        ">
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

        from datetime import datetime
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        greeting = (
            "Good Morning"
            if now.hour < 12
            else "Good Afternoon"
            if now.hour < 18
            else "Good Evening"
        )
        left, right = st.columns([5,2])

        with left:
            st.markdown(f"""
            <div class="greeting-container">
            <div class="greeting-title">
            {greeting}, {user["username"]} 👋
            </div>
            <div class="greeting-subtitle">
            Here's how you've been feeling.
            </div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div class="greeting-container">
            <div class="datetime-box">
                    <span>📅 {now.strftime("%d %b %Y")}</span>
                    <span>🕒 {now.strftime("%I:%M %p")}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if role == "employee":
            section = st.session_state.tool_page or st.session_state.nav

            if section == "Dashboard":
                history_all = get_user_mood_history(user["id"], limit=500)
                latest = history_all[0] if history_all else None
                today_count = sum(1 for h in history_all if h["mood_date"] == date.today())
                streak = 0
                day_ptr = date.today()
                day_set = {h["mood_date"] for h in history_all}
                while day_ptr in day_set:
                    streak += 1
                    day_ptr = date.fromordinal(day_ptr.toordinal() - 1)

                positive_count = sum(1 for h in history_all if h["sentiment"] == "Happy")
                overall_score = int(100 * positive_count / len(history_all)) if history_all else 0

                m1,m2,m3,m4=st.columns(4)

                with m1:
                    mood="No Mood"
                    emoji="🙂"
                    if latest:
                        mood=latest["sentiment"]
                        emoji=style_for(mood)["emoji"]
                    metric_card(
                        "Current Mood",
                        f" {mood}",
                        "Keep it up! ✨",
                        f"{emoji}",
                        "#EAFBF2",
                        "#16A34A"
                    )
                with m2:
                    metric_card(
                        "Overall Score",
                        f"{overall_score}/100",
                        "↑ Great progress",
                        "📈",
                        "#EFF6FF",
                        "#2563EB"
                    )
                with m3:
                    metric_card(
                        "Entries Today",
                        str(today_count),
                        "Good start!",
                        "📝",
                        "#F5F3FF",
                        "#9333EA"
                    )
                with m4:
                    metric_card(
                        "Current Streak",
                        f"{streak} Days",
                        "Keep Going!",
                        "🔥",
                        "#FFF7ED",
                        "#EA580C"
                    )
                st.write("")

                with st.container(key="mood_section", border=True):
                  st.markdown(f"""
            <div class="greeting-title">
            How Do You Feel?
            </div>
            <div class="greeting-subtitle">
            Select your current mood
            </div>
            </div>
            """, unsafe_allow_html=True)


                  with st.container(key="mood_picker"):
                      cols = st.columns(len(MOOD_LABELS))
                      picked = st.session_state.get("picked_mood")
                      for col, label in zip(cols, MOOD_LABELS):
                          s = style_for(label)
                          with col:
                              if st.button(
                                  s["emoji"],
                                  key=f"pick_{label}",
                                  type="primary" if picked == label else "secondary",
                                  use_container_width=True,
                              ):
                                  st.session_state.picked_mood = label
                                  st.rerun()
                              st.markdown(
                                  f"<p style='text-align:center;font-weight:700;font-size:18px;color:{s['color']};margin-top:4px'>{label}</p>",
                                  unsafe_allow_html=True,
                              )

                  st.write("")
                  confirm_col = st.columns([3, 1, 3])[1]
                  with confirm_col:
                      disabled = picked is None
                      if st.button("Save Mood", type="primary", disabled=disabled, use_container_width=True):
                          save_manual_mood(user["id"], st.session_state.picked_mood)
                          st.session_state.today_mood_saved = True
                          st.session_state.picked_mood = None
                          st.rerun()

                  if st.session_state.today_mood_saved:
                      st.success("Today's mood saved!")
                      st.session_state.today_mood_saved = False
                st.markdown("</div>", unsafe_allow_html=True)

                # --- fetch history early so both columns can use it ---
                history = get_user_mood_history(user["id"], limit=200)
                counts = {label: 0 for label in MOOD_LABELS}
                for h in history:
                    if h["sentiment"] in counts:
                        counts[h["sentiment"]] += 1

                col1, col2 = st.columns([2,2])

                # ---------------- COLUMN 1: MOOD CALENDAR ----------------
                with col1:
                    with st.container(key="mood_calendar_card"):
                        head_l, head_r = st.columns([4, 1.4])
                        with head_l:
                            st.markdown(
                                f"""<div class="cal-title">Mood Calendar</div>
                                <div class="cal-subtitle">{calendar.month_name[st.session_state.cal_month]} {st.session_state.cal_year}</div>""",
                                unsafe_allow_html=True,
                            )
                        with head_r:
                            with st.container(key="cal_nav"):
                                nav_l, nav_r = st.columns(2)
                                if nav_l.button("‹", use_container_width=True):
                                    m, y = st.session_state.cal_month - 1, st.session_state.cal_year
                                    if m == 0: m, y = 12, y - 1
                                    st.session_state.cal_month, st.session_state.cal_year = m, y
                                    st.rerun()
                                if nav_r.button("›", use_container_width=True):
                                    m, y = st.session_state.cal_month + 1, st.session_state.cal_year
                                    if m == 13: m, y = 1, y + 1
                                    st.session_state.cal_month, st.session_state.cal_year = m, y
                                    st.rerun()

                        st.write("")

                        logs = get_mood_logs_for_month(user["id"], st.session_state.cal_year,
                                                        st.session_state.cal_month)
                        by_day = {row["mood_date"].day: row for row in logs}

                        weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(
                            st.session_state.cal_year, st.session_state.cal_month
                        )
                        day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                        header_cols = st.columns(7)
                        for c, name in zip(header_cols, day_names):
                            c.markdown(f"<div class='cal-weekday'>{name}</div>", unsafe_allow_html=True)

                        today = date.today()
                        for week in weeks:
                            cols = st.columns(7)
                            for col, day_num in zip(cols, week):
                                if day_num == 0:
                                    col.markdown(
                                        "<div class='cal-daycell'><div class='cal-daynum empty'>0</div></div>",
                                        unsafe_allow_html=True,
                                    )
                                    continue

                                entry = by_day.get(day_num)
                                s = style_for(entry["sentiment"] if entry else None)
                                is_today = (
                                    day_num == today.day
                                    and st.session_state.cal_month == today.month
                                    and st.session_state.cal_year == today.year
                                )
                                daynum_class = "cal-daynum today" if is_today else "cal-daynum"
                                ring_class = "cal-emoji-wrap today-ring" if is_today else "cal-emoji-wrap"
                                bg = f"{s['color']}22" if entry else "transparent"
                                emoji = s["emoji"] if entry else ""

                                col.markdown(
                                    f"""<div class="cal-daycell">
                                        <div class="{daynum_class}">{day_num}</div>
                                        <div class="{ring_class}" style="background:{bg}">{emoji}</div>
                                    </div>""",
                                    unsafe_allow_html=True,
                                )

                        legend_items = "".join(
                            f"<div class='cal-legend-item'><span class='cal-legend-dot' "
                            f"style='background:{style_for(l)['color']}'></span>{l}</div>"
                            for l in MOOD_LABELS
                        )
                        st.markdown(f"<div class='cal-legend'>{legend_items}</div>", unsafe_allow_html=True)

                # ---------------- COLUMN 2: MOOD DISTRIBUTION ----------------
                with col2:
                    with st.container(key="mood_dist_card"):
                        st.markdown("<div class='dist-title'>Mood Distribution</div>", unsafe_allow_html=True)
                        if not history:
                            st.info("No entries yet — pick a mood on Home or write a journal entry to see your dashboard.")
                        else:
                            total = sum(counts.values())
                            chart_col, legend_col = st.columns([1.1, 1])
                            with chart_col:
                                fig = donut_chart(counts)
                                if fig:
                                    st.pyplot(fig, use_container_width=False)
                                else:
                                    st.bar_chart(counts)
                            with legend_col:
                                legend_html = "".join(
                                    f"<div class='dist-legend-item'>"
                                    f"<span class='dist-legend-dot' style='background:{style_for(k)['color']}'></span>"
                                    f"{k} ({round(100*v/total)}%)</div>"
                                    for k, v in counts.items() if v > 0
                                )
                                st.markdown(f"<div class='dist-legend'>{legend_html}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='dist-total'>Total Entries: {total}</div>", unsafe_allow_html=True)
                c1, c2 = st.columns([2,1])
                with c1:
                    with st.container(key="mood_trend_card"):
                        st.markdown(
                            """<div class="trend-title">Mood Trend</div>
                            <div class="trend-subtitle">Your emotional trend over time</div>""",
                            unsafe_allow_html=True,
                        )
                        by_date = {}
                        for h in history:
                            d = h["mood_date"]
                            by_date.setdefault(d, []).append(MOOD_TO_NUM.get(h["sentiment"], 0))
                        trend = {
                            datetime.strftime(d, "%b %-d") if hasattr(d, "strftime") else str(d): sum(v) / len(v)
                            for d, v in sorted(by_date.items())
                        }
                        fig = trend_chart(trend)
                        if fig:
                            st.pyplot(fig, use_container_width=True)
                        else:
                            st.caption("Not enough data yet to draw a trend.")

                with c2:
                    with st.container(border=True):
                        st.write("**Emotions detected from journal entries**")
                        emo_counts = {}
                        for h in history:
                            if h["source"] == "nlp" and h["emotion"]:
                                emo_counts[h["emotion"]] = emo_counts.get(h["emotion"], 0) + 1
                        if emo_counts:
                            st.bar_chart(emo_counts)
                        else:
                            st.caption("No journal-based emotion data yet.")
                        st.markdown("</div>", unsafe_allow_html=True)

                st.write("**Recent activity**")
                table_rows = [{
                    "Date": h["mood_date"], "Time": h["created_at"].strftime("%H:%M"),
                    "Mood": f"{style_for(h['sentiment'])['emoji']} {h['sentiment']}",
                    "Confidence": f"{h['confidence']:.0%}" if h.get("confidence") is not None else "—",
                    "Source": h["source"],
                } for h in history[:15]]
                st.dataframe(table_rows, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.write("**Export report**")
                oldest_date = history[-1]["mood_date"]
                today = date.today()
                date_range = st.date_input(
                    "Select date range", value=(oldest_date, today),
                    min_value=oldest_date, max_value=today,
                    key="dashboard_export_range",
                )
                if st.button("Export PDF"):
                    if isinstance(date_range, tuple) and len(date_range) == 2:
                        start_d, end_d = date_range
                    else:
                        start_d = end_d = date_range
                    filtered = [h for h in history if start_d <= h["mood_date"] <= end_d]
                    if not filtered:
                        st.warning("No entries in that date range.")
                    else:
                        recommendation_text = get_period_recommendation(filtered)
                        pdf_bytes = build_pdf_report(
                            user["username"], start_d, end_d, filtered, recommendation_text,
                        )
                        st.success(recommendation_text)
                        st.download_button(
                            "Download PDF", data=pdf_bytes,
                            file_name=f"moodmentor_report_{start_d}_{end_d}.pdf",
                            mime="application/pdf",
                        )
                st.divider()
                # -------- Journal --------
                col1, col2 = st.columns([10, 1])

                with col1:
                    st.markdown("### 📖 Journal")
                    st.caption("Write your daily journal and track emotions")

                with col2:
                    if st.button("➜", key="goto_journal"):
                        st.session_state.nav = "Dashboard"
                        st.session_state.tool_page = "Journal"
                        st.rerun()

                st.divider()

                # -------- Wellness Chat --------
                col1, col2 = st.columns([10, 1])

                with col1:
                    st.markdown("### 💬 Wellness Chat")
                    st.caption("Talk with your AI wellness assistant")

                with col2:
                    if st.button("➜", key="goto_chat"):
                        st.session_state.nav = "Dashboard"
                        st.session_state.tool_page = "Wellness Chat"
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            elif section == "Journal":
                if st.button("← Back to Dashboard"):
                    st.session_state.tool_page = None
                    st.session_state.nav = "Dashboard"
                    st.rerun()
                st.subheader(" Journal")
                journal_text = st.text_area(
                    "Write about how you're feeling today", height=150,
                    placeholder="Your note here...",
                )
                if st.button("Analyze my mood"):
                    if not journal_text.strip():
                        st.warning("Write something first.")
                    else:
                        with st.spinner("Running NLP analysis…"):
                            try:
                                resp = requests.post(
                                    f"{BACKEND_URL}/analyze-text",
                                    json={"text": journal_text},
                                    headers=headers, timeout=120,
                                )
                            except requests.exceptions.RequestException as e:
                                st.error(f"Could not reach backend: {e}"); resp = None
                        if resp is not None:
                            if resp.status_code != 200:
                                st.error("Analysis failed.")
                            else:
                                r = resp.json()
                                confidence = r.get("emotion_confidence")
                                save_mood_log(
                                    user["id"], r["final_sentiment"], r["final_emotion"],
                                    r["sentiment_scores"]["compound"], journal_text,
                                    confidence=confidence,
                                )
                                conf_str = f", Confidence: **{confidence:.0%}**" if confidence is not None else ""
                                st.success(f"Saved! Sentiment: **{r['final_sentiment']}**, "
                                           f"Emotion: **{r['final_emotion']}**{conf_str}")
                                st.bar_chart(r["emotion_scores"])
                                if r.get("recommendation"):
                                    st.info(f"**Recommendation:** {r['recommendation']}")
                st.markdown("</div>", unsafe_allow_html=True)

                st.subheader("Or upload a file")
                uploaded = st.file_uploader("Choose a CSV or TXT file", type=["csv", "txt"])
                if uploaded is not None and st.button("Run NLP Analysis on file"):
                    files = {"file": (uploaded.name, uploaded.getvalue())}
                    with st.spinner("Running multilingual NLP pipeline…"):
                        try:
                            resp = requests.post(f"{BACKEND_URL}/analyze", files=files,
                                                  headers=headers, timeout=120)
                        except requests.exceptions.RequestException as e:
                            st.error(f"Could not reach backend: {e}"); resp = None
                    if resp is not None:
                        if resp.status_code != 200:
                            st.error("Analysis failed.")
                        else:
                            r = resp.json()
                            confidence = r.get("emotion_confidence")
                            save_mood_log(
                                user["id"], r["final_sentiment"], r["final_emotion"],
                                r["sentiment_scores"]["compound"], r.get("cleaned_text", ""),
                                confidence=confidence,
                            )
                            conf_str = f", Confidence: **{confidence:.0%}**" if confidence is not None else ""
                            st.success(f"Saved! Sentiment: **{r['final_sentiment']}**, "
                                       f"Emotion: **{r['final_emotion']}**{conf_str}")
                            st.bar_chart(r["emotion_scores"])
                            if r.get("recommendation"):
                                st.info(f"**Recommendation:** {r['recommendation']}")
                st.markdown("</div>", unsafe_allow_html=True)

                st.subheader(" Past entries")
                history = [h for h in get_user_mood_history(user["id"], limit=20)
                           if h["journal_text"]]
                if not history:
                    st.caption("No journal entries yet.")
                for h in history:
                    s = style_for(h["sentiment"])
                    conf_str = f" · Confidence: {h['confidence']:.0%}" if h.get("confidence") is not None else ""
                    with st.expander(
                        f"{s['emoji']} {h['sentiment']} — {h['created_at'].strftime('%Y-%m-%d %H:%M')}{conf_str}"
                    ):
                        st.write(h["journal_text"])
                st.markdown("</div>", unsafe_allow_html=True)

            elif section == "Wellness Chat":
                if st.button("← Back to Dashboard"):
                    st.session_state.tool_page = None
                    st.session_state.nav = "Dashboard"
                    st.rerun()
                st.subheader(" Wellness Chat")
                st.caption("A supportive space to talk about how you're feeling. "
                           "Not a substitute for professional care.")
                chat_box = st.container(height=450)
                with chat_box:
                    for turn in st.session_state.chat_history:
                        with st.chat_message(turn["role"]):
                            st.write(turn["content"])

                user_msg = st.chat_input("How are you feeling today?")
                if user_msg:
                    st.session_state.chat_history.append({"role": "user", "content": user_msg})
                    recent_history = st.session_state.chat_history[-10:-1]
                    try:
                        resp = requests.post(
                            f"{BACKEND_URL}/chat",
                            json={"message": user_msg, "history": recent_history},
                            headers=headers, timeout=60,
                        )
                        reply = resp.json()["reply"] if resp.status_code == 200 else \
                            "Sorry, I couldn't reach the wellness assistant right now."
                    except requests.exceptions.RequestException:
                        reply = "Sorry, I couldn't reach the wellness assistant right now."
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()

                if st.session_state.chat_history and st.button("Clear chat"):
                    st.session_state.chat_history = []
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)



        else:
            st.subheader("Employee Wellness Report")

            latest = get_latest_mood_per_employee()
            if not latest:
                st.info("No employee entries yet.")
            else:
                st.write("**Latest mood per employee**")
                table_rows = [{
                    "Employee": row["username"],
                    "Email": row["email"],
                    "Date": row["mood_date"],
                    "Time": row["created_at"].strftime("%H:%M"),
                    "Mood": f"{style_for(row['sentiment'])['emoji']} {row['sentiment']}",
                    "Emotion": row["emotion"],
                } for row in latest]
                st.dataframe(table_rows, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.write("**Team mood trend (last 30 days)**")
            history = get_all_employee_mood_logs(limit_days=30)
            if not history:
                st.info("Not enough data yet to draw a trend chart.")
            else:
                by_date = {}
                for row in history:
                    d = row["mood_date"]
                    by_date.setdefault(d, []).append(MOOD_TO_NUM.get(row["sentiment"], 0))
                trend = {str(d): sum(v) / len(v) for d, v in sorted(by_date.items())}
                st.line_chart(trend)
                st.caption("Average mood score per day across all employees "
                           "(2 = Happy, 0 = Neutral, -1 = Sad/Stress, -2 = Angry/Fear)")
            st.markdown("</div>", unsafe_allow_html=True)

        st.stop()
    st.session_state.token = None


if st.session_state.page == "welcome":

    if not st.session_state.show_auth_panel:
        st.markdown('<div class="hero-bg">',unsafe_allow_html=True)

        # ---------------- LANDING NAVBAR ---------------- #

        nav_left, nav_space, nav_login = st.columns([2, 5, 2])

        with nav_left:
            st.markdown("""
            <div class="logo">
                🧠 Mood <span>Mentor</span>
            </div>
            """, unsafe_allow_html=True)

        with nav_login:
            if st.button(
                "Login",
                key="landing_login",
                use_container_width=True
            ):
                st.session_state.show_auth_panel = True
                st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
        # ---------------- HERO ---------------- #
        st.markdown('<br>',unsafe_allow_html=True)
        left,right=st.columns([1.2,1])

        with left:

            st.markdown("""
        <div class="badge">

        AI POWERED EMPLOYEE WELLNESS PLATFORM

        </div>
        """,unsafe_allow_html=True)

            st.markdown("""
        <div class="hero-title">

        Understand Your Emotions,<br>

        <span>Improve Your Well-being.</span>

        </div>
        """,unsafe_allow_html=True)

            st.markdown("""
        <div class="hero-text">

        Mood Mentor combines AI-powered emotion detection,

        journal analysis, wellness chat, and mood analytics

        to help employees maintain better mental health.

        </div>
        """,unsafe_allow_html=True)

        with right:

            with st.container(key="hero_image"):
                st.image(
                    "Images/Landing1.avif",
                    use_container_width=True
                )

        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("""
        <div class="section-title">
        Powerful Features for a Healthier You
        </div>

        <div class="section-subtitle">
        Everything you need to understand, track and improve employee well-being.
        </div>
        """,unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)

        with c1:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">😊</div>

        <div class="feature-title">

        Mood Tracking

        </div>

        <div class="feature-text">

        Track your daily emotions effortlessly and build healthy habits.

        </div>

        </div>
        """,unsafe_allow_html=True)

        with c2:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">📖</div>

        <div class="feature-title">

        AI Journal Analysis

        </div>

        <div class="feature-text">

        Analyze journals using AI emotion detection and receive personalized insights.

        </div>

        </div>
        """,unsafe_allow_html=True)

        with c3:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">📈</div>

        <div class="feature-title">

        Mood Analytics

        </div>

        <div class="feature-text">

        Visualize emotional trends through interactive charts and dashboards.

        </div>

        </div>
        """,unsafe_allow_html=True)
        st.write("")

        c1,c2,c3=st.columns(3)

        with c1:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">📅</div>

        <div class="feature-title">

        Mood Calendar

        </div>

        <div class="feature-text">

        See your emotional journey day-by-day in a beautiful calendar.

        </div>

        </div>
        """,unsafe_allow_html=True)

        with c2:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">💬</div>

        <div class="feature-title">

        Wellness Chat

        </div>

        <div class="feature-text">

        Talk privately with your AI wellness companion anytime.

        </div>

        </div>
        """,unsafe_allow_html=True)

        with c3:

            st.markdown("""
        <div class="feature-card">

        <div class="feature-icon">📄</div>

        <div class="feature-title">

        PDF Reports

        </div>

        <div class="feature-text">

        Download comprehensive wellness reports and insights anytime.

        </div>

        </div>
        """,unsafe_allow_html=True)
        # ---------------- STATS ---------------- #

        with st.container(key="stats_container"):

            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.markdown("""
                <div class="stat-item stat-divider">
                <div class="stat-icon" style="background:#EEF4FF;">
                📈
                </div>
                <div class="stat">
                    <div class="stat-number">98%</div>
                    <div class="stat-title">Emotion Detection</div>
                    <div class="stat-sub">AI Accuracy</div>
                </div>
                """, unsafe_allow_html=True)

            with s2:
                st.markdown("""
                <div class="stat-item stat-divider">
                <div class="stat-icon" style="background:#EEF4FF;">
                👥
                </div>
                <div class="stat">
                    <div class="stat-number">10K+</div>
                    <div class="stat-title">Mood Entries</div>
                    <div class="stat-sub">Successfully Logged</div>
                </div>
                """, unsafe_allow_html=True)

            with s3:
                st.markdown("""
                <div class="stat-item stat-divider">
                <div class="stat-icon" style="background:#EEF4FF;">
                🕒
                </div>
                <div class="stat">
                    <div class="stat-number">24/7</div>
                    <div class="stat-title">AI Assistant</div>
                    <div class="stat-sub">Always Available</div>
                </div>
                """, unsafe_allow_html=True)

            with s4:
                st.markdown("""
                <div class="stat-item stat-divider">
                <div class="stat-icon" style="background:#EEF4FF;">
                🕒
                </div>
                <div class="stat">
                    <div class="stat-number">100%</div>
                    <div class="stat-title">Secure</div>
                    <div class="stat-sub">Private & Encrypted</div>
                </div>
                """, unsafe_allow_html=True) 
        st.markdown("""

        <div class="section-title">

        How Mood Mentor Works

        </div>

        <div class="section-subtitle">

        A simple journey towards better emotional wellness.

        </div>

        """,unsafe_allow_html=True)  
        c1,c2,c3,c4,c5=st.columns(5)

        steps=[

        ("😊","Log Mood","Select today's mood."),

        ("📖","Write Journal","Express your thoughts."),

        ("🤖","AI Analysis","Detect emotions instantly."),

        ("📊","Get Insights","Visualize emotional trends."),

        ("🌱","Improve Wellness","Build healthier habits.")

        ]

        for col,(icon,title,text) in zip([c1,c2,c3,c4,c5],steps):

            with col:

                st.markdown(f"""

        <div class="timeline-card">

        <div class="timeline-icon">

        {icon}

        </div>

        <div class="timeline-number">

        {steps.index((icon,title,text))+1}

        </div>

        <div class="timeline-title">

        {title}

        </div>

        <div class="timeline-text">

        {text}

        </div>

        </div>

        """,unsafe_allow_html=True)    
                
        # ---------------- CTA ---------------- #

        with st.container(key="cta_container"):

            left, right = st.columns([1, 1.3], gap="large")

            # LEFT — Image
            with left:
                st.markdown('<div class="cta-image">', unsafe_allow_html=True)

                st.image(
                    "Images/Landing.jpg.jpeg",
                    use_container_width=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

            # RIGHT — CTA Content
            with right:

                st.markdown("""
                <div class="cta-title">
                    Start Your Wellness Journey Today
                </div>

                <div class="cta-text">
                    Take the first step toward a healthier workplace.

                    Mood Mentor helps employees monitor emotions,
                    reduce stress, and improve overall well-being
                    through AI-powered insights.
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "🚀 Login to Get Started",
                    use_container_width=True,
                    key="cta_login"
                ):
                    st.session_state.show_auth_panel = True
                    st.rerun() 
        st.markdown("""

        <div class="footer">

        🧠 <b>Mood Mentor</b><br><br>

        © 2026 Mood Mentor

        AI Powered Employee Wellness Platform

        </div>

        """,unsafe_allow_html=True)               

        st.stop()

    # ============================================================
    # AUTHENTICATION PAGE
    # ============================================================
    # ============================================================
    # AUTHENTICATION PAGE
    # ============================================================

    with st.container(key="auth_page_container"):

        left, right = st.columns(
            [1.15, 0.85],
            gap="small")

        # ============================================================
        # LEFT — BRAND / AUTH INTRO
        # ============================================================

        with left:

            st.markdown("""
            <div class="auth-left">
                <div class="auth-logo">
                    <div class="auth-logo-icon">🧠</div>
                    <div class="auth-logo-text">
                        Mood<span>Mentor</span>
                    </div>
                </div>
                <div class="auth-badge">
                    ✨ AI-Powered Emotional Wellness Platform
                </div>
                <div class="auth-heading">
                    Better Insights.<br>
                    Better <span>You.</span>
                </div>
                <div class="auth-description">
                    Understand your emotions. Improve your well-being.
                    Track your mood, reflect in your journal, and get
                    personalized support to live your best work life.
                </div>
                <div class="auth-features">
                    <div class="auth-feature">
                        <div class="auth-feature-icon"
                            style="background:#E8F8EE;">
                            📈
                        </div>
                        <div class="auth-feature-title">
                            Track Mood
                        </div>
                        <div class="auth-feature-text">
                            Log and monitor your emotions.
                        </div>
                    </div>
                    <div class="auth-feature">
                        <div class="auth-feature-icon"
                            style="background:#EEE9FF;">
                            🧠
                        </div>
                        <div class="auth-feature-title">
                            AI Insights
                        </div>
                        <div class="auth-feature-text">
                            Get personalized recommendations.
                        </div>
                    </div>
                    <div class="auth-feature">
                        <div class="auth-feature-icon"
                            style="background:#E8F1FF;">
                            📖
                        </div>
                        <div class="auth-feature-title">
                            Journal
                        </div>
                        <div class="auth-feature-text">
                            Express your thoughts freely.
                        </div>
                    </div>
                    <div class="auth-feature">
                        <div class="auth-feature-icon"
                            style="background:#FFF0E2;">
                            💬
                        </div>
                        <div class="auth-feature-title">
                            Wellness Chat
                        </div>
                        <div class="auth-feature-text">
                            Talk and feel better, anytime.
                        </div>
                    </div>
                </div>
                <div class="auth-visual">
                    <img src="Images/Landing.jpg.jpeg">
                </div>
                <div class="auth-quote">
                    Small steps every day lead to big changes. 💜
                </div>
            </div>
            """, unsafe_allow_html=True)


        # ============================================================
        # RIGHT — LOGIN / SIGNUP / VERIFY / FORGOT / RESET
        # ============================================================

        with right:

            with st.container(key="auth_right_container"):

                with st.container(key="auth_card_container"):

                    mode = st.session_state.auth_mode

                    # --------------------------------------------------------
                    # LOGIN
                    # --------------------------------------------------------

                    if mode == "login":

                        st.markdown("""
                        <div class="auth-title">
                            Welcome Back!
                        </div>
                        <div class="auth-subtitle">
                            Login to your account
                        </div>
                        """, unsafe_allow_html=True)

                        with st.form("login"):

                            email = st.text_input(
                                "Email",
                                placeholder="Enter your email"
                            )

                            pw = st.text_input(
                                "Password",
                                type="password",
                                placeholder="Enter your password"
                            )

                            go = st.form_submit_button(
                                "Login  →",
                                type="primary",
                                use_container_width=True
                            )

                        if go:

                            u = get_user(email.strip().lower())

                            if not u or not check_pw(
                                pw,
                                u["password_hash"]
                            ):

                                st.error("Invalid email or password.")

                            elif not u["is_verified"]:

                                st.warning("Verify your email first.")

                                st.session_state.email = u["email"]

                                goto_auth("verify")

                            else:

                                st.session_state.token = make_token(u)

                                st.rerun()


              
                        if st.button(
                            "Forgot password?",
                            key="login_forgot",
                            use_container_width=False
                        ):
                            goto_auth("forgot")
                        if st.button(
                            "Create a new account",
                            key="login_signup",
                            use_container_width=False
                        ):
                            goto_auth("signup")


                    # --------------------------------------------------------
                    # SIGNUP
                    # --------------------------------------------------------

                    elif mode == "signup":

                        st.markdown("""
                        <div class="auth-card-illustration"></div>
                        <div class="auth-title">
                            Create Account
                        </div>
                        <div class="auth-subtitle">
                            Start your wellness journey
                        </div>
                        """, unsafe_allow_html=True)

                        with st.form("signup"):

                            username = st.text_input(
                                "Full Name",
                                placeholder="Enter your full name"
                            )

                            email = st.text_input(
                                "Email",
                                placeholder="Enter your email"
                            )

                            pw = st.text_input(
                                "Password",
                                type="password",
                                placeholder="Create password"
                            )

                            role_label = st.radio(
                                "I am signing up as a:",
                                ["Employee", "Manager"],
                                horizontal=True
                            )

                            go = st.form_submit_button(
                                "Send OTP  →",
                                type="primary",
                                use_container_width=True
                            )

                        if go:

                            email = email.strip().lower()

                            role = (
                                "manager"
                                if role_label == "Manager"
                                else "employee"
                            )

                            if len(username) < 3:

                                st.error("Username too short.")

                            elif not valid_pw(pw):

                                st.error(
                                    "Password needs 8+ chars, letters and numbers."
                                )

                            elif username_taken(username) or get_user(email):

                                st.error(
                                    "Username or email already in use."
                                )

                            else:

                                create_user(
                                    username,
                                    email,
                                    pw,
                                    role=role
                                )

                                code = new_otp()

                                save_otp(
                                    email,
                                    code,
                                    "signup"
                                )

                                ok, msg = send_otp(
                                    email,
                                    code,
                                    "signup"
                                )

                                if ok:

                                    st.session_state.email = email

                                    st.success(
                                        "Check your email for the code."
                                    )

                                    goto_auth("verify")

                                else:

                                    st.error(
                                        f"Email failed: {msg}"
                                    )

                        if st.button(
                            "← Already have an account? Login",
                            key="signup_login"
                        ):
                            goto_auth("login")


                    # --------------------------------------------------------
                    # VERIFY OTP
                    # --------------------------------------------------------

                    elif mode == "verify":

                        email = st.session_state.email

                        st.markdown("""
                        <div class="auth-card-illustration"></div>

                        <div class="auth-title">
                            Verify Your Email
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(
                            f"""
                            <div class="auth-subtitle">
                                We sent a 6-digit verification code to<br>
                                <b>{email}</b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        with st.form("verify"):

                            code = st.text_input(
                                "Verification Code",
                                max_chars=6,
                                placeholder="Enter 6-digit code"
                            )

                            go = st.form_submit_button(
                                "Verify OTP  →",
                                type="primary",
                                use_container_width=True
                            )

                        if go:

                            if check_otp(
                                email,
                                code.strip(),
                                "signup"
                            ):

                                verify_user(email)

                                st.success(
                                    "Verified! Please log in."
                                )

                                goto_auth("login")

                            else:

                                st.error(
                                    "Invalid or expired code."
                                )

                        if st.button(
                            "← Back to login",
                            key="verify_back"
                        ):
                            goto_auth("login")


                    # --------------------------------------------------------
                    # FORGOT PASSWORD
                    # --------------------------------------------------------

                    elif mode == "forgot":

                        st.markdown("""
                        <div class="auth-card-illustration"></div>

                        <div class="auth-title">
                            Forgot Password?
                        </div>

                        <div class="auth-subtitle">
                            We'll send you a reset code
                        </div>
                        """, unsafe_allow_html=True)

                        with st.form("forgot"):

                            email = st.text_input(
                                "Email",
                                placeholder="Enter your account email"
                            )

                            go = st.form_submit_button(
                                "Send Reset Code  →",
                                type="primary",
                                use_container_width=True
                            )

                        if go:

                            email = email.strip().lower()

                            if get_user(email):

                                code = new_otp()

                                save_otp(
                                    email,
                                    code,
                                    "password_reset"
                                )

                                send_otp(
                                    email,
                                    code,
                                    "password_reset"
                                )

                            st.session_state.email = email

                            st.info(
                                "If that email exists, a code was sent."
                            )

                            goto_auth("reset")

                        if st.button(
                            "← Back to login",
                            key="forgot_back"
                        ):
                            goto_auth("login")


                    # --------------------------------------------------------
                    # RESET PASSWORD
                    # --------------------------------------------------------

                    elif mode == "reset":

                        email = st.session_state.email

                        st.markdown("""
                        <div class="auth-card-illustration"></div>

                        <div class="auth-title">
                            Reset Password
                        </div>

                        <div class="auth-subtitle">
                            Create a new secure password
                        </div>
                        """, unsafe_allow_html=True)

                        with st.form("reset"):

                            code = st.text_input(
                                "Reset Code",
                                max_chars=6,
                                placeholder="Enter reset code"
                            )

                            pw = st.text_input(
                                "New Password",
                                type="password",
                                placeholder="Enter new password"
                            )

                            go = st.form_submit_button(
                                "Reset Password  →",
                                type="primary",
                                use_container_width=True
                            )

                        if go:

                            if not valid_pw(pw):

                                st.error(
                                    "Password needs 8+ chars, letters and numbers."
                                )

                            elif not check_otp(
                                email,
                                code.strip(),
                                "password_reset"
                            ):

                                st.error(
                                    "Invalid or expired code."
                                )

                            else:

                                set_password(
                                    email,
                                    pw
                                )

                                st.success(
                                    "Password reset. Please log in."
                                )

                                goto_auth("login")

                        if st.button(
                            "← Back to login",
                            key="reset_back"
                        ):
                            goto_auth("login")


                    
                    st.markdown("""
                    <div class="auth-security">
                        🛡️ &nbsp; Your data is safe, secure and confidential.
                    </div>
                    """, unsafe_allow_html=True)

  
    st.stop()

