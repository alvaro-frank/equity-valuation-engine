import pytest
from decimal import Decimal
from unittest.mock import MagicMock

from domain.entities.entities import Ticker, EarningsReport, CorePerformance, MetricWithGrowth, CapitalAllocation, RiskDeconstruction
from application.use_cases.analyse_earnings_report import EarningsReportUseCase
from application.dtos.dtos import EarningsReportResult

class TestEarningsReportUseCase:

    @pytest.fixture
    def mock_adapters(self, mocker):
        quant_port = mocker.MagicMock()
        quant_port.get_ticker_info = mocker.AsyncMock()
        qual_port = mocker.MagicMock()
        qual_port.analyse_earnings_report = mocker.AsyncMock()
        return qual_port, quant_port

    @pytest.mark.anyio
    async def test_analyse_earnings_report_returns_valid_dto(self, mock_adapters):
        qual_port, quant_port = mock_adapters
        
        quant_port.get_ticker_info.return_value = Ticker(
            symbol="MSFT",
            name="Microsoft Corp",
            sector="Technology",
            industry="Software"
        )
        
        qual_port.analyse_earnings_report.return_value = EarningsReport(
            period_end_date="2026-03-31",
            core_performance=CorePerformance(
                adjusted_revenue=MetricWithGrowth(amount=Decimal("50000"), yoy_growth=Decimal("15")),
                adjusted_eps=MetricWithGrowth(amount=Decimal("5"), yoy_growth=Decimal("10")),
                adjusted_ebitda_margin=MetricWithGrowth(amount=Decimal("40"), yoy_growth=Decimal("2")),
                free_cash_flow=MetricWithGrowth(amount=Decimal("15000"), yoy_growth=Decimal("5"))
            ),
            capital_allocation=CapitalAllocation(
                share_buybacks=Decimal("2000"),
                dividends=Decimal("1000"),
                capex_rd=Decimal("5000"),
                infrastructure_assessment="Accelerating"
            ),
            forward_guidance="Raise",
            moat_trajectory="Expanding",
            risk_deconstruction=RiskDeconstruction(
                macro_risks=["Interest rates"],
                internal_risks=["Execution delay"]
            ),
            bottom_line="Excellent execution."
        )

        use_case = EarningsReportUseCase(adapter=qual_port, quant_adapter=quant_port)
        result = await use_case.analyse_earnings_report("MSFT", "dummy.pdf")

        assert isinstance(result, EarningsReportResult)
        assert result.ticker.symbol == "MSFT"
        assert result.period_end_date == "2026-03-31"
        assert result.core_performance.adjusted_revenue.amount == Decimal("50000")
        assert result.capital_allocation.infrastructure_assessment == "Accelerating"
        assert result.risk_deconstruction.macro_risks[0] == "Interest rates"
        
        quant_port.get_ticker_info.assert_called_once_with("MSFT")
        qual_port.analyse_earnings_report.assert_called_once_with("MSFT", "dummy.pdf")
