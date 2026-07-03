# Generic calculator module exporting all specialized calculators
from .investment import InvestmentCalculator
from .revenue import RevenueCalculator
from .expenses import ExpenseCalculator
from .profit import ProfitCalculator
from .roi import ROICalculator
from .break_even import BreakEvenCalculator
from .cashflow import CashflowCalculator


class FinanceCalculator:
    """Facade for all finance calculators."""

    investment = InvestmentCalculator
    revenue = RevenueCalculator
    expenses = ExpenseCalculator
    profit = ProfitCalculator
    roi = ROICalculator
    break_even = BreakEvenCalculator
    cashflow = CashflowCalculator
