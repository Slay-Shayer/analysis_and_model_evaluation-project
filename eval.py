import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

uploaded_files = st.file_uploader('Upload your file', type=['csv'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"**File name:** {uploaded_file.name}")
        df = pd.read_csv(uploaded_file)
        st.write(df.head(2))

        st.write('File Description:')
        st.write(df.describe(include='all'))

        with st.expander('Select anything you want to see.'):
            expander1 = st.radio('Select', ['Shape', 'Null Values', 'Data Types', 'Heatmap'])
            if expander1 == 'Shape':
                st.write(f'This data has `{df.shape[0]}` rows and `{df.shape[1]}` columns.')
            elif expander1 == 'Null Values':
                st.write(df.isnull().sum())
            elif expander1 == 'Data Types':
                st.write(df.dtypes)
            elif expander1 == 'Heatmap':
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, fmt=".2f", cmap='Blues', ax=ax)
                plt.title('Heatmap of the DataFrame')
                st.pyplot(fig)


        individual_graphs = st.selectbox('Select the type of graph', ['Histogram', 'Boxplot', 'Densityplot', 'Scatterplot', 'Barplot'])
        var_of_interest = st.text_input('Type your variable of interest', placeholder='Make sure not to make any typo')

        if var_of_interest:
            if var_of_interest not in df.columns:
                st.error('Column not found. Please check your spelling.')
            elif df[var_of_interest].dtype == 'object':
                st.warning('Please select a numerical column for plotting.')
            else:
                plt.style.use('ggplot')
                fig, ax = plt.subplots()
                if individual_graphs == 'Histogram':
                    sns.histplot(df[var_of_interest], ax=ax, palette='Blues', kde=True)
                elif individual_graphs == 'Boxplot':
                    sns.boxplot(y=df[var_of_interest], ax=ax, palette='Blues')
                elif individual_graphs == 'Densityplot':
                    sns.kdeplot(df[var_of_interest], ax=ax, palette='Blues')
                elif individual_graphs == 'Scatterplot':
                    other_var = st.text_input('Type another numerical variable for x-axis')
                    hue_var = st.text_input('Type a categorical variable for hue (optional)')
                    if other_var in df.columns and df[other_var].dtype != 'object':
                        if hue_var in df.columns and df[hue_var].dtype == 'object':
                            sns.scatterplot(x=df[other_var], y=df[var_of_interest], hue=df[hue_var], ax=ax, palette='Blues')
                        else:
                            sns.scatterplot(x=df[other_var], y=df[var_of_interest], ax=ax, palette='Blues')
                    else:
                        st.warning('Please enter a valid second numerical column.')
                elif individual_graphs == 'Barplot':
                    sns.barplot(x=df[var_of_interest].value_counts().index, y=df[var_of_interest].value_counts().values, ax=ax)
                st.pyplot(fig)
