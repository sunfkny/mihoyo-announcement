import { Api } from "@/api";
import { Progress } from "@/components/ui/progress";
import { headers } from "next/headers";

export const revalidate = 60;

export async function Bh3Announcement() {
  const host = headers().get("host") || "localhost:8000";
  const scheme = headers().get("x-forwarded-proto") || "https";
  const api = new Api({ baseUrl: `${scheme}://${host}/` });
  const data = await api.api.apiBh3ApiBh3Get();
  return (
    <div>
      {data.data.progress.percent && (
        <div className="my-4">
          <Progress className="h-2" value={data.data.progress.percent * 100} />
          <span>{data.data.progress.text}</span>
        </div>
      )}
      {!data.data.progress.percent && (
        <div className="my-4">
          <Progress className="h-2" value={0} />
          <span>{data.data.progress.text || "获取版本信息失败"}</span>
        </div>
      )}

      {data.data.gacha_info.map((item) => (
        <div key={item.ann_id}>
          <img src={item.image} alt={item.title} />
          <p>{item.title}</p>
          {item.info_html && (
            <div dangerouslySetInnerHTML={{ __html: item.info_html }} />
          )}
        </div>
      ))}
    </div>
  );
}
