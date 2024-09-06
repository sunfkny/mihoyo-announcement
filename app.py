from fastapi import FastAPI

from api.service.bh3 import Bh3Response, get_bh3_gacha_info
from api.service.hk4e import Hk4eResponse, get_hk4e_gacha_info
from api.service.hkrpg import HkrpgResponse, get_hkrpg_gacha_info
from api.service.nap import NapResponse, get_nap_gacha_info

app = FastAPI(docs_url="/api/docs")


@app.get("/api/bh3")
async def api_bh3() -> Bh3Response:
    return await get_bh3_gacha_info()


@app.get("/api/hk4e")
async def api_hk4e() -> Hk4eResponse:
    return await get_hk4e_gacha_info()


@app.get("/api/hkrpg")
async def api_hkrpg() -> HkrpgResponse:
    return await get_hkrpg_gacha_info()


@app.get("/api/nap")
async def api_nap() -> NapResponse:
    return await get_nap_gacha_info()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{__name__}:app", host="127.0.0.1", port=8000, reload=True)
