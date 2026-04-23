import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://emoji.observer',
  base: '/',
  output: 'static',
  integrations: [sitemap()],
  vite: {
    server: {
      allowedHosts: ['grindavik', '192.168.86.155', '100.82.99.58', '.ngrok-free.app', '.ngrok.app'],
    },
  },
});
