/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/templates/**/*.html",
  ],
  theme: {
    // Overridden (not extended) so oversized defaults like rounded-2xl/3xl
    // simply don't exist — the brief calls for restrained radius throughout.
    borderRadius: {
      none: "0px",
      sm: "4px",
      DEFAULT: "6px",
      md: "6px",
      lg: "8px",
      full: "9999px",
    },
    extend: {
      colors: {
        navy: {
          950: "rgb(var(--color-navy-950) / <alpha-value>)",
          800: "rgb(var(--color-navy-800) / <alpha-value>)",
        },
        accent: {
          DEFAULT: "rgb(var(--color-accent) / <alpha-value>)",
          dark: "rgb(var(--color-accent-dark) / <alpha-value>)",
        },
        ink: "rgb(var(--color-ink) / <alpha-value>)",
        gray: {
          50: "rgb(var(--color-gray-50) / <alpha-value>)",
          200: "rgb(var(--color-gray-200) / <alpha-value>)",
          500: "rgb(var(--color-gray-500) / <alpha-value>)",
        },
      },
      fontFamily: {
        sans: ["Inter", '"IBM Plex Sans"', "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
