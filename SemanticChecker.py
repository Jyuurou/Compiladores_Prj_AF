
idList = []


def allocate_id_declared(id_name):
    idList.append(id_name)


def is_id_allocated(id_name):
    if id_name in idList:
        return True
    return False
