import pandas as pd
import plotly.express as px

class PosTab:

    def __init__(self):
        return

    def selection(self, df, input1):
        print("-------------")
        print(input1)
        print("-------------")
        value = list(df[input1].unique())
        options = [{'label':tag, 'value':tag} for tag in value]
        print("-------------")
        print(options)
        print("-------------")
        return value, options

    def dynamic_attributes(self, df, pos_counts, input1, input2):
        new_df = df.copy()
        new_df = new_df.groupby(['ID', 'Tags', 'Year', 'WordCount', input1]).size().to_frame(name = 'AttributeCount').reset_index()
        new_df['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100
        attr_mask = new_df[input1].isin(input2)
        pos_mask = new_df['Tags'].isin(['NN1'])
        mask = pd.concat((attr_mask, pos_mask), axis=1)
        new_df = new_df[pos_mask]
        new_df = new_df[attr_mask]
        fig= px.bar(
            # can choose only one tag at a time
            data_frame=new_df.groupby(['Year', input1]).mean().reset_index(),
            x='Year', 
            y='PosCountNorm',
            range_y=[0,30],
            labels={
                'Year': 'Year', 
                'PosCountNorm':'Percentage of Tag'},
            color=input1,
            barmode='group',
            title='Compare tags of selected attribute')
        return fig