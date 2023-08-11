import './globals.css'
import type { Metadata } from 'next'
import Navbar from './components/Navbar'
import MyProfilePic from './components/MyProfilePic'
import Footer from './components/Footer'
import { Analytics } from '@vercel/analytics/react';
import { Toaster } from "@/components/ui/toaster"

export const metadata: Metadata = {
  title: 'College Football - Every Weekend.',
  description: 'Generated by... AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="dark:bg-slate-800 flex flex-col min-h-screen">
        <Navbar />
        <MyProfilePic />
        <main className="flex-grow pb-8">
          {children}
        </main>
        <Toaster />
        <Footer />
        <Analytics />
      </body>
    </html>
  )
}