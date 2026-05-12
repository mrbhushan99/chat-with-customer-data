import pandas as pd
import re


def process_query(df, query):

    query = query.lower()

    try:

        filtered_df = df.copy()

        # =========================
        # FIND IMPORTANT COLUMNS
        # =========================

        budget_col = find_column(
            df,
            ['budget', 'price', 'amount']
        )

        location_col = find_column(
            df,
            ['location', 'city', 'area']
        )

        property_col = find_column(
            df,
            ['property', 'bhk', 'type']
        )

        status_col = find_column(
            df,
            ['status', 'intent', 'lead']
        )

        possession_col = find_column(
            df,
            ['possession']
        )

        call_status_col = find_column(
            df,
            ['call status', 'last call']
        )

        # =========================
        # PROPERTY FILTER
        # =========================

        bhk_match = re.search(r'(\d+)\s*bhk', query)

        if bhk_match:

            bhk = bhk_match.group(1)

            filtered_df = filtered_df[
                filtered_df[property_col]
                .astype(str)
                .str.lower()
                .str.contains(bhk, na=False)
            ]

        # =========================
        # DYNAMIC LOCATION FILTER
        # =========================

        all_locations = (
            df[location_col]
            .dropna()
            .astype(str)
            .str.lower()
            .unique()
        )

        for location in all_locations:

            if location in query:

                filtered_df = filtered_df[
                    filtered_df[location_col]
                    .astype(str)
                    .str.lower()
                    .str.contains(location, na=False)
                ]

                break

        # =========================
        # CALL STATUS FILTER
        # =========================

        all_statuses = (
            df[call_status_col]
            .dropna()
            .astype(str)
            .str.lower()
            .str.strip()
            .unique()
        )

        for status in all_statuses:

            if status in query:

                filtered_df = filtered_df[
                    filtered_df[call_status_col]
                    .astype(str)
                    .str.lower()
                    .str.strip() == status
                ]

                break

        # =========================
        # HIGH INTENT FILTER
        # =========================

        if any(word in query for word in [
            'high intent',
            'high potential',
            'hot lead',
            'premium'
        ]):

            filtered_df = filtered_df[
                filtered_df[status_col]
                .astype(str)
                .str.lower()
                .str.contains(
                    'high|hot|premium',
                    regex=True,
                    na=False
                )
            ]

        # =========================
        # POSSESSION FILTER
        # =========================

        if any(word in query for word in [
            'ready possession',
            'immediate possession'
        ]):

            filtered_df = filtered_df[
                filtered_df[possession_col]
                .astype(str)
                .str.lower()
                .str.contains(
                    'ready|immediate',
                    regex=True,
                    na=False
                )
            ]

        # =========================
        # POSSESSION YEAR FILTER
        # =========================

        year_match = re.search(r'20\d{2}', query)

        if year_match:

            year = year_match.group(0)

            filtered_df = filtered_df[
                filtered_df[possession_col]
                .astype(str)
                .str.contains(year, na=False)
            ]

        # =========================
        # BUDGET FILTER
        # =========================

        if any(word in query for word in [
            'budget',
            'price',
            'cost',
            'amount'
        ]):

            numbers = re.findall(r'\d+\.?\d*', query)

            if numbers:

                value = float(numbers[0])

                # Crore
                if any(word in query for word in [
                    'crore',
                    'crores',
                    'cr'
                ]):

                    value = value * 10000000

                # Lakh
                elif any(word in query for word in [
                    'lakh',
                    'lakhs',
                    'lac'
                ]):

                    value = value * 100000

                # Above
                if any(word in query for word in [
                    'above',
                    'over',
                    'greater',
                    'more'
                ]):

                    filtered_df = filtered_df[
                        filtered_df[budget_col] > value
                    ]

                # Below
                elif any(word in query for word in [
                    'below',
                    'under',
                    'less'
                ]):

                    filtered_df = filtered_df[
                        filtered_df[budget_col] < value
                    ]

        # =========================
        # HIGHEST BUDGET
        # =========================

        if any(word in query for word in [
            'highest budget',
            'max budget',
            'maximum budget',
            'top budget',
            'most expensive'
        ]):

            highest_row = filtered_df.loc[
                filtered_df[budget_col].idxmax()
            ]

            return {
                'answer': (
                    f"Customer with highest budget: "
                    f"{highest_row['name']} "
                    f"(₹{highest_row[budget_col]:,.0f})"
                ),
                'data': pd.DataFrame([highest_row])
            }

        # =========================
        # LOWEST BUDGET
        # =========================

        if any(word in query for word in [
            'lowest budget',
            'minimum budget',
            'least budget',
            'cheapest'
        ]):

            lowest_row = filtered_df.loc[
                filtered_df[budget_col].idxmin()
            ]

            return {
                'answer': (
                    f"Customer with lowest budget: "
                    f"{lowest_row['name']} "
                    f"(₹{lowest_row[budget_col]:,.0f})"
                ),
                'data': pd.DataFrame([lowest_row])
            }

        # =========================
        # COUNT QUERY
        # =========================

        if any(word in query for word in [
            'how many',
            'count',
            'total'
        ]):

            return {
                'answer': f'Total matching customers: {len(filtered_df)}',
                'data': filtered_df
            }

        # =========================
        # AVERAGE QUERY
        # =========================

        if any(word in query for word in [
            'average',
            'avg',
            'mean'
        ]):

            avg = filtered_df[budget_col].mean()

            return {
                'answer': f'Average Budget: ₹{avg:,.2f}',
                'data': filtered_df
            }

        # =========================
        # SHOW/LIST/FIND QUERY
        # =========================

        if any(word in query for word in [
            'show',
            'list',
            'find',
            'display',
            'customers',
            'clients'
        ]):

            return {
                'answer': f'Found {len(filtered_df)} matching customers.',
                'data': filtered_df
            }

        # =========================
        # DEFAULT RESPONSE
        # =========================

        return {
            'answer': f'Found {len(filtered_df)} matching customers.',
            'data': filtered_df
        }

    except Exception as e:

        return {
            'answer': f'Error processing query: {e}',
            'data': pd.DataFrame()
        }


# ======================================
# HELPER FUNCTION
# ======================================

def find_column(df, keywords):

    for col in df.columns:

        for keyword in keywords:

            if keyword.lower() in col.lower():

                return col

    return df.columns[0]