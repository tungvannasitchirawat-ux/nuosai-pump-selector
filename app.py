import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# 1. การตั้งค่าหน้าจอระดับโปร
st.set_page_config(
    page_title="Nuosai Pump Selection Engine", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌐 ฟังก์ชันดึงโลโก้
def get_company_logo():
    base_dir = "images/"
    logo_names = ["logo.png", "logo.jpg", "logo.jpeg", "LOGO.PNG", "LOGO.JPG"]
    if os.path.exists(base_dir):
        for name in logo_names:
            full_path = os.path.join(base_dir, name)
            if os.path.exists(full_path):
                return full_path
    return None

logo_path = get_company_logo()

# 2. คลังข้อมูลภาษา
translation = {
    "TH": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "ระบบคำนวณทางวิศวกรรมชลศาสตร์ Nuosai",
        "sidebar_title": "⚙️ การตั้งค่าระบบ / Settings",
        "lang_select": "🌐 เลือกภาษา (Language)",
        "sec_input": "📥 1. กรอกข้อมูลการออกแบบหน้างาน (Inputs)",
        "cat_select": "ประเภทกลุ่มงานที่ต้องการใช้งาน",
        "series_select": "เลือกซีรีส์รุ่นชนิดปั๊มที่ต้องการ (Pump Series)",
        "all_series": "แสดงทุกซีรีส์ปั๊มน้ำ (All Series)",
        
        "cat_building": "1. งานบ้านพักอาศัยขนาด 1-3 ชั้น (Residential Houses)",
        "cat_booster": "2. ชุดปั๊มเสริมแรงดันอัตโนมัติ (Booster Pump Set)",
        "cat_watersupply": "3. ระบบสูบส่งน้ำขึ้นดาดฟ้า (Transfer / Water Supply)",
        "cat_agriculture": "4. งานการเกษตรและระบบชลประทาน (Agriculture & Irrigation)",
        "cat_fire": "5. งานระบบป้องกันอัคคีภัย (Fire Fighting System)",
        "cat_industrial": "6. งานระบบในโรงงานอุตสาหกรรม (Industrial & Process System)",
        "cat_wastewater": "7. งานระบบบำบัดน้ำเสียและสิ่งแวดล้อม (Wastewater & Environmental System)",
        
        "flow_label": "อัตราการไหลที่ต้องการ / Flow Rate (m³/hr)",
        "v_head_label": "ระยะส่งสูงแนวดิ่งจริง / Vertical Static Head (m)",
        "h_pipe_label": "ระยะทางเดินท่อนอนรวม / Horizontal Pipe Length (m)",
        "pipe_dia_label": "ขนาดท่อส่งหลัก / Main Pipe Diameter (Inch)",
        "pipe_mat_label": "ชนิดวัสดุของท่อส่ง / Pipe Material",
        "particle_label": "ลักษณะของเหลวและสารแขวนลอย / Liquid & Particles Type",
        "temp_label": "🌡️ อุณหภูมิของเหลวหน้างาน / Liquid Temperature (°C)",
        
        "sec_calc": "📊 ผลลัพธ์การวิเคราะห์ระบบจากการคำนวณ (Hydraulic Outputs)",
        "metric_flow": "อัตราการไหลดีไซน์",
        "metric_head": "ระยะส่งรวม (TDH)",
        "metric_motor": "มอเตอร์ที่แนะนำขั้นต่ำ",
        
        "sec_match": "🎯 ผลลัพธ์ปั๊มน้ำรุ่นที่ผ่านเกณฑ์คำนวณ",
        "select_pump_label": "🔍 เลือกรุ่นปั๊มน้ำจากผลลัพธ์การคำนวณ:",
        "matches_count": "พบรุ่นผลิตภัณฑ์ที่รองรับสเปกหน้างานของคุณทั้งหมด {count} รุ่น",
        "error_msg": "⚠️ ไม่พบรุ่นปั๊มที่ตรงสเปกในช่วงคำนวณนี้",
        "btn_submit": "🚀 คำนวณสเปกและค้นหารุ่นปั๊มน้ำ",
        "btn_back": "⬅️ ย้อนกลับไปแก้ไขข้อมูลสเปก",
        "curve_title": "📉 1. Factory Performance Curve",
        "dim_title": "📐 2. Pump Outline Dimensions"
    },
    "EN": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "Advanced Hydraulic Calculation & Performance Curve Viewer",
        "sidebar_title": "🎛️ Control Panel",
        "lang_select": "🌐 Language Selector",
        "sec_input": "📥 1. Design Parameters (Inputs)",
        "cat_select": "Application Classification",
        "series_select": "Select Pump Series",
        "all_series": "All Pump Series",
        "sec_calc": "📊 Hydraulic Engineering Outputs",
        "metric_flow": "Design Flow Rate",
        "metric_head": "Total Dynamic Head",
        "metric_motor": "Min. Motor Required",
        "sec_match": "🎯 Matching Nuosai Product Selection",
        "select_pump_label": "🔍 Select pump model based on calculation below:",
        "matches_count": "Found {count} models matching your design parameters.",
        "error_msg": "⚠️ No matching models found.",
        "btn_submit": "🚀 Run Calculation & Match Products",
        "btn_back": "⬅️ Back to Modify Inputs",
        "curve_title": "📉 1. Factory Performance Curve",
        "dim_title": "📐 2. Pump Outline Dimensions"
    }
}

