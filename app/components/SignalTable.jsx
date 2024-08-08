// components/SignalTable.jsx
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
const gridMaxWidth = "1200px";
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

const SignalTable = ({ data }) => {
  /*
  AGGrid Style: 
  1. Pair names' header and cell are aligned to left  
  other columns have header and cell aligned to right.
  2. As window size adjust, Table size has fixed min width and max width; 
  and columns use variable sizes
  3. Freeze first column and border for first column
  4. Color code the Key score from white -> green
  5. bold and blue color the tickers pair
  */
  /*
  More data design:
  Symbol 1 | MC1 | PE ratio 1 | 52 Week range 1 | Symbol 2 | MC2 | PE ratio 2 | 52 Week range 1 | Key Score   
  */
  const minValue = Math.min(...data.map((row) => row.key_score));
  const maxValue = Math.max(...data.map((row) => row.key_score));
  const columnDefs = [
    {
      //header and text to left; blue text with link; underline when hovered
      headerName: "Symbol 1",
      field: "symbol1",
      cellStyle: { color: "#0073e6", fontWeight: 600 },
      cellClass: "hover-underline",
      cellRenderer: (params) => {
        return <Link href="/todo">{params.value}</Link>;
      },
      flex: 1,
    },
    {
      headerName: "Market Cap 1",
      field: "market_cap_1",
      valueFormatter: (params) => mcFormater(params.value),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "PE ratio 1",
      field: "pe_ratio_1",
      valueFormatter: (params) =>
        params.value != null ? params.value.toFixed(2) : "N/A",
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "Symbol 2",
      field: "symbol2",
      cellStyle: { color: "#0073e6", fontWeight: 600 },
      cellClass: "hover-underline",
      cellRenderer: (params) => {
        return <Link href="/todo">{params.value}</Link>;
      },
      flex: 1,
    },
    {
      headerName: "Market Cap 2",
      field: "market_cap_2",
      valueFormatter: (params) => mcFormater(params.value),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "PE ratio 2",
      field: "pe_ratio_2",
      valueFormatter: (params) =>
        params.value != null ? params.value.toFixed(2) : "N/A",
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "P-Value",
      field: "pvalue",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "OLS Constant",
      field: "ols_const",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "OLS Coefficient",
      field: "ols_coeff",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "R-Squared",
      field: "r_squared",
      valueFormatter: (params) => {
        //format as percentage
        return params.value != null
          ? (params.value * 100).toFixed(0) + "%"
          : "";
      },
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1.1,
    },
    {
      headerName: "Key Score",
      field: "key_score",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: (params) => {
        const color = getKeyScoresColor(params.value, minValue, maxValue);
        return { color: color, textAlign: "right" };
      },
      headerClass: "ag-right-aligned-header",
      flex: 1.1,
    },
    {
      headerName: "Last Updated",
      field: "last_updated",
      valueFormatter: (params) => new Date(params.value).toLocaleDateString(),
      cellStyle: { textAlign: "right" },
      headerClass: "ag-right-aligned-header",
      // minWidth: 200, //unused for now
      flex: 1.1,
    },
  ];

  return (
    <div
      className="ag-theme-alpine"
      style={{
        // width: gridWidth,
        minWidth: gridMinWidth,
        maxWidth: gridMaxWidth,
      }}
    >
      <AgGridReact
        rowData={data}
        columnDefs={columnDefs}
        pagination={gridPagination}
        paginationPageSize={gridPaginationSize}
        paginationPageSizeSelector={paginationPageSizeSelector}
        domLayout="autoHeight" //make table height fit to num of rows
        rowHeight={gridRowHeight}
        defaultColDef={{
          // sortable and fixed size
          sortable: true,
          // filter: true,
          resizable: false,
        }}
      ></AgGridReact>
    </div>
  );
};

export default SignalTable;
