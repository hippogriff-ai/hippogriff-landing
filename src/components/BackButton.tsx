'use client';

import { useRouter } from 'next/navigation';

export default function BackButton() {
  const router = useRouter();

  return (
    <button
      className="blog-post-back"
      aria-label="Go back to previous page"
      onClick={() => {
        if (document.referrer && new URL(document.referrer).origin === window.location.origin) {
          router.back();
        } else {
          router.push('/blog');
        }
      }}
    >
      &larr; Back
    </button>
  );
}
