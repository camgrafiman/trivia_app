#  Paginate function:
def paginate(request, selection, quantity):
    # Here, the pagination is done by getting the ?page=2 (value), 1 is set as default, and expects an integer :)
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * quantity
    end = start + quantity

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def hasNextPage(page, request, restant_pages):
    # print("page: " + str(page))
    # print("total_pages: " + str(total_pages))
    if restant_pages < page:
        nextpage = request.args.get('page', 1, type=int) + 1
        return str(request.url_root + 'questions?page=') + str(nextpage)
    else:
        return str(request.url_root + 'questions?page=1')
