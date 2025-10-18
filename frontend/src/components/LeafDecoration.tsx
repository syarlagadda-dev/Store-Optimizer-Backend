interface LeafDecorationProps {
  position: 'top-left' | 'bottom-right';
  className?: string;
}

export function LeafDecoration({ position, className = '' }: LeafDecorationProps) {
  const isTopLeft = position === 'top-left';
  
  return (
    <div
      className={`absolute ${
        isTopLeft ? 'top-0 left-0' : 'bottom-0 right-0'
      } ${isTopLeft ? '' : 'rotate-180'} pointer-events-none ${className}`}
    >
      <svg
        width="120"
        height="120"
        viewBox="0 0 120 120"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="opacity-20"
      >
        {/* Main leaf */}
        <path
          d="M10 10C10 10 20 30 25 50C30 70 35 90 45 100C55 110 70 115 80 110C90 105 95 90 95 80C95 70 90 55 80 45C70 35 50 25 30 20C20 17 10 10 10 10Z"
          fill="#666D55"
        />
        {/* Secondary leaf */}
        <path
          d="M10 10C10 10 30 15 45 20C60 25 75 30 85 40C95 50 105 65 105 75C105 85 100 95 90 100C80 105 65 105 55 95C45 85 35 65 30 45C27 30 10 10 10 10Z"
          fill="#A7866B"
          opacity="0.7"
        />
        {/* Small accent leaf */}
        <path
          d="M15 15C15 15 25 20 32 28C39 36 44 48 42 56C40 64 32 68 26 66C20 64 16 56 15 48C14 40 15 25 15 15Z"
          fill="#725842"
          opacity="0.5"
        />
      </svg>
    </div>
  );
}
