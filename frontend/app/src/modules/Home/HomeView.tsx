import { useNavigate } from 'react-router-dom';
import { GlobalSearchBox } from '@/modules/Search/components/GlobalSearchBox';

import { HomeHero } from './components/HomeHero';
import { TrendingTickers } from './components/TrendingTickers';

export function HomeView() {
  const navigate = useNavigate();
  
  const handleTrendingSelect = (symbol: string) => {
    navigate(`/${symbol}/summary`);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] max-w-2xl mx-auto w-full px-4 animate-fade-in">
      <HomeHero />

      <GlobalSearchBox variant="home" />

      <TrendingTickers onSelect={(symbol) => handleTrendingSelect(symbol)} />
    </div>
  );
}
