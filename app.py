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

# 🌐 ฟังก์ชันสำหรับดึงภาพโลโก้บริษัทอย่างปลอดภัยบนระบบ Cloud
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

# 2. คลังข้อมูลภาษาสำหรับการแปลระบบ (สลับ TH/EN สมบูรณ์แบบ)
translation = {
    "TH": {
        "brand_title": "NUOSAI PUMP SELECTION SYSTEM",
        "brand_sub": "ระบบคำนวณทางวิศวกรรมชลศาสตร์และค้นหาภาพแคตตาล็อกผลิตภัณฑ์ Nuosai",
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
        
        "part_clean": "💧 น้ำสะอาดบริสุทธิ์ (ไม่มีพาร์ทิเคิลเจือปน)",
        "part_soft": "🍃 น้ำปนเศษตะกอนอ่อน (มีเศษดิน/ทรายละเอียด < 5mm)",
        "part_slurry": "🪵 น้ำโคลนหนาแน่น / สารเคมีหนืด / น้ำเสียเข้มข้น",
        
        "mat_pvc": "ท่อ PVC / PE (ผิวเรียบมาก แรงเสียดทานต่ำสุด)",
        "mat_ss": "ท่อสแตนเลส (Stainless Steel)",
        "mat_galvanized": "ท่อเหล็กชุบสังกะสี (Galvanized Steel)",
        "mat_black_iron": "ท่อเหล็กดำ / เหล็กหล่อ (Black Iron)",
        
        "sec_calc": "📊 ผลลัพธ์การวิเคราะห์ระบบจากการคำนวณ (Hydraulic Outputs)",
        "metric_flow": "อัตราการไหลดีไซน์",
        "metric_head": "ระยะส่งรวม (TDH)",
        "metric_motor": "มอเตอร์ที่แนะนำขั้นต่ำ",
        
        "sec_match": "🎯 ผลลัพธ์ปั๊มน้ำรุ่นที่ผ่านเกณฑ์คำนวณ",
        "select_pump_label": "🔍 เลือกรุ่นปั๊มน้ำจากผลลัพธ์การคำนวณ:",
        "matches_count": "พบรุ่นผลิตภัณฑ์ที่รองรับสเปกหน้างานของคุณทั้งหมด {count} รุ่น",
        "error_msg": "⚠️ ไม่พบรุ่นปั๊มที่ตรงสเปกในช่วงคำนวณนี้ คุณน้าสามารถใช้ระบบ 'ค้นหารุ่นตรงโดยตรง' ที่แถบซ้ายมือเพื่อดึงรูปกราฟมาดูได้ทันทีครับ",
        "temp_extreme_alert": "❌ ของเหลวร้อนเกินขีดจำกัดความปลอดภัยของโครงสร้างปั๊มรุ่นมาตรฐาน",
        
        "meter": "เมตร",
        "curve_title": "📉 1. Factory Performance Curve (กราฟประสิทธิภาพจากโรงงาน)",
        "dim_title": "📐 2. Pump Outline Dimensions (ขนาดมิติและสัดส่วนโครงสร้างตัวปั๊ม)",
        "img_not_found": "ℹ️ ไม่พบไฟล์ภาพของรุ่นนี้ในคลัง",
        "btn_submit": "🚀 คำนวณสเปกและค้นหารุ่นปั๊มน้ำ",
        "btn_back": "⬅️ ย้อนกลับไปแก้ไขข้อมูลสเปก",
        "manual_select_label": "🔍 ค้นหา/เลือกรุ่นปั๊มเพื่อดูแคตตาล็อกโดยตรง"
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
        "select_pump_label": "🔍 Select pump model based on calculation below:",
        "matches_count": "Found {count} models matching your design parameters.",
        "error_msg": "⚠️ No matching models found. You can use the 'Manual Model Lookup' on the left sidebar to pull images directly.",
        "temp_extreme_alert": "❌ Liquid Temp exceeds safe operational limits.",
        
        "meter": "m",
        "curve_title": "📉 1. Factory Performance Curve",
        "dim_title": "📐 2. Pump Outline Dimensions",
        "img_not_found": "ℹ️ Catalog image file not found in images folder.",
        "btn_submit": "🚀 Run Calculation & Match Products",
        "btn_back": "⬅️ Back to Modify Inputs",
        "manual_select_label": "🔍 Manual Model Lookup (Direct Sheet Viewer)"
    }
}