# 3. Sidebar
st.sidebar.markdown(f"### 🎛️ Control Panel")
lang_choice = st.sidebar.radio("🌐 Language Selector", ["🇹🇭 ไทย / TH", "🇺🇸 English / EN"], index=0)
lang = "TH" if "🇹🇭" in lang_choice else "EN"
t = translation[lang]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "input_page"

def find_pump_images(code_key):
    base_dir = "images/"
    if not os.path.exists(base_dir): return None, None
    clean_code = code_key.lower().replace(" ", "").replace("-", "").replace("_", "")
    curve_img, dim_img = None, None
    for f in os.listdir(base_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            f_clean = f.lower().replace(" ", "").replace("-", "").replace("_", "")
            if clean_code in f_clean or f_clean in clean_code:
                if "dimension" in f.lower(): dim_img = os.path.join(base_dir, f)
                elif "curve" in f.lower() or "curev" in f.lower(): curve_img = os.path.join(base_dir, f)
    return curve_img, dim_img

# 4. แสดงผลหลัก
if logo_path:
    col_log1, col_log2 = st.columns([1, 5])
    with col_log1: st.image(Image.open(logo_path), width=110)
    with col_log2: st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 15px; border-radius: 12px; height: 110px; display: flex; flex-direction: column; justify-content: center;'><h1 style='color: white; font-size: 24px; font-weight: 700; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 13px; margin: 4px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px;'><h1 style='color: white; font-size: 26px; font-weight: 700; text-align: center; margin: 0;'>{t['brand_title']}</h1></div>", unsafe_allow_html=True)

# เนื้อหาหลัก (คำนวณอัตโนมัติเท่านั้น)
if st.session_state["current_page"] == "input_page":
    st.markdown(f"### {t['sec_input']}")
    col1, col2 = st.columns(2, gap="medium")
    with st.container(border=True):
        cat_options = [t["cat_building"], t["cat_booster"], t["cat_watersupply"], t["cat_agriculture"], t["cat_fire"], t["cat_industrial"], t["cat_wastewater"]]
        select_cat = st.selectbox(t["cat_select"], cat_options)
        
        series_options = [t["all_series"], "PWPC", "NSWA", "NSTQW", "NSQW", "NSLA", "PMP", "PMPA"]
        select_series = st.selectbox(t["series_select"], series_options, index=0)
        selected_series_key = None if select_series == t["all_series"] else select_series
        
        with col1:
            flow_rate = st.number_input(t["flow_label"], value=20.0, step=1.0)
            static_head = st.number_input(t["v_head_label"], value=20.0, step=1.0)
            horiz_pipe = st.number_input(t["h_pipe_label"], value=20.0, step=2.0)
        with col2:
            pipe_dia = st.selectbox(t["pipe_dia_label"], [1.0, 1.5, 2.0, 2.5, 3.0, 4.0], index=2)
            temp = st.slider(t["temp_label"], -10, 150, 25)
            
    if st.button(t["btn_submit"], type="primary", use_container_width=True):
        st.session_state.update({"flow": flow_rate, "head": static_head, "series": selected_series_key, "current_page": "output_page"})
        st.rerun()

elif st.session_state["current_page"] == "output_page":
    if st.button(t["btn_back"], type="secondary"):
        st.session_state["current_page"] = "input_page"
        st.rerun()
    st.markdown("---")
    st.success(t["matches_count"].format(count=5)) # จำลองผลลัพธ์
    selected_model = st.selectbox(t["select_pump_label"], ["100PMPA64-1", "50NSQW15-15-1.5", "NSLA32-25-2"])
    
    curve_img, dim_img = find_pump_images(selected_model)
    if curve_img:
        st.write(f"### {t['curve_title']}")
        st.image(Image.open(curve_img), use_container_width=True)
    if dim_img:
        st.write(f"### {t['dim_title']}")
        st.image(Image.open(dim_img), use_container_width=True)
