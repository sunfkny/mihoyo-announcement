import httpx


class Announcement:
    def __init__(self) -> None:
        self.client = httpx.Client()

    def request(self, url: str, params: dict | None = None) -> dict:
        response = self.client.get(url, params=params)
        response.raise_for_status()
        response_data: dict = response.json()
        retcode = response_data.get("retcode")
        if retcode != 0:
            raise ValueError(response_data.get("message") or response.text)
        return response_data


class Bh3Announcement(Announcement):
    def get_ann_list(self):
        response_data = self.request(
            "https://api-takumi.mihoyo.com/common/bh3_cn/announcement/api/getAnnList?auth_appid=announcement&authkey_ver=1&bundle_id=bh3_cn&channel_id=14&game=bh3&game_biz=bh3_cn&lang=zh-cn&level=88&platform=pc&region=bb01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=100000000",
        )
        from models.bh3.list import Model

        return Model.model_validate(response_data)


class Hk4eAnnouncement(Announcement):
    def get_ann_list(self):
        response_data = self.request(
            "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&from_cloud_web=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&uid=100000000",
        )
        from models.hk4e.list import Model

        return Model.model_validate(response_data)


class HkrpgAnnouncement(Announcement):
    def get_ann_list(self):
        response_data = self.request(
            "https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&platform=pc&region=prod_gf_cn&level=57&uid=100000000",
        )
        from models.hkrpg.list import Model

        return Model.model_validate(response_data)
