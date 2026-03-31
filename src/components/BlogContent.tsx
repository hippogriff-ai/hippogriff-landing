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

    // Click-to-zoom on images (works on both desktop and mobile)
    const images = container.querySelectorAll('img');
    images.forEach((img) => {
      img.style.cursor = 'zoom-in';
      img.style.transition = 'transform 0.2s ease';
      // Prevent mobile browser from intercepting taps for its own zoom
      img.style.touchAction = 'manipulation';
      img.addEventListener('mouseenter', () => { img.style.transform = 'scale(1.02)'; });
      img.addEventListener('mouseleave', () => { img.style.transform = 'scale(1)'; });
      img.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;padding:1rem;touch-action:none;';
        const zoomed = document.createElement('img');
        zoomed.src = img.src;
        zoomed.alt = img.alt;
        // On mobile, allow horizontal scroll for wide screenshots
        zoomed.style.cssText = 'max-width:none;max-height:90vh;object-fit:contain;border-radius:4px;';
        // Wrap in scrollable container for wide images on mobile
        const wrapper = document.createElement('div');
        wrapper.style.cssText = 'overflow:auto;max-width:95vw;max-height:95vh;-webkit-overflow-scrolling:touch;';
        wrapper.appendChild(zoomed);
        overlay.appendChild(wrapper);
        // Close on tap/click outside the image
        overlay.addEventListener('click', (ev) => { if (ev.target === overlay) overlay.remove(); });
        // Close button for mobile
        const close = document.createElement('button');
        close.textContent = '✕';
        close.style.cssText = 'position:absolute;top:1rem;right:1rem;background:none;border:none;color:white;font-size:2rem;cursor:pointer;z-index:10000;padding:0.5rem;';
        close.addEventListener('click', () => overlay.remove());
        overlay.appendChild(close);
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
