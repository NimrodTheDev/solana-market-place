import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': {},
  },
  resolve: {
    alias: {
      process: "process/browser",
      stream: "stream-browserify",
      zlib: "browserify-zlib",
      util: 'util',
      buffer: 'buffer',
      'bn.js': 'bn.js'
    }
  },
  optimizeDeps: {
    include: ["buffer", "bn.js"],
    esbuildOptions: {
      define: {
        global: 'globalThis'
      }
    }
  }
}) 