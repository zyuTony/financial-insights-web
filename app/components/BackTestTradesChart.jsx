import React, { useEffect, useRef, useMemo } from "react";
import { createChart } from "lightweight-charts";

const chartOptions = {
  width: 1800,
  layout: {
    backgroundColor: "#ffffff",
    textColor: "rgba(33, 56, 77, 1)",
  },
  grid: {
    vertLines: { color: "rgba(197, 203, 206, 0.5)" },
    horzLines: { color: "rgba(197, 203, 206, 0.5)" },
  },
  crosshair: { mode: "normal" },
  rightPriceScale: { borderColor: "rgba(197, 203, 206, 1)" },
  timeScale: { borderColor: "rgba(197, 203, 206, 1)" },
};

const useChartData = (priceData, tradesData) => {
  return useMemo(() => {
    if (!priceData || !tradesData) return {};

    const formattedPriceData = priceData.reduce((acc, data) => {
      const time = Math.floor(new Date(data.date).getTime() / 1000); // Convert to seconds
      if (!acc.some((item) => item.time === time)) {
        acc.push({ ...data, time });
      }
      return acc;
    }, []);

    const price_sma = formattedPriceData
      .filter((data) => data.close_SMA !== null && !isNaN(data.close_SMA))
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.close_SMA),
      }));

    const volume = formattedPriceData
      .filter((data) => data.volume !== null && !isNaN(data.volume))
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.volume),
      }));

    const volume_short_sma = formattedPriceData
      .filter(
        (data) =>
          data.volume_short_sma !== null && !isNaN(data.volume_short_sma)
      )
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.volume_short_sma),
      }));

    const volume_long_sma = formattedPriceData
      .filter(
        (data) => data.volume_long_sma !== null && !isNaN(data.volume_long_sma)
      )
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.volume_long_sma),
      }));

    const rsi = formattedPriceData
      .filter((data) => data.RSI !== null && !isNaN(data.RSI))
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.RSI),
      }));

    const rsi_2 = formattedPriceData
      .filter((data) => data.RSI_2 !== null && !isNaN(data.RSI_2))
      .map((data) => ({
        time: data.time,
        value: parseFloat(data.RSI_2),
      }));

    const formattedTradesData = tradesData
      .map((trade) => ({
        ...trade,
        time: Math.floor(new Date(trade.date).getTime() / 1000),
      }))
      .sort((a, b) => new Date(a.date) - new Date(b.date));

    const buyMarkers = formattedTradesData
      .filter((trade) => trade.action === "buy")
      .map((trade) => ({
        time: trade.time,
        position: "belowBar",
        color: "#2196F3",
        shape: "arrowUp",
        size: 2,
        text: `Buy@${trade.price.toFixed(2)}`,
      }));

    const sellMarkers = formattedTradesData
      .filter((trade) => trade.action === "sell")
      .map((trade) => ({
        time: trade.time,
        position: "aboveBar",
        color: "#e91e63",
        shape: "arrowDown",
        size: 2,
        text: `Sell@${trade.price.toFixed(2)}`,
      }));

    const allMarkers = [...buyMarkers, ...sellMarkers].sort(
      (a, b) => a.time - b.time
    );

    return {
      formattedPriceData,
      price_sma,
      rsi,
      rsi_2,
      allMarkers,
      volume,
      volume_short_sma,
      volume_long_sma,
    };
  }, [priceData, tradesData]);
};

