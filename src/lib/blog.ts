import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import remarkGfm from 'remark-gfm';
import html from 'remark-html';

const postsDirectory = path.join(process.cwd(), 'content/blog');

export interface Post {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  pinned?: boolean;
  image?: string;
  content?: string;
}

// Social-card image: explicit frontmatter `image` wins, else first raster image in the
// post body. SVG is excluded — X and other card processors don't support it.
function resolvePostImage(data: { image?: string }, content: string): string | undefined {
  if (data.image) return data.image;
  for (const match of content.matchAll(/!\[[^\]]*\]\(([^)\s]+)/g)) {
    if (/\.(png|jpe?g|gif|webp)$/i.test(match[1])) return match[1];
  }
  return undefined;
}

export function getAllPosts(): Post[] {
  const filenames = fs.readdirSync(postsDirectory);
  const posts = filenames
    .filter((name) => name.endsWith('.md'))
    .map((filename) => {
      const slug = filename.replace(/\.md$/, '');
      const fullPath = path.join(postsDirectory, filename);
      const fileContents = fs.readFileSync(fullPath, 'utf8');
      const { data, content } = matter(fileContents);

      return {
        slug,
        title: data.title,
        date: data.date,
        excerpt: data.excerpt,
        pinned: data.pinned || false,
        image: resolvePostImage(data, content),
      };
    });

  return posts.sort((a, b) => (a.date > b.date ? -1 : 1));
}

export function getLatestPosts(count: number = 4): Post[] {
  return getAllPosts().slice(0, count);
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

function addHeadingIds(htmlContent: string): string {
  return htmlContent.replace(
    /<(h[23])>(.*?)<\/\1>/g,
    (_match, tag, inner) => {
      const id = slugify(inner);
      return `<${tag} id="${id}">${inner}</${tag}>`;
    }
  );
}

function embedYouTubeUrls(htmlContent: string): string {
  // Match standalone YouTube URLs in their own <p> tag
  // Handles both raw URLs and auto-linked URLs (from remark-gfm)
  return htmlContent.replace(
    /<p>\s*(?:<a href="[^"]*">)?\s*https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)[^\s<]*(?:<\/a>)?\s*<\/p>/g,
    (_match, videoId) => {
      return `<div class="video-embed"><iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
    }
  );
}

export async function getPostBySlug(slug: string): Promise<Post & { content: string }> {
  const fullPath = path.join(postsDirectory, `${slug}.md`);
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);

  const processed = await remark()
    .use(remarkGfm)
    .use(html, { allowDangerousHtml: true })
    .process(content);

  let htmlContent = processed.toString();
  htmlContent = addHeadingIds(htmlContent);
  htmlContent = embedYouTubeUrls(htmlContent);

  return {
    slug,
    title: data.title,
    date: data.date,
    excerpt: data.excerpt,
    pinned: data.pinned || false,
    image: resolvePostImage(data, content),
    content: htmlContent,
  };
}

export function getAllSlugs(): string[] {
  const filenames = fs.readdirSync(postsDirectory);
  return filenames
    .filter((name) => name.endsWith('.md'))
    .map((name) => name.replace(/\.md$/, ''));
}
