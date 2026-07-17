import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# 1. การตั้งค่าหน้าจอระดับโปร (Layout กว้างเต็มตา สมดุล สวยงาม)
st.set_page_config(
    page_title="Nuosai Pump Selection Engine", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌐 ฟังก์ชันสำหรับดึงภาพโลโก้บริษัทอย่างปลอดภัย
def get_company_logo():
    base_dir = "C:/nuosai-pump-selector/images/"
    logo_names = ["logo.png", "logo.jpg", "logo.jpeg", "LOGO.PNG", "LOGO.JPG"]
    if os.path.exists(base_dir):
        for name in logo_names:
            full_path = os.path.join(base_dir, name)
            if os.path.exists(full_path):
                return full_path
    return None

# ประกาศตัวแปรโลโก้ให้ถูกต้อง ป้องกันหน้าจอขาว
logo_path = get_company_logo()

# 2. คลังข้อมูลภาษาสำหรับการแปลระบบ (สลับ TH/EN สมบูรณ์แบบ)
translation = {
    "TH": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "ระบบคำนวณทางวิศวกรรมชลศาสตร์และคัดเลือกรุ่นผลิตภัณฑ์ Nuosai",
        "sidebar_title": "⚙️ การตั้งค่าระบบ / Settings",
        "lang_select": "🌐 เลือกภาษา (Language)",
        "sec_input": "📥 กรอกข้อมูลการออกแบบหน้างาน (Inputs)",
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
        
        "part_clean": "💧 น้ำสะอาดบริสุทธิ์ (ไม่มีพาร์ทิเคิลเจือปน)",
        "part_soft": "🍃 น้ำปนเศษตะกอนอ่อน (มีเศษดิน/ทรายละเอียด < 5mm)",
        "part_slurry": "🪵 น้ำโคลนหนาแน่น / สารเคมีหนืด / น้ำเสียเข้มข้น",
        
        "mat_pvc": "ท่อ PVC / PE (ผิวเรียบมาก แรงเสียดทานต่ำสุด)",
        "mat_ss": "ท่อสแตนเลส (Stainless Steel)",
        "mat_galvanized": "ท่อเหล็กชุบสังกะสี (Galvanized Steel)",
        "mat_black_iron": "ท่อเหล็กดำ / เหล็กหล่อ (Black Iron)",
        
        "sec_calc": "📊 ผลลัพธ์การวิเคราะห์ระบบจากการคำนวณ (Hydraulic Engineering Outputs)",
        "metric_flow": "อัตราการไหลดีไซน์",
        "metric_head": "ระยะส่งรวม (TDH)",
        "metric_motor": "มอเตอร์ที่แนะนำขั้นต่ำ",
        
        "sec_match": "🎯 ผลิตภัณฑ์ Nuosai รุ่นที่ผ่านเกณฑ์การคำนวณ",
        "select_pump_label": "🔍 เลือกรุ่นปั๊มน้ำที่ต้องการใช้งานจากผลลัพธ์คำนวณด้านล่างนี้:",
        "matches_count": "พบรุ่นผลิตภัณฑ์ที่รองรับสเปกหน้างานของคุณทั้งหมด {count} รุ่น",
        "motor_size": "ขนาดมอเตอร์ติดตั้งจริงของรุ่นนี้",
        "meter": "เมตร",
        "error_msg": "⚠️ ไม่พบรุ่นสินค้าในแคตตาล็อกที่รองรับแรงดัน (Head) หรืออัตราไหลในช่วงคำนวณนี้ กรุณาขยายขนาดท่อเพื่อลด Friction หรือปรับลดสเปกหน้างาน",
        "temp_extreme_alert": "❌ ของเหลวร้อนเกินขีดจำกัดความปลอดภัยของโครงสร้างปั๊มรุ่นมาตรฐานทั่วไป",
        
        "tab_pic": "📐 ขนาดและมิติตัวปั๊ม (Dimension Sheet)",
        "tab_curve_catalog": "📉 กราฟจากแคตตาล็อกโรงงาน (Performance Curve)",
        "img_not_found": "ℹ️ ไม่พบไฟล์ภาพในโฟลเดอร์ คาดว่าชื่อไฟล์ในระบบไม่ตรงกับชื่อรุ่น",
        
        "btn_submit": "🚀 คำนวณสเปกและค้นหารุ่นปั๊มน้ำ",
        "btn_back": "⬅️ ย้อนกลับไปแก้ไขข้อมูลสเปก"
    },
    "EN": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "Advanced Hydraulic Calculation & Product Matching Engine",
        "sidebar_title": "⚙️ System Configuration",
        "lang_select": "🌐 Select Language",
        "sec_input": "📥 Design Parameters (Inputs)",
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
        "pipe_mat_label": "Pipe Material",
        "particle_label": "Liquid & Particles Type",
        "temp_label": "🌡️ Liquid Temperature (°C)",
        
        "part_clean": "💧 Pure Clean Water",
        "part_soft": "🍃 Water with Soft Solids (< 5mm)",
        "part_slurry": "🪵 Slurry & Viscous Liquids",
        
        "mat_pvc": "PVC / PE Pipe (Low Friction)",
        "mat_ss": "Stainless Steel Pipe",
        "mat_galvanized": "Galvanized Steel Pipe",
        "mat_black_iron": "Black Iron / Cast Iron Pipe",
        
        "sec_calc": "📊 Hydraulic Engineering Outputs",
        "metric_flow": "Design Flow Rate",
        "metric_head": "Total Dynamic Head",
        "metric_motor": "Min. Motor Required",
        
        "sec_match": "🎯 Matching Nuosai Product Selection",
        "select_pump_label": "🔍 Select the desired pump model based on calculation below:",
        "matches_count": "Found {count} models matching your design parameters.",
        "motor_size": "Fitted Motor Power",
        "meter": "m",
        "error_msg": "⚠️ No matching models found within safe operating parameters. Try adjusting inputs.",
        "temp_extreme_alert": "❌ Liquid Temp exceeds safe operational limits.",
        
        "tab_pic": "📐 Product Dimensions & Specs",
        "tab_curve_catalog": "📉 Factory Performance Curve",
        "img_not_found": "ℹ️ Image file not found inside images folder.",
        
        "btn_submit": "🚀 Run Calculation & Match Products",
        "btn_back": "⬅️ Back to Modify Inputs"
    }
}

