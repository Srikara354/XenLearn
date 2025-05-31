import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Any

class ChartGenerator:
    """Handles creation of various chart types using Plotly"""
    
    def create_chart(self, data: pd.DataFrame, chart_type: str, x_axis: Optional[str], 
                    y_axis: Optional[str], color_column: Optional[str], 
                    title: str, height: int = 500) -> Optional[go.Figure]:
        """Create a chart based on the specified parameters"""
        
        try:
            if data.empty:
                st.warning("No data available to create chart.")
                return None
            
            # Configure common chart properties
            chart_config = {
                'title': title,
                'height': height,
                'template': 'plotly_white'
            }
            
            fig = None
            
            if chart_type == "Scatter Plot":
                fig = self._create_scatter_plot(data, x_axis, y_axis, color_column, chart_config)
            
            elif chart_type == "Line Chart":
                fig = self._create_line_chart(data, x_axis, y_axis, color_column, chart_config)
            
            elif chart_type == "Bar Chart":
                fig = self._create_bar_chart(data, x_axis, y_axis, color_column, chart_config)
            
            elif chart_type == "Histogram":
                fig = self._create_histogram(data, x_axis, color_column, chart_config)
            
            elif chart_type == "Box Plot":
                fig = self._create_box_plot(data, x_axis, y_axis, color_column, chart_config)
            
            elif chart_type == "Heatmap":
                fig = self._create_heatmap(data, chart_config)
            
            elif chart_type == "Pie Chart":
                fig = self._create_pie_chart(data, x_axis, y_axis, chart_config)
            
            if fig:
                # Apply mobile-friendly configurations
                fig.update_layout(
                    autosize=True,
                    margin=dict(l=20, r=20, t=40, b=20),
                    font=dict(size=12),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                # Make it responsive
                fig.update_layout(
                    xaxis=dict(automargin=True),
                    yaxis=dict(automargin=True)
                )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating {chart_type}: {str(e)}")
            return None
    
    def _create_scatter_plot(self, data: pd.DataFrame, x_axis: str, y_axis: str, 
                           color_column: Optional[str], config: dict) -> go.Figure:
        """Create a scatter plot"""
        fig = px.scatter(
            data, 
            x=x_axis, 
            y=y_axis, 
            color=color_column,
            title=config['title'],
            height=config['height'],
            template=config['template']
        )
        
        # Add trend line for numeric data
        if data[x_axis].dtype in ['int64', 'float64'] and data[y_axis].dtype in ['int64', 'float64']:
            fig.add_trace(
                go.Scatter(
                    x=data[x_axis], 
                    y=np.poly1d(np.polyfit(data[x_axis], data[y_axis], 1))(data[x_axis]),
                    mode='lines',
                    name='Trend Line',
                    line=dict(dash='dash', color='red')
                )
            )
        
        return fig
    
    def _create_line_chart(self, data: pd.DataFrame, x_axis: str, y_axis: str, 
                          color_column: Optional[str], config: dict) -> go.Figure:
        """Create a line chart"""
        if color_column:
            fig = px.line(
                data, 
                x=x_axis, 
                y=y_axis, 
                color=color_column,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        else:
            fig = px.line(
                data, 
                x=x_axis, 
                y=y_axis,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        
        return fig
    
    def _create_bar_chart(self, data: pd.DataFrame, x_axis: str, y_axis: str, 
                         color_column: Optional[str], config: dict) -> go.Figure:
        """Create a bar chart"""
        # Aggregate data if needed
        if y_axis:
            agg_data = data.groupby(x_axis)[y_axis].sum().reset_index()
        else:
            agg_data = data[x_axis].value_counts().reset_index()
            agg_data.columns = [x_axis, 'count']
            y_axis = 'count'
        
        fig = px.bar(
            agg_data, 
            x=x_axis, 
            y=y_axis, 
            color=color_column if color_column in agg_data.columns else None,
            title=config['title'],
            height=config['height'],
            template=config['template']
        )
        
        return fig
    
    def _create_histogram(self, data: pd.DataFrame, x_axis: str, 
                         color_column: Optional[str], config: dict) -> go.Figure:
        """Create a histogram"""
        fig = px.histogram(
            data, 
            x=x_axis, 
            color=color_column,
            title=config['title'],
            height=config['height'],
            template=config['template'],
            nbins=30
        )
        
        # Add statistics
        mean_val = data[x_axis].mean()
        median_val = data[x_axis].median()
        
        fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                     annotation_text=f"Mean: {mean_val:.2f}")
        fig.add_vline(x=median_val, line_dash="dash", line_color="blue", 
                     annotation_text=f"Median: {median_val:.2f}")
        
        return fig
    
    def _create_box_plot(self, data: pd.DataFrame, x_axis: Optional[str], y_axis: str, 
                        color_column: Optional[str], config: dict) -> go.Figure:
        """Create a box plot"""
        if x_axis:
            fig = px.box(
                data, 
                x=x_axis, 
                y=y_axis, 
                color=color_column,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        else:
            fig = px.box(
                data, 
                y=y_axis,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        
        return fig
    
    def _create_heatmap(self, data: pd.DataFrame, config: dict) -> go.Figure:
        """Create a correlation heatmap"""
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            raise ValueError("Need at least 2 numeric columns for heatmap")
        
        corr_matrix = numeric_data.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title=config['title'],
            height=config['height'],
            template=config['template'],
            color_continuous_scale="RdBu_r"
        )
        
        return fig
    
    def _create_pie_chart(self, data: pd.DataFrame, x_axis: str, y_axis: Optional[str], 
                         config: dict) -> go.Figure:
        """Create a pie chart"""
        if y_axis:
            # Use specified value column
            agg_data = data.groupby(x_axis)[y_axis].sum().reset_index()
            fig = px.pie(
                agg_data, 
                names=x_axis, 
                values=y_axis,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        else:
            # Use count of categories
            value_counts = data[x_axis].value_counts()
            fig = px.pie(
                values=value_counts.values, 
                names=value_counts.index,
                title=config['title'],
                height=config['height'],
                template=config['template']
            )
        
        return fig
    
    def get_chart_recommendations(self, data: pd.DataFrame) -> list:
        """Suggest appropriate chart types based on data characteristics"""
        recommendations = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object', 'string']).columns
        
        # Based on data types, suggest appropriate charts
        if len(numeric_cols) >= 2:
            recommendations.extend(["Scatter Plot", "Line Chart", "Heatmap"])
        
        if len(numeric_cols) >= 1:
            recommendations.extend(["Histogram", "Box Plot"])
        
        if len(categorical_cols) >= 1:
            recommendations.extend(["Bar Chart", "Pie Chart"])
        
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            recommendations.extend(["Box Plot", "Bar Chart"])
        
        return list(set(recommendations))  # Remove duplicates
