import { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { WelcomeState } from '@/modules/Dashboard/components/WelcomeState';
import { FilingsView } from '@/modules/Filings/FilingsView';

function App() {
  const [ticker, setTicker] = useState<string>('');
  const [hasError, setHasError] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('SUMMARY');

  return (
    <Layout 
      activeTicker={ticker} 
      hasError={hasError} 
      onSearch={(newTicker) => { setTicker(newTicker); setHasError(false); setActiveTab('SUMMARY'); }}
      activeTab={activeTab}
      onTabChange={setActiveTab}
    >
      {!ticker ? (
        <WelcomeState onSearch={(t) => { setTicker(t); setHasError(false); setActiveTab('SUMMARY'); }} />
      ) : (
        <>
          {activeTab === 'SUMMARY' && <Dashboard ticker={ticker} isParentError={hasError} onErrorChange={setHasError} onSearch={(t) => { setTicker(t); setHasError(false); }} />}
          {activeTab === 'FILINGS' && <FilingsView ticker={ticker} />}
        </>
      )}
    </Layout>
  )
}

export default App
