import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG VÀ THÔNG TIN BẢNG GIÁ
# ---------------------------------------------------------
st.set_page_config(
    page_title="Quản Lý Hóa Đơn Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# Danh sách menu & Bảng giá (VND)
MENU_DRINKS = {
    "Trà sữa truyền thống": 25000,
    "Trà sữa Oolong": 30000,
    "Trà sữa Matcha": 32000,
    "Trà sữa Trái cây (Đào/Vải)": 28000,
    "Trà sữa Kem Trứng Nướng": 35000,
    "Trà Trái Cây Tươi": 25000
}

SIZE_PRICE = {
    "Nhỏ (S)": 0,
    "Vừa (M)": 5000,
    "Lớn (L)": 10000
}

TOPPING_PRICE = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding Flau": 8000,
    "Kem Cheese": 10000
}

ICE_LEVELS = ["100% Đá", "70% Đá", "50% Đá", "Không đá"]

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE (BỘ NHỚ TẠM)
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

def clear_order():
    st.session_state.cart = []
    st.session_state.paid = False

# ---------------------------------------------------------
# 3. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 Hệ Thống Tính Tiền & Xuất Hóa Đơn Trà Sữa")
st.markdown("---")

col_left, col_right = st.columns([1, 1], gap="large")

# ---------------------------------------------------------
# CỘT TRÁI: NHẬP THÔNG TIN VÀ CHỌN MÓN
# ---------------------------------------------------------
with col_left:
    st.subheader("📝 Nhập Thông Tin Đặt Hàng")
    
    # Thông tin khách hàng
    customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")
    
    st.markdown("### Chọn Món Nước")
    
    # Form chọn chi tiết món nước
    drink_choice = st.selectbox("Loại trà sữa:", list(MENU_DRINKS.keys()))
    size_choice = st.selectbox("Size ly:", list(SIZE_PRICE.keys()))
    ice_choice = st.select_slider("Mức độ đá:", options=ICE_LEVELS)
    topping_choices = st.multiselect("Thêm Topping:", list(TOPPING_PRICE.keys()))
    quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)
    
    # Tính giá tiền cho 1 ly
    base_price = MENU_DRINKS[drink_choice]
    size_extra = SIZE_PRICE[size_choice]
    topping_extra = sum([TOPPING_PRICE[t] for t in topping_choices])
    item_unit_price = base_price + size_extra + topping_extra
    item_total = item_unit_price * quantity
    
    st.info(f"💰 Đơn giá/ly: **{item_unit_price:,} VNĐ** | Tổng món này: **{item_total:,} VNĐ**")
    
    # Nút thêm món vào giỏ
    if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):
        item = {
            "Tên món": drink_choice,
            "Size": size_choice,
            "Đá": ice_choice,
            "Topping": ", ".join(topping_choices) if topping_choices else "Không",
            "Số lượng": quantity,
            "Đơn giá": item_unit_price,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item)
        st.session_state.paid = False
        st.success(f"Đã thêm {quantity} {drink_choice} vào danh sách!")

# ---------------------------------------------------------
# CỘT PHẢI: XEM GIỎ HÀNG VÀ XUẤT HÓA ĐƠN
# ---------------------------------------------------------
with col_right:
    st.subheader("🛒 Danh Sách Món Đã Chọn")
    
    if len(st.session_state.cart) > 0:
        # Hiển thị bảng danh sách món đã thêm
        df_cart = pd.DataFrame(st.session_state.cart)
        
        # Định dạng tiền tệ hiển thị bảng
        st.dataframe(
            df_cart[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]],
            hide_index=True,
            use_container_width=True
        )
        
        # Tính tổng đơn hàng
        grand_total = sum(item["Thành tiền"] for item in st.session_state.cart)
        st.markdown(f"### 🧮 Tổng Tiền Thanh Toán: :red[{grand_total:,} VNĐ]")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💳 Thanh Toán & Xuất Hóa Đơn", type="primary", use_container_width=True):
                if not customer_name.strip():
                    st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi thanh toán!")
                else:
                    st.session_state.paid = True
        
        with col_btn2:
            if st.button("🗑️ Xóa/Làm mới hóa đơn", use_container_width=True):
                clear_order()
                st.rerun()

        # ---------------------------------------------------------
        # HIỂN THỊ VÀ XUẤT HÓA ĐƠN KHI BẤM THANH TOÁN
        # ---------------------------------------------------------
        if st.session_state.paid:
            st.markdown("---")
            st.subheader("🧾 HÓA ĐƠN BÁN HÀNG")
            
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Tạo nội dung hóa đơn dạng Text
            bill_content = f"===================================\n"
            bill_content += f"        QUÁN TRÀ SỮA BOBA      \n"
            bill_content += f"===================================\n"
            bill_content += f"Thời gian : {now_str}\n"
            bill_content += f"Khách hàng: {customer_name}\n"
            bill_content += f"-----------------------------------\n"
            
            for idx, item in enumerate(st.session_state.cart, 1):
                bill_content += f"{idx}. {item['Tên món']} ({item['Size']})\n"
                bill_content += f"   - Đá: {item['Đá']}\n"
                bill_content += f"   - Topping: {item['Topping']}\n"
                bill_content += f"   - SL: {item['Số lượng']} x {item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
            
            bill_content += f"-----------------------------------\n"
            bill_content += f"TỔNG CỘNG: {grand_total:,} VNĐ\n"
            bill_content += f"===================================\n"
            bill_content += f"     Cảm ơn & Hẹn gặp lại quý khách!  \n"

            # Khung xem trước hóa đơn
            st.code(bill_content, language="text")

            # Nút Tải Hóa Đơn
            st.download_button(
                label="📥 Tải file Hóa Đơn (.txt)",
                data=bill_content,
                file_name=f"HoaDon_{customer_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("Chưa có món nào được thêm vào hóa đơn.")
