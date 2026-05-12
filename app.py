import streamlit as st
import pandas as pd

from modules.data_loader import load_file
from modules.intent_classifier import classify_intent
from modules.query_engine import process_query
from modules.rag_engine import RAGEngine
from modules.summarizer import generate_summary
from modules.chart_generator import generate_chart
from modules.utils import dataset_summary


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title='Chat with Customer Data',
    layout='wide'
)


# =========================
# TITLE
# =========================

st.title('Chat with Customer Data using RAG and Gemini')


# =========================
# SESSION STATE
# =========================

if 'history' not in st.session_state:
    st.session_state.history = []


# =========================
# SIDEBAR FILE UPLOAD
# =========================

uploaded_file = st.sidebar.file_uploader(
    'Upload Excel or CSV File',
    type=['xlsx', 'csv']
)


# =========================
# MAIN APP
# =========================

if uploaded_file:

    # Load Data
    df = load_file(uploaded_file)

    if df is not None:

        # Dataset Summary
        summary = dataset_summary(df)

        st.sidebar.success('File Loaded Successfully')

        st.sidebar.write(f"Rows: {summary['rows']}")
        st.sidebar.write(f"Columns: {summary['columns']}")
        st.sidebar.write(f"Missing Values: {summary['missing_values']}")

        # =========================
        # TOP NAVIGATION
        # =========================

        st.markdown("## Navigation")

        page = st.radio(
            "",
            [
                "Dataset Preview",
                "Chat",
                "Analytics"
            ],
            horizontal=True
        )

        # =========================
        # DATASET PREVIEW PAGE
        # =========================

        if page == "Dataset Preview":

            st.subheader('Dataset Preview')

            st.dataframe(
                df.head(20),
                use_container_width=True
            )

            st.subheader('Columns')

            st.write(df.columns.tolist())

            st.subheader('Data Types')

            st.write(df.dtypes)

        # =========================
        # CHAT PAGE
        # =========================

        elif page == "Chat":

            st.subheader('Ask Questions About Your Data')

            query = st.text_input(
                'Enter your question',
                placeholder='How many customers have budget above 90 lakhs?'
            )

            if st.button('Submit Query'):

                if query.strip() != '':

                    try:

                        # =========================
                        # DETECT INTENT
                        # =========================

                        intent = classify_intent(query)

                        st.write(f'Intent Detected: {intent}')

                        # =========================
                        # PROCESS QUERY
                        # =========================

                        result = process_query(df, query)

                        st.success(result['answer'])

                        # =========================
                        # SHOW TABLE
                        # =========================

                        if not result['data'].empty:

                            st.dataframe(
                                result['data'],
                                use_container_width=True
                            )

                            # =========================
                            # RAG SEARCH
                            # =========================

                            rag = RAGEngine()

                            rag.create_embeddings(df)

                            rag_results = rag.search(query)

                            rag_context = '\n'.join(rag_results)

                            # =========================
                            # AI SUMMARY
                            # =========================

                            summary = generate_summary(
                                rag_context,
                                query
                            )

                            st.subheader('AI Summary')

                            st.write(summary)

                        else:

                            st.warning(
                                'No matching records found for this query.'
                            )

                        # =========================
                        # SAVE QUERY HISTORY
                        # =========================

                        st.session_state.history.append(query)

                    except Exception as e:

                        st.error(f'Error: {e}')

            # =========================
            # QUERY HISTORY
            # =========================

            if len(st.session_state.history) > 0:

                st.subheader('Query History')

                for item in st.session_state.history:

                    st.write('-', item)

        # =========================
        # ANALYTICS PAGE
        # =========================

        elif page == "Analytics":

            st.subheader('Analytics & Charts')

            chart_query = st.text_input(
                'Enter chart request',
                placeholder='Show budget distribution chart'
            )

            if st.button('Generate Chart'):

                try:

                    fig = generate_chart(df, chart_query)

                    if fig is not None:

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    else:

                        st.error('Could not generate chart.')

                except Exception as e:

                    st.error(f'Chart Error: {e}')

else:

    st.info('Please upload a file to continue.')