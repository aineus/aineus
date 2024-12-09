'use client';

import PromptForm from '@/components/prompts/prompt-form';

export default function CreatePromptPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-normal mb-6">Create New Prompt Newspaper</h1>
      <PromptForm />
    </div>
  );
}