# 3. Sidebar แผงควบคุมหลัก
st.sidebar.markdown(f"### 🎛️ Control Panel")
lang_choice = st.sidebar.radio("🌐 Language Selector", ["🇹🇭 ไทย / TH", "🇺🇸 English / EN"], index=0)
lang = "TH" if "🇹🇭" in lang_choice else "EN"
t = translation[lang]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "input_page"

# 🔍 4. ฟังก์ชันค้นหาไฟล์แยกประเภทอัจฉริยะ (ดึงทั้ง Curve และ Dimension คู่กัน)
def find_pump_images(code_key):
    base_dir = "images/"
    if not os.path.exists(base_dir):
        return None, None
    
    clean_code = code_key.lower().replace(" ", "").replace("-", "").replace("_", "")
    curve_img = None
    dim_img = None
    
    for f in os.listdir(base_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            f_clean = f.lower().replace(" ", "").replace("-", "").replace("_", "")
            
            # จับคู่หารหัสรุ่นโมเดล
            if clean_code in f_clean or f_clean in clean_code:
                if "dimension" in f.lower():
                    dim_img = os.path.join(base_dir, f)
                elif "curve" in f.lower() or "curev" in f.lower():
                    curve_img = os.path.join(base_dir, f)
                    
    return curve_img, dim_img

# 🎯 รายชื่อรหัสรุ่นโมเดลหลักทั้งหมดของคุณน้า
all_uploaded_models = [
    "เลือกโหมดคำนวณอัตโนมัติ",
    # ซีรีส์ NSQW / NSTQW / QJ
    "50NSQW10-10-0.75", "50NSQW10-13-1.1", "50NSQW10-18-1.5", "50NSQW15-15-1.5", "50NSQW15-20-2.2", "50NSQW15-27-3", 
    "50NSQW20-13-1.5", "50NSQW20-18-2.2", "50NSQW20-25-3", "50NSQW25-10-1.5", "50NSQW25-15-2.2", "50NSQW25-20-3", 
    "50NSQW25-28-4", "50NSQW25-35-5.5", "50NSQW25-38-7.5", "50NSQW-10-22-2.2", "50NSQW-15-15-1.5", 
    "50NSTQW10-10-0.75", "50NSTQW10-20-2.2", "50NSTQW12-10-1.1", "50NSTQW12-15-1.5", "50NSTQW15-20-3",
    "65NSQW10-18-1.5", "65NSQW25-28-4", "65NSQW10-10-0.75", "65NSQW10-22-2.2", "65NSQW15-15-1.5", "65NSQW15-20-2.2", 
    "65NSQW15-27-3", "65NSQW20-13-1.5", "65NSQW20-18-2.2", "65NSQW20-25-3", "65NSQW25-10-1.5", "65NSQW25-15-2.2", 
    "65NSQW25-20-3", "65NSQW25-32-5.5", "65NSQW25-38-7.5", "65NSQW30-13-2.2", "65NSQW30-18-3", "65NSQW30-25-4", 
    "65NSQW30-75-22", "65NSQW40-15-4", "65NSTQW20-10-1.5", "65NSTQW25-15-2.2", "65NSTQW25-20-4", "65NSTQW35-13-3", 
    "65BSQW10-13-1.1", "80NSQW20-13-1.5", "80NSQW20-18-2.2", "80NSQW20-25-3", "80NSQW25-10-1.5", "80NSQW25-15-2.2", 
    "80NSQW25-20-3", "80NSQW25-28-4", "80NSQW25-32-5.5", "80NSQW25-38-7.5", "80NSQW30-13-2.2", "80NSQW30-18-3", 
    "80NSQW30-25-4", "80NSQW40-15-4", "80NSQW40-30-7.5", "80NSQW45-20-5.5", "80NSQW50-17-5.5", "80NSQW50-25-7.5", 
    "80NSQW65-15-5.5", "80NSQW65-25-7.5", "80NSQW70-13-5.5", "80NSQW80-13-7.5", "80NSTQW35-10-2.2", "80NSTQW40-12-3", 
    "80NSTQW45-15-4", "80NSTQW45-20-5.5", "100NSQW40-15-4", "100NSQW40-30-7.5", "100NSQW45-20-5.5", "100NSQW50-17-5.5", 
    "100NSQW65-15-5.5", "100NSQW65-25-7.5", "100NSQW70-13-5.5", "100NSQW80-13-7.5", "100NSTQW100-15-7.5", 
    "100NSTQW65-15-5.5", "150NSQW110-10-5.5", "150NSQW110-16-7.5", "150NSQW130-14-7.5", "150NSQW130-18-11", 
    "150NSQW130-8-5.5", "150NSQW140-23-15", "150NSQW150-15-11", "150NSQW150-6-5.5", "150NSQW160-10-7.5", 
    "150NSQW160-21-15", "150NSQW180-14-11", "150NSQW180-20-15", "150NSQW200-11-11", "150NSQW200-17-15", 
    "150NSTQW120-10-7.5", "200NSQW150-15-11", "200NSQW150-6-5.5", "200NSQW160-10-7.5", "200NSQW160-21-15", 
    "200NSQW180-14-11", "200NSQW180-20-15", "200NSQW200-11-11", "200NSQW200-17-15", "250QJ80-120-6",
    
    # ซีรีส์ PMP / PMPA
    "25PMP1", "25PMP2", "25PMP3", "25PMPA1", "25PMPA2", "25PMPA3", "32PMP4", "32PMP5", "32PMPA4", "32PMPA5", 
    "40PMP8", "40PMP10", "40PMPA8", "40PMPA10", "50PMP12", "50PMP15", "50PMP20", "50PMPA12", "50PMPA15", "50PMPA20", 
    "65PMP32", "65PMPA32", "80PMP45", "80PMPA45", "100PMP64-1", "100PMP64-2", "100PMP64-3", "100PMP64-4", 
    "100PMP64-5", "100PMP64-6", "100PMP64-7", "100PMP64-8", "100PMP90-1", "100PMP90-2", "100PMP90-3", "100PMP90-4", 
    "100PMP90-5", "100PMP90-6", "100PMPA64-1", "100PMPA64-2", "100PMPA64-3", "100PMPA64-4", "100PMPA64-5", 
    "100PMPA64-6", "100PMPA64-7", "100PMPA64-8", "100PMPA90-1", "100PMPA90-2", "100PMPA90-3", "100PMPA90-4", 
    "100PMPA90-5", "100PMPA90-6", "125PMP120-1", "125PMP120-2", "125PMP120-3", "125PMP120-4", "125PMP120-5", 
    "125PMP120-6", "125PMP120-7", "125PMP150-1", "125PMP150-2", "125PMP150-3", "125PMP150-4", "125PMP150-5", 
    "125PMP150-6", "125PMPA120-1", "125PMPA120-2", "125PMPA120-3", "125PMPA120-4", "125PMPA120-5", "125PMPA120-6", 
    "125PMPA120-7", "125PMPA150-1", "125PMPA150-2", "125PMPA150-3", "125PMPA150-4", "125PMPA150-5", "125PMPA150-6", 
    "150PMP200-1", "150PMP200-2", "150PMP200-3", "150PMP200-4", "150PMPA200-1", "150PMPA200-2", "150PMPA200-3", "150PMPA200-4",
    
    # ซีรีส์ NSLA / NSWA / PWPC / SWA
    "NSLA32-18-2", "NSLA32-21-2", "NSLA32-25-2", "NSLA32-32-2", "NSLA32-38-2", "NSLA32-50-2", "NSLA40-16-2", 
    "NSLA40-18-2", "NSLA40-20-2", "NSLA40-25-2", "NSLA40-30-2", "NSLA40-36-2", "NSLA40-48-2", "NSLA50-12-2", 
    "NSLA50-15-2", "NSLA50-18-2", "NSLA50-24-2", "NSLA50-28-2", "NSLA50-32-2", "NSLA50-35-2", "NSLA50-38-2", 
    "NSLA50-40-2", "NSLA50-48-2", "NSLA50-50-2", "NSLA50-58-2", "NSLA50-60-2", "NSLA50-70-2", "NSLA50-80-2", 
    "NSLA50-81-2", "NSLA65-15-2", "NSLA65-19-2", "NSLA65-22-2", "NSLA65-30-2", "NSLA65-34-2", "NSLA65-36-2", 
    "NSLA65-40-2", "NSLA65-48-2", "NSLA65-50-2", "NSLA65-61-2", "NSLA65-67-2", "NSLA65-86-2", "NSLA80-13-2", 
    "NSLA80-18-2", "NSLA80-22-2", "NSLA80-30-2", "NSLA80-31-2", "NSLA80-38-2", "NSLA80-40-2", "NSLA80-47-2", 
    "NSLA80-48-2", "NSLA80-54-2", "NSLA80-71-2", "NSLA100-9-2", "NSLA100-15-2", "NSLA100-17-2", "NSLA100-22-2", 
    "NSLA100-27-2", "NSLA100-33-2", "NSLA100-40-2", "NSLA100-48-2", "NSLA100-55-2", "NSLA125-11-4", "NSLA125-14-4", 
    "NSLA125-18-4", "NSLA125-22-4", "NSLA125-28-4", "NSLA125-32-4", "NSLA125-40-4", "NSLA125-48-4", "NSLA150-12.5-4", 
    "NSLA150-17-4", "NSLA150-21-4", "NSLA150-25-4", "NSLA150-33-4", "NSLA150-40-4", "NSLA150-50-4", "NSLA200-12.5-4", 
    "NSLA200-15-4", "NSLA200-18-4", "NSLA200-20-4", "NSLA200-23-4", "NSLA200-24-4", "NSLA200-27-4", "NSLA200-30-4", 
    "NSLA200-32-4", "NSLA200-35-4", "NSLA200-43-4", "NSLA200-44-4", "NSLA200-50-4", "NSLA200-53-4", "NSLA250-12.5-4", 
    "NSLA250-14-4", "NSLA250-15-4", "NSLA250-17-4", "NSLA250-18-4", "NSLA250-20-4", "NSLA250-21-4", "NSLA250-26-4", 
    "NSLA250-27-4", "NSLA250-32-4", "NSLA250-36-4", "NSLA250-40-4", "NSLA250-44-4", "NSLA250-50-4", "NSLA250-53-4", 
    "NSLA300-15-4", "NSLA300-20-4", "NSLA300-25-4", "NSLA300-30-4", "NSLA300-35-4", "NSLA300-44-4", "NSLA300-55-4", 
    "NSWA40-16-2", "NSWA40-18-2", "NSWA40-20-2", "NSWA40-25-2", "NSWA40-30-2", "NSWA40-36-2", "NSWA40-48-2", 
    "NSWA50-12-2", "NSWA50-15-2", "NSWA50-18-2", "NSWA50-24-2", "NSWA50-28-2", "NSWA50-32-2", "NSWA50-35-2", 
    "NSWA50-38-2", "NSWA50-40-2", "NSWA50-48-2", "NSWA50-50-2", "NSWA50-58-2", "NSWA50-60-2", "NSWA50-70-2", 
    "NSWA50-80-2", "NSWA50-81-2", "NSWA65-15-2", "NSWA65-19-2", "NSWA65-22-2", "NSWA65-30-2", "NSWA65-34-2", 
    "NSWA65-36-2", "NSWA65-40-2", "NSWA65-48-2", "NSWA65-50-2", "NSWA65-61-2", "NSWA65-67-2", "NSWA65-83-2", 
    "NSWA80-13-2", "NSWA80-18-2", "NSWA80-22-2", "NSWA80-28-2", "NSWA80-30-2", "NSWA80-38-2", "NSWA80-40-2", 
    "NSWA80-47-2", "NSWA80-48-2", "NSWA80-54-2", "NSWA80-67-2", "NSWA100-9-2", "NSWA100-15-2", "NSWA100-17-2", 
    "NSWA100-22-2", "NSWA100-27-2", "NSWA100-33-2", "NSWA100-40-2", "NSWA100-48-2", "NSWA100-52-2", "NSWA125-11-4", 
    "NSWA125-14-4", "NSWA125-22-4", "NSWA125-28-4", "NSWA125-32-4", "NSWA125-40-4", "NSWA125-48-4", "NSWA150-12.5-4", 
    "NSWA150-17-4", "NSWA150-21-4", "NSWA150-25-4", "NSWA150-33-4", "NSWA150-40-4", "NSWA150-50-4", "NSWA200-12.5-4", 
    "NSWA200-15-4", "NSWA200-18-4", "NSWA200-20-4", "NSWA200-23-4", "NSWA200-24-4", "NSWA200-27-4", "NSWA200-30-4", 
    "NSWA200-32-4", "NSWA200-35-4", "NSWA200-43-4", "NSWA200-44-4", "NSWA200-50-4", "NSWA200-53-4", "NSWA250-12.5-4", 
    "NSWA250-15-4", "NSWA250-17-4", "NSWA250-18-4", "NSWA250-20-4", "NSWA250-21-4", "NSWA250-26-4", "NSWA250-27-4", 
    "NSWA250-32-4", "NSWA250-36-4", "NSWA250-40-4", "NSWA250-44-4", "NSWA250-50-4", "NSWA250-53-4",
    "PWPC2-2", "PWPC2-3", "PWPC2-4", "PWPC2-5", "PWPC2-6", "PWPC4-2", "PWPC4-3", "PWPC4-4", "PWPC8-1", "PWPC8-2", 
    "PWPC8-3", "PWPC8-4", "PWPC8-5", "PWPC12-1", "PWPC12-2", "PWPC12-3", "PWPC12-4", "PWPC12-5", "PWPC15-1", 
    "PWPC15-2", "PWPC15-3", "PWPC20-1", "PWPC20-2", "SWA125-18-4", "SWA250-14-4"
]

st.sidebar.markdown("---")
manual_select = st.sidebar.selectbox(t["manual_select_label"], all_uploaded_models)

# ฐานข้อมูลภายในระบบคำนวณอัตโนมัติ (ขยายเพื่อรองรับทุกซีรีส์ของคุณน้า)
nuosai_pumps = [
    {"Series": "PMPA", "Model_Code": "100PMPA64-1", "PumpKey": "booster_set", "Motor_HP": 5.5, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 10.0, "Max_Head": 30.0},
    {"Series": "PMPA", "Model_Code": "100PMPA64-2", "PumpKey": "booster_set", "Motor_HP": 10.0, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 25.0, "Max_Head": 58.0},
    {"Series": "PMPA", "Model_Code": "100PMPA64-3", "PumpKey": "booster_set", "Motor_HP": 15.0, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 40.0, "Max_Head": 88.0},
    {"Series": "PMPA", "Model_Code": "125PMPA120-3", "PumpKey": "booster_set", "Motor_HP": 40.0, "Min_Flow": 60.0, "Max_Flow": 160.0, "Min_Head": 45.0, "Max_Head": 95.0},
    {"Series": "PMP", "Model_Code": "100PMP64-1", "PumpKey": "watersupply", "Motor_HP": 5.5, "Min_Flow": 30.0, "Max_Flow": 85.0, "Min_Head": 10.0, "Max_Head": 32.0},
    {"Series": "PMP", "Model_Code": "125PMP120-1", "PumpKey": "watersupply", "Motor_HP": 20.0, "Min_Flow": 50.0, "Max_Flow": 140.0, "Min_Head": 20.0, "Max_Head": 60.0},
    {"Series": "NSLA", "Model_Code": "NSLA32-25-2", "PumpKey": "industrial_pump", "Motor_HP": 3.0, "Min_Flow": 3.0, "Max_Flow": 16.0, "Min_Head": 10.0, "Max_Head": 32.0},
    {"Series": "NSLA", "Model_Code": "NSLA50-32-2", "PumpKey": "industrial_pump", "Motor_HP": 7.5, "Min_Flow": 10.0, "Max_Flow": 50.0, "Min_Head": 15.0, "Max_Head": 48.0},
    {"Series": "NSWA", "Model_Code": "NSWA50-32-2", "PumpKey": "industrial_pump", "Motor_HP": 7.5, "Min_Flow": 10.0, "Max_Flow": 50.0, "Min_Head": 12.0, "Max_Head": 45.0},
    {"Series": "NSWA", "Model_Code": "NSWA100-40-2", "PumpKey": "industrial_pump", "Motor_HP": 30.0, "Min_Flow": 40.0, "Max_Flow": 150.0, "Min_Head": 20.0, "Max_Head": 55.0},
    {"Series": "NSQW", "Model_Code": "50NSQW15-15-1.5", "PumpKey": "submersible", "Motor_HP": 2.0, "Min_Flow": 5.0, "Max_Flow": 25.0, "Min_Head": 5.0, "Max_Head": 18.0},
    {"Series": "NSQW", "Model_Code": "65NSQW25-28-4", "PumpKey": "submersible", "Motor_HP": 5.5, "Min_Flow": 12.0, "Max_Flow": 42.0, "Min_Head": 10.0, "Max_Head": 30.0},
    {"Series": "NSTQW", "Model_Code": "50NSTQW12-15-1.5", "PumpKey": "submersible", "Motor_HP": 2.0, "Min_Flow": 4.0, "Max_Flow": 20.0, "Min_Head": 5.0, "Max_Head": 22.0},
    {"Series": "NSTQW", "Model_Code": "65NSTQW25-20-4", "PumpKey": "submersible", "Motor_HP": 5.5, "Min_Flow": 10.0, "Max_Flow": 38.0, "Min_Head": 8.0, "Max_Head": 28.0},
    {"Series": "PWPC", "Model_Code": "PWPC4-3", "PumpKey": "building", "Motor_HP": 1.0, "Min_Flow": 1.5, "Max_Flow": 6.0, "Min_Head": 10.0, "Max_Head": 35.0},
    {"Series": "PWPC", "Model_Code": "PWPC8-4", "PumpKey": "building", "Motor_HP": 2.0, "Min_Flow": 3.0, "Max_Flow": 12.0, "Min_Head": 15.0, "Max_Head": 45.0}
]
df_db = pd.DataFrame(nuosai_pumps)

# 5. หัวเว็บไซต์พรีเมียม
if logo_path:
    col_log1, col_log2 = st.columns([1, 5])
    with col_log1:
        st.image(Image.open(logo_path), width=110)
    with col_log2:
        st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 15px; border-radius: 12px; height: 110px; display: flex; flex-direction: column; justify-content: center;'><h1 style='color: white; font-size: 24px; font-weight: 700; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 13px; margin: 4px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px;'><h1 style='color: white; font-size: 26px; font-weight: 700; text-align: center; margin: 0;'>{t['brand_title']}</h1><p style='color: #e2e8f0; font-size: 14px; text-align: center; margin: 6px 0 0 0;'>{t['brand_sub']}</p></div>", unsafe_allow_html=True)

# ==========================================
# เคสการทำงานที่ 1: โหมดจิ้มดูรูปตรงๆ (Manual Override)
# ==========================================
if manual_select != "เลือกโหมดคำนวณอัตโนมัติ":
    st.markdown(f"## 🎯 โหมดดึงข้อมูลตรง: รุ่น Nuosai {manual_select}")
    st.write("---")
    
    curve_img, dim_img = find_pump_images(manual_select)
    
    if curve_img:
        st.success(f"🔍 พบไฟล์ภาพกราฟชาร์ตประจำรุ่น {manual_select} แล้วครับ")
        st.write(f"### {t['curve_title']}")
        st.image(Image.open(curve_img), use_container_width=True)
    else:
        st.info(f"ℹ️ {t['curve_title']}: {t['img_not_found']}")
        
    st.write("---")
    
    if dim_img:
        st.success(f"🔍 พบไฟล์ภาพขนาดสัดส่วนมิติปั๊มประจำรุ่น {manual_select} แล้วครับ")
        st.write(f"### {t['dim_title']}")
        st.image(Image.open(dim_img), use_container_width=True)
    else:
        st.info(f"ℹ️ {t['dim_title']}: {t['img_not_found']}")

# ==========================================
# เคสการทำงานที่ 2: โหมดคำนวณตามสเปกวิศวกรรม (โหมดปกติ)
# ==========================================
else:
    if st.session_state["current_page"] == "input_page":
        st.markdown(f"### {t['sec_input']}")
        col1, col2 = st.columns(2, gap="medium")
        
        with st.container(border=True):
            cat_options = [t["cat_building"], t["cat_booster"], t["cat_watersupply"], t["cat_agriculture"], t["cat_fire"], t["cat_industrial"], t["cat_wastewater"]]
            select_cat = st.selectbox(t["cat_select"], cat_options)
            
            # กำหนดขอบเขตซีรีส์ปั๊มเบื้องต้นตามลักษณะงานแต่ละประเภท
            if select_cat == t["cat_building"]:
                allowed_series = ["PWPC", "NSLA", "PMP", "PMPA"]
                init_flow, init_v_head, init_h_pipe = 5.0, 15.0, 10.0  
                selected_cat_key = "building"
            elif select_cat == t["cat_booster"]:
                allowed_series = ["PMPA", "PMP"]
                init_flow, init_v_head, init_h_pipe = 35.0, 45.0, 20.0
                selected_cat_key = "booster"
            elif select_cat == t["cat_watersupply"]:
                allowed_series = ["PMP", "PMPA", "NSLA", "NSWA"]
                init_flow, init_v_head, init_h_pipe = 40.0, 30.0, 25.0
                selected_cat_key = "watersupply"
            elif select_cat == t["cat_agriculture"]:
                allowed_series = ["NSLA", "NSWA", "PMP"]
                init_flow, init_v_head, init_h_pipe = 15.0, 25.0, 40.0
                selected_cat_key = "agriculture"
            elif select_cat == t["cat_fire"]:
                allowed_series = ["PMPA", "PMP", "NSLA", "NSWA"]
                init_flow, init_v_head, init_h_pipe = 60.0, 65.0, 50.0
                selected_cat_key = "fire"
            elif select_cat == t["cat_industrial"]:
                allowed_series = ["PWPC", "NSLA", "NSWA", "NSTQW", "NSQW", "PMP", "PMPA"]
                init_flow, init_v_head, init_h_pipe = 35.0, 40.0, 30.0
                selected_cat_key = "industrial"
            else:
                allowed_series = ["NSQW", "NSTQW", "NSWA", "NSLA"]
                init_flow, init_v_head, init_h_pipe = 25.0, 12.0, 20.0
                selected_cat_key = "wastewater"
                
            # 🎯 ช่องเลือกซีรีส์ที่คุณน้าต้องการ (All Series จะรวมครบทุกซีรีส์)
            series_options = [t["all_series"], "PWPC", "NSWA", "NSTQW", "NSQW", "NSLA", "PMP", "PMPA"]
            select_series = st.selectbox(t["series_select"], series_options, index=0)
            selected_series_key = None if select_series == t["all_series"] else select_series
            
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

        if st.button(t["btn_submit"], type="primary", use_container_width=True):
            st.session_state["current_page"] = "output_page"
            st.rerun()

    elif st.session_state["current_page"] == "output_page":
        if st.button(t["btn_back"], type="secondary"):
            st.session_state["current_page"] = "input_page"
            st.rerun()
            
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
            
            residual_head = 25.0 if selected_cat_key == "booster" else 10.0
            tdh = static_head + friction_loss + residual_head
            suggested_hp = ((flow_rate * tdh * solid_sg_factor) / (367 * 0.60) * 1.341) * 1.20 
            
            st.markdown(f"#### {t['sec_calc']}")
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric(label=t["metric_flow"], value=f"{flow_rate:.1f} m³/h")
            m_col2.metric(label=t["metric_head"], value=f"{tdh:.1f} {t['meter']}", delta=f"Static:{static_head}m | Friction:{friction_loss:.1f}m")
            m_col3.metric(label=t["metric_motor"], value=f"{suggested_hp:.1f} HP")
            
            st.markdown("---")
            
            # กรองเงื่อนไขการเลือกซีรีส์ปั๊มน้ำ
            if selected_series_key:
                condition = (df_db["Series"] == selected_series_key) & \
                            (df_db["Min_Flow"] <= flow_rate) & (df_db["Max_Flow"] >= flow_rate) & \
                            (df_db["Min_Head"] <= tdh) & (df_db["Max_Head"] >= tdh)
            else:
                condition = df_db["Series"].isin(allowed_series) & \
                            (df_db["Min_Flow"] <= flow_rate) & (df_db["Max_Flow"] >= flow_rate) & \
                            (df_db["Min_Head"] <= tdh) & (df_db["Max_Head"] >= tdh)
                
            matched_pumps = df_db[condition].copy()
            
            if not matched_pumps.empty:
                st.success(t["matches_count"].format(count=len(matched_pumps)))
                model_list = matched_pumps["Model_Code"].tolist()
                selected_model = st.selectbox(t["select_pump_label"], model_list)
                
                chosen_pump = matched_pumps[matched_pumps["Model_Code"] == selected_model].iloc[0]
                
                st.markdown(f"### 📦 ข้อมูลทางเทคนิคโมเดล: {chosen_pump['Model_Code']}")
                
                curve_img, dim_img = find_pump_images(chosen_pump['Model_Code'])
                
                if curve_img:
                    st.write(f"### {t['curve_title']}")
                    st.image(Image.open(curve_img), use_container_width=True)
                
                if dim_img:
                    st.write(f"### {t['dim_title']}")
                    st.image(Image.open(dim_img), use_container_width=True)
                    
                if not curve_img and not dim_img:
                    st.info(t['img_not_found'])
            else:
                st.error(t["error_msg"])
