from application.ports.core_financial_ports import TranscriptDataPort
from application.dtos.earnings import EarningsCallTranscriptResult, TranscriptStatementResult
from application.exceptions.exceptions import TickerNotFoundError

class GetEarningsCallTranscriptUseCase:
    """
    Use Case responsible for orchestrating the retrieval of an Earnings Call Transcript
    and converting it to a Data Transfer Object (DTO) for the frontend.
    """
    def __init__(self, transcript_port: TranscriptDataPort):
        self.transcript_port = transcript_port

    async def execute(self, ticker: str, year: int, quarter: int) -> EarningsCallTranscriptResult:
        # 1. Ask the data port for the Domain Entity
        transcript_entity = await self.transcript_port.get_earnings_call_transcript(ticker, year, quarter)
        
        if not transcript_entity:
            raise TickerNotFoundError(f"Transcript not found for {ticker} in Q{quarter} {year}")
            
        # 2. Convert Domain Entity to DTO
        statements_dto = [
            TranscriptStatementResult(
                speaker=t.speaker,
                title=t.title,
                content=t.content,
                sentiment=t.sentiment
            ) for t in transcript_entity.transcripts
        ]
        
        return EarningsCallTranscriptResult(
            ticker=transcript_entity.ticker,
            quarter=transcript_entity.quarter,
            year=transcript_entity.year,
            date=transcript_entity.date,
            transcripts=statements_dto
        )
