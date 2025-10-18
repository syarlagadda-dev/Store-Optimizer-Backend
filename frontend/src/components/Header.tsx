import logo from "figma:asset/f824e5a95a858ee9d58dc3f764c2b8a7a89c2a31.png";

// Import Shadows Into Light Two font from Google Fonts
const fontLink = document.createElement('link');
fontLink.href = 'https://fonts.googleapis.com/css2?family=Shadows+Into+Light+Two&display=swap';
fontLink.rel = 'stylesheet';
if (!document.querySelector(`link[href="${fontLink.href}"]`)) {
  document.head.appendChild(fontLink);
}

export function Header() {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <header className="border-b-4 border-[#A7866B] bg-[#F0ECE4] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-28">
          <div className="flex items-center gap-4">
            <img src={logo} alt="Market Match" className="h-20 w-auto" />
            <span className="text-[#666D55] tracking-wide" style={{ fontFamily: "'Shadows Into Light Two', cursive", fontSize: '32px', fontWeight: '900', letterSpacing: '0.05em' }}>MARKET MATCH</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-6">
            <button onClick={() => scrollToSection('how-it-works')} className="bg-[#666D55] text-white px-4 py-2 rounded-lg hover:bg-[#A7866B] transition-all shadow-sm">How It Works</button>
            <button onClick={() => scrollToSection('search-section')} className="bg-[#666D55] text-white px-4 py-2 rounded-lg hover:bg-[#A7866B] transition-all shadow-sm">Get Started</button>
            <button onClick={() => scrollToSection('partner-stores')} className="bg-[#666D55] text-white px-4 py-2 rounded-lg hover:bg-[#A7866B] transition-all shadow-sm">Partner Stores</button>
          </nav>
        </div>
      </div>
    </header>
  );
}