from validator_collection import checkers


def is_http_url(url: str) -> bool:
    return checkers.is_url(url)
