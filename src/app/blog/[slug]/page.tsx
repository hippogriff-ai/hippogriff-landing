import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { getPostBySlug, getAllSlugs } from '@/lib/blog';
import Link from 'next/link';

export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  return (
    <main>
      <Navbar />
      <article className="blog-post">
        <Link href="/blog" className="blog-post-back">
          &larr; Back to writing
        </Link>
        <h1 className="blog-post-title">{post.title}</h1>
        <div className="blog-post-date">{post.date}</div>
        <div
          className="blog-post-content"
          dangerouslySetInnerHTML={{ __html: post.content }}
        />
      </article>
      <Footer />
    </main>
  );
}
