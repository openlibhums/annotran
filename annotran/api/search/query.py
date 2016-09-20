from h.api.search import query as hq


def build(self, params, sort=True):
    """
    Get the resulting query object from this query builder.
    :param self: an instance of a query object
    :param params: a set of parameters to pass to a query
    :param sort: whether or not to include sort and other keys that pertain only to a search query
    :return:
    """
    params = params.copy()

    p_from = hq.extract_offset(params)
    p_size = hq.extract_limit(params)
    p_sort = hq.extract_sort(params)

    filters = [f(params) for f in self.filters]
    matchers = [m(params) for m in self.matchers]
    filters = [f for f in filters if f is not None]
    matchers = [m for m in matchers if m is not None]

    # Remaining parameters are added as straightforward key-value matchers
    for key, value in params.items():
        matchers.append({"match": {key: value}})

    query = {"match_all": {}}

    if matchers:
        query = {"bool": {"must": matchers}}

    if filters:
        query = {
            "filtered": {
                "filter": {"and": filters},
                "query": query,
            }
        }

    ret = {
        "query": query,
    }

    if sort:
        ret["from"] = p_from
        ret["sort"] = p_sort
        ret["size"] = p_size

    return ret
