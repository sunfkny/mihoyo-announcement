import { Suspense } from "react";
import {
  Game,
  GameNavigationBar,
  getAnnouncementComponent,
} from "./components/game-navigation-bar";
import AnnouncementSkeleton from "./components/announcement-skeleton";

export const revalidate = 60;

export default async function Home({
  params,
}: {
  params: Promise<{ game: Game | string }>;
}) {
  const { game } = await params;
  const Announcement = getAnnouncementComponent(game);

  return (
    <main className="flex min-h-screen flex-col items-center p-4">
      <GameNavigationBar game={game} />
      <div className="max-w-[768px] w-full flex justify-center">
        <Suspense fallback={<AnnouncementSkeleton />}>
          {Announcement && <Announcement />}
          {!Announcement && <div className="my-4">Invalid game: {game}</div>}
        </Suspense>
      </div>
    </main>
  );
}
