import * as amplitude from '@amplitude/analytics-browser';

let initialized = false;

export function initAmplitude() {
  const apiKey = process.env.NEXT_PUBLIC_AMPLITUDE_API_KEY;
  if (!apiKey || initialized) return;

  amplitude.init(apiKey, {
    autocapture: false,
  });
  initialized = true;
}

export function trackPageView(pagePath: string, pageTitle?: string) {
  if (!initialized) return;
  amplitude.track('page_view', {
    page_path: pagePath,
    page_title: pageTitle ?? document.title,
  });
}

export function trackPageExit(pagePath: string, durationSeconds: number) {
  if (!initialized) return;
  amplitude.track('page_exit', {
    page_path: pagePath,
    duration_seconds: Math.round(durationSeconds),
  });
}

export function trackLinkClick(destination: string, sourcePage: string) {
  if (!initialized) return;
  amplitude.track('link_click', {
    destination,
    source_page: sourcePage,
  });
}
