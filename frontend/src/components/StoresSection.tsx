import targetLogo from "figma:asset/12a6e06c90056442b3cd80188aa2fd33ba3b15b4.png";
import walmartLogo from "figma:asset/33836b57c300f57b795e5c67e45e0964676dfe75.png";
import lidlLogo from "figma:asset/22da2dfbc0ef8ff8978defdd6ad9309d01e8ed6a.png";
import aldiLogo from "figma:asset/dcf1f0d3f3ec0caf061372f51c5930bbf985a543.png";
import samsClubLogo from "figma:asset/0fc3c1ab30c1f9e5abb96b019963cb942c69e720.png";
import traderJoesLogo from "figma:asset/7184bbf2558b6289237c2a174245972163c77e4d.png";
import harrisTeeterLogo from "figma:asset/ed0fe6b885288896b536fdb48f47405dc70d36f2.png";
import bjsLogo from "figma:asset/8f236dbd7a52f696afbbd3d84837a968139637f7.png";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { LeafDecoration } from "./LeafDecoration";

const stores = [
  {
    name: "Target",
    alt: "Target logo",
    imageUrl: targetLogo,
    className: "w-full h-16 object-contain"
  },
  {
    name: "Walmart",
    alt: "Walmart logo",
    imageUrl: walmartLogo,
    className: "w-full h-20 object-contain"
  },
  {
    name: "Lidl",
    alt: "Lidl logo",
    imageUrl: lidlLogo
  },
  {
    name: "Aldi",
    alt: "Aldi logo",
    imageUrl: aldiLogo
  },
  {
    name: "Harris Teeter",
    alt: "Harris Teeter logo",
    imageUrl: harrisTeeterLogo
  },
  {
    name: "Trader Joe's",
    alt: "Trader Joe's logo",
    imageUrl: traderJoesLogo
  },
  {
    name: "Sam's Club",
    alt: "Sam's Club logo",
    imageUrl: samsClubLogo
  },
  {
    name: "BJ's",
    alt: "BJ's Wholesale Club logo",
    imageUrl: bjsLogo
  }
];

export function StoresSection() {
  return (
    <section id="partner-stores" className="bg-white border-t border-[#D6C9B8] py-16 md:py-20 relative overflow-hidden">
      <LeafDecoration position="top-left" />
      <LeafDecoration position="bottom-right" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-[#725842] mb-4 text-4xl font-bold">Our Partner Stores</h2>
          <p className="text-[#725842] max-w-2xl mx-auto">
            We compare prices across these trusted retailers to find you the best deals
          </p>
        </div>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 md:gap-8">
          {stores.map((store, index) => (
            <div
              key={index}
              className="flex items-center justify-center p-6"
            >
              {typeof store.imageUrl === 'string' ? (
                <ImageWithFallback
                  src={store.imageUrl}
                  alt={store.alt}
                  className={store.className || "w-full h-25 object-contain"}
                />
              ) : (
                <img
                  src={store.imageUrl}
                  alt={store.alt}
                  className={store.className || "w-full h-25 object-contain"}
                />
              )}
              <div className="sr-only">{store.name}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
