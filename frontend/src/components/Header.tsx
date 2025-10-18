import { ShoppingCart } from "lucide-react";

export function Header() {
  return (
    <header className="border-b bg-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <ShoppingCart className="w-8 h-8 text-emerald-600" />
            <span className="text-emerald-600">MarketMatch</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-8">
            <a href="#" className="text-gray-700 hover:text-gray-900">How it works</a>
            <a href="#" className="text-gray-700 hover:text-gray-900">About</a>
            <a href="#" className="text-gray-700 hover:text-gray-900">Help</a>
          </nav>
        </div>
      </div>
    </header>
  );
}