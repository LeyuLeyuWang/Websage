import { useCallback, useState } from 'react';

type SummaryResponse = {
  summary: string;
  source?: string;
};

export function useLLM() {
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const summarize = useCallback(async (url: string, prompt: string) => {
    if (!url || !prompt) {
      setError('Both URL and prompt are required.');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, prompt }),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || 'Unable to fetch summary.');
      }

      const data = (await response.json()) as SummaryResponse;
      setResponse(data.summary ?? '');
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : 'Unexpected error occurred.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { response, loading, error, summarize };
}
