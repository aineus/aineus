import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, RefreshCw, Search, Filter } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useRouter } from 'next/navigation';
import { promptsApi } from '@/lib/api';

interface Prompt {
  id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  refresh_interval: number;
  total_articles: number;
  latest_refresh: string;
  categories_summary: Record<string, number>;
  prompt_text: string;
  llm_provider: string;
}

const PromptDashboard = () => {
  const router = useRouter();
  const [search, setSearch] = React.useState('');
  
  const { data: prompts, isLoading, refetch } = useQuery({
    queryKey: ['prompts'],
    queryFn: promptsApi.getPrompts
  });

  const filteredPrompts = React.useMemo(() => {
    if (!prompts) return [];
    return prompts.filter(prompt => 
      prompt.name.toLowerCase().includes(search.toLowerCase()) ||
      prompt.description?.toLowerCase().includes(search.toLowerCase())
    );
  }, [prompts, search]);

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Your Prompt Newspapers</h1>
        <div className="flex gap-2">
          <Button 
            variant="outline"
            onClick={() => refetch()}
            className="flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" /> Refresh
          </Button>
          <Button 
            onClick={() => router.push('/prompts/create')}
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" /> Create New
          </Button>
        </div>
      </div>

      <div className="flex gap-4 items-center">
        <div className="relative flex-1">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search prompts..."
            className="pl-8"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <ScrollArea className="h-[calc(100vh-250px)]">
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="w-full h-48 animate-pulse bg-gray-100" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredPrompts.map((prompt: Prompt) => (
              <Card 
                key={prompt.id} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => router.push(`/prompts/${prompt.id}`)}
              >
                <CardHeader>
                  <CardTitle className="flex justify-between items-center">
                    {prompt.name}
                    {prompt.is_public && (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                        Public
                      </span>
                    )}
                  </CardTitle>
                  <CardDescription>{prompt.description}</CardDescription>
                </CardHeader>
                
                <CardContent>
                  <div className="text-sm space-y-2">
                    <p>Articles: {prompt.total_articles}</p>
                    <p>Last Updated: {new Date(prompt.latest_refresh).toLocaleString()}</p>
                    <p>Categories: {Object.keys(prompt.categories_summary).length}</p>
                    <p>Model: {prompt.llm_provider}</p>
                  </div>
                </CardContent>

                <CardFooter className="flex justify-between">
                  <div className="text-xs text-muted-foreground">
                    Refresh: {prompt.refresh_interval}h
                  </div>
                  <Button variant="ghost" size="sm">View Details →</Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default PromptDashboard;