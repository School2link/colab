/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./packages/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        impact: ["Impact", "sans-serif"],
        montserrat: ["Montserrat", "sans-serif"],
        syne: ["Syne", "sans-serif"],
      },
    },
  },
  plugins: [],
};
