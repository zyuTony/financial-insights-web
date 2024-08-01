import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const signals = await prisma.stock_signal.findMany({
      where: {
        pvalue: { lt: 0.05 },
      },
      orderBy: {
        key_score: "desc",
      },
      take: 100,
    });
    const formattedSignals = signals.map((signal) => ({
      ...signal,
      pvalue: parseFloat(signal.pvalue),
      ols_const: parseFloat(signal.ols_const),
      ols_coeff: parseFloat(signal.ols_coeff),
      r_squared: parseFloat(signal.r_squared),
      key_score: parseFloat(signal.key_score),
    }));
    return new Response(JSON.stringify(formattedSignals), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to retrieve" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}

// export const config = {
//   api: {
//     bodyParser: {
//       sizeLimit: "1mb",
//     },
//   },
//   // Specifies the maximum allowed duration for this function to execute (in seconds)
//   maxDuration: 5,
// };
