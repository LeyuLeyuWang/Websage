import './styles/global.css';
import { SummaryPanel } from './components/SummaryPanel';

function App() {
  return (
    <div className="app">
      <header className="app__header">
        <h1>Websage</h1>
        <p>Your research companion for smarter browsing.</p>
      </header>
      <main>
        <SummaryPanel />
      </main>
    </div>
  );
}

export default App;
