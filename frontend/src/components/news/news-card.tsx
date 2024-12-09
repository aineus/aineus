import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Newspaper, ExternalLink, Clock } from 'lucide-react';

interface NewsCardProps {
  news: {
    id: number;
    title: string;
    content: string;
    summary: string;
    source: string;
    url: string;
    published_at: string;
    author: string;
    transformed_content?: string;
    relevance_score?: number;
  };
  viewType: 'list' | 'grid';
}

export const NewsCard = ({ news, viewType }: NewsCardProps) => {
  return (
    <Card className={viewType === 'list' ? 'flex flex-col md:flex-row' : ''}>
      <div className={viewType === 'list' ? 'flex-1' : ''}>
        <CardHeader>
          <CardTitle className="flex justify-between items-start gap-4">
            <span>{news.title}</span>
            {news.relevance_score && (
              <Badge variant="secondary">
                {Math.round(news.relevance_score * 100)}% relevant
              </Badge>
            )}
          </CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-sm text-muted-foreground">
            {news.summary}
          </p>
          <div className="flex items-center gap-2 mt-4 text-xs text-muted-foreground">
            <span>{news.source}</span>
            {news.author && (
              <>
                <span>•</span>
                <span>{news.author}</span>
              </>
            )}
            <span>•</span>
            <Clock className="w-3 h-3" />
            <span>{new Date(news.published_at).toLocaleString()}</span>
          </div>
        </CardContent>
      </div>

      <CardFooter className={`${viewType === 'list' ? 'flex-col justify-end gap-2 p-6' : 'flex justify-between'}`}>
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="sm">
              <Newspaper className="w-4 h-4 mr-2" />
              Transformed
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-[90vw] sm:w-[540px]">
            <SheetHeader>
              <SheetTitle>{news.title}</SheetTitle>
              <SheetDescription>Transformed by AI</SheetDescription>
            </SheetHeader>
            <ScrollArea className="h-[calc(100vh-200px)] mt-6">
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold mb-2">Original</h3>
                  <p className="text-sm text-muted-foreground">{news.content}</p>
                </div>
                {news.transformed_content && (
                  <div>
                    <h3 className="font-semibold mb-2">Transformed</h3>
                    <p className="text-sm text-muted-foreground">{news.transformed_content}</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </SheetContent>
        </Sheet>

        <Button variant="ghost" size="sm" onClick={() => window.open(news.url, '_blank')}>
          <ExternalLink className="w-4 h-4 mr-2" />
          Source
        </Button>
      </CardFooter>
    </Card>
  );
};