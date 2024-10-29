import { Game, getGameName, isGame } from "@/constants/game";
import { GameNavigationBar } from "@/components/game-navigation-bar";
import type { Metadata, ResolvingMetadata } from "next";
export async function generateMetadata(
  { params }: { params: Promise<{ game: Game | string }> },
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { game } = await params;
  if (isGame(game)) {
    return {
      title: getGameName(game),
    };
  }
  return {};
}

export default async function AnnouncementLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ game: Game | string }>;
}) {
  const { game } = await params;
  return (
    <main className="flex min-h-screen flex-col items-center p-4">
      <GameNavigationBar game={game} />
      <div className="max-w-[768px] w-full flex justify-center">{children}</div>
    </main>
  );
}
