import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The watcher serves everything under /static (FastAPI StaticFiles mount) and returns the
// built index.html at "/". So base = /static/ and the build lands in the repo's static/ dir,
// which deploy.sh already tars to Frankfurt. `npm run dev` proxies /api to the live backend.
export default defineConfig({
  plugins: [react()],
  base: '/static/',
  build: {
    outDir: '../static',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8765',
    },
  },
})
