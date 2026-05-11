import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    category: z.enum([
      'EAA',
      'AX-readiness',
      'AI Ops',
      'Site Factory',
      'MCP-Commerce',
      'Case Study',
      'CENTAUR',
    ]),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    draft: z.boolean().default(false),
    // For schema.org Article structured data — boosts AI engine citations
    author: z.string().default('Chris Conen'),
    readingTime: z.number().optional(),
  }),
});

export const collections = { blog };
