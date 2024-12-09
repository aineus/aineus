import React from 'react';
import { useRouter } from 'next/navigation';
import { RefreshCw, Edit2, ArrowLeft, Newspaper } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { newsApi } from '@/lib/api';
import { toast } from 'sonner';

interface PromptDetailProps {
  prompt: any;  // Replace with proper type
  news: any[];  // Replace with proper type
}

const PromptDetail = ({ prompt, news }: PromptDetailProps) => {
  const router = useRouter();
  const [isRefreshing, setIsRefreshing] = React.useState(false);

  const handleRefresh = async () => {
    try {
      setIsRefreshing(true);
      await newsApi.refreshPromptNews(prompt.id);
      toast.success('News refreshed successfully');
      // Optionally refetch news data here
    } catch (error) {
      toast.error('Failed to refresh news');
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => router.back()}>
            <ArrowLeft className="w-4 h-4 mr-2" /> Back
          </Button>
          <h1 className="text-3xl font-normal">{prompt.name}</h1>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            {isRefreshing ? 'Refreshing...' : 'Refresh News'}
          </Button>
          <Button onClick={() => router.push(`/prompts/${prompt.id}/edit`)}>
            <Edit2 className="w-4 h-4 mr-2" /> Edit Prompt
          </Button>
        </div>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="news">News</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
          <TabsTrigger value="stats">Statistics</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Prompt Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">{prompt.description}</p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="font-semibold">Prompt Text</h3>
                  <p className="text-sm mt-1">{prompt.prompt_text}</p>
                </div>
                <div>
                  <h3 className="font-semibold">System Prompt</h3>
                  <p className="text-sm mt-1">{prompt.system_prompt}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>News Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-normal">{prompt.total_articles}</div>
                <p className="text-sm text-muted-foreground">Total Articles</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-normal">
                  {Object.keys(prompt.categories_summary).length}
                </div>
                <p className="text-sm text-muted-foreground">Active Categories</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Last Update</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm">
                  {new Date(prompt.latest_refresh).toLocaleString()}
                </div>
                <p className="text-sm text-muted-foreground">
                  Updates every {prompt.refresh_interval}h
                </p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="news">
          <Card>
            <CardContent className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {news?.map((item: any) => (
                  <Card key={item.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <CardTitle className="text-lg">{item.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground">{item.summary}</p>
                      <div className="flex justify-between items-center mt-4">
                        <span className="text-xs">{item.source}</span>
                        <Button variant="ghost" size="sm">
                          <Newspaper className="w-4 h-4 mr-2" /> Read More
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings">
          {/* Add settings content */}
        </TabsContent>

        <TabsContent value="stats">
          {/* Add statistics content */}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default PromptDetail;