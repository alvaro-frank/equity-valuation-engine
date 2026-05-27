import { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { WelcomeState } from '@/modules/Dashboard/components/WelcomeState';

function App() {
  const [ticker, setTicker] = useState<string>('');
  const [hasError, setHasError] = useState<boolean>(false);

  return (
    <Layout activeTicker={ticker} hasError={hasError} onSearch={(newTicker) => { setTicker(newTicker); setHasError(false); }}>
      {!ticker ? (
        <WelcomeState onSearch={(t) => { setTicker(t); setHasError(false); }} />
      ) : (
        <Dashboard ticker={ticker} isParentError={hasError} onErrorChange={setHasError} />
      )}
    </Layout>
  )
}

export default App
