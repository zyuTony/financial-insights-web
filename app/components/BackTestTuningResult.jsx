import React, { useEffect, useRef, useMemo } from "react";
import { createChart } from "lightweight-charts";

const usePerformancesData = (backtestPerformancesOutput) => {
  return useMemo(() => {
    if (!backtestPerformancesOutput || backtestPerformancesOutput.length === 0)
      return {};

    const stratReturn = {};
    const baselineReturn = {};
    const seenDates = new Set();

    //for each distinct symbol+strategy+parameters, extract the symbol price data
    //for each distinct symbol+strategy,            extract the baseline price change
    backtestPerformancesOutput.forEach((row) => {
      const paramsCombo = Object.values(row.params).join("_");

      //strat returns
      const stratReturnKey = `${row.symbol}_${row.strat_name}_${paramsCombo}`;
      if (!stratReturn[stratReturnKey]) {
        stratReturn[stratReturnKey] = [];
      }
      const time = new Date(row.rolling_30d_end).getTime() / 1000;
      stratReturn[stratReturnKey].push({
        time,
        value: parseFloat(row.profit_pct) * 100,
      });

      //baseline returns
      const baselineReturnKey = `${row.symbol}_${row.strat_name}`;
      if (!baselineReturn[baselineReturnKey]) {
        baselineReturn[baselineReturnKey] = [];
      }
      if (!seenDates.has(`${baselineReturnKey}_${time}`)) {
        baselineReturn[baselineReturnKey].push({
          time,
          value: parseFloat(row.baseline_pct) * 100,
        });
        seenDates.add(`${baselineReturnKey}_${time}`);
      }
    });

    return {
      stratReturn,
      baselineReturn,
    };
  }, [backtestPerformancesOutput]);
};

const useTradesData = (backtestTradesOutput) => {
  return useMemo(() => {
    if (!backtestTradesOutput || backtestTradesOutput.length === 0) return {};

    const tradesData = {};
    const seenDates = new Set();

    // For each distinct symbol+strat+param, extract the trade data
    backtestTradesOutput.forEach((row) => {
      const paramsCombo = Object.values(row.params).join("_");
      const tradesDataKey = `${row.symbol}_${row.strat_name}_${paramsCombo}`;
      if (!tradesData[tradesDataKey]) {
        tradesData[tradesDataKey] = [];
      }

      const time = new Date(row.date).getTime() / 1000;
      if (!seenDates.has(`${tradesDataKey}_${time}`)) {
        tradesData[tradesDataKey].push({
          time,
          symbol: row.symbol,
          action: row.action,
          price: parseFloat(row.price),
        });
        seenDates.add(`${tradesDataKey}_${time}`);
      }
    });

    const allMarkers = Object.values(tradesData)
      .flatMap((trades) =>
        trades.map((trade) => ({
          time: trade.time,
          symbol: trade.symbol,
          position: trade.action === "BUY" ? "belowBar" : "aboveBar",
          color: trade.action === "BUY" ? "#2196F3" : "#e91e63",
          shape: trade.action === "BUY" ? "arrowUp" : "arrowDown",
          size: 2,
          text: `${
            trade.action === "BUY" ? "Buy" : "Sell"
          }@${trade.price.toFixed(2)}`,
        }))
      )
      .sort((a, b) => a.time - b.time);

    return {
      allMarkers,
    };
  }, [backtestTradesOutput]);
};

const useChartsData = (backtestChartsOutput) => {
  return useMemo(() => {
    if (!backtestChartsOutput || backtestChartsOutput.length === 0) return {};

    const chartOHLC = {};
    const seenDates = new Set();

    //for each distinct symbol, extract the OHLC data
    backtestChartsOutput.forEach((row) => {
      //baseline returns
      const chartOHLCKey = `${row.symbol}_${row.start_date}_${row.end_date}`;
      if (!chartOHLC[chartOHLCKey]) {
        chartOHLC[chartOHLCKey] = [];
      }
      const time = new Date(row.date).getTime() / 1000;
      if (!seenDates.has(`${chartOHLCKey}_${time}`)) {
        chartOHLC[chartOHLCKey].push({
          time,
          symbol: row.symbol,
          open: parseFloat(row.open),
          high: parseFloat(row.high),
          low: parseFloat(row.low),
          close: parseFloat(row.close),
        });
        seenDates.add(`${chartOHLCKey}_${time}`);
      }
    });

    Object.keys(chartOHLC).forEach((key) => {
      chartOHLC[key].sort((a, b) => a.time - b.time);
    });

    return {
      chartOHLC,
    };
  }, [backtestChartsOutput]);
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
  leftPriceScale: { borderColor: "rgba(197, 203, 206, 1)", visible: true },
  timeScale: { borderColor: "rgba(197, 203, 206, 1)" },
};

