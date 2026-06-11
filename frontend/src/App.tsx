import { useState } from 'react';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { HomeView } from '@/modules/Home';
import { FilingsView } from '@/modules/Filings/FilingsView';
import { ThesisView } from '@/modules/Thesis';
import { SectorView } from '@/modules/Sector/SectorView';
import { FinancialsView } from '@/modules/Financials';
import { PlaceholderView } from '@/common/components/PlaceholderView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';

interface TabContentProps {
  activeTab: string;
  ticker: string;
  hasError: boolean;
  setHasError: (val: boolean) => void;
  setTicker: (val: string) => void;
}

function TabContent({ activeTab, ticker, hasError, setHasError, setTicker }: TabContentProps) {
  switch (activeTab) {
    case 'SUMMARY':
      return <Dashboard ticker={ticker} isParentError={hasError} onErrorChange={setHasError} onSearch={(t) => { setTicker(t); setHasError(false); }} />;
    case 'THESIS':
      return <ThesisView ticker={ticker} />;
    case 'FILINGS':
      return <FilingsView ticker={ticker} />;
    case 'FINANCIALS':
      return <FinancialsView ticker={ticker} />;
    case 'VALUATION':
      return <PlaceholderView title="Modelos de Valuation" description="Calculadoras interativas de valor intrínseco (DCF, Múltiplos) para determinar o preço alvo." icon="calculate" />;
    case 'SECTOR':
      return <SectorView ticker={ticker} />;
    default:
      return null;
  }
}

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
      <ErrorBoundary>
        {!ticker ? (
          <HomeView onSearch={(t) => { setTicker(t); setHasError(false); setActiveTab('SUMMARY'); }} />
        ) : (
          <TabContent 
            activeTab={activeTab} 
            ticker={ticker} 
            hasError={hasError} 
            setHasError={setHasError} 
            setTicker={setTicker} 
          />
        )}
      </ErrorBoundary>
    </Layout>
  )
}

export default App
