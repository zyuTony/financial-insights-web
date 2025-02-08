"use client";
import Link from "next/link";
import React from "react";
import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS
import "../lib/AgGridComponent.css";

const priceFormatter = (number) => {
  let decimals = 0;
  if (number < 1) {
    decimals = 5; // Show all decimals for very small numbers
  } else if (number < 100) {
    decimals = 2;
  }

  const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return formatter.format(number);
};

const gridConfig = {
  minWidth: "800px",
  maxWidth: "2000px",
  paginationSize: 25,
  pagination: true,
  paginationPageSizeSelector: [10, 25, 50],
  rowHeight: 35,
};

const columnsConfig = {
  fontWeightNormal: 500,
  fontWeightBold: 600,
  colorNormal: "#666666",
  colorSymbol: "#0073e6",
  colorMaxCoint: "#00AA00",
  colorMinCoint: "#000000",
  getRankingColor: (value, min, max) => {
    if (value === min) return columnsConfig.colorMinCoint;
    const ratio = (value - min) / (max - min);
    const g = Math.round(0 * (1 - ratio) + 170 * ratio);
    return `rgb(0, ${g}, 0)`;
  },
};

const columnDefs = [
  {
    headerName: "Symbol",
    field: "symbol",
    cellStyle: (params) => ({
      color: params.value === "BTC" ? "#f7931a" : columnsConfig.colorSymbol,
      fontWeight: params.value === "BTC" ? 700 : columnsConfig.fontWeightBold,
    }),
    cellClass: "hover-underline",
    minWidth: 50,
    maxWidth: 200,
    flex: 0.7,
  },

  {
    headerName: "Current Price",
    field: "currentPrice",
    valueFormatter: (params) => priceFormatter(params.value),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 200,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Volume (M)",
    field: "usdVolume14d",
    valueFormatter: (params) =>
      params.value ? `$${Math.round(params.value / 1000000)}M` : "N/A",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 120,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "7d Gain",
    field: "gain7d",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 0.8,
  },
  {
    headerName: "30d Gain",
    field: "gain30d",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 0.8,
  },
  {
    headerName: "90d Gain",
    field: "gain90d",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 0.8,
  },
  {
    headerName: "180d Gain",
    field: "gain180d",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 0.8,
  },
  {
    headerName: "Altseason 1 Gain",
    field: "gainAltseason1",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 140,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Altseason 2 Gain",
    field: "gainAltseason2",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 140,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Altseason 3 Gain",
    field: "gainAltseason3",
    valueFormatter: (params) =>
      params.value ? `${Math.round(params.value)}%` : "N/A",
    cellStyle: (params) => ({
      textAlign: "right",
      color:
        params.value > 0
          ? "green"
          : params.value < 0
          ? "red"
          : columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightBold,
    }),
    headerClass: "ag-right-aligned-header",
    minWidth: 140,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Last Updated",
    field: "last_updated",
    valueFormatter: (params) => new Date(params.value).toLocaleDateString(),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 180,
    maxWidth: 200,
    flex: 1,
  },
];

const CryptoPerformanceTable = ({ data }) => {
  return (
    <div
      className="w-full ag-theme-alpine"
      style={{
        minWidth: gridConfig.minWidth,
        maxWidth: gridConfig.maxWidth,
      }}
    >
      <AgGridReact
        rowData={data}
        columnDefs={columnDefs}
        pagination={gridConfig.pagination}
        paginationPageSize={gridConfig.paginationSize}
        paginationPageSizeSelector={gridConfig.paginationPageSizeSelector}
        domLayout="autoHeight"
        rowHeight={gridConfig.rowHeight}
        defaultColDef={{
          sortable: true,
          resizable: false,
        }}
      ></AgGridReact>
    </div>
  );
};

export default CryptoPerformanceTable;
