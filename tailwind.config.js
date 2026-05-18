/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js"],
  theme: {
    extend: {
      colors: {
        primary: '#0ea5e9',
        secondary: '#10b981',
        emergency: '#ef4444',
        warning: '#f59e0b',
      },
    },
  },
  plugins: [],
}
