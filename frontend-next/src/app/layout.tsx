'use client'

import './globals.css';
import { Inter } from 'next/font/google';
import { SessionProvider , SessionProviderProps} from 'next-auth/react';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Spotify Reccomender',
  description: 'Get Songs Recommended by Spotify',
};

export interface LayoutProps extends SessionProviderProps {
  children: React.ReactNode;
}

export default function RootLayout({
  children,
  session,

}: LayoutProps) {
  return (
    <html lang="en" className='h-full'>
      <SessionProvider session={session}>
        <body className={inter.className + ' h-full'}>{children} </body>
      </SessionProvider>
    </html>
  );
}
