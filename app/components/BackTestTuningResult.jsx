import React, { useEffect, useRef, useMemo } from "react";
import { createChart } from "lightweight-charts";

const useChartData = (tuningResult) => {
  return useMemo(() => {
    if (!tuningResult || tuningResult.length === 0) return {};

    const stratReturn = {};
    const baselineReturn = {};
    const seenDates = new Set();

    //for each distinct symbol+strategy+parameters, extract the symbol price data
    //for each distinct symbol+strategy,            extract the baseline price change
    tuningResult.forEach((row) => {
      const paramsCombo = Object.values(row.params).join("_");

      //strat returns
      const stratReturnKey = `${row.symbol}_${row.strat_name}_${paramsCombo}`;
      if (!stratReturn[stratReturnKey]) {
        stratReturn[stratReturnKey] = [];
      }
      const time = new Date(row.rolling_30d_end).getTime() / 1000;
      stratReturn[stratReturnKey].push({
        time,
        value: parseFloat(row.profit_pct),
      });

      //baseline returns
      const baselineReturnKey = `${row.symbol}_${row.strat_name}`;
      if (!baselineReturn[baselineReturnKey]) {
        baselineReturn[baselineReturnKey] = [];
      }
      if (!seenDates.has(`${baselineReturnKey}_${time}`)) {
        baselineReturn[baselineReturnKey].push({
          time,
          value: parseFloat(row.baseline_pct),
        });
        seenDates.add(`${baselineReturnKey}_${time}`);
      }
    });

    return {
      stratReturn,
      baselineReturn,
    };
  }, [tuningResult]);
};

const genericChartOptions = {
  width: 1600,
  layout: {
    backgroundColor: "#ffffff",
    textColor: "rgba(33, 56, 77, 1)",
  },
  grid: {
    vertLines: { color: "rgba(197, 203, 206, 0.3)" },
    horzLines: { color: "rgba(197, 203, 206, 0.3)" },
  },
  crosshair: { mode: "normal" },
  rightPriceScale: { borderColor: "rgba(197, 203, 206, 1)" },
  leftPriceScale: { borderColor: "rgba(197, 203, 206, 1)" },
  timeScale: { borderColor: "rgba(197, 203, 206, 1)" },
};

//line lineColors
const stratReturnLineColors = [
  "rgba(4, 111, 232, 1)",
  "rgba(255, 140, 0, 1)",
  "rgba(76, 175, 80, 1)",
  "rgba(233, 30, 99, 1)",
  "rgba(156, 39, 176, 1)",
];

const baselineReturnLineColors = [
  "rgba(4, 111, 232, 1)",
  "rgba(255, 140, 0, 1)",
  "rgba(76, 175, 80, 1)",
  "rgba(233, 30, 99, 1)",
  "rgba(156, 39, 176, 1)",
];

const legendStyle = `position: absolute; left: 80px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;

const BackTestTuningResult = ({
  tuningResult,
  selectedSymbols,
  selectedStrats,
}) => {
  const chartContainerRef = useRef();
  const { stratReturn, baselineReturn } = useChartData(tuningResult);

  useEffect(() => {
    if (Object.keys(stratReturn).length === 0) return; // break if no data
    const chartContainer = chartContainerRef.current; // hold the mounted div object
    chartContainer.innerHTML = ""; // clear div in case not empty

    //chart settings
    const chart = createChart(chartContainer, {
      ...genericChartOptions,
      height: 400,
    });

    //----- DATA SERIES  DATA SERIES  DATA SERIES  DATA SERIES  DATA SERIES -----//
    const stratReturnSeries = {};
    const baselineReturnSeries = {};

    Object.keys(stratReturn).forEach((key, index) => {
      const [symbol, strat] = key.split("_");
      if (
        (selectedSymbols.length === 0 || selectedSymbols.includes(symbol)) &&
        (selectedStrats.length === 0 || selectedStrats.includes(strat))
      ) {
        stratReturnSeries[key] = chart.addLineSeries({
          color: stratReturnLineColors[index % stratReturnLineColors.length],
          lineWidth: 2,
          title: key,
          priceScaleId: "right",
        });
        stratReturnSeries[key].setData(stratReturn[key]);
      }
    });

    Object.keys(baselineReturn).forEach((key, index) => {
      const [symbol, strat] = key.split("_");
      if (
        (selectedSymbols.length === 0 || selectedSymbols.includes(symbol)) &&
        (selectedStrats.length === 0 || selectedStrats.includes(strat))
      ) {
        baselineReturnSeries[key] = chart.addLineSeries({
          color:
            baselineReturnLineColors[index % baselineReturnLineColors.length],
          lineWidth: 1,
          lineStyle: 3,
          title: key,
          priceScaleId: "left",
        });
        baselineReturnSeries[key].setData(baselineReturn[key]);
      }
    });

    // Add y=0 axis
    const zeroLine = chart.addLineSeries({
      color: "rgba(0, 0, 0, 1)",
      lineWidth: 1.5,
      lineStyle: 0,
      // hide the 0 label
      lastValueVisible: false,
      priceLineVisible: false,
    });

    // Find the earliest and latest times across all series
    const allTimestamps = [
      ...Object.values(stratReturn),
      ...Object.values(baselineReturn),
    ]
      .flat()
      .map((item) => item.time);
    const earliestTime = Math.min(...allTimestamps);
    const latestTime = Math.max(...allTimestamps);
    zeroLine.setData([
      { time: earliestTime, value: 0 },
      { time: latestTime, value: 0 },
    ]);

    // Fit the chart to full space
    chart.timeScale().fitContent();

    //----- LEGEND LEGEND LEGEND LEGEND LEGEND LEGEND -----//
    const legend = document.createElement("div");
    legend.style = legendStyle;
    let legendHTML = "";

    // Add legend for each strat return line
    Object.keys(stratReturnSeries).forEach((key, index) => {
      legendHTML += `<div style="color: ${
        stratReturnLineColors[index % stratReturnLineColors.length]
      };">StratReturn_${key}: <span id="stratReturn_${key}Value"></span></div>`;
    });

    // Add legend for each baseline return line
    Object.keys(baselineReturnSeries).forEach((key, index) => {
      legendHTML += `<div style="color: ${
        baselineReturnLineColors[index % baselineReturnLineColors.length]
      };">Baseline_${key}: <span id="baseline_${key}Value"></span></div>`;
    });
    legend.innerHTML = legendHTML;
    chartContainer.appendChild(legend);

    // Interactive legend values on crosshair move
    chart.subscribeCrosshairMove((param) => {
      if (param.time) {
        // Update strat returns
        Object.keys(stratReturnSeries).forEach((key) => {
          const data = param.seriesData.get(stratReturnSeries[key]);
          if (data) {
            document.getElementById(`stratReturn_${key}Value`).textContent =
              data.value.toFixed(2) + "%";
          }
        });

        // Update baseline returns
        Object.keys(baselineReturnSeries).forEach((key) => {
          const data = param.seriesData.get(baselineReturnSeries[key]);
          if (data) {
            document.getElementById(`baseline_${key}Value`).textContent =
              data.value.toFixed(2) + "%";
          }
        });
      }
    });

    //useEffect ends
    return () => {
      chart.remove();
    };
  }, [stratReturn, baselineReturn, selectedSymbols, selectedStrats]);

  if (Object.keys(stratReturn).length === 0) {
    return <div>No data available</div>;
  }

  return (
    <div
      ref={chartContainerRef}
      style={{
        width: "1200px",
        position: "relative",
        marginTop: "20px", // Add margin to move the chart down
      }}
    />
  );
};

export default BackTestTuningResult;
