from pymongo.client_session import ClientSession
from pymongo.collection import Collection


def load(host: dict, collection: Collection, session: ClientSession) -> None:
    """
    load takes a host dict, mongodb collection, and mongodb client session and performs an update
    with upsert in the session to attempt to maintain db consistency across workers.
    """

    # filter on the combination of kind and kind_id in case there's a collision between kinds
    update_filter = {"kind": host["kind"], "kind_id": host["kind_id"]}
    # since we omit the unset fields when returning the values from,
    # it's safe to push the entire object up
    update = {"$set": host}

    # using upsert allows the update to create the object if it doesn't already exist
    collection.update_one(update_filter, update, upsert=True, session=session)
