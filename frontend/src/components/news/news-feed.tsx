import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { NewsFilters } from './news-filters';
import { NewsCard } from './news-card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { RefreshCw, Filter, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { newsApi } from '@/lib/api';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface NewsItem {
  id: number;
  title: string;
  content: string;
  summary: string;
  source: string;
  url: string;
  published_at: string;
  author: string;
  image_url: string;
  transformed_content?: string;
  relevance_score: number;
}

const NewsFeed = () => {
  const [showFilters, setShowFilters] = React.useState(false);
  const [activePrompt, setActivePrompt] = React.useState<number | null>(null);
  const [filters, setFilters] = React.useState({
    category: 'all',
    sortBy: 'relevance',
    search: '',
  });

  const { data: news, isLoading, refetch } = useQuery({
    queryKey: ['news', activePrompt, filters],
    queryFn: () => newsApi.getPromptNews({ 
      promptId: activePrompt || 0,
      category: filters.category === 'all' ? undefined : filters.category
    })
  });

  const filteredNews = React.useMemo(() => {
    if (!news) return [];
    
    let filtered = news.filter(item => 
      item.title.toLowerCase().includes(filters.search.toLowerCase()) ||
      item.summary.toLowerCase().includes(filters.search.toLowerCase())
    );

    filtered = filtered.sort((a, b) => {
      if (filters.sortBy === 'relevance') {
        return (b.relevance_score || 0) - (a.relevance_score || 0);
      }
      return new Date(b.published_at).getTime() - new Date(a.published_at).getTime();
    });

    return filtered;
  }, [news, filters]);

  const hasActiveFilters = filters.category !== 'all' || 
                          filters.search !== '' || 
                          activePrompt !== null;

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">News Feed</h1>
        <div className="flex items-center gap-2">
          <Button 
            variant={showFilters ? "default" : "outline"}
            onClick={() => setShowFilters(!showFilters)}
            className="relative"
          >
            {showFilters ? (
              <X className="w-4 h-4 mr-2" />
            ) : (
              <Filter className="w-4 h-4 mr-2" />
            )}
            Filters
            {hasActiveFilters && !showFilters && (
              <span className="absolute -top-1 -right-1 w-2 h-2 bg-primary rounded-full" />
            )}
          </Button>
          <Button 
            variant="outline"
            onClick={() => refetch()}
            disabled={isLoading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
      </div>

      {showFilters && (
        <div className="border rounded-lg p-4 bg-card">
          <NewsFilters 
            filters={filters}
            onChange={setFilters}
            onPromptChange={setActivePrompt}
          />
        </div>
      )}

      <Tabs defaultValue="list" className="w-full">
        <TabsList>
          <TabsTrigger value="list">List View</TabsTrigger>
          <TabsTrigger value="grid">Grid View</TabsTrigger>
        </TabsList>

        <TabsContent value="list">
          <ScrollArea className="h-[calc(100vh-250px)]">
            <div className="space-y-4">
              {isLoading ? (
                Array(5).fill(0).map((_, i) => (
                  <div key={i} className="w-full h-48 animate-pulse bg-gray-100 rounded-lg" />
                ))
              ) : filteredNews.map((item: NewsItem) => (
                <NewsCard 
                  key={item.id}
                  news={item}
                  viewType="list"
                />
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="grid">
          <ScrollArea className="h-[calc(100vh-250px)]">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {isLoading ? (
                Array(6).fill(0).map((_, i) => (
                  <div key={i} className="w-full h-48 animate-pulse bg-gray-100 rounded-lg" />
                ))
              ) : filteredNews.map((item: NewsItem) => (
                <NewsCard 
                  key={item.id}
                  news={item}
                  viewType="grid"
                />
              ))}
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default NewsFeed;