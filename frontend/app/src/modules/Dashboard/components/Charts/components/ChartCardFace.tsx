interface ChartCardFaceProps {
  title: string;
  actionText: string;
  onAction: () => void;
  isBackFace?: boolean;
  children: React.ReactNode;
}

export function ChartCardFace({ title, actionText, onAction, isBackFace = false, children }: ChartCardFaceProps) {
  return (
    <div 
      className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden" 
      style={{ backfaceVisibility: 'hidden', transform: isBackFace ? 'rotateY(180deg)' : 'none' }}
    >
      <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {title}
        </h3>
        <button 
          onClick={onAction}
          className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
        >
          {actionText}
        </button>
      </div>
      <div className="p-4 flex-1 min-h-0 min-w-0">
        {children}
      </div>
    </div>
  );
}
