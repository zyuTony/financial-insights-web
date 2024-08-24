"use client";
// pages/index.js
import useSWR from "swr";
import TradeHistoryTable from "../../components/TradeHistoryTable";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function Home() {
  const { data, error } = useSWR("/api/get_trades", fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <div className="px-10">loading...</div>;

  return (
    <div className="flex flex-col items-center px-24 py-12 h-auto w-auto">
      {/* table centered at middle as a flex col.  */}
      <h1 className="text-3xl px-24 pb-6">Latest Trades</h1>
      <TradeHistoryTable data={data} />
    </div>
  );
}
