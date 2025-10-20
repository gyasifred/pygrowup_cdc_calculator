"""
Integrated Growth Calculator

Combines CDC and WHO (pygrowup2) growth calculations for z-scores and percentiles.
Selects standards based on age: WHO for 0-60 months, CDC for 60+ months.

Author: Frederick Gyasi (gyasi@musc.edu)
Institution: Medical University of South Carolina, Biomedical Informatics Center
Lab: HeiderLab
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
from pathlib import Path
from scipy.stats import norm

logger = logging.getLogger(__name__)

# PyGrowUp2 integration
try:
    from pygrowup import Observation
    PYGROWUP_AVAILABLE = True
    logger.info("PyGrowUp2 successfully imported for WHO calculations")
except ImportError:
    PYGROWUP_AVAILABLE = False
    logger.warning("PyGrowUp2 not available: WHO calculations will be skipped.")

# CDC calculator integration
try:
    from .cdc_growth_calculator import CDCGrowthCalculator, GrowthMetric as CDCGrowthMetric, Sex as CDCSex
    CDC_AVAILABLE = True
except ImportError:
    CDC_AVAILABLE = False
    logger.warning("CDC growth calculator not available")

class GrowthStandard(Enum):
    """Growth reference standards with specific age ranges"""
    WHO = "WHO"  # 0-60 months
    CDC = "CDC"  # 60+ months
    AUTO = "AUTO"  # Automatic selection based on age

@dataclass
class ZScoreResult:
    """Result of a z-score calculation"""
    measurement_type: str
    z_score: float
    percentile: float
    measurement_value: float
    age_months: float
    sex: str
    standard: str
    date_recorded: Optional[datetime] = None

class MedicalGrowthCalculator:
    """
    Integrated growth calculator for CDC and WHO standards.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize growth calculator.
        
        Args:
            data_path: Path to CDC growth reference data files
        """
        self.data_path = data_path or Path(__file__).parent / "cdc_data"
        self.pygrowup_available = PYGROWUP_AVAILABLE
        self.cdc_available = CDC_AVAILABLE
        self._cdc_calculator = None
        
        if self.cdc_available:
            try:
                self._cdc_calculator = CDCGrowthCalculator(data_directory=str(self.data_path))
                logger.info("CDC calculator initialized successfully")
            except Exception as e:
                logger.error(f"CDC calculator initialization failed: {e}")
                self.cdc_available = False
    
    def calculate_z_score(self, 
                         measurement_type: str,
                         value: float,
                         age_months: float,
                         sex: str,
                         height_cm: Optional[float] = None,
                         date_recorded: Optional[datetime] = None) -> Optional[ZScoreResult]:
        """
        Calculate z-score using appropriate standard (WHO for <60 months, CDC for >=60 months).
        
        Args:
            measurement_type: Type of measurement (e.g., weight_for_age)
            value: Measurement value
            age_months: Age in months
            sex: Patient sex ('male' or 'female')
            height_cm: Height in cm (for weight-for-height)
            date_recorded: Date of measurement
            
        Returns:
            ZScoreResult or None if calculation fails
        """
        try:
            sex_normalized = self._normalize_sex_input(sex)
            if not sex_normalized:
                logger.error(f"Invalid sex value: {sex}")
                return None
            
            if age_months < 0:
                logger.error(f"Invalid age: {age_months}")
                return None
            
            if value <= 0:
                logger.error(f"Invalid measurement value: {value}")
                return None
            
            if age_months < 60 and self.pygrowup_available:
                return self._calculate_who_z_score(measurement_type, value, age_months, sex_normalized, height_cm, date_recorded)
            elif self.cdc_available:
                return self._calculate_cdc_z_score(measurement_type, value, age_months, sex_normalized, height_cm, date_recorded)
            else:
                logger.error("No valid calculator available")
                return None
                
        except Exception as e:
            logger.error(f"Z-score calculation failed: {e}")
            return None
    
    def _normalize_sex_input(self, sex: Union[str, Any]) -> Optional[str]:
        """
        Normalize sex input to handle data type inconsistencies.
        """
        try:
            if isinstance(sex, tuple):
                for item in sex:
                    if item and str(item).strip():
                        sex = str(item).strip()
                        break
                else:
                    return None
            
            sex_str = str(sex).strip().lower()
            male_variants = ['male', 'm', 'boy', 'masculine', '1']
            female_variants = ['female', 'f', 'girl', 'feminine', '2']
            
            if sex_str in male_variants:
                return 'male'
            elif sex_str in female_variants:
                return 'female'
            return None
                
        except Exception as e:
            logger.error(f"Error normalizing sex input: {e}")
            return None
    
    def _calculate_who_z_score(self,
                             measurement_type: str,
                             value: float,
                             age_months: float,
                             sex: str,
                             height_cm: Optional[float],
                             date_recorded: Optional[datetime]) -> Optional[ZScoreResult]:
        """
        Calculate WHO z-score using pygrowup2.
        """
        try:
            sex_constant = Observation.MALE if sex.lower() == 'male' else Observation.FEMALE
            obs = Observation(sex=sex_constant, age_in_months=age_months)
            
            measurement_type_lower = measurement_type.lower()
            if measurement_type_lower in ['weight_for_age', 'wfa']:
                z_score = float(obs.weight_for_age(value))
            elif measurement_type_lower in ['height_for_age', 'length_for_age', 'hfa', 'lfa']:
                z_score = float(obs.length_or_height_for_age(value))
            elif measurement_type_lower in ['weight_for_height', 'weight_for_length', 'wfh', 'wfl']:
                if height_cm is None:
                    logger.warning("Height required for weight-for-height calculation")
                    return None
                z_score = float(obs.weight_for_length(value, height_cm))
            elif measurement_type_lower in ['head_circumference_for_age', 'hcfa']:
                z_score = float(obs.head_circumference_for_age(value))
            elif measurement_type_lower in ['bmi_for_age', 'bmifa'] and hasattr(obs, 'bmi_for_age'):
                z_score = float(obs.bmi_for_age(value))
            else:
                logger.warning(f"Unknown measurement type for pygrowup: {measurement_type}")
                return None
            
            percentile = round(norm.cdf(z_score) * 100, 2)
            
            return ZScoreResult(
                measurement_type=measurement_type,
                z_score=round(z_score, 2),
                percentile=percentile,
                measurement_value=value,
                age_months=age_months,
                sex=sex,
                standard="WHO",
                date_recorded=date_recorded
            )
            
        except Exception as e:
            logger.error(f"WHO z-score calculation failed: {e}")
            return None
    
    def _calculate_cdc_z_score(self,
                             measurement_type: str,
                             value: float,
                             age_months: float,
                             sex: str,
                             height_cm: Optional[float],
                             date_recorded: Optional[datetime]) -> Optional[ZScoreResult]:
        """
        Calculate CDC z-score for older children.
        """
        try:
            if not self.cdc_available or not self._cdc_calculator:
                logger.warning("CDC calculator not available")
                return None
            
            cdc_metric_map = {
                'weight_for_age': CDCGrowthMetric.WEIGHT_FOR_AGE,
                'height_for_age': CDCGrowthMetric.STATURE_FOR_AGE,
                'length_for_age': CDCGrowthMetric.STATURE_FOR_AGE,
                'weight_for_height': CDCGrowthMetric.WEIGHT_FOR_STATURE,
                'weight_for_length': CDCGrowthMetric.WEIGHT_FOR_STATURE,
                'bmi_for_age': CDCGrowthMetric.BMI_FOR_AGE,
                'head_circumference_for_age': CDCGrowthMetric.HEAD_CIRCUMFERENCE
            }
            
            cdc_metric = cdc_metric_map.get(measurement_type.lower())
            if not cdc_metric:
                logger.warning(f"CDC metric not available for {measurement_type}")
                return None
            
            cdc_sex = CDCSex.MALE if sex.lower() == 'male' else CDCSex.FEMALE
            cdc_result = self._cdc_calculator.calculate_growth_percentile(
                metric=cdc_metric,
                sex=cdc_sex,
                value=value,
                age_months=age_months,
                height_cm=height_cm
            )
            
            if not cdc_result:
                return None
            
            return ZScoreResult(
                measurement_type=measurement_type,
                z_score=cdc_result.z_score,
                percentile=cdc_result.percentile,
                measurement_value=value,
                age_months=age_months,
                sex=sex,
                standard="CDC",
                date_recorded=date_recorded
            )
            
        except Exception as e:
            logger.error(f"CDC z-score calculation failed: {e}")
            return None
