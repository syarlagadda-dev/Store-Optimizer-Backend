import { LeafDecoration } from "./LeafDecoration";

export function HowItWorks() {
  const steps = [
    {
      number: 1,
      title: "Enter Your Information",
      description: "Provide your home address, grocery list, budget, and number of stores"
    },
    {
      number: 2,
      title: "Click 'Find Cheapest Route'",
      description: "Our algorithm analyzes prices and distances to optimize your shopping trip"
    },
    {
      number: 3,
      title: "Enjoy Your Savings",
      description: "Follow your custom route and save money on groceries"
    }
  ];

  return (
    <section id="how-it-works" className="bg-white py-12 md:py-16 border-b-4 border-[#A7866B] relative overflow-hidden">
      <LeafDecoration position="top-left" />
      <LeafDecoration position="bottom-right" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-[#725842] mb-4 text-4xl font-bold">How It Works</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {steps.map((step) => (
            <div
              key={step.number}
              className="bg-white border-2 border-[#A7866B]/30 rounded-2xl p-8 text-center shadow-md hover:shadow-lg transition-shadow"
            >
              <div className="w-12 h-12 bg-[#725842] text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                {step.number}
              </div>
              <h3 className="text-[#725842] mb-3 font-bold text-xl">{step.title}</h3>
              <p className="text-[#725842]">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
