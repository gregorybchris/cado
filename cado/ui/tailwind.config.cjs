/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#121214",
        rock: "#292c33",
        "black-rock": "#1d1f23",
        "dark-rock": "#22252a",
        "light-rock": "#2c3039",
      },
    },
    fontFamily: {
      sen: "Sen",
    },
  },
  plugins: [],
};
