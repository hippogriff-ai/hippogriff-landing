'use client';

import { useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';
import { initAmplitude, trackPageView, trackPageExit } from '@/lib/amplitude';

export default function AmplitudeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const enterTimeRef = useRef<number>(Date.now());
  const prevPathRef = useRef<string>(pathname);

  // Init on mount
  useEffect(() => {
    initAmplitude();
    trackPageView(pathname);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Track on route change
  useEffect(() => {
    if (prevPathRef.current !== pathname) {
      const duration = (Date.now() - enterTimeRef.current) / 1000;
      trackPageExit(prevPathRef.current, duration);
      trackPageView(pathname);
      enterTimeRef.current = Date.now();
      prevPathRef.current = pathname;
    }
  }, [pathname]);

  // Track exit on unload
  useEffect(() => {
    const handleBeforeUnload = () => {
      const duration = (Date.now() - enterTimeRef.current) / 1000;
      trackPageExit(prevPathRef.current, duration);
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, []);

  return <>{children}</>;
}
