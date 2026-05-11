import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime());

  return rss({
    title: 'Conen Digital Blog',
    description:
      'Webfejlesztés, AI Ops, EAA megfelelés, AX-readiness — szakmai cikkek a CENTAUR keretrendszerből.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.publishedAt,
      description: post.data.summary,
      link: `/blog/${post.id.replace(/\.md$/, '')}/`,
      categories: [post.data.category, ...post.data.tags],
      author: post.data.author,
    })),
    customData: '<language>hu-hu</language>',
    stylesheet: false,
  });
}
