'use client'

import { NewsCard } from './news-card';
import { Skeleton } from '@/components/ui/skeleton';

type NewsItem = {
  id: string;
  title: string;
  content: string;
  summary: string;
  source: string;
  publishedAt: string;
  url: string;
};

interface NewsListProps {
  news: NewsItem[];
  isLoading?: boolean;
  error?: string;
}

export function NewsList({ news, isLoading, error }: NewsListProps) {
  if (error) {
    return (
      <div className="text-center py-8 text-red-500">
        {error}
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <NewsCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (news.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No news articles found.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {news.map((item) => (
        <NewsCard key={item.id} news={item} />
      ))}
    </div>
  );
}

function NewsCardSkeleton() {
  return (
    <div className="p-4 border rounded-lg space-y-3">
      <Skeleton className="h-6 w-3/4" />
      <Skeleton className="h-4 w-1/4" />
      <Skeleton className="h-20 w-full" />
    </div>
  );
}