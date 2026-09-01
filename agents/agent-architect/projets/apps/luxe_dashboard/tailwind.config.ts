import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        luxe: {
          gold: "#D4AF37",
          emerald: "#50C878",
          ruby: "#E0115F",
          onyx: "#0F0F0F",
          zinc: "#18181B",
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      boxShadow: {
        'luxe-gold': '0 0 20px rgba(212, 175, 55, 0.2)',
        'luxe-emerald': '0 0 20px rgba(80, 200, 120, 0.2)',
      }
    },
  },
  plugins: [],
};
export default config;
