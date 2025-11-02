# PyGrowUp CDC Calculator

A comprehensive Python package for calculating pediatric growth metrics (z-scores and percentiles) using both CDC and WHO growth standards.

## Features

- **CDC Growth Standards**: Support for children and adolescents aged 2-20 years
- **WHO Growth Standards**: Support for infants and young children aged 0-60 months (via pygrowup2)
- **Multiple Metrics**:
  - Weight-for-age
  - Stature/length-for-age
  - Weight-for-stature
  - BMI-for-age
  - Head circumference
- **Automatic Standard Selection**: Automatically chooses appropriate growth standard based on age
- **LMS Method**: Uses the Lambda-Mu-Sigma method for accurate percentile calculations
- **Type-Safe**: Built with Python type hints and dataclasses

## Installation

### From PyPI (once published)
```bash
pip install pygrowup-cdc-calculator
```

### From Source
```bash
git clone https://github.com/gyasifred/pygrowup_cdc_calculator.git
cd pygrowup_cdc_calculator
pip install -e .
```

## Requirements

- Python >= 3.6
- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- pygrowup2 (optional, for WHO standards)

## Quick Start

### Using CDC Calculator

```python
from pygrowup_cdc_calculator import CDCGrowthCalculator, Sex, GrowthMetric

# Initialize calculator
calc = CDCGrowthCalculator()

# Calculate BMI-for-age percentile
result = calc.calculate_percentile(
    metric=GrowthMetric.BMI_FOR_AGE,
    sex=Sex.MALE,
    age_months=120,  # 10 years old
    bmi=18.5
)

print(f"Percentile: {result.percentile:.1f}")
print(f"Z-Score: {result.z_score:.2f}")
```

### Using Integrated Medical Calculator

```python
from pygrowup_cdc_calculator import MedicalGrowthCalculator, GrowthStandard

# Initialize calculator
calc = MedicalGrowthCalculator()

# Calculate with automatic standard selection
result = calc.calculate_zscore(
    measurement_type="weight",
    age_months=36,
    sex="M",
    weight_kg=14.5,
    standard=GrowthStandard.AUTO  # Automatically selects WHO for age < 60 months
)

print(f"Z-Score: {result.z_score:.2f}")
print(f"Percentile: {result.percentile:.1f}")
print(f"Standard used: {result.standard}")
```

## API Documentation

### CDCGrowthCalculator

Main class for CDC growth calculations.

#### Methods

- `calculate_percentile()`: Calculate percentile for a given metric
- `calculate_zscore()`: Calculate z-score for a given metric
- `inverse_percentile()`: Find measurement value for a given percentile

### MedicalGrowthCalculator

Integrated calculator that combines CDC and WHO standards.

#### Methods

- `calculate_zscore()`: Calculate z-score with automatic or manual standard selection
- `calculate_batch()`: Process multiple measurements at once
- `get_applicable_standard()`: Determine which standard to use for a given age

### Enumerations

#### Sex
- `Sex.MALE` (1)
- `Sex.FEMALE` (2)

#### GrowthMetric
- `GrowthMetric.WEIGHT_FOR_AGE`
- `GrowthMetric.STATURE_FOR_AGE`
- `GrowthMetric.WEIGHT_FOR_STATURE`
- `GrowthMetric.BMI_FOR_AGE`
- `GrowthMetric.HEAD_CIRCUMFERENCE`

#### GrowthStandard
- `GrowthStandard.WHO` - WHO standards (0-60 months)
- `GrowthStandard.CDC` - CDC standards (60+ months)
- `GrowthStandard.AUTO` - Automatic selection based on age

## Data Sources

- **CDC Growth Charts**: Based on the 2000 CDC Growth Charts
- **WHO Growth Standards**: Via pygrowup2 package (WHO 2006/2007 standards)

## Development

### Running Tests
```bash
pytest tests/
```

### Building from Source
```bash
python setup.py sdist bdist_wheel
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Frederick Gyasi**
- Email: gyasi@musc.edu
- Institution: Medical University of South Carolina, Biomedical Informatics Center
- Lab: HeiderLab

## Acknowledgments

- CDC for providing growth chart data
- WHO for growth standards
- pygrowup2 package for WHO calculations

## Citation

If you use this package in your research, please cite:

```bibtex
@software{pygrowup_cdc_calculator,
  author = {Gyasi, Frederick},
  title = {PyGrowUp CDC Calculator: Pediatric Growth Metrics Calculator},
  year = {2025},
  url = {https://github.com/gyasifred/pygrowup_cdc_calculator}
}
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/gyasifred/pygrowup_cdc_calculator/issues
- Email: gyasi@musc.edu
