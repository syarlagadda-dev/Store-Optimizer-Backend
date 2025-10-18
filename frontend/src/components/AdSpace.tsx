interface AdSpaceProps {
  size: "banner" | "sidebar" | "square" | "leaderboard";
  label?: string;
}

export function AdSpace({ size, label = "Advertisement" }: AdSpaceProps) {
  const sizeClasses = {
    banner: "h-24 md:h-32",
    sidebar: "h-[600px]",
    square: "h-64 aspect-square",
    leaderboard: "h-20 md:h-24",
  };

  return (
    <div className={`w-full ${sizeClasses[size]} bg-gradient-to-br from-[#D6C9B8] to-[#F0ECE4] border border-[#D6C9B8] rounded-lg flex flex-col items-center justify-center p-4 shadow-sm`}>
      <div className="text-center">
        <div className="w-12 h-12 bg-[#A7866B] rounded-full mx-auto mb-3 flex items-center justify-center">
          <span className="text-white text-xl">Ad</span>
        </div>
        <p className="text-[#725842] text-sm mb-2">{label}</p>
        <p className="text-xs text-[#A7866B]">Your ad could be here</p>
        <div className="mt-4 px-4 py-2 bg-[#725842] text-white text-xs rounded">
          Learn More
        </div>
      </div>
    </div>
  );
}