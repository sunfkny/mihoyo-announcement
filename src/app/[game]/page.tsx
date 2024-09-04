import { Suspense } from "react";
import {
  Game,
  GameNavigationBar,
  isGame,
  getAnnouncementComponent,
} from "./components/game-navigation-bar";
import AnnouncementSkeleton from "./components/announcement-skeleton";

export const revalidate = 60;

export default function Home({ params }: { params: { game: Game | string } }) {
  const Announcement = getAnnouncementComponent(params.game);

  return (
    <main className="flex min-h-screen flex-col items-center p-4">
      <GameNavigationBar game={params.game} />
      <div className="max-w-[768px] w-full flex justify-center">
        <Suspense fallback={<AnnouncementSkeleton />}>
          {Announcement && <Announcement />}
          {!Announcement && (
            <div className="my-4">Invalid game: {params.game}</div>
          )}
        </Suspense>
      </div>
    </main>
  );
}
