# brands/vspink.py
import streamlit as st
import pandas as pd
from utils.helpers import excel_to_bytes

def transform_vspink_data(df):
    df.columns = df.columns.str.strip().str.replace("\n"," ").str.replace("\r"," ")
    ex_col = [c for c in df.columns if "ex-mill" in c.lower()][0]
    qty_col = [c for c in df.columns if "qty" in c.lower()][0]
    article_col = [c for c in df.columns if "article" in c.lower()][0]

    metadata_cols = ["Customer","Supplier","Supplier COO","Production Plant (region)",
                     "Program","Construction",article_col,
                     "# of repeats in Article ( optional)","Composition",
                     "If Yarn Dyed/ Piece Dyed", ex_col]
    metadata_cols = [c for c in metadata_cols if c in df.columns]

    df["EX-mill_dt"] = pd.to_datetime(df[ex_col], errors="coerce")
    df["Month-Year"] = df["EX-mill_dt"].dt.strftime("%b-%y")

    df[qty_col] = pd.to_numeric(df[qty_col].astype(str).str.replace(",","").str.strip(), errors="coerce").fillna(0)
    grouped = df.groupby([article_col,"Month-Year"], as_index=False)[qty_col].sum()

    pivot_df = grouped.pivot_table(index=article_col, columns="Month-Year", values=qty_col, aggfunc="sum", fill_value=0).reset_index()
    parsed_months = pd.to_datetime(pivot_df.columns[1:], format="%b-%y", errors="coerce")
    month_order = parsed_months.sort_values().strftime("%b-%y").tolist()
    pivot_df = pivot_df[[article_col] + month_order]

    meta = df.groupby(article_col, as_index=False)[metadata_cols].first()
    final_df = pd.merge(meta, pivot_df, on=article_col, how="left")
    return final_df

def run_page():
    st.header("VSPINK — Brief → MCU")
    file = st.file_uploader("Upload VSPINK file", type=["xlsx","xls"], key="vspink_file")
    if file:
        df = pd.read_excel(file)
        df_out = transform_vspink_data(df)
        st.subheader("Preview — MCU")
        st.dataframe(df_out.head())
        out_bytes = excel_to_bytes(df_out, "VSPINK MCU")
        st.download_button("📥 Download VSPINK MCU", out_bytes, "vspink_mcu.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
