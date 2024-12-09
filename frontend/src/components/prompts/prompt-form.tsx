import React from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { promptsApi } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

const PromptForm = () => {
  const router = useRouter();
  const [formData, setFormData] = React.useState({
    name: '',
    description: '',
    prompt_text: '',
    system_prompt: '',
    is_public: false,
    refresh_interval: 24,
    max_articles: 50,
    custom_categories: {
      categories: ['tech', 'ai', 'startups']
    },
    source_preferences: {
      preferred_sources: [],
      excluded_sources: []
    },
    llm_provider: 'openai'
  });

  const createPromptMutation = useMutation({
    mutationFn: promptsApi.createPrompt,
    onSuccess: () => {
      toast.success('Prompt created successfully');
      router.push('/prompts');
    },
    onError: (error) => {
      toast.error('Failed to create prompt');
      console.error('Error creating prompt:', error);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createPromptMutation.mutate(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="p-6">
        <div className="space-y-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Tech News Summarizer"
              required
            />
          </div>

          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Summarizes tech news in a concise format..."
            />
          </div>

          <div>
            <Label htmlFor="prompt_text">Prompt Text</Label>
            <Textarea
              id="prompt_text"
              value={formData.prompt_text}
              onChange={(e) => setFormData({ ...formData, prompt_text: e.target.value })}
              placeholder="Summarize this tech news article in 3-4 sentences..."
              required
            />
          </div>

          <div>
            <Label htmlFor="system_prompt">System Prompt</Label>
            <Textarea
              id="system_prompt"
              value={formData.system_prompt}
              onChange={(e) => setFormData({ ...formData, system_prompt: e.target.value })}
              placeholder="You are a technology journalist writing for a tech-savvy audience..."
            />
          </div>

          <div className="flex items-center space-x-2">
            <Switch
              id="is_public"
              checked={formData.is_public}
              onCheckedChange={(checked) => setFormData({ ...formData, is_public: checked })}
            />
            <Label htmlFor="is_public">Make Public</Label>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="refresh_interval">Refresh Interval (hours)</Label>
              <Input
                id="refresh_interval"
                type="number"
                value={formData.refresh_interval}
                onChange={(e) => setFormData({ ...formData, refresh_interval: parseInt(e.target.value) })}
                min="1"
              />
            </div>
            <div>
              <Label htmlFor="max_articles">Max Articles</Label>
              <Input
                id="max_articles"
                type="number"
                value={formData.max_articles}
                onChange={(e) => setFormData({ ...formData, max_articles: parseInt(e.target.value) })}
                min="1"
                max="1000"
              />
            </div>
          </div>
        </div>
      </Card>

      <div className="flex justify-end gap-4">
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push('/prompts')}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={createPromptMutation.isPending}
        >
          {createPromptMutation.isPending ? 'Creating...' : 'Create Prompt'}
        </Button>
      </div>
    </form>
  );
};

export default PromptForm;