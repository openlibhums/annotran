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

    :returns: A dict with keys:
      "rows" (the list of matching annotations, as dicts)
      "total" (the number of matching annotations, an int)
      "replies": (the list of all replies to the annotations in "rows", if
        separate_replies=True was passed)
    :rtype: dict
    """
    def make_builder():
        builder_output = query.Builder()
        builder_output.append_filter(query.AuthFilter(request, private=private))
        builder_output.append_filter(query.UriFilter())
        builder_output.append_filter(lambda _: nipsa.nipsa_filter(request.authenticated_userid))
        builder_output.append_filter(query.GroupFilter())
        builder_output.append_matcher(query.AnyMatcher())
        builder_output.append_matcher(query.TagsMatcher())

        return builder_output

    builder = make_builder()

    es = request.es

    # N.B.: this function _does_ take a sort argument because hypothesis's version of the function is monkey-patched
    # to point to the version in query.py while still retaining the rest of the class
    es.conn.delete_by_query(index=es.index, doc_type=es.t.annotation, body=builder.build(params, sort=False))
