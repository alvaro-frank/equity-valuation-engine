from domain.interfaces import QuantitativeDataProvider
from domain.stock_market import Stock, Price, Ticker, FinancialYear
from services.dtos import QuantitativeDataDTO, QuantitativeValuationDTO, MetricAnalysisDTO, MetricYearlyDTO, FinancialYearDTO

class QuantitativeValuationService:
    """
    Service responsible for performing stock quantitative valuation analysis based on the provided stock data, including financial metrics across multiple fiscal years.
    This service takes in a QuantitativeDataDTO, analyzes the financial metrics for a specified number of recent years, and returns a QuantitativeValuationDTO containing the analysis results.
    """
    def __init__(self, adapter: QuantitativeDataProvider):
        """
        Initializes the QuantitativeValuationService with the QuantitativeDataProvider to fetch fundamental business data.
        """
        self.adapter = adapter
        
    def evaluate_ticker(self, symbol: str, years: int = 5) -> QuantitativeValuationDTO:
        """
        Orchestrates the valuation process by fetching data and then performing the analysis.
        
        Args:
            symbol (str): The stock ticker symbol to analyze.
            years (int): Number of recent years to analyze.
            
        Returns:
            QuantitativeValuationDTO: The result of the quantitative analysis.
        """
        stock_dto = self.adapter.get_stock_fundamental_data(symbol)
        
        return self.evaluate_stock(stock_dto, years_to_analyze=years)
        
    def evaluate_stock(self, stock_dto: QuantitativeDataDTO, years_to_analyze: int = 5) -> QuantitativeValuationDTO:
        """
        Evaluates the stock's financial data and performs analysis on key metrics for a specified number of recent years.
        
        Args:
            stock_dto (QuantitativeDataDTO): The data transfer object containing the stock's fundamental data, including financial years and current price.
            years_to_analyze (int): The number of recent fiscal years to include in the analysis (default is 5).
            
        Returns:
            QuantitativeValuationDTO: The result of the quantitative valuation analysis.
        """
        stock_entity = self._map_to_domain(stock_dto)
        
        all_fields = list(FinancialYearDTO.model_fields.keys())
        excluded_fields = ["fiscal_date_ending"]
        
        metrics_to_check = [f for f in all_fields if f not in excluded_fields]
        analysis_map = {}

        for field in metrics_to_check:
            cagr = stock_entity.calculate_cagr(field, years_to_analyze)
            
            sorted_years = sorted(stock_entity.financial_years, key=lambda x: x.fiscal_date_ending)
            analysis_years = sorted_years[-years_to_analyze:]
            
            yearly_data = [
                MetricYearlyDTO(date=y.fiscal_date_ending, value=getattr(y, field))
                for y in analysis_years
            ]

            analysis_map[field] = MetricAnalysisDTO(
                metric_name=field.replace("_", " ").title(),
                yearly_data=yearly_data,
                cagr=cagr
            )

        return QuantitativeValuationDTO(
            ticker=stock_dto.ticker,
            metrics=analysis_map
        )
        
    def _map_to_domain(self, dto: QuantitativeDataDTO) -> Stock:
        """
        Helper to convert DTO into Domain Entity.
        
        Args:
            dto (QuantitativeDataDTO): DTO to be converted
            
        Returns:
            Stock: new created Stock Domain Entity
        """
        ticker = Ticker(
            symbol=dto.ticker.symbol,
            name=dto.ticker.name,
            sector=dto.ticker.sector,
            industry=dto.ticker.industry
        )
        price = Price(amount=dto.price.amount, currency=dto.price.currency)
        years = [FinancialYear(**year.model_dump()) for year in dto.financial_years]
        
        return Stock(ticker=ticker, price=price, financial_years=years)