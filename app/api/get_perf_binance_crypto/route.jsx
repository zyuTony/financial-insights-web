import { prisma } from "@/app/lib/prisma";

export async function GET(request) {
  try {
    // Get query parameters for custom date range
    const { searchParams } = new URL(request.url);
    const startDate = searchParams.get("startDate");
    const endDate = searchParams.get("endDate");

    // Get historical prices for calculating gains
    const historicalPrices = await prisma.binance_market_data.findMany({
      select: {
        symbol: true,
        close: true,
        date: true,
      },
      where: {
        date: {
          gte: startDate
            ? new Date(startDate)
            : new Date(Date.now() - 180 * 24 * 60 * 60 * 1000),
          lte: endDate ? new Date(endDate) : new Date(),
        },
      },
      orderBy: {
        date: "asc",
      },
    });

    // Get performance data from binance_periods_performance table
    const performance = await prisma.binance_periods_performance.findMany({
      select: {
        symbol: true,
        latest_close: true,
        avg_volume_14d: true,
        pct_change_7d: true,
        pct_change_30d: true,
        pct_change_90d: true,
        pct_change_180d: true,
        latest_date: true,
      },
    });

    // Format the performance data
    const formattedPerformance = performance.map((p) => {
      // Find custom period price if dates provided
      let customPeriodGain = null;
      if (startDate && endDate) {
        const startPrice = historicalPrices.find(
          (h) => h.symbol === p.symbol && h.date >= new Date(startDate)
        )?.close;
        const endPrice = historicalPrices.find(
          (h) => h.symbol === p.symbol && h.date <= new Date(endDate)
        )?.close;

        if (startPrice && endPrice) {
          customPeriodGain = ((endPrice - startPrice) / startPrice) * 100;
        }
      }

      return {
        symbol: p.symbol,
        currentPrice: parseFloat(p.latest_close),
        usdVolume14d: parseFloat(p.avg_volume_14d),
        gain7d: p.pct_change_7d ? parseFloat(p.pct_change_7d) : null,
        gain30d: p.pct_change_30d ? parseFloat(p.pct_change_30d) : null,
        gain90d: p.pct_change_90d ? parseFloat(p.pct_change_90d) : null,
        gain180d: p.pct_change_180d ? parseFloat(p.pct_change_180d) : null,
        customPeriodGain: customPeriodGain,
      };
    });

    return new Response(JSON.stringify(formattedPerformance), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error in GET request:", error);
    return new Response(
      JSON.stringify({
        error: "Failed to retrieve data",
        message: error.message,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
