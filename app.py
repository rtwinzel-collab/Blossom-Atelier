import sqlite3
import streamlit as st

st.set_page_config(page_title="Blossom Atelier - Management System", layout="wide")

# Google Font & Soft Pastel Aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&family=Poppins:wght@300;400;600&display=swap');

    .stApp {
        background-color: #FAF6F8;
        font-family: 'Poppins', sans-serif;
    }
    .shop-title {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 38px;
        color: #6C5B7B;
        text-align: center;
        margin-bottom: 0px;
    }
    .shop-subtitle {
        text-align: center;
        color: #8E7C93;
        font-size: 13px;
        margin-bottom: 15px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .header-container {
        background: linear-gradient(135deg, #FFECF2 0%, #E6F2FF 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #F3D1DC;
        margin-bottom: 20px;
    }
    .product-box {
        background-color: #FFFFFF;
        border: 1px solid #E6EEF8;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.02);
    }
    .receipt-box {
        background-color: #FFF9FB;
        border: 1px dashed #F3D1DC;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Courier New', Courier, monospace;
        color: #4A4A4A;
    }
    .stButton>button {
        background-color: #E6F2FF !important;
        color: #4A6984 !important;
        border-radius: 8px !important;
        border: 1px solid #C5E1A5 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div class="header-container">
        <div class="shop-title">Blossom Atelier</div>
        <div class="shop-subtitle">Boutique POS, Event Styling & Delivery Tracker</div>
    </div>
""", unsafe_allow_html=True)

def get_connection():
    return sqlite3.connect("flower_shop.db")

# Session state initialization
if "cart" not in st.session_state:
    st.session_state.cart = []

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "🌸 Blossom Menu",
    ["🛒 POS Checkout & Catalog", "📅 Event Bookings & Registration", "🚚 Deliveries & Tracking", "📂 Archived Records"]
)

# ----------------------------------------------------
# 1. POS CHECKOUT & CATALOG
# ----------------------------------------------------
if menu == "🛒 POS Checkout & Catalog":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, category, type, stock, price FROM inventory")
    all_items = cursor.fetchall()
    conn.close()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🛍️ Product Catalog")
        
        category_choice = st.radio(
            "Select Category:",
            ["🌸 Fresh Flowers", "🌺 Artificial / Dried Flowers", "🎀 Decors & Accessories"],
            horizontal=True
        )
        
        selected_cat = "Fresh Flowers" if "Fresh" in category_choice else ("Artificial Flowers" if "Artificial" in category_choice else "Decors & Hardware")
        filtered_items = [item for item in all_items if item[2] == selected_cat]

        st.write("---")
        
        cols = st.columns(2)
        for idx, (item_id, name, cat, ftype, stock, price) in enumerate(filtered_items):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="product-box">
                        <h5 style="margin:0; color:#5C4B51; font-size:15px;">{name}</h5>
                        <p style="margin:5px 0; color:#7F8C8D; font-size:13px;">
                            <b>Price:</b> ₱{price:,.2f} | <b>Stock:</b> {stock} pcs
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Add to Order", key=f"add_{item_id}"):
                    if stock > 0:
                        st.session_state.cart.append({"id": item_id, "name": name, "price": price})
                        st.toast(f"Added {name}!", icon="🌸")
                    else:
                        st.error("Out of stock!")

    with col2:
        st.subheader("📋 Grocery-Style Cart & Receipt")
        
        if st.session_state.cart:
            st.write("---")
            total_amount = 0
            
            # Itemized Cart Display
            for idx, item in enumerate(st.session_state.cart):
                c_info, c_del = st.columns([4, 1])
                with c_info:
                    st.write(f"*{idx+1}. {item['name']}* — ₱{item['price']:,.2f}")
                with c_del:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                total_amount += item['price']

            st.write("---")
            st.markdown(f"### *Total:* <span style='color:#B85B7A;'>₱{total_amount:,.2f}</span>", unsafe_allow_html=True)
            
            payment_method = st.selectbox("💳 Payment Method", ["Cash", "GCash", "Maya", "Credit/Debit Card", "Bank Transfer"])
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("❌ Clear All Cart"):
                    st.session_state.cart = []
                    st.rerun()
            with b2:
                if st.button("🧾 Checkout & Print"):
                    # Online payment notification simulator
                    if payment_method in ["GCash", "Maya", "Credit/Debit Card", "Bank Transfer"]:
                        st.success(f"📱 *[ONLINE PAYMENT NOTIFICATION]* Payment of ₱{total_amount:,.2f} via {payment_method} received successfully! Confirmed in system.")
                    
                    conn = get_connection()
                    cur = conn.cursor()
                    for item in st.session_state.cart:
                        cur.execute("UPDATE inventory SET stock = stock - 1 WHERE id = ?", (item['id'],))
                        cur.execute("INSERT INTO pos_sales (item_name, quantity, total_price, payment_method) VALUES (?, ?, ?, ?)",
                                    (item['name'], 1, item['price'], payment_method))
                    conn.commit()
                    conn.close()
                    
                    # Grocery-Style Official Receipt Output
                    receipt_items_html = ""
                    for i, itm in enumerate(st.session_state.cart):
                        receipt_items_html += f"<tr><td>{i+1}. {itm['name']}</td><td style='text-align:right;'>1x</td><td style='text-align:right;'>₱{itm['price']:,.2f}</td></tr>"

                    st.markdown(f"""
                        <div class="receipt-box">
                            <h3 style="text-align:center; margin:0; font-family:'Playfair Display',serif;">Blossom Atelier</h3>
                            <p style="text-align:center; font-size:11px; margin:2px 0;">Official Sales Receipt</p>
                            <hr style="border-top:1px dashed #F3D1DC;">
                            <table style="width:100%; font-size:12px;">
                                {receipt_items_html}
                            </table>
                            <hr style="border-top:1px dashed #F3D1DC;">
                            <p><b>Payment Method:</b> {payment_method}</p>
                            <p style="font-size:15px;"><b>TOTAL AMOUNT: ₱{total_amount:,.2f}</b></p>
                            <p style="text-align:center; font-size:10px; margin-top:10px;">Thank you for shopping with us! 💐</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.cart = []
        else:
            st.info("Your cart is empty. Select items from the catalog.")

# ----------------------------------------------------
# 2. EVENT BOOKINGS & REGISTRATION
# ----------------------------------------------------
elif menu == "📅 Event Bookings & Registration":
    st.subheader("📅 Client Event Registration & Floral Styling")
    
    with st.form("event_reservation_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            c_name = st.text_input("Client Full Name *")
            c_phone = st.text_input("Contact Number / Delivery Address *")
            e_type = st.selectbox("Event Occasion", [
                "Grand Wedding Ceremony & Reception",
                "Debutante Ball (18th Birthday)",
                "Birthday Celebration",
                "Funeral & Sympathy Floral Setup",
                "Anniversary Celebration",
                "Graduation & Recognition",
                "Marriage Proposal Setup",
                "Church & Religious Event",
                "Corporate Gala / Formal Event",
                "Valentine / Mother's Day Custom Order"
            ])
            e_date = st.date_input("Event / Delivery Date")
        
        with col_b:
            e_package = st.selectbox("Floral / Decor Package Tier", [
                "Full Venue Grand Floral Setup (₱35,000.00)",
                "Deluxe Wedding & Entourage Set (₱22,000.00)",
                "Sympathy Standing Wreath Pair (₱7,500.00)",
                "Intimate Stage & Table Flowers (₱9,000.00)",
                "Romantic Proposal & Petals Setup (₱6,500.00)",
                "Customized Arrangement"
            ])
            pay_method = st.selectbox("Payment Method", ["GCash", "Cash", "Maya", "Bank Transfer", "Credit Card"])
            est_price = st.number_input("Final Agreed Amount (₱)", value=7500.0, step=500.0)

        notes = st.text_area("Customization Details (Color theme, flower types, special instructions)")
        submit = st.form_submit_button("✅ Submit & Register Event Booking")

        if submit:
            if not c_name.strip():
                st.error("Please enter Client Name.")
            else:
                if pay_method in ["GCash", "Maya", "Bank Transfer", "Credit Card"]:
                    st.success(f"📱 *[ONLINE PAYMENT NOTIFICATION]* Downpayment/Full payment of ₱{est_price:,.2f} via {pay_method} confirmed!")
                
                conn = get_connection(); cur = conn.cursor()
                cur.execute("""
                    INSERT INTO event_bookings 
                    (client_name, contact_num, event_type, event_date, package, custom_notes, payment_method, status, total_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
                """, (c_name, c_phone, e_type, str(e_date), e_package, notes, pay_method, est_price))
                conn.commit(); conn.close()
                st.success(f"Event booking successfully registered for {c_name}!")

# ----------------------------------------------------
# 3. DELIVERIES & TRACKING
# ----------------------------------------------------
elif menu == "🚚 Deliveries & Tracking":
    st.subheader("🚚 Active Deliveries & Event Status Tracker")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, client_name, contact_num, event_type, event_date, package, custom_notes, payment_method, status, total_amount FROM event_bookings WHERE status != 'Delivered & Completed' ORDER BY id DESC")
    active_bookings = cur.fetchall(); conn.close()
    
    if active_bookings:
        for b in active_bookings:
            b_id, name, phone, etype, edate, pkg, notes, pay, status, total = b
            
            with st.expander(f"📌 Order #{b_id} - {name} ({etype}) — Status: [{status}]"):
                st.write(f"*Contact/Address:* {phone} | *Date:* {edate}")
                st.write(f"*Package:* {pkg} | *Payment:* {pay} ({total:,.2f})")
                if notes:
                    st.write(f"*Notes:* {notes}")
                
                st.write("*Update Delivery Progress Status:*")
                sc1, sc2, sc3, sc4 = st.columns(4)
                
                with sc1:
                    if st.button("⏳ Pending", key=f"p_{b_id}"):
                        conn = get_connection(); cur = conn.cursor()
                        cur.execute("UPDATE event_bookings SET status = 'Pending' WHERE id = ?", (b_id,)); conn.commit(); conn.close(); st.rerun()
                with sc2:
                    if st.button("🌸 In Preparation", key=f"prep_{b_id}"):
                        conn = get_connection(); cur = conn.cursor()
                        cur.execute("UPDATE event_bookings SET status = 'In Preparation' WHERE id = ?", (b_id,)); conn.commit(); conn.close(); st.rerun()
                with sc3:
                    if st.button("🚚 Out for Delivery", key=f"del_{b_id}"):
                        conn = get_connection(); cur = conn.cursor()
                        cur.execute("UPDATE event_bookings SET status = 'Out for Delivery' WHERE id = ?", (b_id,)); conn.commit(); conn.close(); st.rerun()
                with sc4:
                    if st.button("✅ Delivered & Complete", key=f"comp_{b_id}"):
                        conn = get_connection(); cur = conn.cursor()
                        cur.execute("UPDATE event_bookings SET status = 'Delivered & Completed' WHERE id = ?", (b_id,)); conn.commit(); conn.close(); st.rerun()
    else:
        st.info("No active deliveries in queue right now.")

# ----------------------------------------------------
# 4. ARCHIVED RECORDS
# ----------------------------------------------------
elif menu == "📂 Archived Records":
    st.subheader("📂 Completed & Archived Records History")
    st.caption("All finished deliveries and fully paid bookings are securely recorded here for future references and client history.")
    
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, client_name, contact_num, event_type, event_date, package, payment_method, total_amount, date_created FROM event_bookings WHERE status = 'Delivered & Completed' ORDER BY id DESC")
    archived = cur.fetchall(); conn.close()
    
    if archived:
        for a in archived:
            a_id, name, phone, etype, edate, pkg, pay, total, created = a
            st.success(f"✔️ *Order #{a_id} - {name}* | {etype} | Date: {edate} | Paid: ₱{total:,.2f} via {pay} | Contact: {phone}")
    else:
        st.info("No archived transactions yet.")