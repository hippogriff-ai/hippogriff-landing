import type { Metadata } from 'next';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import BackButton from '@/components/BackButton';
import BlogContent from '@/components/BlogContent';
import { getPostBySlug, getAllSlugs } from '@/lib/blog';
import { SITE_URL, SITE_NAME, AUTHOR, FEED_ALTERNATE } from '@/lib/site';

export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `/blog/${slug}`,
      types: FEED_ALTERNATE,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.date,
      url: `/blog/${slug}`,
      siteName: SITE_NAME,
      authors: [AUTHOR],
    },
  };
}

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.excerpt,
    datePublished: post.date,
    dateModified: post.date,
    url: `${SITE_URL}/blog/${slug}`,
    mainEntityOfPage: `${SITE_URL}/blog/${slug}`,
    author: {
      '@type': 'Person',
      name: AUTHOR,
      url: SITE_URL,
    },
  };

  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Navbar />
      <article className="blog-post">
        <BackButton />
        <h1 className="blog-post-title">{post.title}</h1>
        <div className="blog-post-date">{post.date}</div>
        <BlogContent html={post.content} />
      </article>
      <Footer />
    </main>
  );
}
