"""
Example usage of pygrowup_cdc_calculator package

This script demonstrates how to use the CDC growth calculator
and the integrated medical growth calculator.
"""

from pygrowup_cdc_calculator import (
    CDCGrowthCalculator,
    MedicalGrowthCalculator,
    Sex,
    GrowthMetric,
    GrowthStandard
)


def example_cdc_calculator():
    """Examples using CDC Growth Calculator"""
    print("=" * 60)
    print("CDC Growth Calculator Examples")
    print("=" * 60)

    # Initialize calculator
    calc = CDCGrowthCalculator()

    # Example 1: Calculate BMI-for-age percentile
    print("\n1. BMI-for-age calculation for 10-year-old boy")
    result = calc.calculate_percentile(
        metric=GrowthMetric.BMI_FOR_AGE,
        sex=Sex.MALE,
        age_months=120,  # 10 years
        bmi=18.5
    )
    print(f"   BMI: 18.5 kg/m²")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Z-Score: {result.z_score:.2f}")

    # Example 2: Calculate weight-for-age
    print("\n2. Weight-for-age for 5-year-old girl")
    result = calc.calculate_percentile(
        metric=GrowthMetric.WEIGHT_FOR_AGE,
        sex=Sex.FEMALE,
        age_months=60,
        weight_kg=18.0
    )
    print(f"   Weight: 18.0 kg")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Z-Score: {result.z_score:.2f}")

    # Example 3: Calculate stature-for-age
    print("\n3. Stature-for-age for 15-year-old boy")
    result = calc.calculate_percentile(
        metric=GrowthMetric.STATURE_FOR_AGE,
        sex=Sex.MALE,
        age_months=180,
        height_cm=170.0
    )
    print(f"   Height: 170.0 cm")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Z-Score: {result.z_score:.2f}")

    # Example 4: Head circumference for infant
    print("\n4. Head circumference for 6-month-old girl")
    result = calc.calculate_percentile(
        metric=GrowthMetric.HEAD_CIRCUMFERENCE,
        sex=Sex.FEMALE,
        age_months=6,
        head_circumference_cm=42.0
    )
    print(f"   Head circumference: 42.0 cm")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Z-Score: {result.z_score:.2f}")


def example_medical_calculator():
    """Examples using Medical Growth Calculator (integrated CDC/WHO)"""
    print("\n\n" + "=" * 60)
    print("Medical Growth Calculator Examples (CDC + WHO)")
    print("=" * 60)

    # Initialize calculator
    calc = MedicalGrowthCalculator()

    # Example 1: Calculate with automatic standard selection (young child)
    print("\n1. Weight for 3-year-old (36 months) - AUTO standard selection")
    result = calc.calculate_zscore(
        measurement_type="weight",
        age_months=36,
        sex="M",
        weight_kg=14.5,
        standard=GrowthStandard.AUTO
    )
    print(f"   Weight: 14.5 kg")
    print(f"   Z-Score: {result.z_score:.2f}")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Standard used: {result.standard}")
    print(f"   Note: AUTO selected WHO for age < 60 months")

    # Example 2: Explicitly use CDC standard
    print("\n2. Height for 7-year-old (84 months) - CDC standard")
    result = calc.calculate_zscore(
        measurement_type="height",
        age_months=84,
        sex="F",
        height_cm=120.0,
        standard=GrowthStandard.CDC
    )
    print(f"   Height: 120.0 cm")
    print(f"   Z-Score: {result.z_score:.2f}")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Standard used: {result.standard}")

    # Example 3: BMI calculation
    print("\n3. BMI for 12-year-old (144 months)")
    result = calc.calculate_zscore(
        measurement_type="bmi",
        age_months=144,
        sex="M",
        height_cm=150.0,
        weight_kg=45.0,
        standard=GrowthStandard.AUTO
    )
    print(f"   Height: 150.0 cm, Weight: 45.0 kg")
    print(f"   BMI: {45.0 / (1.5 ** 2):.1f} kg/m²")
    print(f"   Z-Score: {result.z_score:.2f}")
    print(f"   Percentile: {result.percentile:.1f}%")
    print(f"   Standard used: {result.standard}")


def example_batch_processing():
    """Example of batch processing multiple measurements"""
    print("\n\n" + "=" * 60)
    print("Batch Processing Example")
    print("=" * 60)

    calc = MedicalGrowthCalculator()

    # Sample patient data
    patients = [
        {"age_months": 24, "sex": "M", "weight_kg": 12.5, "height_cm": 86.0},
        {"age_months": 72, "sex": "F", "weight_kg": 22.0, "height_cm": 118.0},
        {"age_months": 120, "sex": "M", "weight_kg": 32.0, "height_cm": 140.0},
    ]

    print("\nProcessing multiple patients:")
    for i, patient in enumerate(patients, 1):
        result = calc.calculate_zscore(
            measurement_type="bmi",
            age_months=patient["age_months"],
            sex=patient["sex"],
            weight_kg=patient["weight_kg"],
            height_cm=patient["height_cm"],
            standard=GrowthStandard.AUTO
        )

        print(f"\nPatient {i}:")
        print(f"   Age: {patient['age_months']} months")
        print(f"   Sex: {patient['sex']}")
        print(f"   Height: {patient['height_cm']} cm, Weight: {patient['weight_kg']} kg")
        print(f"   BMI Z-Score: {result.z_score:.2f}")
        print(f"   BMI Percentile: {result.percentile:.1f}%")
        print(f"   Standard: {result.standard}")


if __name__ == "__main__":
    # Run all examples
    example_cdc_calculator()
    example_medical_calculator()
    example_batch_processing()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
