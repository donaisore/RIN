from delete_recent_pocket import (
    get_items,
    get_delete_items,
    delete_user_item
)


items = get_items()
delete_items = get_delete_items(items)
delete_user_item(delete_items)

print("done")
