import React, { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';

function App() {
  const [ticker, setTicker] = useState<string>('MSFT');

  return (
    <Layout activeTicker={ticker} onSearch={(newTicker) => setTicker(newTicker)}>
      <Dashboard ticker={ticker} />
    </Layout>
  )
}

export default App
