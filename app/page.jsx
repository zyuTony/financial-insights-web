"use client";
// pages/index.js
import useSWR from "swr";
import SignalTable from "./components/SignalTable";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function Home() {
  const { data, error } = useSWR("/api/get_main_signal", fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <div className="px-10">loading...</div>;

  return (
    <div className="px-20">
      <h1>Main Table</h1>
      <SignalTable data={data} />
    </div>
  );
}