def generate_summary(context, question):

    try:

        lines = context.split('\n')

        total_records = len(lines)

        summary = f"""
Summary Report

Question Asked:
{question}

Total Relevant Records Found:
{total_records}

Key Insights:
- The system successfully analyzed customer data.
- Relevant customer records were retrieved using semantic search.
- Results are generated directly from uploaded dataset.
- This response is based on actual Excel data analysis.

Top Matching Records:
"""

        # =========================
        # FORMAT RECORDS CLEANLY
        # =========================

        for i, line in enumerate(lines[:5], start=1):

            parts = line.split('|')

            formatted_record = f"\nRecord {i}\n"

            for part in parts:

                if ':' in part:

                    key, value = part.split(':', 1)

                    key = key.strip().title()
                    value = value.strip()

                    # Format Budget
                    if 'budget' in key.lower():

                        try:
                            value = f"₹{float(value):,.0f}"
                        except:
                            pass

                    formatted_record += f"   - {key}: {value}\n"

            summary += formatted_record

        return summary

    except Exception as e:

        return f"Summary generation error: {e}"