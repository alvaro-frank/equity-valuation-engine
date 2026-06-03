from application.dtos.dtos import EarningsReportResult, TickerResult
from application.ports.ports import EarningsReportPort, QuantitativeDataPort
from dataclasses import asdict

class EarningsReportUseCase:
    """
    Service responsible for performing stock earnings report analysis based on the provided stock data.
    This service takes in an entity Ticker, analyses the quality, moat and background of a business, and returns a DTO containing all information about the Qualitative data of the business.
    """
    def __init__(self, adapter: EarningsReportPort, quant_adapter: QuantitativeDataPort):
        """
        Initialises the EarningsReportUseCase with the adapters for AI-driven analysis.
        """
        self.adapter = adapter
        self.quant_adapter = quant_adapter

    async def analyse_earnings_report(self, ticker_symbol: str, pdf_file_path: str, language: str = "en") -> EarningsReportResult:
        """
        Analyses the earnings report of a company for a specific fiscal period (either a year or a quarter)
        
        Args:
            ticker_symbol (str): The ticker symbol of the company
            pdf_file_path (str): The path to the PDF file to be analysed
            
        Returns:
            EarningsReportResult: DTO containing the data given the PDF file
        """
        er = await self.adapter.analyse_earnings_report(
            symbol=ticker_symbol,
            pdf_file_path=pdf_file_path,
            language=language
        )

        ticker_info = await self.quant_adapter.get_ticker_info(ticker_symbol)
        
        ticker_dto = TickerResult(
            symbol=ticker_symbol,
            name=ticker_info.name,
            sector=ticker_info.sector,
            industry=ticker_info.industry
        )

        return EarningsReportResult(
            ticker=ticker_dto,
            **asdict(er)
        )