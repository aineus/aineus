import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ClientProviders } from '@/components/providers/client-provider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MyNeos - AI-Powered News',
  description: 'Personalized news with customizable AI prompts',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ClientProviders>
          <main className="min-h-screen bg-gray-50">
            {children}
          </main>
        </ClientProviders>
      </body>
    </html>
  )
}