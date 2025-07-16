import streamlit as st  # type: ignore
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("SHOPPING_API_KEY")

st.set_page_config(page_title="Premium Shopping Agent", page_icon="🛍️", layout="centered")

# ---- Custom CSS for Styling ----
st.markdown("""
    <style>
        .main {background-color: #f7f9fa;}
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #f5b301;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #444;
        }
        .product-card {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 15px;
            background-color: #fff;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("<div class='title'>🛍️ Premium Shopping Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Welcome! Browse or search products easily.</div><br>", unsafe_allow_html=True)

# ---- Options ----
option = st.selectbox("Choose Option", ["Browse Products", "View Product by ID"])

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}"
    }

# ---- Browse Products ----
if option == "Browse Products":
    try:
        res = requests.get(f"{API_URL}/products", headers=get_headers())
        res.raise_for_status()
        products = res.json()

        for p in products:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h4>{p['title']}</h4>
                    <p><strong>ID:</strong> {p['id']}</p>
                    <p><strong>Price:</strong> ${p['price']}</p>
                    <p><strong>Category:</strong> {p['category']}</p>
                    <details>
                        <summary>Description</summary>
                        <p>{p['description']}</p>
                    </details>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error fetching products: {e}")

# ---- View by ID ----
elif option == "View Product by ID":
    product_id = st.text_input("Enter Product ID (number only):")

    if product_id.isdigit():
        if st.button("Fetch Product"):
            try:
                res = requests.get(f"{API_URL}/products/{product_id}", headers=get_headers())
                res.raise_for_status()
                p = res.json()

                st.markdown(f"""
                <div class="product-card">
                    <h4>{p['title']}</h4>
                    <p><strong>ID:</strong> {p['id']}</p>
                    <p><strong>Price:</strong> ${p['price']}</p>
                    <p><strong>Category:</strong> {p['category']}</p>
                    <p><strong>Description:</strong><br>{p['description']}</p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error fetching product: {e}")
    elif product_id:
        st.warning("⚠️ Please enter a valid number.")
