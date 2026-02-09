import fs from 'fs';
import path from 'path';
import { remark } from 'remark';
import html from 'remark-html';
import Navbar from '@/components/Navbar';
import Header from '@/components/Header';
import ProjectCard from '@/components/ProjectCard';
import BlogPreview from '@/components/BlogPreview';
import Footer from '@/components/Footer';

const PROJECTS = [
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

  return (
    <main>
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
