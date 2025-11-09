/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pastel-sky': '#e6f7ff',
        'pastel-purple': '#f3e8ff',
        'pastel-mint': '#ecfdf5',
      }
    },
  },
  plugins: [],
}