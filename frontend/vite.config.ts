import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    react(),
    viteCompression(),
  ],
  resolve: {
    dedupe: ['react', 'react-dom'],
  },
})