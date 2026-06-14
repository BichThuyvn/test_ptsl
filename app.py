# =====================================================================
# MỨC 3 - ĐOẠN 4: WEB DASHBOARD - TRIỂN KHAI HOÀN TOÀN BẰNG STREAMLIT
# =====================================================================
import streamlit as st
import pandas as pd
import numpy as np

# Cấu hình trang hiển thị của Streamlit (Phải đặt ở dòng đầu tiên)
st.set_page_config(
    page_title="Banking Performance Dashboard",
    page_icon="📈",
    layout="wide" # Hiển thị giao diện rộng tràn màn hình
)

# Khởi tạo các biến Icon hệ thống
ICON_WARN_YELLOW = "⚠️"  # Emoji hệ thống hiển thị màu vàng chuẩn trên trình duyệt
ICON_WAIT = "🔄"         # Vòng xoay tiến trình trạng thái chờ

# Khởi tạo giá trị mặc định trong st.session_state nếu chưa có
if "atm_val" not in st.session_state: st.session_state.atm_val = 0.0
if "mobile_val" not in st.session_state: st.session_state.mobile_val = 0.0
if "online_val" not in st.session_state: st.session_state.online_val = 0.0
if "fee_val" not in st.session_state: st.session_state.fee_val = None
if "run_sim" not in st.session_state: st.session_state.run_sim = False

# Thiết lập tiêu đề và mô tả hệ thống bằng Markdown
st.markdown("# 📈 Hệ Thống Dự Báo & Mô Phỏng Kịch Bản Chiến Lược Ngân Hàng")
st.markdown("*Nghiên cứu ứng dụng Prescriptive Analytics nhằm tối ưu hóa vận hành hệ thống số.*")
st.markdown("---")

# Thiết lập tỷ lệ cột [4, 5] giúp cột trái rộng rãi, tiêu đề "What-If" không bị vỡ dòng
col_left, col_right = st.columns([4, 5], gap="large")

# =====================================================================
# CỘT TRÁI: BẢNG ĐIỀU KHIỂN ĐẦU VÀO (WHAT-IF CONFIGURATION)
# =====================================================================
with col_left:
    st.markdown("### 🎯 Cấu hình kịch bản (What-If)")
    
    # Tạo các thanh trượt nhập tham số gắn liền với session_state
    atm = st.slider("Tăng trưởng quy mô kênh ATM", min_value=0.0, max_value=0.2, step=0.05, key="atm_val")
    mobile = st.slider("Đầu tư phát triển Mobile Banking", min_value=0.0, max_value=0.4, step=0.1, key="mobile_val")
    online = st.slider("Khuyến khích Online Banking", min_value=0.0, max_value=0.25, step=0.05, key="online_val")
    
    # Hộp chọn chính sách phí dịch vụ gắn liền với session_state
    fee_options = [None, -0.05, 0.0, 0.1]
    fee = st.selectbox(
        "Chính sách điều chỉnh phí dịch vụ", 
        options=fee_options, 
        key="fee_val",
        format_func=lambda x: "Chưa xác định" if x is None else f"{x*100:+.1f}%"
    )
    
    # 🛠️ ĐỊNH NGHĨA HÀM RESET NGẦM QUA CALLBACK ĐỂ TRÁNH LỖI XUNG ĐỘT WIDGET
    def reset_all_filters():
        st.session_state.atm_val = 0.0
        st.session_state.mobile_val = 0.0
        st.session_state.online_val = 0.0
        st.session_state.fee_val = None
        st.session_state.run_sim = False

    # Tạo hàng chứa 2 nút bấm điều khiển
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 CHẠY MÔ PHỎNG", use_container_width=True, type="primary"):
            st.session_state.run_sim = True
    with col_btn2:
        # Gọi hàm xử lý ngầm thông qua thuộc tính on_click trước khi Streamlit load lại trang
        st.button("🗑️ XÓA BỘ LỌC", use_container_width=True, on_click=reset_all_filters)

# =====================================================================
# CỘT PHẢI: XỬ LÝ LOGIC VÀ HIỂN THỊ KẾT QUẢ ĐẦU RA CAO CẤP (BOX CARDS)
# =====================================================================
with col_right:
    st.markdown("### 📌 Chỉ số kết quả đầu ra")
    
    # Tạo sẵn cấu trúc lưới 2 hàng, 2 cột để định vị vị trí các Card
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # TRƯỜNG HỢP 1: Trạng thái chờ kích hoạt (Tạo các Hộp Card trống bo góc có viền mờ cân đối)
    if not st.session_state.run_sim:
        with row1_col1:
            with st.container(border=True):
                st.markdown("<p style='color: gray; font-size: 14px; margin-bottom: 5px;'>Tổng lượng giao dịch mô phỏng</p>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: lightgray; margin-top: 0; font-weight: normal;'>🔄 Đang chờ...</h3>", unsafe_allow_html=True)
                
        with row1_col2:
            with st.container(border=True):
                st.markdown("<p style='color: gray; font-size: 14px; margin-bottom: 5px;'>Doanh thu kênh (Channel Revenue)</p>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: lightgray; margin-top: 0; font-weight: normal;'>🔄 Đang chờ...</h3>", unsafe_allow_html=True)
                
        with row2_col1:
            with st.container(border=True):
                st.markdown("<p style='color: gray; font-size: 14px; margin-bottom: 5px;'>Doanh thu từ phí dịch vụ</p>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: lightgray; margin-top: 0; font-weight: normal;'>🔄 Đang chờ...</h3>", unsafe_allow_html=True)
                
        with row2_col2:
            with st.container(border=True):
                st.markdown("<p style='color: gray; font-size: 14px; margin-bottom: 5px;'>Điểm hiệu suất chi nhánh (Branch Score)</p>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: lightgray; margin-top: 0; font-weight: normal;'>🔄 Đang chờ...</h3>", unsafe_allow_html=True)
                
        st.info("🔄 **Hệ thống đang ở trạng thái chờ kích hoạt tiến trình mô phỏng từ bảng điều khiển.**")

    # TRƯỜNG HỢP 2: Người dùng nhấn nút CHẠY MÔ PHỎNG
    else:
        # Kiểm tra lỗi khuyết dữ liệu đầu vào
        if fee is None:
            with row1_col1:
                with st.container(border=True): st.metric(label="Tổng lượng giao dịch mô phỏng", value="⚠️ Khuyết")
            with row1_col2:
                with st.container(border=True): st.metric(label="Doanh thu kênh (Channel Revenue)", value="⚠️ Khuyết")
            with row2_col1:
                with st.container(border=True): st.metric(label="Doanh thu từ phí dịch vụ", value="⚠️ Khuyết")
            with row2_col2:
                with st.container(border=True): st.metric(label="Điểm hiệu suất chi nhánh (Branch Score)", value="⚠️ Khuyết")
                
            st.error("**⚠️ THÔNG BÁO HỆ THỐNG:** Vui lòng xác định **Chính sách điều chỉnh phí dịch vụ** tại bảng cấu hình trước khi tiến hành thực hiện mô phỏng kịch bản.")
            
        else:
            # KHỐI TRUY VẤN DỮ LIỆU TỪ FILE EXCEL HỆ THỐNG
            try:
                df_wi = pd.read_excel
