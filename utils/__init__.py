import math

from utils.exceptions import ResponseException
from utils.config import SECRET_KEY, ITEMS_ON_PER_PAGE, STORAGE_PATH, STORAGE_DIRECTORIES
from utils.database import SessionLocal


def make_response(payload=None, status='success', status_code=200, result=0):
    return {
        'status': status,
        'payload': payload,
        'result': result,
    }, status_code


def orm_to_dict(orm, keys, additional_fields=None):
    if orm is None:
        return None
    if 'id' not in keys:
        keys += ['id']
    if additional_fields is None:
        additional_fields = {}
    if isinstance(orm, list):
        items = []
        for i in orm:
            d = {}
            for j in keys:
                d[j] = getattr(i, j)
            for j in additional_fields.keys():
                d[j] = additional_fields[j](i)
            items.append(d)
        return items

    resp = {k: getattr(orm, k) for k in keys}

    for j in additional_fields.keys():
        resp[j] = additional_fields[j](orm)

    return resp


def apply_paging(query, page=1):
    return query.limit(ITEMS_ON_PER_PAGE).offset((page - 1) * ITEMS_ON_PER_PAGE)


def orm_list_with_pages(render, query, page=1):
    try:
        page = int(page)
        assert page > 0
    except (TypeError, ValueError, AssertionError) as e:
        page = 1
    items = apply_paging(query, page=page)
    total = query.count()
    return {
        'current_page': page,
        'page_size': ITEMS_ON_PER_PAGE,
        'total_pages': int(math.ceil(total / float(ITEMS_ON_PER_PAGE))),
        'list': render(items),
        'total': query.count(),
    }
