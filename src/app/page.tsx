import fs from 'fs';
import path from 'path';
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
];

function getAboutParagraphs(): string[] {
  const filePath = path.join(process.cwd(), 'content/about.md');
  const raw = fs.readFileSync(filePath, 'utf8').trim();
  return raw.split(/\n\s*\n/).filter(Boolean);
}

export default function Home() {
  const aboutParagraphs = getAboutParagraphs();

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
        <div className="about-text">
          {aboutParagraphs.map((para, i) => (
            <p key={i}>{para}</p>
          ))}
        </div>
      </section>

      <Footer />
    </main>
  );
}
