import type { ReactNode } from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';

interface InfoTooltipProps {
  content: ReactNode;
}

export function InfoTooltip({ content }: InfoTooltipProps) {
  return (
    <Tooltip.Provider delayDuration={200}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button className="text-on-surface-variant hover:text-on-surface transition-colors focus:outline-none ml-3 mt-0.5 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </button>
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content 
            className="z-[100] max-w-sm px-4 py-3 bg-surface-container-high border border-outline-variant text-on-surface text-sm rounded-lg shadow-xl leading-relaxed" 
            sideOffset={8}
          >
            {content}
            <Tooltip.Arrow className="fill-surface-container-high" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
