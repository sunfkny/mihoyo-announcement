import {
  Game,
  games,
  getAnnouncementComponent,
  isGame,
} from "./components/game-navigation-bar";

export const revalidate = 60;

export async function generateStaticParams() {
  return games.map((game) => {
    return { game };
  });
}

export default async function Home({
  params,
}: {
  params: Promise<{ game: Game | string }>;
}) {
  const { game } = await params;
  if (isGame(game)) {
    const Announcement = getAnnouncementComponent(game);
    return <Announcement />;
  }
  return <div className="my-4">Invalid game: {game}</div>;
}
