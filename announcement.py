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
    def get_list(self):
        response_data = self.request(
            "https://api-takumi.mihoyo.com/common/bh3_cn/announcement/api/getAnnList?auth_appid=announcement&authkey_ver=1&bundle_id=bh3_cn&channel_id=14&game=bh3&game_biz=bh3_cn&lang=zh-cn&level=88&platform=pc&region=bb01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=100000000",
        )
        from models.bh3.list import Model

        return Model.model_validate(response_data)

    def get_version_info(self):
        data = self.get_list()
        for lst in data.data.list:
            for i in lst.list:
                if "游戏更新内容问题修复及优化说明" in i.title:
                    return i

    def get_gacha_info(self):
        for i in self.get_list().data.list:
            for j in i.list:
                if j.title.split("丨").pop(0).endswith("补给"):
                    yield j


class Hk4eAnnouncement(Announcement):
    def get_list(self):
        response_data = self.request(
            "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&from_cloud_web=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&uid=100000000",
        )
        from models.hk4e.list import Model

        return Model.model_validate(response_data)

    def get_version_info(self):
        data = self.get_list()
        for lst in data.data.list:
            for i in lst.list:
                if "游戏更新修复与优化说明" in i.title:
                    return i

    def get_gacha_info(self):
        for i in self.get_list().data.list:
            for j in i.list:
                if j.subtitle.endswith("祈愿"):
                    yield j


class HkrpgAnnouncement(Announcement):
    def get_list(self):
        response_data = self.request(
            "https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&platform=pc&region=prod_gf_cn&level=57&uid=100000000",
        )
        from models.hkrpg.list import Model

        return Model.model_validate(response_data)

    def get_version_info(self):
        data = self.get_list()
        for lst in data.data.list:
            for i in lst.list:
                if "游戏优化及已知问题说明" in i.title:
                    return i

    def get_gacha_info(self):
        for i in self.get_list().data.pic_list:
            for j in i.type_list[0].list:
                if j.title.split("：").pop(0).endswith("跃迁"):
                    yield j
