import { FormEvent, useState } from 'react';
import { useLLM } from '../hooks/useLLM';

export function SummaryPanel() {
  const { response, loading, error, summarize } = useLLM();
  const [url, setUrl] = useState('');
  const [prompt, setPrompt] = useState('Summarize the content of this page.');

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    summarize(url.trim(), prompt.trim());
  }

  return (
    <section className="panel">
      <form className="panel__controls" onSubmit={handleSubmit}>
        <label className="panel__field">
          <span>Page URL</span>
          <input
            type="url"
            placeholder="https://example.com/article"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            required
          />
        </label>
        <label className="panel__field">
          <span>Prompt</span>
          <textarea
            rows={4}
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Summarizing…' : 'Summarize'}
        </button>
      </form>
      <div className="panel__output">
        {error && <p className="panel__error">{error}</p>}
        {!error && response && <p>{response}</p>}
        {!error && !response && !loading && <p>No summary yet.</p>}
      </div>
    </section>
  );
}
