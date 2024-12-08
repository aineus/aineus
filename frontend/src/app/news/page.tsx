'use client'

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { newsApi } from '@/lib/api';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { NewsCard } from '@/components/news/news-card';
import { useAuth } from '@/contexts/AuthContext';

const CATEGORIES = ['All', 'Technology', 'Business', 'Politics', 'Science'];

export default function NewsPage() {
  const { user } = useAuth();
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [page, setPage] = useState(1);
  const limit = 10;

  const { data, isLoading, error } = useQuery({
    queryKey: ['news', selectedCategory, page],
    queryFn: () => newsApi.getNews({
      skip: (page - 1) * limit,
      limit,
      category: selectedCategory === 'All' ? undefined : selectedCategory.toLowerCase(),
    }),
  });

  if (!user) {
    return <div>Please login to view news</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">Latest News</h1>

      {/* Categories */}
      <Card className="p-4">
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? "default" : "outline"}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </Button>
          ))}
        </div>
      </Card>

      {/* News List */}
      <div className="space-y-4">
        {isLoading ? (
          <div>Loading...</div>
        ) : error ? (
          <div>Error loading news</div>
        ) : data?.items?.length ? (
          data.items.map((news: any) => (
            <NewsCard
              key={news.id}
              news={news}
            />
          ))
        ) : (
          <div>No news found</div>
        )}
      </div>

      {/* Pagination */}
      <div className="flex justify-center gap-2">
        <Button
          variant="outline"
          disabled={page === 1}
          onClick={() => setPage(p => p - 1)}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </Button>
      </div>
    </div>
  );
}