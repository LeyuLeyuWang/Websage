import { useLLM } from '../hooks/useLLM';

export function SummaryPanel() {
  const { response, loading, summarize } = useLLM();

  return (
    <section className="panel">
      <div className="panel__controls">
        <textarea
          placeholder="Paste a URL or text snippet to summarize"
          onBlur={(event) => summarize(event.target.value)}
        />
      </div>
      <div className="panel__output">
        {loading ? <p>Summarizing...</p> : <p>{response || 'No summary yet.'}</p>}
      </div>
    </section>
  );
}
