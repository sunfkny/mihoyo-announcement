import { Progress } from "@/components/ui/progress";
import { getNapInfo } from "@/service/nap";

export async function NapAnnouncement() {
  const data = await getNapInfo();
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
          <p>开始时间：{item.start_time}</p>
          <p>结束时间：{item.end_time}</p>
        </div>
      ))}
    </div>
  );
}
