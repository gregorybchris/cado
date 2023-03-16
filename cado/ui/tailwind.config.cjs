/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#121214",
        rock: "#2c3038",
        "black-rock": "#1d1f23",
        "dark-rock": "#22252a",
        "light-rock": "#333742",
        "lighter-rock": "#464c5b",
      },
    },
    fontFamily: {
      sen: "Sen",
      poppins: "Poppins",
    },
  },
  plugins: [],
};
