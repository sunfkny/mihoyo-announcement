export default function Loading() {
  return (
    <div className="w-full animate-pulse">
      <div className="my-4">
        <div className="h-2 bg-gray-200 rounded w-full"></div>
        <div className="h-4 my-1 bg-gray-200 rounded max-w-full w-[500px]"></div>
      </div>
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i}>
          <div className="h-[280px] my-1 bg-gray-200 rounded w-full"></div>
          <div className="h-4 my-1 bg-gray-200 rounded max-w-full w-[400px]"></div>
          <div className="h-4 my-1 bg-gray-200 rounded max-w-full w-[260px]"></div>
          <div className="h-4 my-1 bg-gray-200 rounded max-w-full w-[360px]"></div>
        </div>
      ))}
    </div>
  );
}
