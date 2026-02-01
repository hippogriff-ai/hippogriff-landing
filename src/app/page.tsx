import Navbar from '@/components/Navbar';
import Header from '@/components/Header';
import ProjectCard from '@/components/ProjectCard';
import BlogPreview from '@/components/BlogPreview';
import Footer from '@/components/Footer';

const PROJECTS = [
  {
    name: 'TypeCraft',
    desc: 'A Space Invaders typing game that finds your weak keys',
    url: 'https://typecraft.hippogriff.io',
    hasAnimation: true,
  },
];

export default function Home() {
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

      <Footer />
    </main>
  );
}
