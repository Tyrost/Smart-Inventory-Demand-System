from threading import Thread
import time


def timed_first(session, table, id_type, result):
    try:
        item = session.query(table).filter_by(**id_type).first()
        result.append(item)
    except Exception as e:
        result.append(e)

def safe_first(session, table, id_type, timeout=5):
    result = []
    t = Thread(target=timed_first, args=(session, table, id_type, result))
    t.start()
    t.join(timeout)
    if t.is_alive():
        print(f"[WARNING] Query timed out after {timeout} seconds.")
        return None
    return result[0]