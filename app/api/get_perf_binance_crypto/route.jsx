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
            ? new Date(
                Math.min(
                  new Date(startDate).getTime(),
                  Date.now() - 180 * 24 * 60 * 60 * 1000
                )
              )
            : new Date(Date.now() - 180 * 24 * 60 * 60 * 1000),
        },
      },
      orderBy: {
        date: "desc",
      },
    });

    // Get latest date and prices from historical data
    const latestDate = historicalPrices[0].date;
    const performance = historicalPrices
      .filter((price) => price.date.getTime() === latestDate.getTime())
      .map((price) => ({
        symbol: price.symbol,
        _max: {
          close: price.close,
          date: price.date,
        },
      }));

    // Calculate gains for each period
    const formattedPerformance = performance.map((symbol) => {
      const currentPrice = symbol._max.close;
      const prices = historicalPrices.filter((p) => p.symbol === symbol.symbol);

      // Find prices at different periods
      const price7d = prices.find(
        (p) => p.date <= new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
      )?.close;
      const price30d = prices.find(
        (p) => p.date <= new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      )?.close;
      const price90d = prices.find(
        (p) => p.date <= new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
      )?.close;
      const price180d = prices.find(
        (p) => p.date <= new Date(Date.now() - 180 * 24 * 60 * 60 * 1000)
      )?.close;

      // Find custom period price if dates provided
      let customPeriodGain = null;
      if (startDate && endDate) {
        const startPrice = prices.findLast(
          (p) => p.date >= new Date(startDate)
        )?.close;
        const endPrice = prices.find((p) => p.date <= new Date(endDate))?.close;

        if (startPrice && endPrice) {
          customPeriodGain = ((endPrice - startPrice) / startPrice) * 100;
        }
      }

      return {
        symbol: symbol.symbol,
        currentPrice: parseFloat(currentPrice),
        gain7d: price7d ? ((currentPrice - price7d) / price7d) * 100 : null,
        gain30d: price30d ? ((currentPrice - price30d) / price30d) * 100 : null,
        gain90d: price90d ? ((currentPrice - price90d) / price90d) * 100 : null,
        gain180d: price180d
          ? ((currentPrice - price180d) / price180d) * 100
          : null,
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
