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
    
    # Tạo các thanh trượt nhập tham số
    atm = st.slider("Tăng trưởng quy mô kênh ATM", min_value=0.0, max_value=0.2, step=0.05, value=0.0)
    mobile = st.slider("Đầu tư phát triển Mobile Banking", min_value=0.0, max_value=0.4, step=0.1, value=0.0)
    online = st.slider("Khuyến khích Online Banking", min_value=0.0, max_value=0.25, step=0.05, value=0.0)
    
    # Hộp chọn chính sách phí (Mặc định ban đầu chưa chọn để kích hoạt cảnh báo)
    fee_options = [None, -0.05, 0.0, 0.1]
    fee = st.selectbox(
        "Chính sách điều chỉnh phí dịch vụ", 
        options=fee_options, 
        format_func=lambda x: "Chưa xác định" if x is None else f"{x*100:+.1f}%"
    )
    
    # Tạo hàng chứa 2 nút bấm điều khiển
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_run = st.button("🚀 CHẠY MÔ PHỎNG", use_container_width=True, type="primary")
    with col_btn2:
        btn_reset = st.button("🗑️ XÓA BỘ LỌC", use_container_width=True)

# =====================================================================
# CỘT PHẢI: XỬ LÝ LOGIC VÀ HIỂN THỊ KẾT QUẢ ĐẦU RA CAO CẤP (BOX CARDS)
# =====================================================================
with col_right:
    st.markdown("### 📌 Chỉ số kết quả đầu ra")
    
    # Tạo sẵn cấu trúc lưới 2 hàng, 2 cột để định vị vị trí các Card
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # TRƯỜNG HỢP 1: Trạng thái chờ kích hoạt (Tạo các Hộp Card trống bo góc có viền mờ cân đối)
    if btn_reset or (not btn_run):
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
    elif btn_run:
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
                df_wi = pd.read_excel("Banking_Analytics_Result.xlsx", sheet_name="WhatIf")
                df_wi['ATM'] = df_wi['ATM'].round(2)
                df_wi['Mobile'] = df_wi['Mobile'].round(2)
                df_wi['Online'] = df_wi['Online'].round(2)
                df_wi['Fee'] = df_wi['Fee'].round(2)
                
                atm_val = round(atm, 2)
                mob_val = round(mobile, 2)
                onl_val = round(online, 2)
                fee_val = round(float(fee), 2)
                
                # Tìm kiếm dòng dữ liệu kịch bản trùng khớp
                matched = df_wi[
                    (df_wi['ATM'] == atm_val) &
                    (df_wi['Mobile'] == mob_val) &
                    (df_wi['Online'] == onl_val) &
                    (df_wi['Fee'] == fee_val)
                ]
                
                if not matched.empty:
                    res = matched.iloc[0]
                    score_val = f"{res['FinalScore']:.3f}"
                else:
                    # Thuật toán tính toán khoảng cách hình học để nội suy kịch bản gần nhất
                    df_wi['Distance'] = (df_wi['ATM'] - atm_val).abs() + (df_wi['Mobile'] - mob_val).abs() + (df_wi['Online'] - onl_val).abs() + (df_wi['Fee'] - fee_val).abs()
                    res = df_wi.sort_values(by='Distance').iloc[0]
                    score_val = f"{res['FinalScore']:.3f} (Nội suy)"
                
                # Hiển thị số liệu thật to, đậm, rõ ràng đặt gọn gàng trong các Card bo góc cao cấp
                with row1_col1:
                    with st.container(border=True):
                        st.metric(label="Tổng lượng giao dịch mô phỏng", value=f"{res['TotalVolume']:.0f} GD")
                with row1_col2:
                    with st.container(border=True):
                        st.metric(label="Doanh thu kênh (Channel Revenue)", value=f"${res['TotalRevenue']:,.2f}")
                with row2_col1:
                    with st.container(border=True):
                        st.metric(label="Doanh thu từ phí dịch vụ", value=f"${res['TotalFeeRevenue']:,.2f}")
                with row2_col2:
                    with st.container(border=True):
                        st.metric(label="Điểm hiệu suất chi nhánh (Branch Score)", value=f"{res['BranchScore']:.3f}")
                
                # Khung thông báo kết quả chiến lược tổng hợp đồng bộ màu xanh lục
                st.success(f"🏆 **CHỈ SỐ ĐÁNH GIÁ CHIẾN LƯỢC TỔNG HỢP (FINAL SCORE): {score_val}**")
                
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống khi đọc dữ liệu tệp Excel: {str(e)}")
