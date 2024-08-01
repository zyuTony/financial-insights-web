// components/SignalTable.jsx
"use client";
import React, { useState } from "react";

const SignalTable = ({ data }) => {
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "ascending",
  });
  const [filterConfig, setFilterConfig] = useState("");

  const sortedData = React.useMemo(() => {
    let sortableData = [...data];
    if (sortConfig.key !== null) {
      sortableData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableData;
  }, [data, sortConfig]);

  const filteredData = sortedData.filter((item) => {
    return (
      item.name1.toLowerCase().includes(filterConfig.toLowerCase()) ||
      item.name2.toLowerCase().includes(filterConfig.toLowerCase())
    );
  });

  const requestSort = (key) => {
    let direction = "ascending";
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  const formatNumber = (number) => {
    console.log(number, typeof number);
    return typeof number === "number" ? number.toFixed(2) : number;
  };

  return (
    <div className="container mx-auto px-4">
      <h2 className="text-2xl font-semibold mb-4">Stock Signals</h2>
      <input
        type="text"
        placeholder="Filter by name"
        value={filterConfig}
        onChange={(e) => setFilterConfig(e.target.value)}
        className="mb-4 p-2 border border-gray-300 rounded"
      />
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200 rounded-md">
          <thead>
            <tr>
              <th className="p-4 border-b">Index</th>
              <th
                onClick={() => requestSort("name1")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "name1" ? "bg-gray-300" : ""
                }`}
              >
                Name 1
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("name2")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "name2" ? "bg-gray-300" : ""
                }`}
              >
                Name 2
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("pvalue")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "pvalue" ? "bg-gray-300" : ""
                }`}
              >
                P-Value
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("ols_const")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "ols_const" ? "bg-gray-300" : ""
                }`}
              >
                OLS Constant
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("ols_coeff")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "ols_coeff" ? "bg-gray-300" : ""
                }`}
              >
                OLS Coefficient
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("r_squared")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "r_squared" ? "bg-gray-300" : ""
                }`}
              >
                R-Squared
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("key_score")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "key_score" ? "bg-gray-300" : ""
                }`}
              >
                Key Score
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
              <th
                onClick={() => requestSort("last_updated")}
                className={`p-4 border-b cursor-pointer relative ${
                  sortConfig.key === "last_updated" ? "bg-gray-300" : ""
                }`}
              >
                Last Updated
                <span className="absolute top-0 right-0 mr-2 opacity-0 hover:opacity-100">
                  🔼
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((signal, index) => (
              <tr
                key={`${signal.name1}-${signal.name2}-${signal.last_updated}`}
                className="hover:bg-gray-100"
              >
                <td className="p-4 border-b">{index + 1}</td>
                <td className="p-4 border-b">{signal.name1}</td>
                <td className="p-4 border-b">{signal.name2}</td>
                <td className="p-4 border-b">{formatNumber(signal.pvalue)}</td>
                <td className="p-4 border-b">
                  {formatNumber(signal.ols_const)}
                </td>
                <td className="p-4 border-b">
                  {formatNumber(signal.ols_coeff)}
                </td>
                <td className="p-4 border-b">
                  {formatNumber(signal.r_squared)}
                </td>
                <td className="p-4 border-b">
                  {formatNumber(signal.key_score)}
                </td>
                <td className="p-4 border-b">
                  {new Date(signal.last_updated).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SignalTable;
