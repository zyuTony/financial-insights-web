// components/SignalTable.jsx
"use client";

import React from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS

// pagination filter
const pagination = true;
const paginationPageSize = 50;
const paginationPageSizeSelector = [10, 20, 50, 100];

const gridHeight = "800px";
const gridWidth = "1200px";
const gridMinWidth = "800px";
const gridMaxWidth = "1200px";

// percentage formatter
const pctFormatter = (params) => {
  return params.value != null ? (params.value * 100).toFixed(0) + "%" : "";
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
  Ticker 1 | MC1 | PE ratio 1 | 52 Week range 1 | Ticker 2 | MC2 | PE ratio 2 | 52 Week range 1 | Key Score   
  */
  const columnDefs = [
    {
      headerName: "Name 1",
      field: "name1",
      flex: 1,
    },
    {
      headerName: "Name 2",
      field: "name2",
      flex: 1,
    },
    {
      headerName: "P-Value",
      field: "pvalue",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "OLS Constant",
      field: "ols_const",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "OLS Coefficient",
      field: "ols_coeff",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1,
    },
    {
      headerName: "R-Squared",
      field: "r_squared",
      valueFormatter: pctFormatter,
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      flex: 1.2,
    },
    {
      headerName: "Key Score",
      field: "key_score",
      valueFormatter: (params) => params.value.toFixed(2),
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      minwidth: 200,
      flex: 1.2,
    },
    {
      headerName: "Last Updated",
      field: "last_updated",
      valueFormatter: (params) => new Date(params.value).toLocaleDateString(),
      cellStyle: { "text-align": "right" },
      headerClass: "ag-right-aligned-header",
      minwidth: 200,
      flex: 1.5,
    },
  ];

  return (
    <div
      className="ag-theme-alpine"
      style={{
        height: gridHeight,
        // width: gridWidth,
        minWidth: gridMinWidth,
        maxWidth: gridMaxWidth,
      }}
    >
      <AgGridReact
        rowData={data}
        columnDefs={columnDefs}
        pagination={pagination}
        paginationPageSize={paginationPageSize}
        paginationPageSizeSelector={paginationPageSizeSelector}
        defaultColDef={{
          sortable: true,
          // filter: true,
          resizable: false,
        }}
      ></AgGridReact>
    </div>
  );
};

export default SignalTable;
