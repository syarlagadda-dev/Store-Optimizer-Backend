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
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-emerald-100 rounded-lg">
                <DollarSign className="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Cost</p>
                <p className="text-emerald-600">${results.approximate_total_cost.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Navigation className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Distance</p>
                <p className="">{results.miles_traveled.toFixed(2)} miles</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <ShoppingBag className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Items Total</p>
                <p className="">${results.item_total.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Shopping List */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingBag className="w-5 h-5" />
              Your Shopping List
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {results.items.map((item, index) => {
                const [itemDetails, storeLocation] = item.split(" : ");
                const itemName = itemDetails.split(" (")[0];
                const price = itemDetails.match(/\$[\d.]+/)?.[0];
                
                return (
                  <div key={index} className="flex items-start justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <p className="">{itemName}</p>
                      <p className="text-sm text-gray-500">{storeLocation}</p>
                    </div>
                    <Badge variant="secondary" className="bg-emerald-100 text-emerald-700">
                      {price}
                    </Badge>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Route */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Navigation className="w-5 h-5" />
              Your Route
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.route_order.map((route, index) => (
                <div key={index} className="flex items-start gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-white ${
                        route.type === "start"
                          ? "bg-blue-500"
                          : route.type === "store"
                          ? "bg-emerald-500"
                          : "bg-gray-500"
                      }`}
                    >
                      {route.step}
                    </div>
                    {index < results.route_order.length - 1 && (
                      <div className="w-0.5 h-8 bg-gray-300 my-1" />
                    )}
                  </div>
                  <div className="flex-1 pb-4">
                    <p className="text-sm text-gray-500 capitalize">
                      {route.type === "start"
                        ? "Starting Point"
                        : route.type === "store"
                        ? "Store Stop"
                        : "Return Home"}
                    </p>
                    <p className="">{route.address}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Stores Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingDown className="w-5 h-5" />
            Stores You'll Visit
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {results.stores.map((store, index) => (
              <Badge key={index} variant="outline" className="px-4 py-2">
                {store}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
