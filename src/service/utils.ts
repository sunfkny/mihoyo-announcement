import dayjs from "dayjs";
import { Temporal } from "temporal-polyfill";

export function getTimeHumaize(time: dayjs.Dayjs | Date) {
  const endTimeNanosecond = BigInt(time.valueOf()) * BigInt(1000000);
  const endTimeTemporal = new Temporal.ZonedDateTime(
    endTimeNanosecond,
    process.env.TZ || "Asia/Shanghai",
  );
  const nowTemporal = Temporal.Now.zonedDateTimeISO();
  // 现在减去结束时间
  const duration = nowTemporal
    .until(endTimeTemporal)
    .round({ largestUnit: "days" });
  // 结果为正数表示结束时间在未来，负数表示结束时间在过去
  const durationSuffix = duration.sign === 1 ? "后" : "前";
  const durationString = `${Math.abs(duration.days)}天${Math.abs(duration.hours)}小时${Math.abs(duration.minutes)}分钟${durationSuffix}`;
  return durationString;
}
