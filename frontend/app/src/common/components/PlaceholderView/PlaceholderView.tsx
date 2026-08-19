interface PlaceholderViewProps {
  title: string;
  description: string;
  icon: string;
}

export function PlaceholderView({ title, description, icon }: PlaceholderViewProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in zoom-in-95 duration-500">
      <div className="w-24 h-24 bg-surface-container-high border border-outline-variant rounded-full flex items-center justify-center mb-6 shadow-sm">
        <span className="material-symbols-outlined text-[48px] text-on-surface-variant opacity-80">{icon}</span>
      </div>
      
      <div className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-3 py-1 rounded-full mb-4 uppercase tracking-wider">
        Em Desenvolvimento
      </div>
      
      <h2 className="font-display-md text-display-md font-bold text-on-surface mb-3">
        {title}
      </h2>
      
      <p className="text-body-lg text-on-surface-variant max-w-lg mb-8 leading-relaxed">
        {description}
      </p>
      
      <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 max-w-md w-full text-left">
        <div className="flex items-start gap-3">
          <span className="material-symbols-outlined text-secondary text-[20px] mt-0.5">lightbulb</span>
          <div>
            <p className="text-body-sm text-on-surface font-medium mb-1">O que esperar nesta aba?</p>
            <p className="text-body-sm text-on-surface-variant leading-relaxed">
              Estamos a trabalhar para trazer ferramentas analíticas profundas e interativas para esta secção. Esta funcionalidade será ativada numa futura atualização.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
