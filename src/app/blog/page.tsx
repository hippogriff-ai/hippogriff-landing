import Navbar from '@/components/Navbar';
import BlogCard from '@/components/BlogCard';
import Footer from '@/components/Footer';
import { getAllPosts } from '@/lib/blog';

export default function BlogListing() {
  const posts = getAllPosts();

  return (
    <main>
      <Navbar />
      <div className="blog-listing">
        <h1 className="blog-listing-title">Writing</h1>
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
