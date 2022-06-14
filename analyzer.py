from cProfile import label
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import ast
import json

matplotlib.use('Agg')
def save_chart(allOpinions, id_url):
    allOpinions = ast.literal_eval(allOpinions)
    with open("temp_chart_date.json", "w", encoding="UTF-8") as file:
        json.dump(allOpinions, file,ensure_ascii=False)

    file = open(f"temp_chart_date.json", encoding="UTF-8")
    opinions = pd.read_json(file)
    
    print(opinions["stars"])
    opinions["stars"] = opinions["stars"].map(lambda x: int(x))

    stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(1,11,1)), fill_value=0)
    stars.plot.bar(
        color = "#f0b710"
    )
    plt.title("Oceny filmu/serialu")
    plt.xlabel("Liczba gwiazdek")
    plt.ylabel("Liczba opinii")
    plt.grid(True, axis="y")
    plt.xticks(rotation=0)
    plt.savefig(f"./static/plots/{id_url}_stars.png")
    plt.close()