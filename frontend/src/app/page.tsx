import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-32px)] p-4">
      <div className="text-center space-y-8 max-w-2xl">
        <h1 className="text-4xl font-normal mb-4">
          Welcome to WhatsNews
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Reclaim your newspapers. Transform how you read news with customizable AI prompts.
        </p>
        <div className="space-x-4">
          <Link href="/auth/login">
            <Button>Get Started</Button>
          </Link>
          <Link href="/about">
            <Button variant="outline">Learn More</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}