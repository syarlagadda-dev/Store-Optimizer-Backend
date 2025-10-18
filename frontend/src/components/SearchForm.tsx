import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Card, CardContent } from "./ui/card";
import { MapPin, List, DollarSign, Store } from "lucide-react";

interface SearchFormProps {
  onSearch: (data: SearchData) => void;
  isLoading: boolean;
}

export interface SearchData {
  homeAddress: string;
  groceryList: string;
  budget: string;
  numberOfStores: string;
}

export function SearchForm({ onSearch, isLoading }: SearchFormProps) {
  const [formData, setFormData] = useState<SearchData>({
    homeAddress: "",
    groceryList: "",
    budget: "",
    numberOfStores: "3",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="border-[#A7866B]/30 shadow-md bg-white">
        <CardContent className="pt-6">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Home Address */}
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="homeAddress" className="flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                Starting Location
              </Label>
              <Input
                id="homeAddress"
                placeholder="123 Main St, Charlotte, NC 28202"
                value={formData.homeAddress}
                onChange={(e) =>
                  setFormData({ ...formData, homeAddress: e.target.value })
                }
                required
              />
            </div>

            {/* Grocery List */}
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="groceryList" className="flex items-center gap-2">
                <List className="w-4 h-4" />
                Grocery List
              </Label>
              <Textarea
                id="groceryList"
                placeholder="bread, eggs, milk, chicken, rice..."
                value={formData.groceryList}
                onChange={(e) =>
                  setFormData({ ...formData, groceryList: e.target.value })
                }
                rows={4}
                required
              />
              <p className="text-sm text-[#725842]">
                Enter items separated by commas
              </p>
            </div>

            {/* Budget */}
            <div className="space-y-2">
              <Label htmlFor="budget" className="flex items-center gap-2">
                <DollarSign className="w-4 h-4" />
                Budget
              </Label>
              <Input
                id="budget"
                type="number"
                step="0.01"
                placeholder="50.00"
                value={formData.budget}
                onChange={(e) =>
                  setFormData({ ...formData, budget: e.target.value })
                }
                required
              />
            </div>

            {/* Number of Stores */}
            <div className="space-y-2">
              <Label htmlFor="numberOfStores" className="flex items-center gap-2">
                <Store className="w-4 h-4" />
                Max Number of Stores
              </Label>
              <Input
                id="numberOfStores"
                type="number"
                min="1"
                max="10"
                placeholder="3"
                value={formData.numberOfStores}
                onChange={(e) =>
                  setFormData({ ...formData, numberOfStores: e.target.value })
                }
                required
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full mt-6 bg-[#725842] hover:bg-[#666D55] text-white shadow-md"
            disabled={isLoading}
          >
            {isLoading ? "Finding Best Routes..." : "Find Cheapest Route"}
          </Button>
        </CardContent>
      </Card>
    </form>
  );
}
