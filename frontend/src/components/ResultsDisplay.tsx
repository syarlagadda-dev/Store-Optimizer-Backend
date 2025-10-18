import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { MapPin, Navigation, DollarSign, ShoppingBag, TrendingDown } from "lucide-react";

export interface ApiResponse {
  stores: string[];
  items: string[];
  item_total: number;
  miles_traveled: number;
  approximate_total_cost: number;
  route_order: RouteStep[];
}

interface RouteStep {
  step: number;
  type: "start" | "store" | "end";
  address: string;
}

interface ResultsDisplayProps {
  results: ApiResponse;
}

export function ResultsDisplay({ results }: ResultsDisplayProps) {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-[#725842]/30 bg-white shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-[#725842] rounded-lg shadow-sm">
                <DollarSign className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-[#725842]">Total Cost</p>
                <p className="text-[#725842]">${results.approximate_total_cost.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-[#666D55]/30 bg-white shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-[#666D55] rounded-lg shadow-sm">
                <Navigation className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-[#725842]">Distance</p>
                <p className="text-[#725842]">{results.miles_traveled.toFixed(2)} miles</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-[#A7866B]/30 bg-white shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-[#A7866B] rounded-lg shadow-sm">
                <ShoppingBag className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-[#725842]">Items Total</p>
                <p className="text-[#725842]">${results.item_total.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Shopping List */}
        <Card className="border-[#A7866B]/30 shadow-lg overflow-hidden bg-white">
          <CardHeader className="bg-[#725842] text-white">
            <CardTitle className="flex items-center gap-2">
              <ShoppingBag className="w-5 h-5" />
              Your Shopping List
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-3">
              {results.items.map((item, index) => {
                const [itemDetails, storeLocation] = item.split(" : ");
                const itemName = itemDetails.split(" (")[0];
                const price = itemDetails.match(/\$[\d.]+/)?.[0];
                
                return (
                  <div key={index} className="flex items-start justify-between p-3 bg-[#F0ECE4] rounded-lg border border-[#A7866B]/20">
                    <div className="flex-1">
                      <p className="text-[#725842]">{itemName}</p>
                      <p className="text-sm text-[#725842]">{storeLocation}</p>
                    </div>
                    <Badge variant="secondary" className="bg-[#725842] text-white">
                      {price}
                    </Badge>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Route */}
        <Card className="border-[#666D55]/30 shadow-lg overflow-hidden bg-white">
          <CardHeader className="bg-[#666D55] text-white">
            <CardTitle className="flex items-center gap-2">
              <Navigation className="w-5 h-5" />
              Your Route
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {results.route_order.map((route, index) => (
                <div key={index} className="flex items-start gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-white shadow-md ${
                        route.type === "start"
                          ? "bg-[#666D55]"
                          : route.type === "store"
                          ? "bg-[#725842]"
                          : "bg-[#A7866B]"
                      }`}
                    >
                      {route.step}
                    </div>
                    {index < results.route_order.length - 1 && (
                      <div className="w-0.5 h-8 bg-[#D6C9B8] my-1" />
                    )}
                  </div>
                  <div className="flex-1 pb-4">
                    <p className="text-sm text-[#725842] capitalize">
                      {route.type === "start"
                        ? "Starting Point"
                        : route.type === "store"
                        ? "Store Stop"
                        : "Return Home"}
                    </p>
                    <p className="text-[#725842]">{route.address}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Stores Summary */}
      <Card className="border-[#725842]/30 shadow-lg bg-white">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-[#725842]">
            <TrendingDown className="w-5 h-5" />
            Stores You'll Visit
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {results.stores.map((store, index) => (
              <Badge key={index} variant="outline" className="px-4 py-2 bg-[#D6C9B8] border-[#A7866B] text-[#725842]">
                {store}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
