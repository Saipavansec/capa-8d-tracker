"""Streamlit KPI dashboard for the CAPA / 8D tracker."""

import pandas as pd
import streamlit as st

from capa_tracker import (capa_progress, get_connection, init_db, list_capas,
                          overdue_capas, pareto_root_causes)

st.set_page_config(page_title="CAPA / 8D Tracker", layout="wide")
st.title("CAPA / 8D Tracker")

conn = get_connection("capa.db")
init_db("capa.db")

capas = list_capas(conn)
df = pd.DataFrame(capas)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total CAPAs", len(df))
col2.metric("Open", len(df[df["status"] != "closed"]) if len(df) else 0)
col3.metric("Overdue", len(overdue_capas(conn)))
col4.metric("Closed", len(df[df["status"] == "closed"]) if len(df) else 0)

st.subheader("CAPA register")
if len(df):
    df["progress_%"] = df["id"].apply(lambda i: capa_progress(conn, i))
    st.dataframe(df[["id", "title", "severity", "status", "owner",
                     "due_date", "progress_%"]],
                 use_container_width=True)
else:
    st.info("No CAPAs yet — run `python examples/seed.py` to load samples.")

st.subheader("Pareto of root-cause categories")
pareto = pareto_root_causes(conn)
if pareto:
    pdf = pd.DataFrame(pareto, columns=["category", "count"])
    pdf["cum_pct"] = pdf["count"].cumsum() / pdf["count"].sum() * 100
    st.bar_chart(pdf.set_index("category")["count"])
    st.dataframe(pdf, use_container_width=True)
