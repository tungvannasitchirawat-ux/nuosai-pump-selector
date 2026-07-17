import streamlit as st
import pandas as pd
import numpy as np
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Nuosai Pump Selector", layout="wide", initial_sidebar_state="expanded")

# ระบบสลับภาษา (TH / EN)
if 'lang' not in st.session_state:
    st.session_state.lang = 'TH'

def switch_lang(lang_code):
    st.session_state.lang = lang_code

# แถบด้านบนสำหรับเปลี่ยนภาษา
col_l1, col_l2 = st.columns([8, 2])
with col_l2:
    st.button("🇹🇭 TH", on_click=switch_lang, args=('TH',), use_container_width=True)
    st.button("🇺🇸 EN", on_click=switch_lang, args=('EN',), use_container_width=True)

# พจนานุกรมคำศัพท์สองภาษา
text = {
    'TH': {
        'title': "โปรแกรมคำนวณและคัดเลือกรุ่นปั๊มน้ำ Nuosai",
        'subtitle': "ระบบสนับสนุนวิศวกรรมและการเลือกขนาดปั๊มน้ำออนไลน์",
        'input_header': "📊 กรอกค่าพารามิเตอร์หน้างาน",
        'flow': "อัตราการไหล (Flow Rate) [m³/h]",
        'static_head': "ระยะความสูงตรง (Static Head) [m]",
        'pipe_len': "ความยาวท่อรวม (Total Pipe Length) [m]",
        'pipe_dia': "ขนาดเส้นผ่านศูนย์กลางท่อ (Pipe Diameter) [inch]",
        'calc_btn': "🚀 คำนวณหาค่า Total Head",
        'result_header': "📈 ผลการคำนวณทางชลศาสตร์",
        'selected_model': "รุ่นปั๊มน้ำ Nuosai ที่แนะนำสำหรับหน้างานนี้คือ:",
        'curve_title': "📊 Factory Performance Curve (กราฟแสดงประสิทธิภาพ)",
        'dim_title': "📐 Dimension Sheet (มิติตัวปั๊มและการติดตั้ง)",
        'not_found': "⚠️ ไม่พบรูปภาพรายละเอียดของรุ่นนี้ในระบบ"
    },
    'EN': {
        'title': "Nuosai Pump Selection Software",
        'subtitle': "Online Hydraulic Calculation & Pump Selection Support",
        'input_header': "📊 Input Field Parameters",
        'flow': "Flow Rate [m³/h]",
        'static_head': "Static Head [m]",
        'pipe_len': "Total Pipe Length [m]",
        'pipe_dia': "Pipe Diameter [inch]",
        'calc_btn': "🚀 Calculate Total Head",
        'result_header': "📈 Hydraulic Calculation Results",
        'selected_model': "Recommended Nuosai Pump Model:",
        'curve_title': "📊 Factory Performance Curve",
        'dim_title': "📐 Dimension Sheet & Installation Sizes",
        'not_found': "⚠️ Details for this model are not available or images missing"
    }
}[st.session_state.lang]

# แสดงโลโก้บริษัท (ถ้ามีไฟล์ logo.png ในโฟลเดอร์ images)
logo_path = "images/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=220)

st.title(text['title'])
st.caption(text['subtitle'])
st.write("---")

# แบ่งหน้าจอเป็น 2 ฝั่ง (ฝั่งกรอกข้อมูล กับ ฝั่งแสดงผล)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header(text['input_header'])
    flow = st.number_input(text['flow'], min_value=0.0, value=15.0, step=1.0)
    static_head = st.number_input(text['static_head'], min_value=0.0, value=20.0, step=1.0)
    pipe_len = st.number_input(text['pipe_len'], min_value=0.0, value=50.0, step=5.0)
    pipe_dia = st.selectbox(text['pipe_dia'], options=[1.0, 1.5, 2.0, 2.5, 3.0, 4.0], index=2)

    # ปุ่มคำนวณ
    calculate = st.button(text['calc_btn'], type="primary", use_container_width=True)

# คำนวณหา Total Dynamic Head (TDH) เบื้องต้น
# สูตรลัด Hazen-Williams สำหรับท่อเหล็ก/พลาสติกทั่วไป
d_m = pipe_dia * 0.0254 # แปลงนิ้วเป็นเมตร
velocity = (flow / 3600) / (np.pi * (d_m**2) / 4) if flow > 0 else 0
hf = 10.67 * (flow/3600)**1.852 / (130**1.852 * d_m**4.87) * pipe_len if flow > 0 else 0
total_head = static_head + hf

with col2:
    if calculate or flow > 0:
        st.header(text['result_header'])
        
        # แสดงผลลัพธ์ตัวเลข
        res_c1, res_c2, res_c3 = st.columns(3)
        res_c1.metric(label="Total Head (m)", value=f"{total_head:.2f} m")
        res_c2.metric(label="Flow Rate", value=f"{flow:.1f} m³/h")
        res_c3.metric(label="Velocity", value=f"{velocity:.2f} m/s")
        
        st.write("---")
        
        # ลอจิกการคัดเลือกรุ่นปั๊มน้ำอัตโนมัติ (ตัวอย่างอิงตามค่า Head และ Flow)
        if flow <= 10 and total_head <= 25:
            model_name = "NSS-40-25"
        elif flow <= 20 and total_head <= 40:
            model_name = "NSS-50-40"
        elif flow <= 40 and total_head <= 60:
            model_name = "NSS-65-60"
        else:
            model_name = "NSS-80-80"
            
        st.subheader(text['selected_model'])
        st.info(f"🏆 **Nuosai {model_name}**")
        
        # แสดงข้อมูลรูปภาพจากโฟลเดอร์ images (เช็กชื่อรูปตามรุ่นปั๊ม)
        st.write(f"### {text['curve_title']}")
        curve_img = f"images/{model_name.lower()}_curve.png"
        if os.path.exists(curve_img):
            st.image(curve_img, caption=f"Performance Curve - {model_name}")
        else:
            st.warning(text['not_found'])
            
        st.write(f"### {text['dim_title']}")
        dim_img = f"images/{model_name.lower()}_dim.png"
        if os.path.exists(dim_img):
            st.image(dim_img, caption=f"Dimensions - {model_name}")
        else:
            st.warning(text['not_found'])
