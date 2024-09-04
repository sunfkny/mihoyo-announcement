import arrow


def get_tzinfo(timezone: int):
    return arrow.get(tzinfo=f"UTC{timezone:+03d}").tzinfo
