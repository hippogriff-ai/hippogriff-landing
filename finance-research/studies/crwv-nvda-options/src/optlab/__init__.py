"""optlab: small, tested toolkit for options-vs-fundamentals research.

Modules
-------
optlab.analysis.vol        realized vol, implied moves, variance risk premium, earnings-move stats
optlab.analysis.events     event-study windows, abnormal returns, post-earnings drift
optlab.analysis.correlate  rolling beta, lead-lag correlation, Granger tests
optlab.fetch.*             downloaders for Yahoo/Stooq prices, SEC XBRL facts, HN Algolia, Cboe chains
optlab.report.charts       matplotlib figures used by the written report
"""

__all__ = ["analysis", "fetch", "report"]
