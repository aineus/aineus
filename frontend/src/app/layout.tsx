import type { Metadata } from 'next'
import { Source_Sans_3 } from 'next/font/google'
import './globals.css'
import { ClientProviders } from '@/components/providers/client-provider'
import { AuthProvider } from '@/contexts/AuthContext'

const sourceSans = Source_Sans_3({ 
  subsets: ['latin'],
  variable: '--font-sans'
})

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
      <body className={`${sourceSans.variable} font-sans`}>
        <ClientProviders>
          <AuthProvider>
            <main className="min-h-screen bg-background">
              {children}
            </main>
          </AuthProvider>
        </ClientProviders>
      </body>
    </html>
  )
}