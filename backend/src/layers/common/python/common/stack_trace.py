import traceback


def get_stack_trace(limit: int = 10) -> str:
    return traceback.format_exc(limit=limit)
