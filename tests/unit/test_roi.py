from backend.services.agents.finance.roi import ROICalculator


def test_roi_calculation_positive():
    result = ROICalculator.calculate(net_profit=500.0, total_investment=1000.0)
    assert result == 50.0


def test_roi_calculation_zero_investment():
    result = ROICalculator.calculate(net_profit=500.0, total_investment=0.0)
    assert result == 0.0


def test_roi_calculation_negative_profit():
    result = ROICalculator.calculate(net_profit=-200.0, total_investment=1000.0)
    assert result == -20.0
