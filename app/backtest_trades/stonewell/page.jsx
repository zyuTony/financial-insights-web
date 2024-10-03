"use client";
import useSWR from "swr";
import BackTestTradesChart from "../../components/BackTestTradesChart";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function Home() {
  const { data, error } = useSWR("/api/get_backtest_trades", fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <div className="px-10">loading...</div>;

  // Data is already prepared in the API response
  const { priceData, tradesData } = data;
  // console.log(priceData);
  // console.log(tradesData);
  return (
    <div className="pl-4 h-auto w-auto">
      <BackTestTradesChart priceData={priceData} tradesData={tradesData} />
    </div>
  );
}
