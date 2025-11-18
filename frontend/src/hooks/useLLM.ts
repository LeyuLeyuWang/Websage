import { useState } from 'react';

export function useLLM() {
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  async function summarize(input: string) {
    if (!input) return;
    setLoading(true);
    try {
      // Placeholder: In the future call backend API
      await new Promise((resolve) => setTimeout(resolve, 600));
      setResponse(`Stub summary for: ${input.slice(0, 60)}...`);
    } finally {
      setLoading(false);
    }
  }

  return { response, loading, summarize };
}
