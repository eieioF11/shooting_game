
first=True
save_id=0
def identification(id):
    if first:
        save_id=id
        first=False
        return True
    if id==save_id:
        return True
    return False