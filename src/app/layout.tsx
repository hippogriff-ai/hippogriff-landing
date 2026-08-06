import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import AmplitudeProvider from '@/components/AmplitudeProvider';
import { SITE_URL, AUTHOR } from '@/lib/site';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Hippogriff',
    template: '%s | Hippogriff',
  },
  description:
    'Hippogriff is Vicki Zhang\u2019s site for things made on the journey of reimagining human & app interaction \u2014 agents, games, and experiments powered by AI.',
  authors: [{ name: AUTHOR, url: SITE_URL }],
  creator: AUTHOR,
  alternates: {
    types: {
      'application/rss+xml': '/feed.xml',
    },
  },
  openGraph: {
    title: 'Hippogriff',
    description:
      'Agents, games, and experiments by Vicki Zhang \u2014 reimagining human & app interaction.',
    url: SITE_URL,
    siteName: 'Hippogriff',
    type: 'website',
  },
  twitter: {
    card: 'summary',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.variable}>
        <AmplitudeProvider>{children}</AmplitudeProvider>
      </body>
    </html>
  );
}
