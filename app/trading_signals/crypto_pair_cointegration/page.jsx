"use client";
// pages/index.js
import useSWR from "swr";
import CryptoPairCointTable from "@/app/components/CryptoPairCointTable";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function crypto_pair_cointegration() {
  const { data, error } = useSWR("/api/get_pair_coint_crypto", fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <div className="px-10">loading...</div>;

  return (
    <div className="flex flex-col px-24 py-12 h-full w-full">
      {/* explain section */}
      <h1 className="text-center text-3xl px-24 pb-6">Pairs Cointegration</h1>
      <div className="flex justify-center">
        <CryptoPairCointTable data={data} />
      </div>
    </div>
  );
}
