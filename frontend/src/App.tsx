import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from '@/common/components/Layout';
import { Dashboard } from '@/modules/Dashboard/Dashboard';
import { HomeView } from '@/modules/Home';
import { FilingsView } from '@/modules/Filings/FilingsView';
import { ThesisView } from '@/modules/Thesis';
import { SectorView } from '@/modules/Sector/SectorView';
import { FinancialsView } from '@/modules/Financials';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
import { ValuationView } from '@/modules/Valuation/ValuationView';

import { GlobalSearchBox } from '@/modules/Search/components/GlobalSearchBox';

function App() {
  return (
    <ErrorBoundary>
      <Routes>
        <Route path="/" element={<Layout headerSearchComponent={<GlobalSearchBox variant="header" />} />}>
          <Route index element={<HomeView />} />
          <Route path=":ticker">
            <Route index element={<Navigate to="summary" replace />} />
            <Route path="summary" element={<Dashboard />} />
            <Route path="financials" element={<FinancialsView />} />
            <Route path="thesis" element={<ThesisView />} />
            <Route path="sector" element={<SectorView />} />
            <Route path="filings" element={<FilingsView />} />
            <Route path="valuation" element={<ValuationView />} />
          </Route>
        </Route>
      </Routes>
    </ErrorBoundary>
  )
}

export default App
