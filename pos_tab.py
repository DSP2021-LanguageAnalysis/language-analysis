import pandas as pd
import plotly.express as px

class PosTab:

    def __init__(self):
        return

    def selection(self, df, input1):
        value = list(df[input1].unique())
        options = [{'label':tag, 'value':tag} for tag in value]
        return value, options

    def dynamic_attributes(self, df, pos_counts, input1, input2, period_count):
        new_df = df.copy()
        # Create bins and labels for grouping years into periods
        bins = pd.interval_range(start=1700, end=1800, periods=period_count, closed='right')
        labels = list(bins.astype(str))
        # Create new column with periods
        new_df['Year'] = new_df['Year'].astype('int')
        new_df['Period'] = pd.cut(new_df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        new_df['Period'] = new_df['Period'].astype("str")
        # Group data based on selection
        new_df = new_df.groupby(['ID', 'Tags', 'Period', 'WordCount', input1]).size().to_frame(name = 'AttributeCount').reset_index()
        new_df['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100
        # Mask data based on selection
        attr_mask = new_df[input1].isin(input2)
        pos_mask = new_df['Tags'].isin(['NN1'])
        #mask = pd.concat((attr_mask, pos_mask), axis=1)
        new_df = new_df[pos_mask]
        new_df = new_df[attr_mask]
        fig= px.bar(
            # can choose only one tag at a time
            data_frame=new_df.groupby(['Period', input1]).mean().reset_index(),
            x='Period', 
            y='PosCountNorm',
            range_y=[0,30],
            labels={
                'Year': 'Period', 
                'PosCountNorm':'%'},
            color=input1,
            barmode='group',
            title='Compare selected attribute')
        return fig