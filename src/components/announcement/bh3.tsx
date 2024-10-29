import { Progress } from "@/components/ui/progress";
import { getBh3Info } from "@/service/bh3";

export async function Bh3Announcement() {
  const data = await getBh3Info();
  return (
    <div>
      {data.progress.percent && (
        <div className="my-4">
          <Progress className="h-2" value={data.progress.percent * 100} />
          <span>{data.progress.text}</span>
        </div>
      )}
      {!data.progress.percent && (
        <div className="my-4">
          <Progress className="h-2" value={0} />
          <span>{data.progress.text || "获取版本信息失败"}</span>
        </div>
      )}

      {data.gacha_info.map((item) => (
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
