import {
  Bh3Announcement,
  Hk4eAnnouncement,
  HkrpgAnnouncement,
  NapAnnouncement,
} from "@/components/announcement";

export const gameKeys = ["bh3", "hk4e", "hkrpg", "nap"] as const;
export type Game = (typeof gameKeys)[number];
export function isGame(game: string): game is Game {
  return gameKeys.includes(game as Game);
}
const gamesMap: Record<
  Game,
  { name: string; component: React.ComponentType; icon: string }
> = {
  bh3: {
    name: "崩坏3",
    component: Bh3Announcement,
    icon: "https://webstatic.mihoyo.com/upload/op-public/2021/10/03/4080f2eb748823d8c38507c3d7b69b36_936817768851375073.png",
  },
  hk4e: {
    name: "原神",
    component: Hk4eAnnouncement,
    icon: "https://webstatic.mihoyo.com/upload/op-public/2021/10/09/def1f2abcfc2af0bbe2e5900a60a5ee1_5699547505742166353.png",
  },
  hkrpg: {
    name: "崩坏：星穹铁道",
    component: HkrpgAnnouncement,
    icon: "https://webstatic.mihoyo.com/upload/op-public/2021/10/09/870472d6104dbbe7ea18b27c13763ccb_5300916022261002498.png",
  },
  nap: {
    name: "绝区零",
    component: NapAnnouncement,
    icon: "https://webstatic.mihoyo.com/upload/op-public/2022/05/27/3896559583929f643fbe39ec1d6ca1c9_1026345827445617861.png",
  },
};
export const games = gameKeys.map((key) => {
  const game = gamesMap[key];
  return { key, ...game };
});
export function getAnnouncementComponent(game: Game): React.ComponentType {
  return gamesMap[game].component;
}
export function getGameName(game: Game): string {
  return gamesMap[game].name;
}
export function getGame(game: Game | string) {
  if (isGame(game)) {
    return gamesMap[game];
  }
  return null;
}
