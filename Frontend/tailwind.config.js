export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          blue: '#0066FF',
          green: '#00D68F',
          black: '#0A0E27',
        },
        secondary: {
          blue: '#004DBF',
          green: '#00B377',
          black: '#1A1F3A',
        },
        accent: {
          blue: '#00A3FF',
        },
        light: {
          blue: '#E6F2FF',
          green: '#E6FFF5',
          gray: '#F5F7FA',
        },
        dark: {
          gray: '#2D3348',
        },
        error: '#FF3B5C',
        warning: '#FFB800',
        text: {
          primary: '#0A0E27',
          secondary: '#6B7280',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Poppins', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}
