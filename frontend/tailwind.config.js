/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        clario: {
          50: '#f0f7eb',
          100: '#dcecd9',
          200: '#b8dfa6',
          300: '#8cc975',
          400: '#5fbf4d',
          500: '#43ad61',
          600: '#3aa053',
          700: '#2e7a40',
          800: '#265f30',
          900: '#1d4a26',
          950: '#0f2613',
        },
      },
    },
  },
  plugins: [],
}
