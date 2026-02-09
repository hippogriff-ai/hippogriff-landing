import Image from 'next/image';
import InvaderCanvas from './InvaderCanvas';

interface ProjectCardProps {
  name: string;
  desc: string;
  url: string;
  hasAnimation?: boolean;
  image?: string;
  cta?: string;
}

export default function ProjectCard({ name, desc, url, hasAnimation, image, cta = 'Play' }: ProjectCardProps) {
  return (
    <div className="project-card">
      <div className="project-card-visual">
        {hasAnimation && <InvaderCanvas />}
        {image && (
          <Image
            src={image}
            alt={name}
            fill
            style={{ objectFit: 'cover' }}
          />
        )}
      </div>
      <div className="project-card-body">
        <div className="project-card-name">{name}</div>
        <div className="project-card-desc">{desc}</div>
        <a href={url} className="project-card-cta" target="_blank" rel="noopener noreferrer">
          {cta}
        </a>
      </div>
    </div>
  );
}
