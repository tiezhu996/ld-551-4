import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    chunkSizeWarningLimit: 1200,
    rolldownOptions: {
      onLog(level, log, handler) {
        if (
          log.code === 'INVALID_ANNOTATION' &&
          log.id?.includes('@vueuse/core')
        ) {
          return
        }
        handler(level, log)
      }
    }
  },
  server: {
    port: 38401,
    proxy: {
      '/api': {
        target: 'http://localhost:38501',
        changeOrigin: true
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
