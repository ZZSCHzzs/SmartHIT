import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import VueDevTools from 'vite-plugin-vue-devtools';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true, // 监听所有网络接口，相当于 0.0.0.0
    port: 3000, // 自定义端口号，可根据需要更改
    proxy: {
      '/today_hit': {
        target: 'http://today.hit.edu.cn',  // 目标服务器
        changeOrigin: true,  // 是否修改源
        rewrite: (path) => path.replace(/^\/today_hit/, ''),  // 路径重写
      },
    },
  },
});
