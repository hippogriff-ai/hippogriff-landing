import Link from 'next/link';
import { getLatestPosts } from '@/lib/blog';
import BlogCard from './BlogCard';

export default function BlogPreview() {
  const posts = getLatestPosts(4);

  return (
    <section className="blog-section">
      <div className="blog-header">
        <div className="blog-label">blog</div>
        <Link href="/blog" className="blog-more">
          See more &rarr;
        </Link>
      </div>
      <div className="blog-deck">
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
    </section>
  );
}
