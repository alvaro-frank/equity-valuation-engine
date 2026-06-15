import * as Tooltip from '@radix-ui/react-tooltip';

interface CitedTextProps {
  text: string;
  sources?: Record<string, string>;
}

export function CitedText({ text, sources }: CitedTextProps) {
  if (!text) return null;
  if (!sources || Object.keys(sources).length === 0) {
    return <span>{text}</span>;
  }

  // Split text by citations like [1], [2]
  // Capturing group ensures numbers are kept in the resulting array at odd indices
  const parts = text.split(/\[(\d+)\]/g);

  return (
    <Tooltip.Provider delayDuration={200}>
      <span className="leading-relaxed">
        {parts.map((part, index) => {
          // Even indices are regular text
          if (index % 2 === 0) {
            return <span key={index}>{part}</span>;
          }

          // Odd indices are the captured numbers from [1]
          const sourceText = sources[part];
          if (!sourceText) {
            // If there's no matching source, just render it back as [1]
            return <span key={index}>[{part}]</span>;
          }

          return (
            <Tooltip.Root key={index}>
              <Tooltip.Trigger asChild>
                <button
                  className="inline-flex items-center justify-center w-[18px] h-[18px] mx-0.5 align-text-top text-[10px] font-bold text-primary bg-primary/10 hover:bg-primary/20 rounded-full cursor-help transition-colors ring-1 ring-primary/20"
                  aria-label={`Source: ${sourceText}`}
                >
                  {part}
                </button>
              </Tooltip.Trigger>
              <Tooltip.Portal>
                <Tooltip.Content
                  className="z-50 max-w-[280px] px-3 py-2 text-xs font-medium text-surface bg-on-surface rounded shadow-md animate-in fade-in zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out data-[state=closed]:zoom-out-95"
                  sideOffset={5}
                >
                  <div className="flex items-start gap-1.5">
                    <span className="material-symbols-outlined text-[14px] text-surface/70 mt-0.5">article</span>
                    <span>{sourceText}</span>
                  </div>
                  <Tooltip.Arrow className="fill-on-surface" />
                </Tooltip.Content>
              </Tooltip.Portal>
            </Tooltip.Root>
          );
        })}
      </span>
    </Tooltip.Provider>
  );
}
