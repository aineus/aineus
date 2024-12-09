'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { Settings, LogOut, Menu, Newspaper, Library } from 'lucide-react'
import { cn } from '@/lib/utils'

const NAVIGATION_ITEMS = [
  {
    href: '/news',
    label: 'News',
    icon: Newspaper,
  },
  {
    href: '/prompts',
    label: 'Prompts',
    icon: Library,
  },
  {
    href: '/settings',
    label: 'Settings',
    icon: Settings,
  },
]

export function Header() {
  const { user, logout } = useAuth()
  const pathname = usePathname()

  if (pathname === '/' || pathname.startsWith('/auth')) {
    return null
  }

  return (
    <>
      {/* Desktop Side Navigation */}
      <header className="hidden md:flex fixed left-0 top-0 bottom-0 w-64 border-r bg-background flex-col z-50">
        <div className="p-6">
          <Link href="/news" className="text-2xl font-bold">
            AINeus
          </Link>
        </div>

        {user && (
          <div className="flex flex-col flex-1 p-4">
            {/* Main Navigation */}
            <div className="flex-1 space-y-2">
              {NAVIGATION_ITEMS.map((item) => {
                const Icon = item.icon
                const isActive = pathname.startsWith(item.href)
                
                return (
                  <Button 
                    key={item.href}
                    variant={isActive ? "default" : "ghost"}
                    size="lg"
                    asChild
                    className={cn(
                      "w-full justify-start text-base",
                      isActive && "bg-primary"
                    )}
                  >
                    <Link href={item.href}>
                      <Icon className="w-5 h-5 mr-3" />
                      {item.label}
                    </Link>
                  </Button>
                )
              })}
            </div>

            {/* Logout Button */}
            <Button 
              variant="ghost"
              size="lg"
              onClick={logout}
              className="w-full justify-start text-base text-red-600 hover:text-red-700 hover:bg-red-50 mt-4"
            >
              <LogOut className="w-5 h-5 mr-3" />
              Logout
            </Button>
          </div>
        )}
      </header>

      {/* Mobile Top Navigation */}
      <header className="md:hidden fixed top-0 left-0 right-0 h-20 border-b bg-background z-50">
        <div className="flex h-full items-center justify-between px-6">
          <Link href="/news" className="text-2xl font-bold">
            AINeus
          </Link>

          {user && (
            <Button variant="ghost" size="lg" asChild>
              <Link href="/settings">
                <Settings className="w-6 h-6" />
              </Link>
            </Button>
          )}
        </div>

        {/* Mobile Bottom Navigation */}
        {user && (
          <div className="fixed bottom-0 left-0 right-0 border-t bg-background">
            <div className="flex justify-around p-4">
              {NAVIGATION_ITEMS.slice(0, 2).map((item) => {
                const Icon = item.icon
                const isActive = pathname.startsWith(item.href)
                
                return (
                  <Button
                    key={item.href}
                    variant="ghost"
                    size="lg"
                    asChild
                    className={cn(
                      "flex-1 mx-1",
                      isActive && "bg-accent"
                    )}
                  >
                    <Link href={item.href}>
                      <Icon className="w-5 h-5" />
                    </Link>
                  </Button>
                )
              })}
            </div>
          </div>
        )}
      </header>

      {/* Content Padding */}
      <div className="md:pl-64">
        {/* Your page content goes here */}
      </div>
    </>
  )
}