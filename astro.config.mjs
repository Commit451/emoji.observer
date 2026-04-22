import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://emoji.observer',
  base: '/',
  output: 'static',
  vite: {
    server: {
      allowedHosts: ['grindavik', '192.168.86.155', '100.82.99.58'],
    },
  },
});
