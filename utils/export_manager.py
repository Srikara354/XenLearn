import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import io
import base64
from typing import Optional, Dict, Any
import json

class ExportManager:
    """Handles data and visualization export functionality"""
    
    def export_data_to_csv(self, data: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export DataFrame to CSV format"""
        try:
            if filename is None:
                filename = "exported_data.csv"
            
            # Convert DataFrame to CSV string
            csv_string = data.to_csv(index=False)
            return csv_string
            
        except Exception as e:
            st.error(f"Error exporting data to CSV: {str(e)}")
            return ""
    
    def export_data_to_excel(self, data: pd.DataFrame, filename: Optional[str] = None) -> bytes:
        """Export DataFrame to Excel format"""
        try:
            if filename is None:
                filename = "exported_data.xlsx"
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name='Data', index=False)
            
            excel_data = output.getvalue()
            return excel_data
            
        except Exception as e:
            st.error(f"Error exporting data to Excel: {str(e)}")
            return b""
    
    def export_chart_to_html(self, fig: go.Figure, filename: Optional[str] = None) -> str:
        """Export Plotly figure to HTML format"""
        try:
            if filename is None:
                filename = "chart.html"
            
            # Convert figure to HTML
            html_string = fig.to_html(
                include_plotlyjs='cdn',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
                }
            )
            
            return html_string
            
        except Exception as e:
            st.error(f"Error exporting chart to HTML: {str(e)}")
            return ""
    
    def export_chart_to_json(self, fig: go.Figure) -> str:
        """Export Plotly figure to JSON format"""
        try:
            # Convert figure to JSON
            fig_json = fig.to_json()
            return fig_json
            
        except Exception as e:
            st.error(f"Error exporting chart to JSON: {str(e)}")
            return ""
    
    def create_downloadable_link(self, data: str, filename: str, mime_type: str) -> str:
        """Create a downloadable link for data"""
        try:
            # Encode data to base64
            b64_data = base64.b64encode(data.encode()).decode()
            
            # Create download link
            href = f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">Download {filename}</a>'
            return href
            
        except Exception as e:
            st.error(f"Error creating download link: {str(e)}")
            return ""
    
    def generate_report(self, data: pd.DataFrame, charts: list, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive analysis report"""
        try:
            report_lines = []
            
            # Report header
            report_lines.append("# Data Analysis Report")
            report_lines.append(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            
            # Data overview
            report_lines.append("## Data Overview")
            report_lines.append(f"- **Total Rows:** {len(data):,}")
            report_lines.append(f"- **Total Columns:** {len(data.columns)}")
            report_lines.append(f"- **Data Types:** {data.dtypes.value_counts().to_dict()}")
            report_lines.append("")
            
            # Missing values summary
            missing_values = data.isnull().sum()
            if missing_values.sum() > 0:
                report_lines.append("## Missing Values")
                for col, missing_count in missing_values.items():
                    if missing_count > 0:
                        missing_pct = (missing_count / len(data)) * 100
                        report_lines.append(f"- **{col}:** {missing_count} ({missing_pct:.1f}%)")
                report_lines.append("")
            
            # Numeric columns summary
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                report_lines.append("## Numeric Columns Summary")
                summary_stats = data[numeric_cols].describe()
                for col in numeric_cols:
                    report_lines.append(f"### {col}")
                    report_lines.append(f"- Mean: {summary_stats.loc['mean', col]:.2f}")
                    report_lines.append(f"- Median: {summary_stats.loc['50%', col]:.2f}")
                    report_lines.append(f"- Std Dev: {summary_stats.loc['std', col]:.2f}")
                    report_lines.append("")
            
            # Categorical columns summary
            categorical_cols = data.select_dtypes(include=['object', 'string']).columns
            if len(categorical_cols) > 0:
                report_lines.append("## Categorical Columns Summary")
                for col in categorical_cols:
                    unique_count = data[col].nunique()
                    most_common = data[col].mode().iloc[0] if len(data[col].mode()) > 0 else "N/A"
                    report_lines.append(f"### {col}")
                    report_lines.append(f"- Unique Values: {unique_count}")
                    report_lines.append(f"- Most Common: {most_common}")
                    report_lines.append("")
            
            # Charts summary
            if charts:
                report_lines.append("## Visualizations Created")
                for i, chart_info in enumerate(charts, 1):
                    report_lines.append(f"{i}. {chart_info.get('type', 'Unknown Chart')}")
                    if 'title' in chart_info:
                        report_lines.append(f"   - Title: {chart_info['title']}")
                report_lines.append("")
            
            # Analysis insights
            if analysis_results:
                report_lines.append("## Key Insights")
                for insight_type, insight_data in analysis_results.items():
                    report_lines.append(f"### {insight_type.replace('_', ' ').title()}")
                    if isinstance(insight_data, dict):
                        for key, value in insight_data.items():
                            report_lines.append(f"- {key}: {value}")
                    else:
                        report_lines.append(f"- {insight_data}")
                    report_lines.append("")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            return ""
    
    def save_session_state(self, data: pd.DataFrame, filters: Dict[str, Any], 
                          chart_configs: list) -> str:
        """Save current session state for sharing"""
        try:
            session_data = {
                'data_shape': data.shape,
                'data_columns': data.columns.tolist(),
                'data_dtypes': data.dtypes.astype(str).to_dict(),
                'filters_applied': filters,
                'chart_configurations': chart_configs,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            # Convert to JSON
            session_json = json.dumps(session_data, indent=2)
            return session_json
            
        except Exception as e:
            st.error(f"Error saving session state: {str(e)}")
            return ""
    
    def create_shareable_url(self, base_url: str, session_data: Dict[str, Any]) -> str:
        """Create a shareable URL with encoded session data"""
        try:
            # Encode session data
            encoded_data = base64.b64encode(
                json.dumps(session_data).encode()
            ).decode()
            
            # Create shareable URL
            shareable_url = f"{base_url}?session={encoded_data}"
            return shareable_url
            
        except Exception as e:
            st.error(f"Error creating shareable URL: {str(e)}")
            return base_url
