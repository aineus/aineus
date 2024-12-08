'use client'

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { newsApi, promptsApi } from '@/lib/api';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { NewsList } from '@/components/news/news-list';
import { useAuth } from '@/contexts/AuthContext';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';

export default function NewsPage() {
  const { user } = useAuth();
  const [selectedPromptId, setSelectedPromptId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const limit = 10;

  // Fetch prompts
  const { data: prompts, isLoading: isLoadingPrompts } = useQuery({
    queryKey: ['prompts'],
    queryFn: () => promptsApi.getPrompts(),
    enabled: !!user,
  });

  // Set first prompt as default when prompts are loaded
  useEffect(() => {
    if (prompts?.length && !selectedPromptId) {
      setSelectedPromptId(prompts[0].id);
    }
  }, [prompts]);

  // Fetch news for selected prompt
  const { data: news, isLoading: isLoadingNews, error } = useQuery({
    queryKey: ['prompt-news', selectedPromptId, page],
    queryFn: () => newsApi.getPromptNews({
      promptId: selectedPromptId!,
      skip: (page - 1) * limit,
      limit,
    }),
    enabled: !!selectedPromptId,
  });

  if (!user) {
    return <div className="p-8 text-center">Please login to view news</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      {/* Prompts Selector */}
      <Card className="p-4">
        {isLoadingPrompts ? (
          <div className="flex gap-2">
            {[...Array(3)].map((_, i) => (
              <Skeleton key={i} className="h-10 w-24" />
            ))}
          </div>
        ) : prompts?.length ? (
          <ScrollArea className="w-full whitespace-nowrap">
            <div className="flex space-x-2">
              {prompts.map((prompt) => (
                <Button
                  key={prompt.id}
                  variant={selectedPromptId === prompt.id ? "default" : "outline"}
                  onClick={() => setSelectedPromptId(prompt.id)}
                  className="flex-shrink-0"
                >
                  {prompt.name}
                </Button>
              ))}
            </div>
            <ScrollBar orientation="horizontal" />
          </ScrollArea>
        ) : (
          <div className="text-center py-2 text-gray-500">
            No prompts found. Create your first prompt newspaper.
          </div>
        )}
      </Card>

      {/* News List */}
      <NewsList 
        news={news?.items || []}
        isLoading={isLoadingNews}
        error={error?.message}
      />

      {/* Pagination */}
      {news?.items?.length > 0 && (
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
            disabled={news?.items?.length < limit}
            onClick={() => setPage(p => p + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}