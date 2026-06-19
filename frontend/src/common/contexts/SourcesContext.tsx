import { createContext, useContext, type ReactNode } from 'react';

interface SourcesContextType {
  sources?: Record<string, string>;
}

const SourcesContext = createContext<SourcesContextType | undefined>(undefined);

export function SourcesProvider({ 
  sources, 
  children 
}: { 
  sources?: Record<string, string>; 
  children: ReactNode; 
}) {
  return (
    <SourcesContext.Provider value={{ sources }}>
      {children}
    </SourcesContext.Provider>
  );
}

export function useSources() {
  const context = useContext(SourcesContext);
  if (context === undefined) {
    // If not wrapped in a provider, return empty instead of throwing to allow standalone usage
    return {};
  }
  return context.sources || {};
}
