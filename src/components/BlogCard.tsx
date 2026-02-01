import Link from 'next/link';

interface BlogCardProps {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
}

export default function BlogCard({ slug, title, date, excerpt }: BlogCardProps) {
  return (
    <Link href={`/blog/${slug}`} className="blog-card">
      <div className="blog-card-title">{title}</div>
      <div className="blog-card-date">{date}</div>
      <div className="blog-card-excerpt">{excerpt}</div>
    </Link>
  );
}
