import React, { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { WelcomeState } from '@/modules/Dashboard/components/WelcomeState';

function App() {
  const [ticker, setTicker] = useState<string>('');

  return (
    <Layout activeTicker={ticker} onSearch={(newTicker) => setTicker(newTicker)}>
      {!ticker ? (
        <WelcomeState onSearch={setTicker} />
      ) : (
        <Dashboard ticker={ticker} />
      )}
    </Layout>
  )
}

export default App
