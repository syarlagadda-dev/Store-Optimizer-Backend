import { useState } from "react";
import { Header } from "./components/Header";
import { HowItWorks } from "./components/HowItWorks";
import { SearchForm, SearchData } from "./components/SearchForm";
import { ResultsDisplay, ApiResponse } from "./components/ResultsDisplay";
import { AdSpace } from "./components/AdSpace";
import { StoresSection } from "./components/StoresSection";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";

async function callPythonBackend(searchData: SearchData): Promise<ApiResponse> {
  try {
    const response = await fetch("http://localhost:5000/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        csv_path: "prices_with_coords.csv",
        grocery_list: searchData.groceryList
          .split(",")
          .map((item) => item.trim()),
        max_stores: parseInt(searchData.numberOfStores),
        user_address: searchData.homeAddress,
      }),
    });

    const data = await response.json();

    // If Flask returns an error
    if (data.error) {
      throw new Error(data.error);
    }

    return data;
  } catch (err: any) {
    console.error("Error calling backend:", err);
    throw err;
  }
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
    } catch (error: any) {
      toast.error(error.message || "Failed to fetch results. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <HowItWorks />

      <main
        id="search-section"
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12"
      >
        <div className="flex gap-6 items-start mb-12">
          <div className="hidden lg:block w-40 xl:w-48 flex-shrink-0">
            <AdSpace size="sidebar" label="Ad" />
          </div>

          <div className="flex-1 max-w-3xl mx-auto space-y-8">
            <div className="text-center bg-white p-8 rounded-2xl border border-[#A7866B]/30 shadow-md">
              <h1 className="text-[#725842] mb-4 font-bold">
                Optimized, Smart Grocery Shopping
              </h1>
              <p className="text-[#725842] max-w-2xl mx-auto">
                Enter your location, grocery list, and budget. We'll find the
                cheapest stores and the most efficient route to save you time
                and money.
              </p>
            </div>

            <SearchForm onSearch={handleSearch} isLoading={isLoading} />
          </div>

          <div className="hidden lg:block w-40 xl:w-48 flex-shrink-0">
            <AdSpace size="sidebar" label="Ad" />
          </div>
        </div>

        {results && (
          <div className="max-w-6xl mx-auto">
            <ResultsDisplay results={results} />
          </div>
        )}
      </main>

      <div className="border-b-4 border-[#A7866B]"></div>

      <StoresSection />

      <Toaster />
    </div>
  );
}