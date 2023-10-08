from fastapi.params import Query

from server_params.common_entities import Paginator


def get_paginator(limit: int = Query(12, title="Records amount", description="The number of records on the page"),
                  page: int = Query(1, title="Page number", description="Which page we are at"),):
    return Paginator(limit=limit, page=page)
