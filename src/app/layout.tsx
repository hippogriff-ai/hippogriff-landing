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
    'Hippogriff is Vicki Zhang\u2019s site for things made on the journey of reimagining human & app interaction \u2014 agents, games, and experiments powered by AI.',
  openGraph: {
    title: 'Hippogriff',
    description:
      'Agents, games, and experiments by Vicki Zhang \u2014 reimagining human & app interaction.',
    url: 'https://hippogriff.io',
    siteName: 'Hippogriff',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Hippogriff',
    description:
      'Agents, games, and experiments by Vicki Zhang \u2014 reimagining human & app interaction.',
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
