"""
Tests for CDC Growth Calculator

Basic test structure for the package. Expand with actual test cases.
"""

import pytest
from pygrowup_cdc_calculator import CDCGrowthCalculator, Sex, GrowthMetric


class TestCDCGrowthCalculator:
    """Test cases for CDCGrowthCalculator"""

    def setup_method(self):
        """Set up test fixtures"""
        self.calc = CDCGrowthCalculator()

    def test_calculator_initialization(self):
        """Test that calculator initializes correctly"""
        assert self.calc is not None
        assert hasattr(self.calc, 'calculate_percentile')
        assert hasattr(self.calc, 'calculate_zscore')

    def test_bmi_calculation_basic(self):
        """Test basic BMI-for-age calculation"""
        result = self.calc.calculate_percentile(
            metric=GrowthMetric.BMI_FOR_AGE,
            sex=Sex.MALE,
            age_months=120,
            bmi=18.5
        )

        assert result is not None
        assert hasattr(result, 'percentile')
        assert hasattr(result, 'z_score')
        assert 0 <= result.percentile <= 100
        assert isinstance(result.z_score, (int, float))

    def test_weight_for_age(self):
        """Test weight-for-age calculation"""
        result = self.calc.calculate_percentile(
            metric=GrowthMetric.WEIGHT_FOR_AGE,
            sex=Sex.FEMALE,
            age_months=60,
            weight_kg=18.0
        )

        assert result is not None
        assert 0 <= result.percentile <= 100

    def test_stature_for_age(self):
        """Test stature-for-age calculation"""
        result = self.calc.calculate_percentile(
            metric=GrowthMetric.STATURE_FOR_AGE,
            sex=Sex.MALE,
            age_months=180,
            height_cm=170.0
        )

        assert result is not None
        assert 0 <= result.percentile <= 100


# Add more test cases as needed
if __name__ == '__main__':
    pytest.main([__file__])
