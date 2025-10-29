# app.py
import sys
import os
import streamlit as st
import importlib

# ----------------------------
# Fix import paths
# ----------------------------
sys.path.append(os.path.dirname(__file__))

# ----------------------------
# Utils import
# ----------------------------
from utils.helpers import excel_to_bytes

# ----------------------------
# Dynamic brand discovery
# ----------------------------
BRANDS_DIR = os.path.join(os.path.dirname(__file__), "brands")

def discover_brands():
    """Discover all brand pages in the brands folder"""
    brand_modules = []
    for f in os.listdir(BRANDS_DIR):
        if f.endswith(".py") and f != "__init__.py":
            brand_name = f[:-3]  # remove .py
            brand_modules.append(brand_name)
    return sorted(brand_modules)

# ----------------------------
# Load brand page dynamically
# ----------------------------
def load_brand_page(module_name):
    try:
        module = importlib.import_module(f"brands.{module_name}")
        return module
    except Exception as e:
        st.error(f"Failed to load brand module '{module_name}': {e}")
        return None

# ----------------------------
# Home page
# ----------------------------
def page_home():
    st.title("📦 MCU / PLM Projections Tool")
    st.markdown("""
    **Quick guide**
    - Upload Buy Sheet → PLM Upload → MCU format
    - Each brand has its own workflow
    - Do not change sheet names in uploaded files
    """)

# ----------------------------
# Sidebar navigation
# ----------------------------
brand_pages = discover_brands()
menu_options = ["Home"] + [b.replace("_", " ").title() for b in brand_pages]

page_choice = st.sidebar.radio("Choose page", menu_options)

# ----------------------------
# Render selected page
# ----------------------------
if page_choice == "Home":
    page_home()
else:
    # map selected title back to module name
    selected_module = page_choice.lower().replace(" ", "_")
    module = load_brand_page(selected_module)
    if module:
        # Each module must have a `run_page()` function
        if hasattr(module, "run_page"):
            module.run_page()
        else:
            st.error(f"Module '{selected_module}' has no function `run_page()`.")
