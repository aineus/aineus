import React from 'react';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { useQuery } from '@tanstack/react-query';
import { promptsApi } from '@/lib/api';
import { Button } from '@/components/ui/button';

interface NewsFiltersProps {
  filters: {
    category: string;
    sortBy: string;
    search: string;
  };
  onChange: (filters: any) => void;
  onPromptChange: (promptId: number | null) => void;
}

export const NewsFilters = ({ filters, onChange, onPromptChange }: NewsFiltersProps) => {
  const { data: prompts } = useQuery({
    queryKey: ['prompts'],
    queryFn: promptsApi.getPrompts
  });

  const resetFilters = () => {
    onChange({
      category: 'all',
      sortBy: 'relevance',
      search: ''
    });
    onPromptChange(null);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-medium">Filter News</h3>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={resetFilters}
        >
          <X className="w-4 h-4 mr-2" />
          Reset Filters
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="relative">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search news..."
            className="pl-8"
            value={filters.search}
            onChange={(e) => onChange({ ...filters, search: e.target.value })}
          />
        </div>

        <Select
          value={String(filters.category)}
          onValueChange={(value) => onChange({ ...filters, category: value })}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="tech">Technology</SelectItem>
            <SelectItem value="business">Business</SelectItem>
            <SelectItem value="science">Science</SelectItem>
            <SelectItem value="health">Health</SelectItem>
            <SelectItem value="sports">Sports</SelectItem>
            <SelectItem value="entertainment">Entertainment</SelectItem>
            <SelectItem value="politics">Politics</SelectItem>
            <SelectItem value="world">World News</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={filters.sortBy}
          onValueChange={(value) => onChange({ ...filters, sortBy: value })}
        >
          <SelectTrigger>
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="relevance">Relevance</SelectItem>
            <SelectItem value="date">Date</SelectItem>
            <SelectItem value="popularity">Popularity</SelectItem>
          </SelectContent>
        </Select>

        <Select
          onValueChange={(value) => onPromptChange(value === 'all' ? null : Number(value))}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select prompt" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Prompts</SelectItem>
            {prompts?.map((prompt: any) => (
              <SelectItem key={prompt.id} value={String(prompt.id)}>
                {prompt.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
};