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
  }, [html]);

  return (
    <div
      ref={ref}
      className="blog-post-content"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
