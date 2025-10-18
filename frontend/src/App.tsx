import { useState } from "react";
import { Header } from "./components/Header";
import { SearchForm, SearchData } from "./components/SearchForm";
import { ResultsDisplay, ApiResponse } from "./components/ResultsDisplay";
import { AdSpace } from "./components/AdSpace";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";

// Mock function to simulate API call to Python backend
async function callPythonBackend(searchData: SearchData): Promise<ApiResponse> {
  // In production, replace this with actual API call:
  // const response = await fetch('YOUR_PYTHON_API_ENDPOINT', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({
  //     home_address: searchData.homeAddress,
  //     grocery_list: searchData.groceryList.split(',').map(item => item.trim()),
  //     budget: parseFloat(searchData.budget),
  //     max_stores: parseInt(searchData.numberOfStores)
  //   })
  // });
  // return response.json();

  // Mock delay to simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1500));

  // Mock response matching your Python backend format
  return {
    stores: ["Target", "Walmart"],
    items: [
      "bread ($2.30) : Target - 123 Main St, Charlotte, NC",
      "eggs ($2.90) : Target - 123 Main St, Charlotte, NC",
      "milk ($3.60) : Target - 123 Main St, Charlotte, NC",
      "chicken ($7.50) : Walmart - 456 Trade St, Charlotte, NC",
      "rice ($4.20) : Walmart - 456 Trade St, Charlotte, NC",
    ],
    item_total: 20.5,
    miles_traveled: 3.42,
    approximate_total_cost: 21.15,
    route_order: [
      {
        step: 1,
        type: "start",
        address: searchData.homeAddress,
      },
      {
        step: 2,
        type: "store",
        address: "Target - 123 Main St, Charlotte, NC",
      },
      {
        step: 3,
        type: "store",
        address: "Walmart - 456 Trade St, Charlotte, NC",
      },
      {
        step: 4,
        type: "end",
        address: searchData.homeAddress,
      },
    ],
  };
}

export default function App() {
  const [results, setResults] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (searchData: SearchData) => {
    setIsLoading(true);
    try {
      const response = await callPythonBackend(searchData);
      setResults(response);
      toast.success("Route optimized successfully!");
    } catch (error) {
      toast.error("Failed to fetch results. Please try again.");
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Fixed Side Banners */}
      <div className="hidden xl:block fixed left-4 top-24 w-40 2xl:w-48">
        <div className="sticky top-24">
          <AdSpace size="sidebar" label="Ad" />
        </div>
      </div>
      
      <div className="hidden xl:block fixed right-4 top-24 w-40 2xl:w-48">
        <div className="sticky top-24">
          <AdSpace size="sidebar" label="Ad" />
        </div>
      </div>
      
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-gray-900 mb-4">
            Smart Grocery Shopping, Optimized
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Enter your location, grocery list, and budget. We'll find the
            cheapest stores and the most efficient route to save you time and
            money.
          </p>
        </div>

        {/* Search Form */}
        <div className="max-w-3xl mx-auto mb-12">
          <SearchForm onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Results */}
        {results && (
          <div className="max-w-6xl mx-auto">
            <ResultsDisplay results={results} />
          </div>
        )}

        {/* Empty State */}
        {!results && !isLoading && (
          <div className="text-center py-12">
            <p className="text-gray-500">
              Fill out the form above to find your optimized shopping route
            </p>
          </div>
        )}
      </main>

      <Toaster />
    </div>
  );
}