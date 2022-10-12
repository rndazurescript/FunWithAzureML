import pandas as pd
import numpy as np
import os
from pathlib import Path
from pyod.models.pca import PCA
from pyod.models.lof import LOF
from pyod.models.abod import ABOD
import plotly
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import argparse

# Environment setup needed to create the
# DockerContext/requirements.txt file
# %pip install openpyxl
# %pip install pyod
# %pip install -U kaleido
# You can find specific version of packages
# using the following command
# %pip freeze | grep openpyxl

parser = argparse.ArgumentParser()
parser.add_argument(
    "--company-code", type=str, dest="company_code", help="Company code. E.g. CompanyA"
)
parser.add_argument(
    "--input-folder",
    type=str,
    dest="input_folder",
    help="The folder that contains the data",
)
parser.add_argument(
    "--output-folder",
    type=str,
    dest="output_folder",
    help="The folder to store results",
)
parser.add_argument(
    "--input-file",
    type=str,
    dest="input_file",
    help="The name of the Excel containing the data",
    default="Records.xlsx",
)
parser.add_argument(
    "--showgraph", type=bool, dest="showgraph", help="Display graphs", default=False
)

args = parser.parse_args()

excel_file_path = os.path.join(args.input_folder, args.company_code, args.input_file)
print(excel_file_path)

df = pd.read_excel(excel_file_path, engine="openpyxl")
print(df.head())


df_no_date = df.drop(columns="Date", inplace=False)

# Copy some code from https://github.com/yzhao062/pyod/blob/master/notebooks/Compare%20All%20Models.ipynb
models = {
    "pca": PCA(contamination=0.1, n_components=3),
    "lof": LOF(contamination=0.1),
    "abod": ABOD(contamination=0.1),
}

for i, (clf_name, clf) in enumerate(models.items()):
    print(i + 1, "fitting", clf_name)
    clf.fit(df_no_date)
    outliers = clf.predict(df_no_date)
    df[clf_name] = outliers

outputs_folder = os.path.join(args.output_folder, args.company_code)
# Ensure that output folder exist
Path(outputs_folder).mkdir(parents=True, exist_ok=True)

df.to_excel(os.path.join(outputs_folder, "outlier_records.xlsx"))

# Create feature correlations plot
features = [k for k in df_no_date.columns]

fig = ff.create_annotated_heatmap(
    np.array(df_no_date.corr().round(2)),
    colorscale="Viridis",
    x=features,
    y=features,
    hoverongaps=True,
)

fig.update_layout(
    paper_bgcolor="white",
    width=1200,
    height=1200,
    titlefont=dict(size=25),
    title_text="Features correlation plot",
)
fig.update_xaxes(tickangle=90, side="bottom")

fig.write_image(os.path.join(outputs_folder, "correlation_plot.png"))
plotly.offline.plot(fig, filename=os.path.join(outputs_folder, "correlation_plot.html"))

# Let's print a pairplot
# https://doobzncoobz.com/seaborn-pairplot/
plt.figure()
sns_plot = sns.pairplot(df_no_date)
sns_plot.fig.set_size_inches(15, 15)
sns_plot.fig.suptitle("Pair plot", y=1.01, size=30)

sns_plot.savefig(os.path.join(outputs_folder, "sns_pairplot.png"))

outlier_column = list(models.keys())[0]

fig = px.scatter_3d(data_frame=df, x="ft01", y="ft02", z="ft03", symbol=outlier_column)
fig.update_layout(
    margin=dict(l=30, r=30, b=30, t=30),
    autosize=False,
    width=1000,
    height=1000,
    showlegend=False,
    title={
        "text": f"Outlier Plot ({outlier_column})",
        "y": 0.91,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
    },
)

# circle's are outliers, diamonds are normal entries for the specific model
# Let's change the outliers to red X and the rest into green circles
for i, d in enumerate(fig.data):
    if fig.data[i].marker.symbol == "circle":
        fig.data[i].marker.symbol = "x"
        fig.data[i].marker.color = "red"
    else:
        fig.data[i].marker.symbol = "circle"
        fig.data[i].marker.color = "green"

if args.showgraph:
    fig.show()

fig.write_image(os.path.join(outputs_folder, "outlier_plot.png"))
plotly.offline.plot(fig, filename=os.path.join(outputs_folder, "outlier_plot.html"))