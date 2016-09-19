from h.api.search import query
from h.api import nipsa


def delete(request, params, private=True):
    """
    Delete with the given params and return the matching annotations.

    :param request: the request object
    :type request: pyramid.request.Request

    :param params: the search parameters
    :type params: dict-like

    :param private: whether or not to include private annotations in the search
        results
    :type private: bool

    :param separate_replies: Whether or not to include a "replies" key in the
        result containing a list of all replies to the annotations in the
        "rows" key. If this is True then the "rows" key will include only
        top-level annotations, not replies.
    :type private: bool

    :returns: A dict with keys:
      "rows" (the list of matching annotations, as dicts)
      "total" (the number of matching annotations, an int)
      "replies": (the list of all replies to the annotations in "rows", if
        separate_replies=True was passed)
    :rtype: dict
    """
    def make_builder():
        builder = query.Builder()
        builder.append_filter(query.AuthFilter(request, private=private))
        builder.append_filter(query.UriFilter())
        builder.append_filter(
            lambda _: nipsa.nipsa_filter(request.authenticated_userid))
        builder.append_filter(query.GroupFilter())
        builder.append_matcher(query.AnyMatcher())
        builder.append_matcher(query.TagsMatcher())
        return builder

    builder = make_builder()

    es = request.es
    results = es.conn.delete_by_query(index=es.index,
                                      doc_type=es.t.annotation,
                                      body=builder.build(params, sort=False))
