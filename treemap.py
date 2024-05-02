import pandas as pd
import plotly.express as px

data = pd.read_csv('/content/Results_21Mar2022.csv')

# Normalization
metrics = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_ghgs_ch4', 'mean_ghgs_n2o', 'mean_bio', 'mean_watuse', 'mean_acid']
data_normalized = data[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# Assigning weights to each metric
weights = {metric: 1 for metric in metrics}
data['environmental_impact'] = data_normalized.apply(lambda x: sum(x * pd.Series(weights)), axis=1) / sum(weights.values())

# Data aggregation
aggregated_data = data.groupby(['sex', 'diet_group', 'age_group']).agg({
        'environmental_impact': 'sum',
        'mean_ghgs': 'mean',  
        'mean_land': 'mean',  
        'mean_watscar': 'mean',
        'mean_eut': 'mean',
        'mean_bio': 'mean'
    }).reset_index()
      

# Building the treemap 
fig = px.treemap(
        aggregated_data,
        path=['sex', 'diet_group', 'age_group'],  
        values='environmental_impact',  
        color='environmental_impact',  # Color scale based on env impact
        color_continuous_scale='Blues',
        title='Hierarchical Treemap of Environmental Impact by Sex, Diet Group, and Age Group',
        hover_data={
        'environmental_impact': True,
        'mean_ghgs': True,   
        'mean_land': True,
        'mean_watscar': True,
        'mean_eut': True,
        'mean_bio': True
    })

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

fig.show()
    

