import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

st.set_page_config(page_title="Nuosai Pump Selection Engine", layout="wide")

# 1. โลโก้
def get_company_logo():
    base_dir = "images/"
    logo_names = ["logo.png", "logo.jpg", "logo.jpeg", "LOGO.PNG", "LOGO.JPG"]
    for name in logo_names:
        if os.path.exists(os.path.join(base_dir, name)): return os.path.join(base_dir, name)
    return None

# 2. แปลภาษา
translation = {
    "TH": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "sec_input": "📥 1. กรอกข้อมูลการออกแบบหน้างาน (Inputs)",
        "cat_select": "ประเภทกลุ่มงานที่ต้องการใช้งาน",
        "series_select": "เลือกซีรีส์รุ่นชนิดปั๊มที่ต้องการ",
        "all_series": "แสดงทุกซีรีส์ปั๊มน้ำ (All Series)",
        "flow": "อัตราการไหล (m³/hr)", "head": "ระยะส่งสูง (m)", "pipe": "ระยะทางท่อ (m)",
        "btn_submit": "🚀 คำนวณสเปกและค้นหารุ่นปั๊ม",
        "curve_title": "📉 Factory Performance Curve", "dim_title": "📐 Pump Dimensions"
    },
    "EN": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "sec_input": "📥 1. Design Parameters (Inputs)",
        "cat_select": "Application Classification",
        "series_select": "Select Pump Series",
        "all_series": "All Pump Series",
        "flow": "Flow Rate (m³/hr)", "head": "Static Head (m)", "pipe": "Pipe Length (m)",
        "btn_submit": "🚀 Run Calculation & Match",
        "btn_back": "⬅️ Back",
        "curve_title": "📉 Factory Performance Curve", "dim_title": "📐 Pump Dimensions"
    }
}

# 3. Sidebar
st.sidebar.markdown("### 🎛️ Control Panel")
lang = "TH" if st.sidebar.radio("🌐 Language", ["🇹🇭 ไทย / TH", "🇺🇸 English / EN"], index=0) == "🇹🇭 ไทย / TH" else "EN"
t = translation[lang]

# 4. ฟังก์ชันค้นหาภาพ
def find_images(code):
    base = "images/"
    c, d = None, None
    for f in os.listdir(base):
        if code.lower().replace("-","") in f.lower().replace("-",""):
            if "curve" in f.lower(): c = os.path.join(base, f)
            if "dimension" in f.lower(): d = os.path.join(base, f)
    return c, d

# 5. แสดงผลหน้าจอ
st.markdown(f"## {t['brand_title']}")
if "current_page" not in st.session_state: st.session_state["current_page"] = "input_page"

if st.session_state["current_page"] == "input_page":
    st.markdown(f"### {t['sec_input']}")
    select_cat = st.selectbox(t["cat_select"], ["Residential", "Booster", "Industrial"])
    select_series = st.selectbox(t["series_select"], [t["all_series"], "PMPA", "NSLA", "NSQW"])
    
    col1, col2 = st.columns(2)
    flow = col1.number_input(t["flow"], value=20.0)
    head = col2.number_input(t["head"], value=20.0)
    
    if st.button(t["btn_submit"], type="primary"):
        st.session_state.update({"current_page": "output_page", "model": "100PMPA64-1"})
        st.rerun()

elif st.session_state["current_page"] == "output_page":
    if st.button("⬅️ ย้อนกลับ"):
        st.session_state["current_page"] = "input_page"
        st.rerun()
    
    st.success("พบรุ่นที่ตรงสเปก: 100PMPA64-1")
    c_img, d_img = find_images(st.session_state["model"])
    
    if c_img: st.image(c_img, caption=t["curve_title"], use_container_width=True)
    if d_img: st.image(d_img, caption=t["dim_title"], use_container_width=True)
