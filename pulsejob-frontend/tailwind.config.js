/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      colors: {
        bg: '#0f0f0f',
        surface: '#141414',
        border: '#1a1a1a',
        muted: '#444444',
        subtle: '#888888',
        primary: '#e8e8e8',
      }
    },
  },
  plugins: [],
}