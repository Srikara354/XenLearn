import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import DataProcessor
from utils.chart_generator import ChartGenerator
from utils.export_manager import ExportManager
import io
import base64
from urllib.parse import urlencode

# Configure page
st.set_page_config(
    page_title="Team Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'chart_config' not in st.session_state:
    st.session_state.chart_config = {}

def main():
    st.title("📊 Team Data Explorer")
    st.markdown("**Mobile-friendly data analysis and visualization tool for teams**")
    
    # Initialize utilities
    data_processor = DataProcessor()
    chart_generator = ChartGenerator()
    export_manager = ExportManager()
    
    # Sidebar for file upload and basic controls
    with st.sidebar:
        st.header("📁 Data Upload")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload CSV or Excel files for analysis"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Loading data..."):
                    st.session_state.data = data_processor.load_file(uploaded_file)
                    st.session_state.filtered_data = st.session_state.data.copy()
                st.success(f"✅ Loaded {len(st.session_state.data)} rows")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.session_state.data = None
        
        # Show data info if available
        if st.session_state.data is not None:
            st.subheader("📋 Dataset Info")
            st.write(f"**Rows:** {len(st.session_state.data):,}")
            st.write(f"**Columns:** {len(st.session_state.data.columns)}")
            st.write(f"**Size:** {st.session_state.data.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Main content area
    if st.session_state.data is None:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### 🚀 Get Started
            
            Upload a CSV or Excel file using the sidebar to begin your data analysis journey.
            
            **Features:**
            - 📱 Mobile-friendly interface
            - 🔍 Interactive data exploration
            - 📊 Multiple visualization types
            - 🔗 Shareable visualization links
            - 📈 Statistical analysis
            - 💾 Export capabilities
            """)
    else:
        # Data analysis interface
        tabs = st.tabs(["🔍 Explore", "📊 Visualize", "📈 Analyze", "🔗 Share"])
        
        with tabs[0]:  # Explore tab
            explore_data(data_processor)
        
        with tabs[1]:  # Visualize tab
            create_visualizations(chart_generator)
        
        with tabs[2]:  # Analyze tab
            statistical_analysis(data_processor)
        
        with tabs[3]:  # Share tab
            share_visualizations(export_manager)

def explore_data(data_processor):
    """Data exploration interface"""
    st.subheader("🔍 Data Exploration")
    
    # Data filtering controls
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Column selection
        all_columns = st.session_state.data.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to display",
            all_columns,
            default=all_columns[:5] if len(all_columns) > 5 else all_columns,
            help="Choose which columns to show in the data preview"
        )
    
    with col2:
        # Row limit for mobile performance
        row_limit = st.selectbox(
            "Rows to display",
            [50, 100, 500, 1000],
            index=0,
            help="Limit rows for better mobile performance"
        )
    
    # Apply column filtering
    if selected_columns:
        display_data = st.session_state.data[selected_columns].head(row_limit)
    else:
        display_data = st.session_state.data.head(row_limit)
    
    # Advanced filtering
    with st.expander("🔧 Advanced Filters"):
        filter_column = st.selectbox("Filter by column", [None] + all_columns)
        
        if filter_column:
            col_type = st.session_state.data[filter_column].dtype
            
            if col_type in ['object', 'string']:
                # String filtering
                unique_values = st.session_state.data[filter_column].unique()
                selected_values = st.multiselect(
                    f"Select values for {filter_column}",
                    unique_values
                )
                if selected_values:
                    display_data = display_data[display_data[filter_column].isin(selected_values)]
            
            elif col_type in ['int64', 'float64']:
                # Numeric filtering
                min_val = float(st.session_state.data[filter_column].min())
                max_val = float(st.session_state.data[filter_column].max())
                
                selected_range = st.slider(
                    f"Range for {filter_column}",
                    min_val, max_val, (min_val, max_val)
                )
                display_data = display_data[
                    (display_data[filter_column] >= selected_range[0]) &
                    (display_data[filter_column] <= selected_range[1])
                ]
    
    # Update filtered data in session state
    st.session_state.filtered_data = display_data
    
    # Display data
    st.dataframe(
        display_data,
        use_container_width=True,
        height=400
    )
    
    # Quick stats
    if not display_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", len(display_data))
        with col2:
            st.metric("Columns", len(display_data.columns))
        with col3:
            numeric_cols = len(display_data.select_dtypes(include=[np.number]).columns)
            st.metric("Numeric Cols", numeric_cols)
        with col4:
            missing_values = display_data.isnull().sum().sum()
            st.metric("Missing Values", missing_values)

def create_visualizations(chart_generator):
    """Visualization creation interface"""
    st.subheader("📊 Create Visualizations")
    
    if st.session_state.filtered_data is None or st.session_state.filtered_data.empty:
        st.warning("No data available. Please load and explore data first.")
        return
    
    data = st.session_state.filtered_data
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'string']).columns.tolist()
    
    # Chart configuration
    col1, col2 = st.columns([1, 1])
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot", "Heatmap", "Pie Chart"],
            help="Select the type of visualization"
        )
    
    with col2:
        if chart_type in ["Scatter Plot", "Line Chart"]:
            x_axis = st.selectbox("X-axis", numeric_cols + categorical_cols)
            y_axis = st.selectbox("Y-axis", numeric_cols)
        elif chart_type == "Bar Chart":
            x_axis = st.selectbox("Category", categorical_cols)
            y_axis = st.selectbox("Value", numeric_cols)
        elif chart_type == "Histogram":
            x_axis = st.selectbox("Column", numeric_cols)
            y_axis = None
        elif chart_type == "Box Plot":
            x_axis = st.selectbox("Category (optional)", [None] + categorical_cols)
            y_axis = st.selectbox("Value", numeric_cols)
        elif chart_type == "Heatmap":
            x_axis = None
            y_axis = None
        elif chart_type == "Pie Chart":
            x_axis = st.selectbox("Category", categorical_cols)
            y_axis = st.selectbox("Value (optional)", [None] + numeric_cols)
    
    # Additional options
    with st.expander("🎨 Chart Options"):
        color_column = st.selectbox("Color by", [None] + categorical_cols + numeric_cols)
        title = st.text_input("Chart Title", value=f"{chart_type} - {x_axis or 'Data'}")
        
        # Size options for mobile
        chart_height = st.slider("Chart Height", 300, 800, 500)
    
    # Generate chart
    try:
        fig = chart_generator.create_chart(
            data, chart_type, x_axis, y_axis, color_column, title, chart_height
        )
        
        if fig:
            st.plotly_chart(fig, use_container_width=True, height=chart_height)
            
            # Store chart config for sharing
            st.session_state.chart_config = {
                'type': chart_type,
                'x_axis': x_axis,
                'y_axis': y_axis,
                'color_column': color_column,
                'title': title,
                'height': chart_height
            }
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")

def statistical_analysis(data_processor):
    """Statistical analysis interface"""
    st.subheader("📈 Statistical Analysis")
    
    if st.session_state.filtered_data is None or st.session_state.filtered_data.empty:
        st.warning("No data available. Please load and explore data first.")
        return
    
    data = st.session_state.filtered_data
    
    # Summary statistics
    st.write("### 📊 Summary Statistics")
    
    numeric_data = data.select_dtypes(include=[np.number])
    if not numeric_data.empty:
        summary_stats = data_processor.get_summary_statistics(numeric_data)
        st.dataframe(summary_stats, use_container_width=True)
    else:
        st.info("No numeric columns available for statistical analysis.")
    
    # Correlation analysis
    if len(numeric_data.columns) > 1:
        st.write("### 🔗 Correlation Analysis")
        
        corr_matrix = numeric_data.corr()
        
        # Create correlation heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="RdBu_r"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data quality report
    st.write("### 🧹 Data Quality Report")
    
    quality_report = data_processor.get_data_quality_report(data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Missing Values by Column:**")
        missing_data = pd.DataFrame({
            'Column': quality_report['missing_values'].index,
            'Missing Count': quality_report['missing_values'].values,
            'Missing %': (quality_report['missing_values'].values / len(data) * 100).round(2)
        })
        st.dataframe(missing_data, use_container_width=True)
    
    with col2:
        st.write("**Data Types:**")
        dtypes_df = pd.DataFrame({
            'Column': data.dtypes.index,
            'Data Type': data.dtypes.values
        })
        st.dataframe(dtypes_df, use_container_width=True)

def share_visualizations(export_manager):
    """Sharing and export interface"""
    st.subheader("🔗 Share & Export")
    
    if not st.session_state.chart_config:
        st.warning("Create a visualization first to enable sharing options.")
        return
    
    # Shareable link generation
    st.write("### 🔗 Shareable Link")
    
    # Generate a shareable URL with chart configuration
    chart_params = urlencode(st.session_state.chart_config)
    shareable_url = f"{st.get_option('browser.serverAddress')}:{st.get_option('server.port')}?{chart_params}"
    
    st.code(shareable_url, language=None)
    
    if st.button("📋 Copy Link to Clipboard"):
        st.success("Link ready to copy! (Copy from the text box above)")
    
    # Export options
    st.write("### 💾 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Chart as HTML"):
            if st.session_state.filtered_data is not None:
                try:
                    chart_generator = ChartGenerator()
                    fig = chart_generator.create_chart(
                        st.session_state.filtered_data,
                        st.session_state.chart_config['type'],
                        st.session_state.chart_config['x_axis'],
                        st.session_state.chart_config['y_axis'],
                        st.session_state.chart_config['color_column'],
                        st.session_state.chart_config['title'],
                        st.session_state.chart_config['height']
                    )
                    
                    html_string = fig.to_html()
                    st.download_button(
                        label="💾 Download HTML",
                        data=html_string,
                        file_name=f"chart_{st.session_state.chart_config['type'].lower().replace(' ', '_')}.html",
                        mime="text/html"
                    )
                except Exception as e:
                    st.error(f"Error exporting chart: {str(e)}")
    
    with col2:
        if st.button("📄 Export Data as CSV"):
            if st.session_state.filtered_data is not None:
                csv = st.session_state.filtered_data.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
    
    # Share via team collaboration
    st.write("### 👥 Team Collaboration")
    st.info("""
    **Share with your team:**
    1. Copy the shareable link above
    2. Send it to team members
    3. They can view the same visualization with the current data filters
    4. Export options are available for offline analysis
    """)

if __name__ == "__main__":
    main()
