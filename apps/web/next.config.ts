import type { NextConfig } from "next";
import path from "node:path";

const config: NextConfig = {
  async redirects() {
    return [
      { source: "/curriculum", destination: "/ai-ml", permanent: false },
      {
        source: "/library/companies/:slug",
        destination: "/companies/:slug",
        permanent: false,
      },
      ...["q", "track", "saved"].map((key) => ({
        source: "/",
        has: [{ type: "query" as const, key }],
        destination: "/ai-ml",
        permanent: false,
      })),
    ];
  },
  outputFileTracingRoot: path.join(process.cwd(), "../.."),
  outputFileTracingIncludes: {
    "/*": ["../../content/**/*"],
    "/legacy/[[...path]]": ["../../generated/legacy/**/*"],
  },
  devIndicators: false,
  agentRules: false,
};
export default config;
