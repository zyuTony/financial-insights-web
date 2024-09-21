"use client";
import useSWR from "swr";
import BackTestTuningResult from "../../components/BackTestTuningResult";
import React, { useEffect, useRef, useState } from "react";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function Home() {
  const [selectedSymbols, setSelectedSymbols] = useState([]);
  const [selectedStrats, setSelectedStrats] = useState([]);
  const { data, error } = useSWR("/api/get_backtest_tuning_results", fetcher);

  if (error) return <div>Failed to load data</div>;
  if (!data) return <div className="px-10">loading...</div>;

  // Data is already prepared in the API response
  const { tuningResult } = data;

  // Extract unique symbols and strat_names
  const symbols = [...new Set(tuningResult.map((item) => item.symbol))];
  const stratNames = [...new Set(tuningResult.map((item) => item.strat_name))];

  const handleSymbolChange = (symbol) => {
    setSelectedSymbols((prev) =>
      prev.includes(symbol)
        ? prev.filter((s) => s !== symbol)
        : [...prev, symbol]
    );
  };

  const handleStratChange = (strat) => {
    setSelectedStrats((prev) =>
      prev.includes(strat) ? prev.filter((s) => s !== strat) : [...prev, strat]
    );
  };

  // Filter tuningResult based on selections
  const filteredResult = tuningResult.filter(
    (item) =>
      (selectedSymbols.length === 0 || selectedSymbols.includes(item.symbol)) &&
      (selectedStrats.length === 0 || selectedStrats.includes(item.strat_name))
  );

  return (
    <div className="pl-4 h-auto w-auto flex ">
      <div className="flex mb-4 mt-6">
        <div className="mr-4">
          <h3 className="mb-2">Symbols</h3>
          {symbols.map((symbol) => (
            <div key={symbol} className="flex items-center mb-1">
              <input
                type="checkbox"
                id={`symbol-${symbol}`}
                checked={selectedSymbols.includes(symbol)}
                onChange={() => handleSymbolChange(symbol)}
                className="mr-2"
              />
              <label htmlFor={`symbol-${symbol}`}>{symbol}</label>
            </div>
          ))}
        </div>
        <div>
          <h3 className="mb-2">Strategies</h3>
          {stratNames.map((strat) => (
            <div key={strat} className="flex items-center mb-1">
              <input
                type="checkbox"
                id={`strat-${strat}`}
                checked={selectedStrats.includes(strat)}
                onChange={() => handleStratChange(strat)}
                className="mr-2"
              />
              <label htmlFor={`strat-${strat}`}>{strat}</label>
            </div>
          ))}
        </div>
      </div>
      <BackTestTuningResult
        tuningResult={filteredResult}
        selectedSymbols={selectedSymbols}
        selectedStrats={selectedStrats}
      />
    </div>
  );
}
