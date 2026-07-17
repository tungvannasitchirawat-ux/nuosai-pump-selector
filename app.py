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

# 2. คลังข้อมูลภาษา (แก้ไข: เพิ่มรายการแปลที่ขาดหายไป)
translation = {
    "TH": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "ระบบคำนวณทางวิศวกรรมชลศาสตร์ Nuosai",
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
        "btn_submit": "🚀 คำนวณสเปกและค้นหารุ่นปั๊มน้ำ",
        "btn_back": "⬅️ ย้อนกลับไปแก้ไขข้อมูลสเปก",
        "matches_count": "พบรุ่นผลิตภัณฑ์ที่รองรับสเปกหน้างานของคุณทั้งหมด {count} รุ่น",
        "select_pump_label": "🔍 เลือกรุ่นปั๊มน้ำจากผลลัพธ์การคำนวณ:",
        "curve_title": "📉 1. Factory Performance Curve",
        "dim_title": "📐 2. Pump Outline Dimensions"
    },
    "EN": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "Advanced Hydraulic Calculation & Performance Curve Viewer",
        "sec_input": "📥 1. Design Parameters (Inputs)",
        "cat_select": "Application Classification",
        "series_select": "Select Pump Series",
        "all_series": "All Pump Series",
        "cat_building": "1. Residential Houses 1-3 Floors",
        "cat_booster": "2. Automatic Booster Pump Set System",
        "cat_watersupply": "3. Water Supply & Transfer Pump System",
        "cat_agriculture": "4. Agriculture & Irrigation System",
        "cat_fire": "5. Fire Fighting & Protection System",
        "cat_industrial": "6. Industrial & Process System",
        "cat_wastewater": "7. Wastewater & Environmental System",
        "flow_label": "Design Flow Rate (m³/hr)",
        "v_head_label": "Vertical Static Head (meters)",
        "h_pipe_label": "Horizontal Pipe Length (meters)",
        "pipe_dia_label": "Main Pipe Size (Inch)",
        "btn_submit": "🚀 Run Calculation & Match Products",
        "btn_back": "⬅️ Back to Modify Inputs",
        "matches_count": "Found {count} models matching your design parameters.",
        "select_pump_label": "🔍 Select pump model:",
        "curve_title": "📉 1. Factory Performance Curve",
        "dim_title": "📐 2. Pump Outline Dimensions"
    }
}

# 3. Sidebar
st.sidebar.markdown(f"### 🎛️ Control Panel")
lang_choice = st.sidebar.radio("🌐 Language Selector", ["🇹🇭 ไทย / TH", "🇺🇸 English / EN"], index=1 if st.session_state.get("lang") == "EN" else 0)
lang = "TH" if "🇹🇭" in lang_choice else "EN"
st.session_state["lang"] = lang
t = translation[lang]

# เนื้อหาหลัก
if "current_page" not in st.session_state: st.session_state["current_page"] = "input_page"

# ส่วนการคำนวณที่แก้ไข Key Error
st.markdown(f"### {t['sec_input']}")
cat_options = [t["cat_building"], t["cat_booster"], t["cat_watersupply"], t["cat_agriculture"], t["cat_fire"], t["cat_industrial"], t["cat_wastewater"]]
select_cat = st.selectbox(t["cat_select"], cat_options)
# ... (โค้ดส่วนที่เหลือเหมือนเดิมได้เลยครับ)
