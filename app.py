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

# Chia giao diện làm 2 cột: Cột trái (Cấu hình), Cột phải (Kết quả)
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
# CỘT PHẢI: XỬ LÝ LOGIC VÀ HIỂN THỊ KẾT QUẢ KPI (ĐÃ TỐI ƯU CHỮ TO, ĐẬM)
# =====================================================================
with col_right:
    st.markdown("### 📌 Chỉ số kết quả đầu ra")
    
    # Tạo sẵn các ô chứa kết quả dưới dạng lưới 2x2 bằng cấu trúc cột thông minh
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # # Trường hợp 1: Người dùng nhấn nút XÓA BỘ LỌC hoặc chưa thực hiện hành động nào
    # if btn_reset or (not btn_run):
    #     # Điền trạng thái chờ vào các khối hiển thị Metric (Chữ to, rõ ràng)
    #     with row1_col1: st.metric(label="Tổng lượng giao dịch mô phỏng", value="🔄 Đang chờ...")
    #     with row1_col2: st.metric(label="Doanh thu kênh (Channel Revenue)", value="🔄 Đang chờ...")
    #     with row2_col1: st.metric(label="Doanh thu từ phí dịch vụ", value="🔄 Đang chờ...")
    #     with row2_col2: st.metric(label="Điểm hiệu suất chi nhánh (Branch Score)", value="🔄 Đang chờ...")

    # Trường hợp 1: Người dùng nhấn nút XÓA BỘ LỌC hoặc chưa thực hiện hành động nào
    if btn_reset or (not btn_run):
        st.info("🔄 **Hệ thống đang ở trạng thái chờ kích hoạt tiến trình mô phỏng...**")
    
        # Tạo chữ nhỏ tinh tế hiển thị trạng thái chờ
        r1, r2 = st.columns(2)
        r3, r4 = st.columns(2)
        r1.caption("🔹 **Tổng lượng giao dịch mô phỏng:** *Đang chờ...*")
        r2.caption("🔹 **Doanh thu kênh (Channel Revenue):** *Đang chờ...*")
        r3.caption("🔹 **Doanh thu từ phí dịch vụ:** *Đang chờ...*")
        r4.caption("🔹 **Điểm hiệu suất chi nhánh (Branch Score):** *Đang chờ...*")
        
        # Khung thông báo trạng thái chờ dạng thông tin màu xanh lục nhạt
        st.info("🔄 Hệ thống đang ở trạng thái chờ kích hoạt tiến trình mô phỏng...")

    # Trường hợp 2: Người dùng nhấn nút CHẠY MÔ PHỎNG
    elif btn_run:
        # KIỂM TRA LỖI: Nếu chưa chọn chính sách phí dịch vụ
        if fee is None:
            # Hiện trạng thái Khuyết to rõ tại các Metric kết quả đầu ra
            with row1_col1: st.metric(label="Tổng lượng giao dịch mô phỏng", value="⚠️ Khuyết")
            with row1_col2: st.metric(label="Doanh thu kênh (Channel Revenue)", value="⚠️ Khuyết")
            with row2_col1: st.metric(label="Doanh thu từ phí dịch vụ", value="⚠️ Khuyết")
            with row2_col2: st.metric(label="Điểm hiệu suất chi nhánh (Branch Score)", value="⚠️ Khuyết")
            
            # Khung thông báo lỗi tổng thể bên dưới giữ màu đỏ uy tín bằng hàm st.error
            st.error("**⚠️ THÔNG BÁO HỆ THỐNG:** Vui lòng xác định **Chính sách điều chỉnh phí dịch vụ** tại bảng cấu hình trước khi tiến hành thực hiện mô phỏng kịch bản.")
            
        else:
            # KHỐI TÍNH TOÁN DỮ LIỆU THẬT TỪ FILE EXCEL
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
                
                # Quét tìm dòng dữ liệu khớp chính xác kịch bản
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
                    # Thuật toán tính khoảng cách để nội suy kịch bản gần nhất
                    df_wi['Distance'] = (df_wi['ATM'] - atm_val).abs() + (df_wi['Mobile'] - mob_val).abs() + (df_wi['Online'] - onl_val).abs() + (df_wi['Fee'] - fee_val).abs()
                    res = df_wi.sort_values(by='Distance').iloc[0]
                    score_val = f"{res['FinalScore']:.3f} (Nội suy)"
                
                # Đổ dữ liệu thật tìm được lên giao diện Metric (Chữ to đùng, đậm nét màu đen chuẩn Dashboard)
                with row1_col1: 
                    st.metric(label="Tổng lượng giao dịch mô phỏng", value=f"{res['TotalVolume']:.0f} GD")
                with row1_col2: 
                    st.metric(label="Doanh thu kênh (Channel Revenue)", value=f"${res['TotalRevenue']:,.2f}")
                with row2_col1: 
                    st.metric(label="Doanh thu từ phí dịch vụ", value=f"${res['TotalFeeRevenue']:,.2f}")
                with row2_col2: 
                    st.metric(label="Điểm hiệu suất chi nhánh (Branch Score)", value=f"{res['BranchScore']:.3f}")
                
                # Khung thông báo kết quả thành công màu xanh lục của Streamlit
                st.success(f"🏆 **CHỈ SỐ ĐÁNH GIÁ CHIẾN LƯỢC TỔNG HỢP (FINAL SCORE): {score_val}**")
                
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống khi đọc dữ liệu tệp Excel: {str(e)}")
