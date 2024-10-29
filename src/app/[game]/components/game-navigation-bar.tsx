import {
  Bh3Announcement,
  Hk4eAnnouncement,
  HkrpgAnnouncement,
  NapAnnouncement,
} from "@/components/announcement";
import { cn } from "@/lib/utils";
import Link from "next/link";

export const games = ["bh3", "hk4e", "hkrpg", "nap"] as const;
export type Game = (typeof games)[number];
export function isGame(game: string): game is Game {
  return games.includes(game as Game);
}
const tabsMap: Record<Game, { name: string; component: React.ComponentType }> =
  {
    bh3: { name: "崩坏3", component: Bh3Announcement },
    hk4e: { name: "原神", component: Hk4eAnnouncement },
    hkrpg: { name: "崩坏：星穹铁道", component: HkrpgAnnouncement },
    nap: { name: "绝区零", component: NapAnnouncement },
  };
export const tabs = games.map((key) => {
  const game = tabsMap[key];
  return { key, name: game.name, component: game.component };
});
export function getAnnouncementComponent(game: Game): React.ComponentType {
  return tabsMap[game].component;
}

export function GameNavigationBar(params: { game: Game | string }) {
  return (
    <div className="max-w-[768px] w-full flex justify-center">
      <div className="flex">
        {tabs.map((tab) => (
          <Link key={tab.key} href={`/${tab.key}`}>
            <span
              className={cn("hover:bg-gray-100 rounded-md px-4 py-2", {
                "font-bold": tab.key === params.game,
              })}
            >
              {tab.name}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
