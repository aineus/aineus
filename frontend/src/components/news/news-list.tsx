import { NewsCard } from './news-card'

// Temporary mock data
const mockNews = [
  {
    title: "Example News Article",
    summary: "This is a sample news article summary to demonstrate the layout.",
    date: "Dec 8, 2024",
    source: "MyNeos"
  }
]

export function NewsList() {
  return (
    <div className="space-y-4">
      {mockNews.map((news, index) => (
        <NewsCard key={index} {...news} />
      ))}
    </div>
  )
}