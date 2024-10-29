import { Game, games } from "@/constants/game";
import { cn } from "@/lib/utils";
import Link from "next/link";

export function GameNavigationBar(params: { game?: Game | string }) {
  return (
    <div className="max-w-[768px] w-full flex justify-center">
      <div className="flex">
        {games.map((game) => (
          <Link key={game.key} href={`/${game.key}`}>
            <span
              className={cn("hover:bg-gray-100 rounded-md px-4 py-2", {
                "font-bold": game.key === params.game,
              })}
            >
              {game.name}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
