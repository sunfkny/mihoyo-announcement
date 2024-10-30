import { getTime, getTimeHumaize } from "./utils";

interface NapGachaInfo {
  ann_id: number;
  title: string;
  image: string;
  content: string;
  start_time: string;
  end_time: string;
}

interface NapProgress {
  text?: string | null;
  percent?: number | null;
}

interface NapResponse {
  progress: NapProgress;
  gacha_info: NapGachaInfo[];
}

interface AnnContentResponse {
  retcode: number;
  message: string;
  data: {
    list: {
      ann_id: number;
      title: string;
      subtitle: string;
      banner: string;
      content: string;
      lang: string;
    }[];
    pic_list: unknown[];
    total: number;
    pic_total: number;
  };
}

interface AnnListResponse {
  retcode: number;
  message: string;
  data: {
    list: {
      list: {
        ann_id: number;
        title: string;
        subtitle: string;
        banner: string;
        content: string;
        type_label: string;
        tag_label: string;
        tag_icon: string;
        login_alert: number;
        lang: string;
        start_time: string;
        end_time: string;
        type: number;
        remind: number;
        alert: number;
        tag_start_time: string;
        tag_end_time: string;
        remind_ver: number;
        has_content: boolean;
        extra_remind: number;
        tag_icon_hover: string;
      }[];
      type_id: number;
      type_label: string;
    }[];
    total: number;
    type_list: {
      id: number;
      name: string;
      mi18n_name: string;
    }[];
    alert: boolean;
    alert_id: number;
    timezone: number;
    t: string;
    pic_list: unknown[];
    pic_total: number;
    pic_type_list: unknown[];
    pic_alert: boolean;
    pic_alert_id: number;
    static_sign: string;
  };
}

async function getAnnList(): Promise<AnnListResponse> {
  const response = await fetch(
    "https://announcement-api.mihoyo.com/common/nap_cn/announcement/api/getAnnList?" +
      new URLSearchParams({
        game: "nap",
        game_biz: "nap_cn",
        lang: "zh-cn",
        bundle_id: "nap_cn",
        platform: "pc",
        region: "prod_gf_cn",
        level: "40",
        channel_id: "1",
        uid: "10000000",
      }).toString()
  );
  if (response.status !== 200) {
    throw new Error(`Fail to get ann list ${response.status}`);
  }
  if (
    response.headers.get("Content-Type")?.includes("application/json") === false
  ) {
    throw new Error(
      `Fail to get ann list ${response.headers.get("Content-Type")}`
    );
  }
  return await response.json();
}

function getVersionInfoFromAnnList(
  annList: Awaited<ReturnType<typeof getAnnList>>
):
  | {
      start_time: string;
      end_time: string;
    }
  | undefined {
  for (const lst of annList.data.list) {
    for (const i of lst.list) {
      if (
        i.title.includes("已知问题及游戏优化说明") ||
        i.subtitle.includes("版本更新说明")
      ) {
        return i;
      }
    }
  }
}

async function getAnnContent(): Promise<AnnContentResponse> {
  const response = await fetch(
    "https://announcement-api.mihoyo.com/common/nap_cn/announcement/api/getAnnContent?" +
      new URLSearchParams({
        game: "nap",
        game_biz: "nap_cn",
        lang: "zh-cn",
        bundle_id: "nap_cn",
        platform: "pc",
        region: "prod_gf_cn",
        level: "40",
        channel_id: "1",
        uid: "10000000",
      }).toString()
  );
  if (response.status !== 200) {
    throw new Error(`Fail to get ann content ${response.status}`);
  }
  if (
    response.headers.get("Content-Type")?.includes("application/json") === false
  ) {
    throw new Error(
      `Fail to get ann list ${response.headers.get("Content-Type")}`
    );
  }
  return await response.json();
}

function getGachaInfoFromAnnContent(
  annContent: Awaited<ReturnType<typeof getAnnContent>>
): {
  content: string;
  ann_id: number;
  title: string;
  image: string;
}[] {
  return annContent.data.list
    .filter((i) => i.subtitle.includes("调频"))
    .map((i) => {
      return {
        content: i.content,
        ann_id: i.ann_id,
        title: i.subtitle,
        image: i.banner,
      };
    });
}

export async function getNapInfo(): Promise<NapResponse> {
  const [annList, annContent] = await Promise.all([
    getAnnList(),
    getAnnContent(),
  ]);

  const versionInfo = getVersionInfoFromAnnList(annList);
  let progressPercent: number | null = null;
  let progressText: string | null = null;
  const gachaInfo: NapGachaInfo[] = [];

  if (versionInfo) {
    const startTime = getTime(versionInfo.start_time);
    const endTime = getTime(versionInfo.end_time);
    const currentTime = getTime();
    if (currentTime.isBetween(startTime, endTime)) {
      progressPercent = currentTime.diff(startTime) / endTime.diff(startTime);
      const durationString = getTimeHumaize(endTime);
      progressText = `${startTime.format(
        "YYYY-MM-DD HH:mm:ss"
      )} ~ ${endTime.format("YYYY-MM-DD HH:mm:ss")} （${durationString}结束）`;
    }
  }

  getGachaInfoFromAnnContent(annContent).forEach((i) => {
    let start_time: string = "";
    let end_time: string = "";
    const t =
      /(?:([0-9]+\.[0-9]版本更新后)|(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)).*?(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)/.exec(
        i.content
      );
    const groups = Array.from(t || []).slice(1) || [];
    if (groups[0] && groups[2]) {
      start_time = groups[0];
      const end = getTime(groups[2]);
      end_time = `${end.format("YYYY-MM-DD HH:mm:ss")} （${getTimeHumaize(
        end
      )}）`;
    }

    if (groups[1] && groups[2]) {
      const start = getTime(groups[1]);
      const end = getTime(groups[2]);
      start_time = `${start.format(
        "YYYY-MM-DD HH:mm:ss"
      )} （${getTimeHumaize(start)}）`;
      end_time = `${end.format("YYYY-MM-DD HH:mm:ss")} （${getTimeHumaize(
        end
      )}）`;
    }

    gachaInfo.push({
      ann_id: i.ann_id,
      title: i.title,
      image: i.image,
      content: i.content,
      start_time: start_time,
      end_time: end_time,
    });
  });

  return {
    progress: {
      percent: progressPercent,
      text: progressText,
    },
    gacha_info: gachaInfo,
  };
}