# 3. Sidebar แถบควบคุม
st.sidebar.markdown(f"### 🎛️ Control Panel")
lang_choice = st.sidebar.radio("🌐 Language Selector", ["🇹🇭 ไทย / TH", "🇺🇸 English / EN"], index=0)
lang = "TH" if "🇹🇭" in lang_choice else "EN"
t = translation[lang]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "input_page"

# 4. ฐานข้อมูลคลังปั๊ม Nuosai
nuosai_pumps = [
    {"Series": "PMPA", "Model_Code": "100PMPA64-1", "Img_Key": "100PMPA64-1", "PumpKey": "booster_set", "Motor_HP": 5.5, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 10.0, "Max_Head": 30.0},
    {"Series": "PMPA", "Model_Code": "100PMPA64-2", "Img_Key": "100PMPA64-2", "PumpKey": "booster_set", "Motor_HP": 10.0, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 25.0, "Max_Head": 58.0},
    {"Series": "PMPA", "Model_Code": "100PMPA64-3", "Img_Key": "100PMPA64-3", "PumpKey": "booster_set", "Motor_HP": 15.0, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 40.0, "Max_Head": 88.0},
    {"Series": "PMPA", "Model_Code": "100PMPA64-4", "Img_Key": "100PMPA64-4", "PumpKey": "booster_set", "Motor_HP": 20.0, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 60.0, "Max_Head": 118.0},
    {"Series": "PMPA", "Model_Code": "100PMPA90-2", "Img_Key": "100PMPA90-2", "PumpKey": "booster_set", "Motor_HP": 25.0, "Min_Flow": 50.0, "Max_Flow": 120.0, "Min_Head": 30.0, "Max_Head": 70.0},
    {"Series": "PMPA", "Model_Code": "125PMPA120-3", "Img_Key": "125PMPA120-3", "PumpKey": "booster_set", "Motor_HP": 40.0, "Min_Flow": 60.0, "Max_Flow": 160.0, "Min_Head": 45.0, "Max_Head": 95.0},
    {"Series": "PWPC", "Model_Code": "PWPC2-4", "Img_Key": "PWPC2-4", "PumpKey": "transfer_pump", "Motor_HP": 1.0, "Min_Flow": 0.5, "Max_Flow": 4.0, "Min_Head": 10.0, "Max_Head": 32.0},
    {"Series": "PWPC", "Model_Code": "PWPC4-3", "Img_Key": "PWPC4-3", "PumpKey": "transfer_pump", "Motor_HP": 1.5, "Min_Flow": 1.0, "Max_Flow": 6.5, "Min_Head": 12.0, "Max_Head": 38.0},
    {"Series": "PWPC", "Model_Code": "PWPC8-3", "Img_Key": "PWPC8-3", "PumpKey": "transfer_pump", "Motor_HP": 2.0, "Min_Flow": 2.0, "Max_Flow": 11.5, "Min_Head": 15.0, "Max_Head": 42.0},
    {"Series": "PWPC", "Model_Code": "PWPC12-3", "Img_Key": "PWPC12-3", "PumpKey": "transfer_pump", "Motor_HP": 3.0, "Min_Flow": 4.0, "Max_Flow": 17.0, "Min_Head": 15.0, "Max_Head": 46.0},
    {"Series": "NSLA", "Model_Code": "NSLA32-25-2", "Img_Key": "NSLA32-25-2", "PumpKey": "industrial_pump", "Motor_HP": 3.0, "Min_Flow": 3.0, "Max_Flow": 16.0, "Min_Head": 12.0, "Max_Head": 32.0},
    {"Series": "NSLA", "Model_Code": "NSLA40-25-2", "Img_Key": "NSLA40-25-2", "PumpKey": "industrial_pump", "Motor_HP": 5.5, "Min_Flow": 5.0, "Max_Flow": 28.0, "Min_Head": 15.0, "Max_Head": 40.0},
    {"Series": "NSLA", "Model_Code": "NSLA50-32-2", "Img_Key": "NSLA50-32-2", "PumpKey": "industrial_pump", "Motor_HP": 7.5, "Min_Flow": 10.0, "Max_Flow": 50.0, "Min_Head": 15.0, "Max_Head": 48.0},
    {"Series": "NSLA", "Model_Code": "NSLA65-40-2", "Img_Key": "NSLA65-40-2", "PumpKey": "industrial_pump", "Motor_HP": 15.0, "Min_Flow": 15.0, "Max_Flow": 75.0, "Min_Head": 20.0, "Max_Head": 58.0},
    {"Series": "NSLA", "Model_Code": "NSLA80-40-2", "Img_Key": "NSLA80-40-2", "PumpKey": "industrial_pump", "Motor_HP": 25.0, "Min_Flow": 20.0, "Max_Flow": 120.0, "Min_Head": 20.0, "Max_Head": 52.0},
    {"Series": "NSWA", "Model_Code": "NSWA40-25-2", "Img_Key": "NSWA40-25-2", "PumpKey": "industrial_pump", "Motor_HP": 5.5, "Min_Flow": 5.0, "Max_Flow": 28.0, "Min_Head": 15.0, "Max_Head": 42.0},
    {"Series": "NSWA", "Model_Code": "NSWA50-32-2", "Img_Key": "NSWA50-32-2", "PumpKey": "industrial_pump", "Motor_HP": 7.5, "Min_Flow": 10.0, "Max_Flow": 52.0, "Min_Head": 18.0, "Max_Head": 52.0},
    {"Series": "NSWA", "Model_Code": "NSWA65-40-2", "Img_Key": "NSWA65-40-2", "PumpKey": "industrial_pump", "Motor_HP": 15.0, "Min_Flow": 15.0, "Max_Flow": 80.0, "Min_Head": 22.0, "Max_Head": 62.0},
    {"Series": "NSQW", "Model_Code": "50NSQW15-15-1.5", "Img_Key": "50NSQW15-15-1.5", "PumpKey": "submersible", "Motor_HP": 2.0, "Min_Flow": 5.0, "Max_Flow": 22.0, "Min_Head": 5.0, "Max_Head": 18.0},
    {"Series": "NSQW", "Model_Code": "50NSQW25-28-4", "Img_Key": "50NSQW25-28-4", "PumpKey": "submersible", "Motor_HP": 5.5, "Min_Flow": 10.0, "Max_Flow": 35.0, "Min_Head": 12.0, "Max_Head": 32.0},
    {"Series": "NSQW", "Model_Code": "65NSQW25-28-4", "Img_Key": "65NSQW25-28-4", "PumpKey": "submersible", "Motor_HP": 5.5, "Min_Flow": 12.0, "Max_Flow": 40.0, "Min_Head": 10.0, "Max_Head": 30.0},
    {"Series": "NSQW", "Model_Code": "100NSQW40-15-4", "Img_Key": "100NSQW40-15-4", "PumpKey": "submersible", "Motor_HP": 5.5, "Min_Flow": 15.0, "Max_Flow": 65.0, "Min_Head": 8.0, "Max_Head": 18.0},
    {"Series": "NSQW", "Model_Code": "100NSQW50-17-5.5", "Img_Key": "100NSQW50-17-5.5", "PumpKey": "submersible", "Motor_HP": 7.5, "Min_Flow": 20.0, "Max_Flow": 75.0, "Min_Head": 10.0, "Max_Head": 22.0},
    {"Series": "NSQW", "Model_Code": "150NSQW140-23-15", "Img_Key": "150NSQW140-23-15", "PumpKey": "submersible", "Motor_HP": 20.0, "Min_Flow": 50.0, "Max_Flow": 200.0, "Min_Head": 12.0, "Max_Head": 28.0}
]
df_db = pd.DataFrame(nuosai_pumps)

