/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        base: {
          950: "#080B14",
          900: "#0B0F1A",
          850: "#0E1320",
          800: "#121828",
          700: "#1A2236",
          600: "#232D45",
          500: "#2E3A57",
        },
        accent: {
          blue: "#5B8DEF",
          indigo: "#6366F1",
          violet: "#8B5CF6",
          purple: "#A855F7",
          green: "#22C55E",
          amber: "#F59E0B",
          orange: "#F97316",
        },
      },
      boxShadow: {
        card: "0 1px 0 0 rgba(255,255,255,0.03) inset, 0 8px 24px -12px rgba(0,0,0,0.6)",
        glow: "0 0 0 1px rgba(91,141,239,0.15), 0 8px 30px -8px rgba(91,141,239,0.25)",
      },
      backgroundImage: {
        "grid-fade":
          "linear-gradient(to bottom, rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(to right, rgba(255,255,255,0.025) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};
