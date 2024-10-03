"use client";
import Link from "next/link";
import React from "react";
import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS
import "../lib/AgGridComponent.css";

// const gridHeight = "4000px";
// const gridWidth = "1200px";
const gridMinWidth = "800px";
const gridMaxWidth = "800px";
const gridPaginationSize = 25;
const gridPagination = true;
const paginationPageSizeSelector = [10, 25, 50];

const gridRowHeight = 35;
// percentage formatter
const pctFormatter = (params) => {
  return params.value != null ? (params.value * 100).toFixed(0) + "%" : "";
};

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

const getKeyScoresColor = (value, min, max) => {
  const ratio = (value - min) / (max - min);
  const green = Math.round(ratio * 170);
  const color = `rgb(0, ${green}, 0)`;
  return color;
};

const gridConfig = {
  minWidth: "800px",
  maxWidth: "800px",
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
};

const columnDefs = [
  {
    headerName: "Date",
    field: "date",
    valueFormatter: (params) =>
      new Date(params.value).toLocaleString(undefined, {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      }),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    minWidth: 160,
    flex: 1.1,
  },
  {
    headerName: "Symbol",
    field: "symbol",
    cellStyle: {
      color: columnsConfig.colorSymbol,
      fontWeight: columnsConfig.fontWeightBold,
    },
    cellClass: "hover-underline",
    cellRenderer: (params) => {
      return <Link href="/todo">{params.value}</Link>;
    },
    flex: 1,
  },
  {
    headerName: "Action",
    field: "action",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    flex: 1,
  },
  {
    headerName: "$ Amount",
    field: "dollar_amt",
    valueFormatter: (params) =>
      params.value != null ? `$${params.value.toFixed(1)}` : "N/A",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    flex: 1,
  },
  {
    headerName: "Avg Price",
    field: "price",
    valueFormatter: (params) =>
      params.value != null ? `$${params.value.toFixed(1)}` : "N/A",
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    flex: 1,
  },
  {
    headerName: "Amount",
    field: "amt",
    valueFormatter: (params) => (params.value != null ? params.value : "N/A"),
    cellStyle: {
      textAlign: "right",
      color: columnsConfig.colorNormal,
      fontWeight: columnsConfig.fontWeightNormal,
    },
    headerClass: "ag-right-aligned-header",
    flex: 1,
  },
];

const TradeHistoryTable = ({ data }) => {
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

export default TradeHistoryTable;
