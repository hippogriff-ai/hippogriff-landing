'use client';

import { useEffect, useRef } from 'react';

export default function BlogContent({ html }: { html: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = ref.current;
    if (!container) return;

    // Scroll to hash on mount
    if (window.location.hash) {
      const target = document.getElementById(window.location.hash.slice(1));
      if (target) {
        setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 100);
      }
    }

    // Add anchor links to headings
    const headings = container.querySelectorAll('h2[id], h3[id]');
    headings.forEach((heading) => {
      const anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = `#${heading.id}`;
      anchor.textContent = '#';
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        history.replaceState(null, '', `#${heading.id}`);
        heading.scrollIntoView({ behavior: 'smooth' });
        navigator.clipboard.writeText(window.location.href).catch(() => {});
      });
      heading.appendChild(anchor);
    });

    // Click-to-zoom on images
    const images = container.querySelectorAll('img');
    images.forEach((img) => {
      img.style.cursor = 'zoom-in';
      img.style.transition = 'transform 0.2s ease';
      img.addEventListener('mouseenter', () => { img.style.transform = 'scale(1.02)'; });
      img.addEventListener('mouseleave', () => { img.style.transform = 'scale(1)'; });
      img.addEventListener('click', () => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;padding:2rem;';
        const zoomed = document.createElement('img');
        zoomed.src = img.src;
        zoomed.alt = img.alt;
        zoomed.style.cssText = 'max-width:95vw;max-height:95vh;object-fit:contain;border-radius:4px;';
        overlay.appendChild(zoomed);
        overlay.addEventListener('click', () => overlay.remove());
        document.addEventListener('keydown', function handler(e) {
          if (e.key === 'Escape') { overlay.remove(); document.removeEventListener('keydown', handler); }
        });
        document.body.appendChild(overlay);
      });
    });
  }, [html]);

  return (
    <div
      ref={ref}
      className="blog-post-content"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
