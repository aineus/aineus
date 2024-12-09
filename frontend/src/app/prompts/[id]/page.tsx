'use client';

import { useQuery } from '@tanstack/react-query';
import { useParams } from 'next/navigation';
import { promptsApi, newsApi } from '@/lib/api';
import PromptDetail from '@/components/prompts/prompt-detail';

export default function PromptDetailPage() {
  const params = useParams();
  const promptId = parseInt(params.id as string);

  const { data: prompt, isLoading: promptLoading } = useQuery({
    queryKey: ['prompt', promptId],
    queryFn: () => promptsApi.getPrompt(promptId)
  });

  const { data: news, isLoading: newsLoading } = useQuery({
    queryKey: ['prompt-news', promptId],
    queryFn: () => newsApi.getPromptNews({ promptId })
  });

  if (promptLoading) {
    return <div>Loading...</div>;
  }

  return <PromptDetail prompt={prompt} news={news} />;
}