import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from slugify import slugify


na_values = ['?', '', "nc"]
xls = pd.ExcelFile("/Users/Nakouri/Sami_NAKOURI/KitDataScience/Lesson5/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2016.xls")
xls2 = pd.ExcelFile("/Users/Nakouri/Sami_NAKOURI/KitDataScience/Lesson5/estim-pop-dep-sexe-gca-1975-2018.xls")
df = pd.read_excel(xls, "Spécialistes", na_values=na_values)
df2 = pd.read_excel(xls2, "2018", skiprows=[0, 1, 2, 3], header=0, na_values=na_values)
reg = r"[^a-zA-Z]+"
df["Départements"] = df["DEPARTEMENT"].str.replace(reg, "")
result = pd.merge(df, df2, how='left', on="Départements")


#print(result)

#print(result.plot(x="DEPASSEMENTS (Euros)", y="Total"))

#columns = ["DEPASSEMENTS (Euros)", "Total"]
#result_plot = result[columns]
#sns.set(style="ticks", color_codes=True)
#g = sns.pairplot(result_plot, diag_kind="kde", plot_kws={'alpha': 0.2})
#ax = result.plot(x="Total", y="DEPASSEMENTS (Euros)", style=['o', ''])
#plt.show()

#print(df.describe())
#print(df.head())
#print(df2.head())
print(result[["Départements", "Total"]])