// Line colors
const stratReturnLineColors = [
  "rgba(41, 128, 185, 1)", // Steel Blue
  "rgba(241, 196, 15, 1)", // Sun Flower Yellow
  "rgba(46, 204, 113, 1)", // Emerald Green
  "rgba(231, 76, 60, 1)", // Pomegranate Red
  "rgba(142, 68, 173, 1)", // Wisteria Purple
];

const baselineReturnLineColors = [
  "rgba(41, 128, 185, 0.9)", // Steel Blue
  "rgba(241, 196, 15, 0.9)", // Sun Flower Yellow
  "rgba(46, 204, 113, 0.9)", // Emerald Green
  "rgba(231, 76, 60, 0.9)", // Pomegranate Red
  "rgba(142, 68, 173, 0.9)",
];

const legendStyle = `position: absolute; left: 80px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;

const ohlcLegendStyle = `position: absolute; left: 80px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;

const BackTestTuningResult = ({
  backtestPerformancesOutput,
  backtestChartsOutput,
  backtestTradesOutput,
  selectedSymbols,
  selectedStrats,
}) => {
  const chartContainerRef = useRef();
  const ohlcChartContainerRef = useRef();
  const { stratReturn, baselineReturn } = usePerformancesData(
    backtestPerformancesOutput
  );
  const { allMarkers } = useTradesData(backtestTradesOutput);
  const { chartOHLC } = useChartsData(backtestChartsOutput);
  console.log(allMarkers);

  useEffect(() => {
    if (Object.keys(stratReturn).length === 0) return; // break if no data
    const chartContainer = chartContainerRef.current; // hold the mounted div object
    const ohlcChartContainer = ohlcChartContainerRef.current;
    chartContainer.innerHTML = ""; // clear div in case not empty
    ohlcChartContainer.innerHTML = ""; // clear div in case not empty

    //---- CHART CHART CHART CHART CHART -----//
    const chart = createChart(chartContainer, {
      ...genericChartOptions,
      height: 400,
    });

    const ohlcChart = createChart(chartContainer, {
      ...genericChartOptions,
      height: 200,
    });

    //----- DATA SERIES  DATA SERIES  DATA SERIES  DATA SERIES  DATA SERIES -----//
    const stratReturnSeries = {};
    const baselineReturnSeries = {};
    const candlestickSeries = {};

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

    console.log(chartOHLC);
    // Add OHLC chart
    Object.keys(chartOHLC).forEach((key, index) => {
      const [symbol, startDate, endDate] = key.split("_");
      if (selectedSymbols.length === 0 || selectedSymbols.includes(symbol)) {
        candlestickSeries[key] = ohlcChart.addCandlestickSeries({
          upColor: "#26a69a",
          downColor: "#ef5350",
          borderVisible: false,
          wickUpColor: "#26a69a",
          wickDownColor: "#ef5350",
          priceScaleId: index % 2 === 1 ? "left" : "right",
        });
        candlestickSeries[key].setData(chartOHLC[key]);

        // Add markers
        const filteredMarkers = allMarkers.filter(
          (marker) => marker.symbol === symbol
        );
        console.log(filteredMarkers);
        candlestickSeries[key].setMarkers(filteredMarkers);
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

    // Fit the charts to full space
    chart.timeScale().fitContent();
    ohlcChart.timeScale().fitContent();

    // Sync scales for the 2 charts
    const syncTimeScales = (sourceChart, targetChart) => {
      sourceChart.timeScale().subscribeVisibleTimeRangeChange(() => {
        const timeRange = sourceChart.timeScale().getVisibleRange();
        targetChart.timeScale().setVisibleRange(timeRange);
      });
    };

    syncTimeScales(chart, ohlcChart);
    syncTimeScales(ohlcChart, chart);

    //----- LEGEND LEGEND LEGEND LEGEND LEGEND LEGEND -----//

    // Add legend for main chart
    const legend = document.createElement("div");
    legend.style = legendStyle;
    let legendHTML = "";

    Object.keys(stratReturnSeries).forEach((key, index) => {
      legendHTML += `<div style="color: ${
        stratReturnLineColors[index % stratReturnLineColors.length]
      };">StratReturn_${key}: <span id="stratReturn_${key}Value"></span></div>`;
    });
    Object.keys(baselineReturnSeries).forEach((key, index) => {
      legendHTML += `<div style="color: ${
        baselineReturnLineColors[index % baselineReturnLineColors.length]
      };">Baseline_${key}: <span id="baseline_${key}Value"></span></div>`;
    });
    legend.innerHTML = legendHTML;
    chartContainer.appendChild(legend);

    // Add legend for OHLC chart
    const ohlcLegend = document.createElement("div");
    ohlcLegend.style = ohlcLegendStyle;
    let ohlcLegendHTML = "";

    Object.keys(candlestickSeries).forEach((key, index) => {
      ohlcLegendHTML += `
      <div>OHLC_${key}: 
        <span style="color: #26a69a;">O</span> <span id="open_${key}"></span> 
        <span style="color: #26a69a;">H</span> <span id="high_${key}"></span> 
        <span style="color: #ef5350;">L</span> <span id="low_${key}"></span> 
        <span style="color: #ef5350;">C</span> <span id="close_${key}"></span>
      </div>
    `;
    });
    ohlcLegend.innerHTML = ohlcLegendHTML;
    ohlcChartContainerRef.current.appendChild(ohlcLegend);

    // Interactive legend values on crosshair move
    chart.subscribeCrosshairMove((param) => {
      if (param.time) {
        // Update strat returns
        Object.keys(stratReturnSeries).forEach((key) => {
          const data = param.seriesData.get(stratReturnSeries[key]);
          console.log(data);
          if (data) {
            document.getElementById(`stratReturn_${key}Value`).textContent =
              data.value.toFixed(1) + "%";
          }
        });

        // Update baseline returns
        Object.keys(baselineReturnSeries).forEach((key) => {
          const data = param.seriesData.get(baselineReturnSeries[key]);
          if (data) {
            document.getElementById(`baseline_${key}Value`).textContent =
              data.value.toFixed(1) + "%";
          }
        });
      }
    });

    // Interactive OHLC legend values on crosshair move
    ohlcChart.subscribeCrosshairMove((param) => {
      if (param.time) {
        Object.keys(candlestickSeries).forEach((key) => {
          const data = param.seriesData.get(candlestickSeries[key]);
          console.log(data);
          if (data) {
            document.getElementById(`open_${key}`).textContent =
              data.open.toFixed(2);
            document.getElementById(`high_${key}`).textContent =
              data.high.toFixed(2);
            document.getElementById(`low_${key}`).textContent =
              data.low.toFixed(2);
            document.getElementById(`close_${key}`).textContent =
              data.close.toFixed(2);
          }
        });
      }
    });

    //useEffect ends
    return () => {
      chart.remove();
      ohlcChart.remove();
    };
  }, [
    stratReturn,
    baselineReturn,
    chartOHLC,
    allMarkers,
    selectedSymbols,
    selectedStrats,
  ]);

  if (Object.keys(stratReturn).length === 0) {
    return <div>No data available</div>;
  }

  return (
    <div>
      <div
        ref={chartContainerRef}
        style={{
          width: "1200px",
          position: "relative",
          marginTop: "20px", // Add margin to move the chart down
        }}
      />
      <div
        ref={ohlcChartContainerRef}
        style={{
          width: "1200px",
          position: "relative",
          marginTop: "20px", // Add margin to move the chart down
        }}
      />
    </div>
  );
};

export default BackTestTuningResult;
