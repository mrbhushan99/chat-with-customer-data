import re


def classify_intent(query):
    query = query.lower()

    if any(word in query for word in ['chart', 'plot', 'graph', 'visualize']):
        return 'chart'

    if any(word in query for word in ['average', 'mean']):
        return 'average'

    if any(word in query for word in ['count', 'how many', 'total']):
        return 'count'

    if any(word in query for word in ['summary', 'summarize', 'overview']):
        return 'summary'

    if any(word in query for word in ['find', 'show', 'list']):
        return 'filter'

    return 'semantic'