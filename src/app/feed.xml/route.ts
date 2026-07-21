import { getAllPosts, getPostBySlug } from '@/lib/blog';
import { SITE_URL, SITE_NAME, AUTHOR } from '@/lib/site';

export const dynamic = 'force-static';

function escapeXml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

export async function GET() {
  const posts = await Promise.all(
    getAllPosts().map((post) => getPostBySlug(post.slug))
  );

  const items = posts
    .map((post) => {
      const url = `${SITE_URL}/blog/${post.slug}`;
      // RSS has no base-URL semantics: site-relative asset URLs break in feed
      // readers, and a literal ]]> in post content would terminate the CDATA
      // section and corrupt the whole feed.
      const contentHtml = post.content
        .replace(/(src|href)="\//g, `$1="${SITE_URL}/`)
        .replaceAll(']]>', ']]]]><![CDATA[>');
      return `    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${new Date(post.date).toUTCString()}</pubDate>
      <description>${escapeXml(post.excerpt)}</description>
      <content:encoded><![CDATA[${contentHtml}]]></content:encoded>
    </item>`;
    })
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${SITE_NAME}</title>
    <link>${SITE_URL}</link>
    <atom:link href="${SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Posts on software engineering, AI, and agents by ${AUTHOR}.</description>
    <language>en</language>
${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
  });
}
