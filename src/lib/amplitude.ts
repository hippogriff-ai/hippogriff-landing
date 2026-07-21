import * as amplitude from '@amplitude/analytics-browser';

const SITE_NAME = 'hippogriff-landing';
let initialized = false;

const AI_REFERRER_HOSTS: Record<string, string> = {
  'chatgpt.com': 'chatgpt',
  'chat.openai.com': 'chatgpt',
  'claude.ai': 'claude',
  'perplexity.ai': 'perplexity',
  'copilot.microsoft.com': 'copilot',
  'gemini.google.com': 'gemini',
};

function getAiSource(): string | null {
  if (!document.referrer) return null;
  try {
    const host = new URL(document.referrer).hostname.replace(/^www\./, '');
    return AI_REFERRER_HOSTS[host] ?? null;
  } catch {
    return null;
  }
}

export function initAmplitude() {
  const apiKey = process.env.NEXT_PUBLIC_AMPLITUDE_API_KEY;
  if (!apiKey || initialized) return;

  amplitude.init(apiKey, {
    autocapture: false,
  });
  initialized = true;

  const aiSource = getAiSource();
  if (aiSource) {
    const identify = new amplitude.Identify().setOnce(
      'initial_ai_source',
      aiSource
    );
    amplitude.identify(identify);
  }
}

export function trackPageView(pagePath: string, pageTitle?: string) {
  if (!initialized) return;
  const aiSource = getAiSource();
  amplitude.track('page_view', {
    site: SITE_NAME,
    page_path: pagePath,
    page_title: pageTitle ?? document.title,
    referrer: document.referrer || undefined,
    ...(aiSource ? { ai_source: aiSource } : {}),
  });
}

export function trackPageExit(pagePath: string, durationSeconds: number) {
  if (!initialized) return;
  amplitude.track('page_exit', {
    site: SITE_NAME,
    page_path: pagePath,
    duration_seconds: Math.round(durationSeconds),
  });
}

export function trackLinkClick(destination: string, sourcePage: string) {
  if (!initialized) return;
  amplitude.track('link_click', {
    site: SITE_NAME,
    destination,
    source_page: sourcePage,
  });
}
