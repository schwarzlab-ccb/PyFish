"""Regenerate all doc/ images (except logo) referenced in README."""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ensure we import the local pyfish, not a system-installed one
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from pyfish.core import fish_plot, process_data, setup_figure

DOC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "doc")
TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def _save(name, width=1920, height=1080):
    path = os.path.join(DOC_DIR, name)
    print(f"Saving {path}...")
    plt.savefig(path)
    plt.close()


# ── Example data from README (used for test.png, interpolation.png, curved.png)
example_populations = np.array([
    [0, 0, 100], [0, 1, 40], [0, 2, 20], [0, 3, 0],
    [1, 0, 10], [1, 3, 50], [1, 5, 100],
    [2, 4, 20], [2, 5, 50],
    [3, 0, 10], [3, 1, 20], [3, 5, 10],
])
example_parent_tree = np.array([[0, 1], [1, 2], [0, 3]])
example_pops_df = pd.DataFrame(example_populations, columns=["Id", "Step", "Pop"])
example_tree_df = pd.DataFrame(example_parent_tree, columns=["ParentId", "ChildId"])

# ── Test data from tests/populations.csv (used for base, abs, smooth, bound, map, seed)
test_pops_df = pd.read_csv(os.path.join(TEST_DIR, "populations.csv"))
test_tree_df = pd.read_csv(os.path.join(TEST_DIR, "parent_tree.csv"))

# ── Feature data from tests/populations_feature.csv (used for color_by)
feature_pops_df = pd.read_csv(os.path.join(TEST_DIR, "populations_feature.csv"))


def generate_all():
    os.makedirs(DOC_DIR, exist_ok=True)

    # test.png — base example from README
    setup_figure()
    fish_plot(*process_data(example_pops_df, example_tree_df))
    _save("test.png")

    # interpolation.png — --interpolate 2
    setup_figure()
    fish_plot(*process_data(example_pops_df, example_tree_df, interpolate=2))
    _save("interpolation.png")

    # curved.png — --curved
    setup_figure()
    fish_plot(*process_data(example_pops_df, example_tree_df), curved=True)
    _save("curved.png")

    # base.png — default with test data
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df))
    _save("base.png")

    # abs.png — --absolute
    setup_figure(absolute=True)
    fish_plot(*process_data(test_pops_df, test_tree_df, absolute=True))
    _save("abs.png")

    # smooth.png — --smooth 50
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df, smooth=50))
    _save("smooth.png")

    # bound.png — --first 4000 --last 4500
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df, first_step=4000, last_step=4500))
    _save("bound.png")

    # map.png — --cmap viridis
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df, cmap_name="viridis"))
    _save("map.png")

    # color_by.png — --color-by Feature --cmap viridis
    setup_figure()
    fish_plot(*process_data(feature_pops_df, test_tree_df, color_by="Feature", cmap_name="viridis"))
    _save("color_by.png")

    # seed.png — --seed 2022
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df, seed=2022))
    _save("seed.png")

    # separate.png — --separate
    setup_figure()
    fish_plot(*process_data(test_pops_df, test_tree_df, separate=True))
    _save("separate.png")

    print(f"Generated images in {DOC_DIR}")


if __name__ == "__main__":
    generate_all()
