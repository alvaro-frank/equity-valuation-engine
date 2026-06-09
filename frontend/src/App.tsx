import { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { WelcomeState } from '@/modules/Dashboard/components/WelcomeState';
import { FilingsView } from '@/modules/Filings/FilingsView';
import { ThesisView } from '@/modules/Thesis';
import { SectorView } from '@/modules/Sector/SectorView';
import { FinancialsView } from '@/modules/Financials';
import { PlaceholderView } from '@/common/components/PlaceholderView';

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
          {activeTab === 'THESIS' && <ThesisView ticker={ticker} />}
          {activeTab === 'FILINGS' && <FilingsView ticker={ticker} />}
          {activeTab === 'FINANCIALS' && <FinancialsView ticker={ticker} />}
          {activeTab === 'VALUATION' && <PlaceholderView title="Modelos de Valuation" description="Calculadoras interativas de valor intrínseco (DCF, Múltiplos) para determinar o preço alvo." icon="calculate" />}
          {activeTab === 'SECTOR' && <SectorView ticker={ticker} />}
        </>
      )}
    </Layout>
  )
}

export default App
