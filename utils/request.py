import httpx

client = httpx.Client()
def request(url: str, params: dict | None = None) -> dict:
    response = client.get(url, params=params)
    response.raise_for_status()
    response_data: dict = response.json()
    retcode = response_data.get("retcode")
    if retcode != 0:
        raise ValueError(response_data.get("message") or response.text)
    return response_data