const BackTestTradesChart = ({ priceData, tradesData }) => {
  const chartContainerRef = useRef();
  const {
    formattedPriceData,
    price_sma,
    rsi,
    rsi_2,
    allMarkers,
    volume,
    volume_short_sma,
    volume_long_sma,
  } = useChartData(priceData, tradesData);

  useEffect(() => {
    if (!formattedPriceData || formattedPriceData.length === 0) return;

    const chartContainer = chartContainerRef.current;
    chartContainer.innerHTML = ""; // Clear previous charts

    const mainChart = createChart(chartContainer, {
      ...chartOptions,
      height: 400,
    });
    const mainSeries = mainChart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderVisible: false,
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350",
    });

    const smaSeries = mainChart.addLineSeries({
      color: "rgba(4, 111, 232, 1)",
      lineWidth: 2,
    });

    const rsiChart = createChart(chartContainer, {
      ...chartOptions,
      height: 150,
    });
    const rsiSeries = rsiChart.addLineSeries({
      color: "rgba(4, 111, 232, 1)",
      lineWidth: 2,
    });
    const rsi2Series = rsiChart.addLineSeries({
      color: "rgba(214, 40, 40, 1)",
      lineWidth: 2,
    });

    const volumeChart = createChart(chartContainer, {
      ...chartOptions,
      height: 150,
    });
    // const volumeSeries = volumeChart.addHistogramSeries({
    //   color: "rgba(76, 175, 80, 0.5)",
    //   lineWidth: 2,
    // });
    const volumeShortSMASeries = volumeChart.addLineSeries({
      color: "rgba(255, 152, 0, 1)",
      lineWidth: 2,
    });
    const volumeLongSMASeries = volumeChart.addLineSeries({
      color: "rgba(156, 39, 176, 1)",
      lineWidth: 2,
    });

    mainSeries.setData(formattedPriceData);
    smaSeries.setData(price_sma);
    rsiSeries.setData(rsi);
    rsi2Series.setData(rsi_2);
    mainSeries.setMarkers(allMarkers);
    // volumeSeries.setData(volume);
    volumeShortSMASeries.setData(volume_short_sma);
    volumeLongSMASeries.setData(volume_long_sma);

    // Add legend to main chart
    const legend = document.createElement("div");
    legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;
    legend.innerHTML = `<div>OHLC: <span style="color: #26a69a;">O</span> <span id="open"></span> <span style="color: #26a69a;">H</span> <span id="high"></span> <span style="color: #ef5350;">L</span> <span id="low"></span> <span style="color: #ef5350;">C</span> <span id="close"></span></div>
      <div style="color: rgba(4, 111, 232, 1);">SMA: <span id="smaValue"></span></div>`;
    chartContainer.appendChild(legend);

    // Add legend to RSI chart
    const rsiLegend = document.createElement("div");
    rsiLegend.style = `position: absolute; left: 12px; top: 420px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;
    rsiLegend.innerHTML = `<div style="color: rgba(4, 111, 232, 1);">RSI: <span id="rsiValue"></span></div>
        <div style="color: rgba(214, 40, 40, 1);">RSI_2: <span id="rsi2Value"></span></div>`;
    chartContainer.appendChild(rsiLegend);

    // Add legend to Volume chart
    const volumeLegend = document.createElement("div");
    volumeLegend.style = `position: absolute; left: 12px; top: 580px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300; background-color: rgba(255, 255, 255, 0.23); padding: 4px;`;
    volumeLegend.innerHTML = `<div style="color: rgba(76, 175, 80, 1);">Volume: <span id="volumeValue"></span></div>
        <div style="color: rgba(255, 152, 0, 1);">Short SMA: <span id="volumeShortSMAValue"></span></div>
        <div style="color: rgba(156, 39, 176, 1);">Long SMA: <span id="volumeLongSMAValue"></span></div>`;
    chartContainer.appendChild(volumeLegend);

    mainChart.timeScale().fitContent();
    rsiChart.timeScale().fitContent();
    volumeChart.timeScale().fitContent();

    // Sync scales for the 3 charts
    const syncTimeScales = (sourceChart, targetCharts) => {
      sourceChart.timeScale().subscribeVisibleTimeRangeChange(() => {
        const timeRange = sourceChart.timeScale().getVisibleRange();
        targetCharts.forEach((chart) =>
          chart.timeScale().setVisibleRange(timeRange)
        );
      });
    };

    syncTimeScales(mainChart, [rsiChart, volumeChart]);
    syncTimeScales(rsiChart, [mainChart, volumeChart]);
    syncTimeScales(volumeChart, [mainChart, rsiChart]);

    // Update legend values on crosshair move
    mainChart.subscribeCrosshairMove((param) => {
      if (param.time) {
        const data = param.seriesData.get(mainSeries);
        const smaData = param.seriesData.get(smaSeries);
        if (data) {
          document.getElementById("open").textContent = data.open.toFixed(2);
          document.getElementById("high").textContent = data.high.toFixed(2);
          document.getElementById("low").textContent = data.low.toFixed(2);
          document.getElementById("close").textContent = data.close.toFixed(2);
        }
        if (smaData) {
          document.getElementById("smaValue").textContent =
            smaData.value.toFixed(2);
        }
      }
    });

    rsiChart.subscribeCrosshairMove((param) => {
      if (param.time) {
        const rsiData = param.seriesData.get(rsiSeries);
        const rsi2Data = param.seriesData.get(rsi2Series);
        if (rsiData) {
          document.getElementById("rsiValue").textContent =
            rsiData.value.toFixed(2);
        }
        if (rsi2Data) {
          document.getElementById("rsi2Value").textContent =
            rsi2Data.value.toFixed(2);
        }
      }
    });

    volumeChart.subscribeCrosshairMove((param) => {
      if (param.time) {
        const volumeData = param.seriesData.get(volumeSeries);
        const volumeShortSMAData = param.seriesData.get(volumeShortSMASeries);
        const volumeLongSMAData = param.seriesData.get(volumeLongSMASeries);
        if (volumeData) {
          document.getElementById("volumeValue").textContent =
            volumeData.value.toFixed(2);
        }
        if (volumeShortSMAData) {
          document.getElementById("volumeShortSMAValue").textContent =
            volumeShortSMAData.value.toFixed(2);
        }
        if (volumeLongSMAData) {
          document.getElementById("volumeLongSMAValue").textContent =
            volumeLongSMAData.value.toFixed(2);
        }
      }
    });

    return () => {
      mainChart.remove();
      rsiChart.remove();
      volumeChart.remove();
    };
  }, [
    formattedPriceData,
    price_sma,
    rsi,
    rsi_2,
    allMarkers,
    volume,
    volume_short_sma,
    volume_long_sma,
  ]);

  if (
    !priceData ||
    !tradesData ||
    priceData.length === 0 ||
    tradesData.length === 0
  ) {
    return <div>No data available</div>;
  }

  return (
    <div
      ref={chartContainerRef}
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        width: "1200px",
        position: "relative",
      }}
    />
  );
};

export default BackTestTradesChart;
