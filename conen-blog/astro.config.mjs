// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://conendigital.hu',
  base: '/blog',
  trailingSlash: 'ignore',
  integrations: [
    sitemap({
      // Generates /blog/sitemap-index.xml
      changefreq: 'weekly',
      priority: 0.7,
    }),
  ],
  build: {
    // Output to dist/ at project root, content lives under /blog/ on the domain.
    format: 'directory',
  },
  output: 'static',
});
