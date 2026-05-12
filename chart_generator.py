import plotly.express as px



def generate_chart(df, query):

    query = query.lower()

    try:

        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_cols) == 0:
            return None

        if 'histogram' in query or 'distribution' in query:

            fig = px.histogram(
                df,
                x=numeric_cols[0],
                title='Distribution Chart'
            )

            fig.update_layout(
                title='Distribution Chart'
            )

            return fig

        if 'pie' in query:

            category_col = df.select_dtypes(include=['object']).columns[0]

            fig = px.pie(
                df,
                names=category_col,
                title='Pie Chart'
            )

            return fig

        if 'bar' in query:

            category_col = df.select_dtypes(include=['object']).columns[0]

            fig = px.bar(
                df,
                x=category_col,
                y=numeric_cols[0],
                title='Bar Chart'
            )

            return fig

        fig = px.histogram(
            df,
            x=numeric_cols[0],
            title='Auto Generated Chart'
        )

        return fig

    except Exception as e:
        print(e)
        return None