# 🌐 ฟังก์ชันค้นหารูปภาพตรงรุ่น
def find_exact_image(prefix, code_key):
    base_dir = "C:/nuosai-pump-selector/images/"
    if not os.path.exists(base_dir):
        return None
    extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]
    prefixes = [prefix, "Curev"] if prefix == "Curve" else [prefix]
    search_token = f"{prefix.lower()}_{code_key.lower()}".replace(" ", "").replace("-", "")
    alt_token = f"curev_{code_key.lower()}".replace(" ", "").replace("-", "")
    for f in os.listdir(base_dir):
        f_clean = f.lower().replace(" ", "").replace("-", "")
        if search_token in f_clean or alt_token in f_clean:
            return os.path.join(base_dir, f)
    for pref in prefixes:
        for ext in extensions:
            full_path = os.path.join(base_dir, f"{pref}_{code_key}{ext}")
            if os.path.exists(full_path):
                return full_path
    return None

def get_pump_type_name(key, current_lang):
    types_dict = {
        "TH": {
            "booster": "ปั๊มน้ำอัตโนมัติเพิ่มแรงดัน (Automatic Booster Pump)",
            "booster_set": "ชุดปั๊มเสริมแรงดันประสิทธิภาพสูง (High-Performance Booster Pump Set)",
            "transfer_pump": "ปั๊มสูบส่งหมุนเวียนน้ำอาคารและอุตสาหกรรม (Water Supply & Transfer Pump)",
            "industrial_pump": "ปั๊มหอยโข่งโครงสร้างเหล็กและสแตนเลสงานหนัก (Heavy-Duty Centrifugal Pump)",
            "submersible": "ปั๊มจุ่มระบายน้ำเสียและสิ่งปฏิกูล (Submersible Sewage Pump)"
        },
        "EN": {
            "booster": "Automatic Pressure Booster Pump",
            "booster_set": "High-Performance Booster Pump Set System",
            "transfer_pump": "Water Supply & Transfer Circulation Pump",
            "industrial_pump": "Heavy-Duty End-Suction Centrifugal Pump",
            "submersible": "Submersible Sewage & Wastewater Pump"
        }
    }
    return types_dict[current_lang].get(key, key)

