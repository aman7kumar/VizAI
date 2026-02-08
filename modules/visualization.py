import plotly.express as px

def bar_chart(df, x, y):
    return px.bar(df, x=x, y=y)

def line_chart(df, x, y):
    return px.line(df, x=x, y=y)

def scatter_chart(df, x, y):
    return px.scatter(df, x=x, y=y)
