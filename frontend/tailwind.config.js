/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1e40af',
          hover: '#1e3a8a',
          light: '#3b82f6',
        },
        secondary: {
          DEFAULT: '#059669',
          hover: '#047857',
        },
        accent: {
          DEFAULT: '#f59e0b',
        },
        background: {
          light: '#ffffff',
          dark: '#0f172a',
        },
        surface: {
          light: '#f9fafb',
          dark: '#1e293b',
        },
        text: {
          primary: {
            light: '#111827',
            dark: '#f1f5f9',
          },
          secondary: {
            light: '#6b7280',
            dark: '#94a3b8',
          },
        },
        border: {
          light: '#e5e7eb',
          dark: '#334155',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
