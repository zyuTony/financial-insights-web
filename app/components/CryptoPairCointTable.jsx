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
  minWidth: "100px",
  maxWidth: "1000px",
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
    field: "symbol_one",
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
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Symbol 2",
    field: "symbol_two",
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
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Coint P-Value",
    field: "coint_p_value",
    valueFormatter: (params) => params.value.toFixed(4),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Last Updated",
    field: "date",
    valueFormatter: (params) => new Date(params.value).toLocaleDateString(),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 100,
    maxWidth: 200,
    flex: 1,
  },
  {
    headerName: "Signal",
    field: "significant",
    cellStyle: (params) => {
      if (params.value === "Flashed") {
        return {
          textAlign: "right",
          color: "green",
          fontWeight: "bold",
        };
      }
      return {
        textAlign: "right",
        color: columnsConfig.colorNormal,
        fontWeight: columnsConfig.fontWeightNormal,
      };
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 120,
    maxWidth: 200,
    flex: 1,
  },
];

const CryptoPairCointTable = ({ data }) => {
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

export default CryptoPairCointTable;
