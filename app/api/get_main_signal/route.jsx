import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const signals = await prisma.signal_api_output.findMany({
      where: {
        pvalue: { lt: 0.05 },
      },
      orderBy: {
        key_score: "desc",
      },
    });

    const formattedSignals = signals.map((signal) => ({
      ...signal,
      pvalue: parseFloat(signal.pvalue),
      ols_const: parseFloat(signal.ols_const),
      ols_coeff: parseFloat(signal.ols_coeff),
      r_squared: parseFloat(signal.r_squared),
      key_score: parseFloat(signal.key_score),
      market_cap_1: signal.market_cap_1 ? parseInt(signal.market_cap_1) : null,
      market_cap_2: signal.market_cap_2 ? parseInt(signal.market_cap_2) : null,
      pe_ratio_1: signal.pe_ratio_1 ? parseFloat(signal.pe_ratio_1) : null,
      pe_ratio_2: signal.pe_ratio_2 ? parseFloat(signal.pe_ratio_2) : null,
      target_price_1: signal.target_price_1
        ? parseFloat(signal.target_price_1)
        : null,
      target_price_2: signal.target_price_2
        ? parseFloat(signal.target_price_2)
        : null,
    }));

    return new Response(JSON.stringify(formattedSignals), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
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
