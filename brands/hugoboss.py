# brands/hugoboss.py
import streamlit as st
import pandas as pd
from utils.helpers import excel_to_bytes

def transform_hugoboss_buy_to_plm(df):
    df.columns = df.columns.str.strip()
    material_idx = df.columns.get_loc("Material Number")
    month_cols = df.columns[material_idx+1:]
    return df[["Material Number"] + list(month_cols)]

def transform_hugoboss_plm_to_mcu(df):
    df.columns = df.columns.str.strip()
    mask_keep = ~df.columns.str.lower().str.startswith("sum")
    return df.loc[:, mask_keep]

def run_page():
    st.header("Hugo Boss — Buy Sheet → PLM Download")
    buy_file = st.file_uploader("Upload Buy Sheet (HugoBoss)", type=["xlsx","xls"], key="hb_buy")
    if buy_file:
        df = pd.read_excel(buy_file)
        df_out = transform_hugoboss_buy_to_plm(df)
        st.subheader("Preview — PLM Download")
        st.dataframe(df_out.head())
        out_bytes = excel_to_bytes(df_out, "PLM Download")
        st.download_button("📥 Download PLM Download", out_bytes, "plm_download_hugoboss.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("---")
    st.header("Hugo Boss — PLM Upload → MCU")
    plm_file = st.file_uploader("Upload PLM Upload file (HugoBoss)", type=["xlsx","xls"], key="hb_plm")
    if plm_file:
        df = pd.read_excel(plm_file)
        df_out = transform_hugoboss_plm_to_mcu(df)
        st.subheader("Preview — MCU")
        st.dataframe(df_out.head())
        out_bytes = excel_to_bytes(df_out, "MCU")
        st.download_button("📥 Download MCU", out_bytes, "MCU_hugoboss.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
