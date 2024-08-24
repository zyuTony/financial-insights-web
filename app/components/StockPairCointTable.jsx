// components/StockPairCointTable.jsx
"use client";
import Link from "next/link";
import React from "react";
import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS
import "../lib/AgGridComponent.css";

const mcFormater = (number) => {
  if (number >= 1e12) {
    return (number / 1e12).toFixed(3) + "T";
  } else if (number >= 1e9) {
    return (number / 1e9).toFixed(1) + "B";
  } else if (number >= 1e6) {
    return (number / 1e6).toFixed(0) + "M";
  } else if (number >= 1e3) {
    return (number / 1e3).toFixed(0) + "K";
  } else {
    return number.toFixed(2);
  }
};

const gridConfig = {
  minWidth: "800px",
  maxWidth: "1700px",
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
    headerName: "Symbol 1",
    field: "symbol1",
    cellStyle: {
      color: columnsConfig.colorSymbol,
      fontWeight: columnsConfig.fontWeightBold,
    },
    cellClass: "hover-underline",
    cellRenderer: (params) => {
      const symbol = params.value;
      const url = `https://finance.yahoo.com/quote/${symbol}`;
      return (
        <Link href={url} target="_blank" rel="noopener noreferrer">
          {symbol}
        </Link>
      );
    },
    minWidth: 100,
    maxWidth: 100,
    flex: 1,
  },
  {
    headerName: "Market Cap 1",
    field: "market_cap_1",
    valueFormatter: (params) => mcFormater(params.value),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    maxWidth: 120,
    flex: 1,
  },
  {
    headerName: "PE ratio 1",
    field: "pe_ratio_1",
    valueFormatter: (params) =>
      params.value != null ? params.value.toFixed(2) : "N/A",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    maxWidth: 120,
    flex: 1,
  },
  {
    headerName: "Symbol 2",
    field: "symbol2",
    cellStyle: {
      color: columnsConfig.colorSymbol,
      fontWeight: columnsConfig.fontWeightBold,
    },
    cellClass: "hover-underline",
    cellRenderer: (params) => {
      const symbol = params.value;
      const url = `https://finance.yahoo.com/quote/${symbol}`;
      return (
        <Link href={url} target="_blank" rel="noopener noreferrer">
          {symbol}
        </Link>
      );
    },
    minWidth: 100,
    maxWidth: 100,
    flex: 1,
  },
  {
    headerName: "Market Cap 2",
    field: "market_cap_2",
    valueFormatter: (params) => mcFormater(params.value),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    maxWidth: 120,
    flex: 1,
  },
  {
    headerName: "PE ratio 2",
    field: "pe_ratio_2",
    valueFormatter: (params) =>
      params.value != null ? params.value.toFixed(2) : "N/A",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    maxWidth: 120,
    flex: 1,
  },
  {
    headerName: "% Coint (Past 14 Days)",
    field: "most_recent_coint_pct",
    valueFormatter: (params) => `${Math.round(params.value * 100)}%`,
    cellStyle: (params) => {
      const allValues = params.api
        .getModel()
        .rowsToDisplay.map((row) => row.data.most_recent_coint_pct);
      const min = Math.min(...allValues);
      const max = Math.max(...allValues);
      return {
        textAlign: "right",
        color: columnsConfig.getRankingColor(params.value, min, max),
        fontWeight: columnsConfig.fontWeightBold,
      };
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 180,
    flex: 1,
  },
  {
    headerName: "% Coint (Past 60 Days)",
    field: "recent_coint_pct",
    valueFormatter: (params) => `${Math.round(params.value * 100)}%`,
    cellStyle: (params) => {
      const allValues = params.api
        .getModel()
        .rowsToDisplay.map((row) => row.data.recent_coint_pct);
      const min = Math.min(...allValues);
      const max = Math.max(...allValues);
      return {
        textAlign: "right",
        color: columnsConfig.getRankingColor(params.value, min, max),
        fontWeight: columnsConfig.fontWeightBold,
      };
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 180,
    flex: 1,
  },
  {
    headerName: "% Coint (Past 1 Year)",
    field: "hist_coint_pct",
    valueFormatter: (params) => `${Math.round(params.value * 100)}%`,
    cellStyle: (params) => {
      const allValues = params.api
        .getModel()
        .rowsToDisplay.map((row) => row.data.hist_coint_pct);
      const min = Math.min(...allValues);
      const max = Math.max(...allValues);
      return {
        textAlign: "right",
        color: columnsConfig.getRankingColor(params.value, min, max),
        fontWeight: columnsConfig.fontWeightBold,
      };
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 180,
    flex: 1,
  },
  {
    headerName: "OLS Coefficient",
    field: "ols_coeff",
    valueFormatter: (params) => params.value.toFixed(2),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 130,
    flex: 1,
  },
  {
    headerName: "OLS Constant",
    field: "ols_constant",
    valueFormatter: (params) => params.value.toFixed(2),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 120,
    flex: 1,
  },
  {
    headerName: "R-Squared",
    field: "r_squared",
    valueFormatter: (params) => {
      return params.value != null ? (params.value * 100).toFixed(0) + "%" : "";
    },
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 110,
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
    minWidth: 100,
    maxWidth: 120,
    flex: 1,
  },
];

const StockPairCointTable = ({ data }) => {
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

export default StockPairCointTable;