# 5. แบนเนอร์หัวเว็บไซต์แบบพรีเมียม
if logo_path:
    try:
        col_log1, col_log2 = st.columns([1, 5])
        with col_log1:
            st.image(Image.open(logo_path), width=110)
        with col_log2:
            st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 15px; border-radius: 12px; height: 110px; display: flex; flex-direction: column; justify-content: center;'><h1 style='color: white; font-size: 24px; font-weight: 700; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 13px; margin: 4px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)
    except:
        st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px;'><h1 style='color: white; font-size: 26px; font-weight: 700; text-align: center; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 14px; text-align: center; margin: 6px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px;'><h1 style='color: white; font-size: 26px; font-weight: 700; text-align: center; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 14px; text-align: center; margin: 6px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)

# ==========================================
# หน้าที่ 1: หน้ากรอกข้อมูลสเปก (Input Page)
# ==========================================
if st.session_state["current_page"] == "input_page":
    st.markdown(f"### {t['sec_input']}")
    col1, col2 = st.columns(2, gap="medium")
    
    with st.container(border=True):
        cat_options = [t["cat_building"], t["cat_booster"], t["cat_watersupply"], t["cat_agriculture"], t["cat_fire"], t["cat_industrial"], t["cat_wastewater"]]
        select_cat = st.selectbox(t["cat_select"], cat_options)
        
        if select_cat == t["cat_building"]:
            allowed_series = ["PWPC", "NSLA"]
            init_flow, init_v_head, init_h_pipe = 2.0, 15.0, 10.0  
            selected_cat_key = "building"
        elif select_cat == t["cat_booster"]:
            allowed_series = ["PMPA", "PWPC"]
            init_flow, init_v_head, init_h_pipe = 35.0, 45.0, 20.0
            selected_cat_key = "booster"
        elif select_cat == t["cat_watersupply"]:
            allowed_series = ["NSLA", "NSWA", "PMPA"]
            init_flow, init_v_head, init_h_pipe = 40.0, 30.0, 25.0
            selected_cat_key = "watersupply"
        elif select_cat == t["cat_agriculture"]:
            allowed_series = ["NSLA", "NSWA"]
            init_flow, init_v_head, init_h_pipe = 15.0, 25.0, 40.0
            selected_cat_key = "agriculture"
        elif select_cat == t["cat_fire"]:
            allowed_series = ["PMPA", "NSWA", "NSLA"]
            init_flow, init_v_head, init_h_pipe = 60.0, 65.0, 50.0
            selected_cat_key = "fire"
        elif select_cat == t["cat_industrial"]:
            allowed_series = ["PMPA", "PWPC", "NSLA", "NSWA", "NSQW"]
            init_flow, init_v_head, init_h_pipe = 35.0, 40.0, 30.0
            selected_cat_key = "industrial"
        else:
            allowed_series = ["NSLA", "NSQW"]
            init_flow, init_v_head, init_h_pipe = 25.0, 12.0, 20.0
            selected_cat_key = "wastewater"
            
        series_options = [t["all_series"], "PMPA", "PWPC", "NSLA", "NSWA", "NSQW"]
        select_series = st.selectbox(t["series_select"], series_options, index=0)
        selected_series_key = None if select_series == t["all_series"] else select_series
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with col1:
            flow_rate = st.number_input(t["flow_label"], value=init_flow, step=1.0, min_value=0.1)
            static_head = st.number_input(t["v_head_label"], value=init_v_head, step=1.0, min_value=0.0)
            horiz_pipe = st.number_input(t["h_pipe_label"], value=init_h_pipe, step=2.0, min_value=0.0)
            
        with col2:
            pipe_diameter = st.selectbox(t["pipe_dia_label"], [1.0, 1.5, 2.0, 2.5, 3.0, 4.0], index=3 if selected_cat_key in ["fire","booster"] else 2)
            pipe_material = st.selectbox(t["pipe_mat_label"], [t["mat_pvc"], t["mat_ss"], t["mat_galvanized"], t["mat_black_iron"]])
            particle_type = st.selectbox(t["particle_label"], [t["part_clean"], t["part_soft"], t["part_slurry"]])
            
        liquid_temp = st.slider(t["temp_label"], min_value=-10, max_value=150, value=25, step=5)

    st.session_state["flow_rate"] = flow_rate
    st.session_state["static_head"] = static_head
    st.session_state["horiz_pipe"] = horiz_pipe
    st.session_state["pipe_diameter"] = pipe_diameter
    st.session_state["pipe_material"] = pipe_material
    st.session_state["particle_type"] = particle_type
    st.session_state["liquid_temp"] = liquid_temp
    st.session_state["allowed_series"] = allowed_series
    st.session_state["selected_series_key"] = selected_series_key
    st.session_state["selected_cat_key"] = selected_cat_key
    st.session_state["select_cat_name"] = select_cat

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["btn_submit"], type="primary", use_container_width=True):
        st.session_state["current_page"] = "output_page"
        st.rerun()

