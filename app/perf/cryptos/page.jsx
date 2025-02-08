"use client";
import useSWR from "swr";
import CryptoPerformanceTable from "@/app/components/CryptoPerformanceTable";
import LoadingSpinner from "@/app/components/LoadingSpinner";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function CryptoPerformance() {
  const { data, error } = useSWR(`/api/get_perf_binance_crypto`, fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="flex flex-col px-24 py-12 h-full w-full">
      <h1 className="text-center text-3xl px-24 pb-6">
        Binance Listed Coins Performance
      </h1>
      <div className="text-center px-24 pb-8 text-gray-700">
        This table displays the performance metrics of cryptocurrencies listed
        on Binance across different time periods. Analyze historical price
        movements during notable altcoin seasons. The table shows key statistics
        like price changes, trading volume, and market capitalization to help
        identify strong movers for you next trade.
      </div>

      <div className="flex flex-col items-center gap-8">
        <div className="flex justify-center w-full">
          <CryptoPerformanceTable data={data} />
        </div>
      </div>
    </div>
  );
}
