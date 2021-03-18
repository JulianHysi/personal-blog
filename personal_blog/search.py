"""A module used to perform full-text search.

---

Functions
---------
add_to_index(index, model): return None
    create/update documents on the index
remove_from_index(index, model): return None
    delete document from the index
query_index(index, query, page, per_page): list(int), int
    search the index with the given query
"""

from flask import current_app


def add_to_index(index, model):
    """Create/update documents on the index.

    If elastic isn't set up or running, don't do anything.
    Else, add the document to the index, or update it.

    ---

    Parameters
    ----------
    index: elasticsearch index
        the name of the index to be updated
    model: instance of a database models classes
        the model instance record which was added/updated to main db

    Returns
    -------
    None
    """

    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Delete the document stored with the given id.

    If elastic isn't set up or running, don't do anything.
    Else, delete the document with the given id.

    ---

    Parameters
    ----------
    index: elasticsearch index
        the name of the index from which to remove
    model: instance of a database models classes
        the model instance record which was deleted from main db

    Returns
    -------
    None
    """

    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Search the given index with the given query.

    If elastic isn't set up or running, don't do anything.
    Else, search the given index with the given query.
    From the result set, make a list of post ids.
    Get the total of results (number of matches).

    ---

    Parameters
    ----------
    index: elasticsearch index
        the name of the index where the search should take place
    query: str
        the search expression/keywoard
    page: int
        the actual page of the paginated result set
    per_page: int
        the number of results per page

    Returns
    -------
    if elastic isn't running: [], -1
    if elastic is running: list of post ids, total
    """

    if not current_app.elasticsearch:
        return [], -1
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
