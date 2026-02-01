import InvaderCanvas from './InvaderCanvas';

interface ProjectCardProps {
  name: string;
  desc: string;
  url: string;
  hasAnimation?: boolean;
}

export default function ProjectCard({ name, desc, url, hasAnimation }: ProjectCardProps) {
  return (
    <div className="project-card">
      <div className="project-card-visual">
        {hasAnimation && <InvaderCanvas />}
      </div>
      <div className="project-card-body">
        <div className="project-card-name">{name}</div>
        <div className="project-card-desc">{desc}</div>
        <a href={url} className="project-card-cta" target="_blank" rel="noopener noreferrer">
          Play
        </a>
      </div>
    </div>
  );
}
