import fs from 'fs';
import path from 'path';
import type { Metadata } from 'next';
import { remark } from 'remark';
import html from 'remark-html';
import Navbar from '@/components/Navbar';
import Header from '@/components/Header';
import ProjectCard from '@/components/ProjectCard';
import BlogPreview from '@/components/BlogPreview';
import Footer from '@/components/Footer';
import { SITE_URL, SITE_NAME, AUTHOR, FEED_ALTERNATE } from '@/lib/site';

export const metadata: Metadata = {
  alternates: {
    canonical: '/',
    types: FEED_ALTERNATE,
  },
};

const PROJECTS = [
  {
    name: 'Remo',
    desc: 'LiDAR-powered room redesign agent with shopping list support',
    url: 'https://github.com/hippogriff-ai/remo',
    hasAnimation: false,
    image: '/remo.png',
    cta: 'View',
  },
  {
    name: 'TypeCraft',
    desc: 'A Space Invaders typing game that makes you faster',
    url: 'https://typecraft.hippogriff.io',
    hasAnimation: true,
  },
  {
    name: 'Talent Promo',
    desc: 'Resume writing agent that discovers your hidden strengths',
    url: 'https://talent-promo.hippogriff.io',
    hasAnimation: false,
    image: '/talent-promo.png',
    cta: 'Try',
  },
];

async function getAboutHtml(): Promise<string> {
  const filePath = path.join(process.cwd(), 'content/about.md');
  const raw = fs.readFileSync(filePath, 'utf8').trim();
  const processed = await remark().use(html).process(raw);
  return processed.toString();
}

export default async function Home() {
  const aboutHtml = await getAboutHtml();

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebSite',
        name: SITE_NAME,
        url: SITE_URL,
      },
      {
        '@type': 'Person',
        name: AUTHOR,
        url: SITE_URL,
        jobTitle: 'Senior Full Stack Software Engineer',
        sameAs: ['https://github.com/hippogriff-ai'],
      },
    ],
  };

  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Navbar />
      <Header />

      <section className="projects" id="projects">
        <div className="projects-label">projects</div>
        <div className="projects-grid">
          {PROJECTS.map((proj) => (
            <ProjectCard key={proj.name} {...proj} />
          ))}
        </div>
      </section>

      <BlogPreview />

      <section className="about" id="about">
        <div className="about-label">about</div>
        <div
          className="about-text"
          dangerouslySetInnerHTML={{ __html: aboutHtml }}
        />
      </section>

      <Footer />
    </main>
  );
}
