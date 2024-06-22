# example/st_app_gsheets_using_service_account.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

#st.title("Read Google Sheet as DataFrame")

#conn = st.connection("gsheets", type=GSheetsConnection)
#df = conn.read(worksheet="Sheet2",usecols=[0,1,2])

#st.dataframe(df)

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# تنظیمات اولیه
st.title("Google Sheet CRUD Operations")

# اتصال به Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها از Google Sheet
df = conn.read(worksheet="Sheet2", usecols=[0, 1, 2])
df.columns = ["Column1", "Column2", "Column3"]  # تنظیم نام ستون‌ها به صورت دستی

# نمایش داده‌ها
st.subheader("Current Data")
st.dataframe(df)

# عملیات CREATE
st.subheader("Add New Entry")
with st.form("add_form"):
    new_data = {
        "Column1": st.text_input("Column1"),
        "Column2": st.text_input("Column2"),
        "Column3": st.text_input("Column3")
    }
    submitted = st.form_submit_button("Add")
    if submitted:
        conn.write(new_data, worksheet="Sheet2", append=True)
        st.success("New entry added successfully.")

# عملیات UPDATE
st.subheader("Update Entry")
with st.form("update_form"):
    index_to_update = st.number_input("Row index to update", min_value=0, max_value=len(df)-1, step=1)
    updated_data = {
        "Column1": st.text_input("Column1", value=df.at[index_to_update, "Column1"]),
        "Column2": st.text_input("Column2", value=df.at[index_to_update, "Column2"]),
        "Column3": st.text_input("Column3", value=df.at[index_to_update, "Column3"])
    }
    update_submitted = st.form_submit_button("Update")
    if update_submitted:
        conn.update(index_to_update, updated_data, worksheet="Sheet2")
        st.success("Entry updated successfully.")

# عملیات DELETE
st.subheader("Delete Entry")
with st.form("delete_form"):
    index_to_delete = st.number_input("Row index to delete", min_value=0, max_value=len(df)-1, step=1)
    delete_submitted = st.form_submit_button("Delete")
    if delete_submitted:
        conn.delete(index_to_delete, worksheet="Sheet2")
        st.success("Entry deleted successfully.")

# به‌روزرسانی داده‌ها بعد از عملیات CRUD
if submitted or update_submitted or delete_submitted:
    df = conn.read(worksheet="Sheet2", usecols=[0, 1, 2])
    df.columns = ["Column1", "Column2", "Column3"]  # تنظیم نام ستون‌ها به صورت دستی
    st.dataframe(df)

