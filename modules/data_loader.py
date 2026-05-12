import pandas as pd
import streamlit as st
import re


@st.cache_data
def load_file(uploaded_file):

    try:

        # =========================
        # LOAD FILE
        # =========================

        if uploaded_file.name.endswith('.csv'):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(
                uploaded_file,
                engine='openpyxl'
            )

        # =========================
        # CLEAN COLUMN NAMES
        # =========================

        df.columns = (
            df.columns
            .str.lower()
            .str.strip()
        )

        # =========================
        # FIND BUDGET COLUMN
        # =========================

        budget_col = None

        for col in df.columns:

            if any(word in col.lower() for word in [
                'budget',
                'price',
                'amount',
                'cost'
            ]):

                budget_col = col
                break

        # =========================
        # CONVERT BUDGET COLUMN
        # =========================

        if budget_col:

            df[budget_col] = df[budget_col].apply(
                clean_budget
            )

        return df

    except Exception as e:

        st.error(f'Error loading file: {e}')

        return None


# ======================================
# CLEAN BUDGET VALUES
# ======================================

def clean_budget(value):

    try:

        # =========================
        # HANDLE NULLS
        # =========================

        if pd.isna(value):
            return 0

        # =========================
        # IF ALREADY NUMBER
        # =========================

        if isinstance(value, (int, float)):

            return float(value)

        # =========================
        # CONVERT TO STRING
        # =========================

        value = str(value).lower()

        value = value.replace('₹', '')
        value = value.replace(',', '')
        value = value.strip()

        # =========================
        # HANDLE CRORE
        # =========================

        if 'crore' in value or 'cr' in value:

            number = re.findall(r'\\d+\\.?\\d*', value)

            if number:

                return float(number[0]) * 10000000

        # =========================
        # HANDLE LAKH
        # =========================

        elif 'lakh' in value or 'lakhs' in value or 'lac' in value:

            number = re.findall(r'\\d+\\.?\\d*', value)

            if number:

                return float(number[0]) * 100000

        # =========================
        # HANDLE NORMAL NUMBERS
        # =========================

        else:

            return float(value)

    except:

        return 0