import type { Metadata } from 'next'
import { Source_Sans_3 } from 'next/font/google'
import './globals.css'
import { ClientProviders } from '@/components/providers/client-provider'
import { AuthProvider } from '@/contexts/AuthContext'
import { Header } from '@/components/layout/header'

const sourceSans = Source_Sans_3({ 
  subsets: ['latin'],
  variable: '--font-sans'
})

export const metadata: Metadata = {
  title: 'AINeus - Your AI-Powered News',
  description: 'Reclaim your newspaper with customizable AI prompts',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${sourceSans.variable} font-sans`}>
        <ClientProviders>
          <AuthProvider>
            <div className="flex min-h-screen">
              <Header />
              <main className="flex-1">
                {/* For mobile screens */}
                <div className="md:hidden h-16" />
                <div className="p-6">
                  {children}
                </div>
              </main>
            </div>
          </AuthProvider>
        </ClientProviders>
      </body>
    </html>
  )
}