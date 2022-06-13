from cProfile import label
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def save_chart(movie_id):

    file = open(f"opinions/{movie_id}.json", encoding="utf-8")
    opinions = pd.read_json(file)

    opinions["stars"] = opinions["stars"].map(lambda x: float(x))

    stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(1,11,1)), fill_value=0)
    stars.plot.bar(
        color = "#f0b710"
    )
    plt.title("Oceny filmu/serialu")
    plt.xlabel("Liczba gwiazdek")
    plt.ylabel("Liczba opinii")
    plt.grid(True, axis="y")
    plt.xticks(rotation=0)
    plt.savefig(f"app/static/plots/{movie_id}_stars.png")
    plt.close()