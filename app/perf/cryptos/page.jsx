"use client";
import useSWR from "swr";
import CryptoPerformanceTable from "@/app/components/CryptoPerformanceTable";
import { useState } from "react";
import LoadingSpinner from "@/app/components/LoadingSpinner";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function CryptoPerformance() {
  const [startDate, setStartDate] = useState("2023-10-30");
  const [endDate, setEndDate] = useState("2024-03-25");
  const [startDateInput, setStartDateInput] = useState("2023-10-30");
  const [endDateInput, setEndDateInput] = useState("2024-03-25");

  const handlePresetRange = (start, end) => {
    setStartDateInput(start);
    setEndDateInput(end);
  };

  const handleApplyRange = () => {
    setStartDate(startDateInput);
    setEndDate(endDateInput);
  };

  const { data, error } = useSWR(
    `/api/get_perf_binance_crypto?startDate=${startDate}&endDate=${endDate}`,
    fetcher
  );

  if (error) return <div>Failed to load data</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="flex flex-col px-24 py-12 h-full w-full">
      <h1 className="text-center text-3xl px-24 pb-6">
        Binance Listed Coins Performance
      </h1>

      <div className="flex flex-col items-center gap-8">
        <div className="flex flex-col gap-4 w-full max-w-[1300px]">
          <div className="flex gap-4 flex-wrap">
            <button
              onClick={() => handlePresetRange("2019-12-23", "2020-08-17")}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            >
              2020 Altseason
            </button>
            <button
              onClick={() => handlePresetRange("2021-01-04", "2022-01-10")}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            >
              2021 Altseason
            </button>
            <button
              onClick={() => handlePresetRange("2023-10-30", "2024-03-25")}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            >
              2023 Altseason
            </button>
            <button
              onClick={() =>
                handlePresetRange(
                  "2024-10-28",
                  new Date().toISOString().split("T")[0]
                )
              }
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            >
              2024 Altseason
            </button>
          </div>

          <div className="flex items-center gap-4 flex-wrap">
            <label className="text-sm font-medium">Custom Period:</label>
            <input
              type="date"
              value={startDateInput}
              onChange={(e) => setStartDateInput(e.target.value)}
              className="border rounded px-2 py-1"
            />
            <span>to</span>
            <input
              type="date"
              value={endDateInput}
              onChange={(e) => setEndDateInput(e.target.value)}
              className="border rounded px-2 py-1"
            />
            <button
              onClick={handleApplyRange}
              className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Apply
            </button>
          </div>
        </div>

        <div className="flex justify-center w-full">
          <CryptoPerformanceTable data={data} />
        </div>
      </div>
    </div>
  );
}
