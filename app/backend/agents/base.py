"""Base agent class and shared utilities for AI hedge fund agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentSignal:
    """Represents a trading signal produced by an agent."""

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

    def __init__(
        self,
        ticker: str,
        action: str,
        confidence: float,
        reasoning: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if action not in (self.BUY, self.SELL, self.HOLD):
            raise ValueError(f"Invalid action '{action}'. Must be buy, sell, or hold.")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0.")

        self.ticker = ticker.upper()
        self.action = action
        self.confidence = confidence
        self.reasoning = reasoning
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the signal to a dictionary."""
        return {
            "ticker": self.ticker,
            "action": self.action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    def __repr__(self) -> str:
        return (
            f"AgentSignal(ticker={self.ticker!r}, action={self.action!r}, "
            f"confidence={self.confidence:.2f})"
        )


class BaseAgent(ABC):
    """Abstract base class for all hedge fund analysis agents.

    Each agent is responsible for a specific analytical perspective
    (e.g., fundamentals, sentiment, technical analysis) and produces
    a trading signal for one or more tickers.
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    def analyze(self, ticker: str, data: Dict[str, Any]) -> AgentSignal:
        """Analyze the provided data and return a trading signal.

        Args:
            ticker: The stock ticker symbol to analyze.
            data: A dictionary containing relevant market/financial data.

        Returns:
            An AgentSignal representing the agent's recommendation.
        """
        ...

    def analyze_batch(
        self, tickers: List[str], data: Dict[str, Dict[str, Any]]
    ) -> List[AgentSignal]:
        """Analyze multiple tickers and return a list of signals.

        Args:
            tickers: List of ticker symbols to analyze.
            data: Mapping of ticker -> data dict for each ticker.

        Returns:
            List of AgentSignal objects, one per ticker.
        """
        signals: List[AgentSignal] = []
        for ticker in tickers:
            ticker_data = data.get(ticker, {})
            try:
                signal = self.analyze(ticker, ticker_data)
                signals.append(signal)
            except Exception as exc:  # noqa: BLE001
                self._logger.error(
                    "Agent '%s' failed to analyze ticker '%s': %s",
                    self.name,
                    ticker,
                    exc,
                )
        return signals

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
