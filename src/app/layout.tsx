import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import AmplitudeProvider from '@/components/AmplitudeProvider';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  metadataBase: new URL('https://hippogriff.io'),
  title: {
    default: 'Hippogriff',
    template: '%s | Hippogriff',
  },
  description:
    'Hippogriff is Vicki Zhang\u2019s workshop \u2014 a home for games, agents, and experiments at the intersection of design and engineering.',
  openGraph: {
    title: 'Hippogriff',
    description:
      'Games, agents, and experiments by Vicki Zhang.',
    url: 'https://hippogriff.io',
    siteName: 'Hippogriff',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Hippogriff',
    description:
      'Games, agents, and experiments by Vicki Zhang.',
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
