import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as widgets
class visualization:
    def plot(self,d1):
        self.d1=d1
        chart=widgets.Dropdown(
            options=['barplot','boxplot','pie','lineplot','scatterplot','histogram','heatmap'],
            value='barplot',
            description='Graph Type:',
            disabled=False,
        )
        def graph(k):
            dtype1=self.d1.dtypes
            categorical_col=list(dtype1[dtype1=="object"].index)
            numerical_col=list(dtype1[(dtype1=="float64")|(dtype1=="int64")].index)
            num_col=widgets.Dropdown(
                options=numerical_col,
                value=numerical_col[0],
                description='column:',
                disabled=False,)
            num_col1=widgets.Dropdown(
                options=numerical_col,
                value=numerical_col[1],
                description='column:',
                disabled=False,)
            cat_col=widgets.Dropdown(
                options=categorical_col,
                value=categorical_col[-1],
                description='column:',
                disabled=False,)
            bar_agg=widgets.Dropdown(
                options=["sum","mean","count","max","min","median"],
                value="count",
                description='Aggregation:',
                disabled=False,)
            def pie(col1):
                df=d1.loc[:,[col1,numerical_col[0]]].groupby(col1).agg('count')
                plt.pie(list(df[numerical_col[0]]),labels=list(df.index),autopct='%1.1f%%')
                plt.show()
            def boxplot(col1):
                sns.boxplot(d1[col1])
                plt.show()
            def lineplot(col1,col2):
                sns.lineplot(x=col1,y=col2,data=self.d1)
                plt.show()
            def scatterplot(col1,col2):
                sns.scatterplot(x=col1,y=col2,data=self.d1) 
                plt.show()
            def barplot(col1,col2,agg):
                if agg=="count":
                    sns.barplot(x=col2,y=col1,data=self.d1,estimator=len)
                    plt.show()
                else:
                    sns.barplot(x=col2,y=col1,data=self.d1,estimator=agg)
                    plt.show()        
            def histo(col1):
                sns.histplot(self.d1[col1]) 
                plt.show()
            if k=="pie":
                widgets.interact(pie,col1=cat_col)
            elif k=="boxplot":
                widgets.interact(boxplot,col1=num_col)
            elif k=="barplot":
                widgets.interact(barplot,col1=num_col,col2=cat_col,agg=bar_agg)
            elif k=="lineplot":
                widgets.interact(lineplot,col1=num_col,col2=num_col1)
            elif k=="scatterplot":
                widgets.interact(scatterplot,col1=num_col,col2=num_col1)
            elif k=="histogram":
                widgets.interact(histo,col1=num_col)
            elif k=="heatmap":
                sns.heatmap(self.d1[numerical_col].corr())
                plt.show()
        widgets.interact(graph,k=chart)