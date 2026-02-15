from services.dtos import StockDataDTO

class ValuationService:
    def compare_revenue_growth(self, stock_dto: StockDataDTO):
        print(f"\nAnalysing Revenue Growth: {stock_dto.ticker.name}")
        
        years = sorted(stock_dto.financial_years, key=lambda x: x.fiscal_date_ending)
        
        if not years:
            print("Insufficient data to analyze revenue growth.")
            return

        print(f"{'Data':<12} | {'Revenue':<18} | {'YoY Growth'}")
        print("-" * 50)

        prev_revenue = None
        growth_rates = []

        for yr in years:
            growth_str = "---"
            if prev_revenue and prev_revenue > 0:
                growth = ((yr.revenue - prev_revenue) / prev_revenue) * 100
                growth_rates.append(growth)
                growth_str = f"{growth:+.2f}%"
            
            print(f"{yr.fiscal_date_ending:<12} | ${yr.revenue:>16,.2f} | {growth_str}")
            prev_revenue = yr.revenue

        if len(years) >= 2:
            begin_val = years[0].revenue
            end_val = years[-1].revenue
            t = len(years) - 1
            
            if begin_val > 0:
                ratio = float(end_val / begin_val)
                cagr = (pow(ratio, (1 / t)) - 1) * 100
                print("-" * 50)
                print(f"🚀 CAGR ({t} anos): {cagr:.2f}%")
                
                if cagr > 10: print("Excelent growth! (>10%)")
                elif cagr > 0: print("Moderate growth. (0-10%)")
                else: print("Negative growth. (<0%)")