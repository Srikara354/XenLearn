import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Dict, Any

class DataProcessor:
    """Handles data loading, processing, and analysis operations"""
    
    def load_file(self, uploaded_file) -> pd.DataFrame:
        """Load data from uploaded file"""
        try:
            if uploaded_file.name.endswith('.csv'):
                # Try different encodings for CSV files
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)  # Reset file pointer
                    df = pd.read_csv(uploaded_file, encoding='latin-1')
            
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel files.")
            
            # Basic data validation
            if df.empty:
                raise ValueError("The uploaded file is empty.")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            return df
            
        except Exception as e:
            raise Exception(f"Failed to load file: {str(e)}")
    
    def get_summary_statistics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate summary statistics for numeric columns"""
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                return pd.DataFrame()
            
            summary = numeric_data.describe()
            
            # Add additional statistics
            additional_stats = pd.DataFrame({
                col: {
                    'median': numeric_data[col].median(),
                    'mode': numeric_data[col].mode().iloc[0] if len(numeric_data[col].mode()) > 0 else np.nan,
                    'variance': numeric_data[col].var(),
                    'skewness': numeric_data[col].skew(),
                    'kurtosis': numeric_data[col].kurtosis()
                }
                for col in numeric_data.columns
            }).T
            
            # Combine with describe() output
            summary = pd.concat([summary, additional_stats])
            
            return summary.round(3)
            
        except Exception as e:
            st.error(f"Error calculating summary statistics: {str(e)}")
            return pd.DataFrame()
    
    def get_data_quality_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate a comprehensive data quality report"""
        try:
            report = {}
            
            # Missing values analysis
            missing_values = data.isnull().sum()
            report['missing_values'] = missing_values
            
            # Duplicate rows
            report['duplicate_rows'] = data.duplicated().sum()
            
            # Data types
            report['data_types'] = data.dtypes
            
            # Unique values per column
            report['unique_values'] = data.nunique()
            
            # Memory usage
            report['memory_usage'] = data.memory_usage(deep=True)
            
            # Numeric columns statistics
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            report['numeric_columns'] = len(numeric_cols)
            
            # Categorical columns statistics
            categorical_cols = data.select_dtypes(include=['object', 'string']).columns
            report['categorical_columns'] = len(categorical_cols)
            
            # Outliers detection (using IQR method for numeric columns)
            outliers_count = {}
            for col in numeric_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
                outliers_count[col] = len(outliers)
            
            report['outliers'] = outliers_count
            
            return report
            
        except Exception as e:
            st.error(f"Error generating data quality report: {str(e)}")
            return {}
    
    def filter_data(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the data"""
        try:
            filtered_data = data.copy()
            
            for column, filter_config in filters.items():
                if column not in data.columns:
                    continue
                
                filter_type = filter_config.get('type')
                filter_value = filter_config.get('value')
                
                if filter_type == 'equals':
                    filtered_data = filtered_data[filtered_data[column] == filter_value]
                elif filter_type == 'contains':
                    filtered_data = filtered_data[filtered_data[column].str.contains(filter_value, na=False)]
                elif filter_type == 'range':
                    min_val, max_val = filter_value
                    filtered_data = filtered_data[
                        (filtered_data[column] >= min_val) & 
                        (filtered_data[column] <= max_val)
                    ]
                elif filter_type == 'in':
                    filtered_data = filtered_data[filtered_data[column].isin(filter_value)]
            
            return filtered_data
            
        except Exception as e:
            st.error(f"Error filtering data: {str(e)}")
            return data
    
    def get_column_info(self, data: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Get detailed information about a specific column"""
        try:
            if column not in data.columns:
                return {}
            
            col_data = data[column]
            info = {
                'name': column,
                'dtype': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isnull().sum(),
                'unique_count': col_data.nunique(),
                'memory_usage': col_data.memory_usage(deep=True)
            }
            
            # Add type-specific information
            if col_data.dtype in ['int64', 'float64']:
                info.update({
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'std': col_data.std()
                })
            elif col_data.dtype == 'object':
                info.update({
                    'most_frequent': col_data.mode().iloc[0] if len(col_data.mode()) > 0 else None,
                    'avg_length': col_data.astype(str).str.len().mean()
                })
            
            return info
            
        except Exception as e:
            st.error(f"Error getting column info: {str(e)}")
            return {}
