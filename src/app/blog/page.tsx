import type { Metadata } from 'next';
import Navbar from '@/components/Navbar';
import BlogCard from '@/components/BlogCard';
import Footer from '@/components/Footer';
import { getAllPosts } from '@/lib/blog';
import { SITE_NAME, FEED_ALTERNATE } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Blog',
  description: 'Posts on AI agents, software engineering, and building things, by Vicki Zhang.',
  alternates: {
    canonical: '/blog',
    types: FEED_ALTERNATE,
  },
  openGraph: {
    title: 'Blog',
    description: 'Posts on AI agents, software engineering, and building things, by Vicki Zhang.',
    url: '/blog',
    siteName: SITE_NAME,
    type: 'website',
  },
};

export default function BlogListing() {
  const posts = getAllPosts();

  return (
    <main>
      <Navbar />
      <div className="blog-listing">
        <h1 className="blog-listing-title">Blog</h1>
        <div className="blog-listing-grid">
          {posts.map((post) => (
            <BlogCard
              key={post.slug}
              slug={post.slug}
              title={post.title}
              date={post.date}
              excerpt={post.excerpt}
            />
          ))}
        </div>
      </div>
      <Footer />
    </main>
  );
}
