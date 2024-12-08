import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface NewsCardProps {
  title: string;
  summary: string;
  date: string;
  source: string;
}

export function NewsCard({ title, summary, date, source }: NewsCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <p className="text-sm text-gray-500">{source} • {date}</p>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600">{summary}</p>
      </CardContent>
      <CardFooter className="space-x-2">
        <Button size="sm">Read More</Button>
        <Button size="sm" variant="outline">Transform</Button>
      </CardFooter>
    </Card>
  )
}