# ==========================================
# หน้าที่ 2: หน้าแสดงผลลัพธ์ข้อมูลคำนวณ เลือกรุ่น และแสดงภาพแคตตาล็อก (Output Page)
# ==========================================
elif st.session_state["current_page"] == "output_page":
    if st.button(t["btn_back"], type="secondary"):
        st.session_state["current_page"] = "input_page"
        st.rerun()
        
    st.markdown(f"### 📋 ผลการคำนวณสำหรับ: *{st.session_state['select_cat_name']}*")
    
    flow_rate = st.session_state["flow_rate"]
    static_head = st.session_state["static_head"]
    horiz_pipe = st.session_state["horiz_pipe"]
    pipe_diameter = st.session_state["pipe_diameter"]
    pipe_material = st.session_state["pipe_material"]
    particle_type = st.session_state["particle_type"]
    liquid_temp = st.session_state["liquid_temp"]
    allowed_series = st.session_state["allowed_series"]
    selected_series_key = st.session_state["selected_series_key"]
    selected_cat_key = st.session_state["selected_cat_key"]

    if liquid_temp > 120:
        st.error(t["temp_extreme_alert"])
    else:
        material_factor = 0.85 if pipe_material == t["mat_pvc"] else (0.95 if pipe_material == t["mat_ss"] else 1.10)
        solid_sg_factor = 1.0 if particle_type == t["part_clean"] else (1.05 if particle_type == t["part_soft"] else 1.25)
        
        total_pipe_length = (static_head + horiz_pipe) * 1.25  
        f_loss_per_100m = 4.5 * (flow_rate / (pipe_diameter**2 * 8))
        friction_loss = (f_loss_per_100m * total_pipe_length / 100) * material_factor
        
        if selected_cat_key == "building": residual_head = 10.0
        elif selected_cat_key == "booster": residual_head = 25.0
        elif selected_cat_key == "watersupply": residual_head = 4.0
        elif selected_cat_key == "agriculture": residual_head = 15.0
        elif selected_cat_key == "fire": residual_head = 45.0
        elif selected_cat_key == "industrial": residual_head = 20.0
        else: residual_head = 2.0
            
        tdh = static_head + friction_loss + residual_head
        suggested_hp = ((flow_rate * tdh * solid_sg_factor) / (367 * 0.60) * 1.341) * 1.20 
        
        st.markdown(f"#### {t['sec_calc']}")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(label=t["metric_flow"], value=f"{flow_rate:.1f} m³/h")
        m_col2.metric(label=t["metric_head"], value=f"{tdh:.1f} {t['meter']}", delta=f"Static:{static_head}m | Friction:{friction_loss:.1f}m")
        m_col3.metric(label=t["metric_motor"], value=f"{suggested_hp:.1f} HP")
        
        st.markdown("---")
        st.markdown(f"#### {t['sec_match']}")
        
        condition = df_db["Series"].isin(allowed_series) & \
                    (df_db["Min_Flow"] <= flow_rate) & (df_db["Max_Flow"] >= flow_rate) & \
                    (df_db["Min_Head"] <= tdh) & (df_db["Max_Head"] >= tdh)
                    
        if selected_series_key:
            condition = condition & (df_db["Series"] == selected_series_key)
            
        matched_pumps = df_db[condition].copy()
        
        if not matched_pumps.empty:
            st.success(t["matches_count"].format(count=len(matched_pumps)))
            
            model_list = matched_pumps["Model_Code"].tolist()
            selected_model = st.selectbox(t["select_pump_label"], model_list)
            
            chosen_pump = matched_pumps[matched_pumps["Model_Code"] == selected_model].iloc[0]
            pump_type_name = get_pump_type_name(chosen_pump['PumpKey'], lang)
            
            with st.container(border=True):
                st.markdown(f"### 📦 ข้อมูลทางเทคนิคโมเดล: <span style='color:#1d70b8;'>{chosen_pump['Model_Code']}</span>", unsafe_allow_html=True)
                st.markdown(f"**⚙️ ประเภทการใช้งาน:** {pump_type_name}")
                st.markdown("---")
                
                spec_table_data = {
                    "คุณลักษณะทางวิศวกรรม (Technical Specifications)": [
                        "รหัสสินค้าผลิตภัณฑ์ (Model Code)",
                        "ซีรีส์หลัก (Pump Series)",
                        "ขนาดมอเตอร์ติดตั้งประจำรุ่น (Fitted Motor Power)",
                        "ขอบเขตอัตราไหลรองรับ (Operational Flow Range)",
                        "ขอบเขตระยะส่งสูงรองรับ (Operational Head Range)"
                    ],
                    "ข้อมูลแคตตาล็อกโรงงาน (Factory Catalog Value)": [
                        f"{chosen_pump['Model_Code']}",
                        f"ซีรีส์ {chosen_pump['Series']}",
                        f"{chosen_pump['Motor_HP']:.1f} HP (แรงม้า)",
                        f"{chosen_pump['Min_Flow']:.1f} - {chosen_pump['Max_Flow']:.1f} m³/h",
                        f"{chosen_pump['Min_Head']:.1f} - {chosen_pump['Max_Head']:.1f} เมตร"
                    ]
                }
                
                df_spec = pd.DataFrame(spec_table_data)
                st.table(df_spec)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🖼️ เอกสารสเปกภาพแคตตาล็อกและกราฟประจำรุ่น (Factory Sheets)")
                
                tab1, tab2 = st.tabs([t["tab_pic"], t["tab_curve_catalog"]])
                
                with tab1:
                    pic_path = find_exact_image("Dimension", chosen_pump['Img_Key'])
                    if pic_path:
                        try:
                            st.image(Image.open(pic_path), caption=f"Dimensions Specs: {os.path.basename(pic_path)}", use_container_width=True)
                        except Exception as e:
                            st.error(f"Error loading sheet: {str(e)}")
                    else:
                        st.info(f"{t['img_not_found']} (มองหาไฟล์: `Dimension_{chosen_pump['Img_Key']}.jpg`) ")
                        
                with tab2:
                    curve_catalog_path = find_exact_image("Curve", chosen_pump['Img_Key'])
                    if curve_catalog_path:
                        try:
                            st.image(Image.open(curve_catalog_path), caption=f"Factory Performance Curve: {os.path.basename(curve_catalog_path)}", use_container_width=True)
                        except Exception as e:
                            st.error(f"Error loading curve: {str(e)}")
                    else:
                        st.info(f"{t['img_not_found']} (มองหาไฟล์: `Curve_{chosen_pump['Img_Key']}.jpg`)")
        else:
            st.error(t["error_msg"])
