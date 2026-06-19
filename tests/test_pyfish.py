import os
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.testing.compare import compare_images

from pyfish.core import fish_plot, process_data, setup_figure


def try_to_delete_file(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass


def check_figures_equal(file_name, extensions=("png", "pdf", "svg"), tol=20):
    """
    Loosely based on matplotlib.testing.decorators.check_figures_equal
    """
    file_name = file_name
    image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
    try:
        os.mkdir(image_dir)
    except FileExistsError:
        pass

    def decorator(func):

        @pytest.mark.parametrize("ext", extensions)
        def wrapper(*args, ext, **kwargs):

            try:
                fig_test = plt.figure("test")
                ax = fig_test.add_subplot(111)
                kwargs['ax'] = ax
                func(*args, **kwargs)
                test_image_path = os.path.join(image_dir, (file_name + "." + ext))
                ref_image_path = os.path.join(image_dir, (file_name + "_ref" + "." + ext))
                try_to_delete_file(test_image_path)
                fig_test.savefig(test_image_path)

                diff = compare_images(ref_image_path, test_image_path, tol=tol)
                assert diff is None, "Figure mismatch, see figure diff in dir tests/images"

            finally:
                plt.close(fig_test)
                try_to_delete_file(test_image_path)


        return wrapper

    return decorator


@check_figures_equal('test_pyfish_figure', extensions=['png'])
def test_pyfish_figure(ax):
    populations = np.array(
        [[0, 0, 100], [0, 1, 40], [0, 2, 20], [0, 3, 10], [1, 1, 10], [1, 3, 50], [1, 4, 50],
         [1, 5, 100], [2, 4, 0], [2, 5, 50], [3, 0, 10], [3, 1, 10], [3, 5, 20]])

    parent_tree = np.array([[0, 1], [1, 2], [0, 3]])

    populations_df = pd.DataFrame(populations, columns=["Id", "Step", "Pop"])
    parent_tree_df = pd.DataFrame(parent_tree, columns=["ParentId", "ChildId"])

    setup_figure()
    fish_plot(*process_data(populations_df, parent_tree_df, absolute=True,
                            interpolation=1, smooth=1, seed=42), ax=ax)


@pytest.mark.parametrize("absolute,interpolation,smooth",
                         list(product([True, False], [0, 1, 2], [0, 1, 2])))
def test_all_parameters(absolute, interpolation, smooth):
    populations = np.array(
        [[0, 0, 100], [0, 1, 40], [0, 2, 20], [0, 3, 10], [1, 1, 10], [1, 3, 50], [1, 4, 50],
         [1, 5, 100], [2, 4, 0], [2, 5, 50], [3, 0, 10], [3, 1, 10], [3, 5, 20]])

    parent_tree = np.array([[0, 1], [1, 2], [0, 3]])

    populations_df = pd.DataFrame(populations, columns=["Id", "Step", "Pop"])
    parent_tree_df = pd.DataFrame(parent_tree, columns=["ParentId", "ChildId"])

    fish_plot(*process_data(populations_df, parent_tree_df,
                            absolute=absolute, interpolation=interpolation, smooth=smooth))
    # plt.close()


def test_pyfish_missing_tree_root_error():
    populations = np.array(
        [[0, 0, 100], [0, 1, 40], [0, 2, 20], [0, 3, 10], [1, 1, 10], [1, 3, 50], [1, 4, 50],
         [1, 5, 100], [2, 4, 0], [2, 5, 50], [3, 0, 10], [3, 1, 10], [3, 5, 20]])

    parent_tree = np.array([[0, 2], [1, 3]])

    populations_df = pd.DataFrame(populations, columns=["Id", "Step", "Pop"])
    parent_tree_df = pd.DataFrame(parent_tree, columns=["ParentId", "ChildId"])

    with pytest.raises(ValueError):
        _ = process_data(populations_df, parent_tree_df)


def test_pyfish_missing_entries_for_interpolation_error():
    populations = np.array(
        [[0, 0, 100], [0, 1, 40], [0, 2, 20], [0, 3, 10], [1, 1, 10], [1, 3, 50], [1, 4, 50],
         [1, 5, 100], [2, 5, 0], [3, 0, 10], [3, 1, 10], [3, 5, 20]])

    parent_tree = np.array([[0, 1], [1, 2], [0, 3]])

    populations_df = pd.DataFrame(populations, columns=["Id", "Step", "Pop"])
    parent_tree_df = pd.DataFrame(parent_tree, columns=["ParentId", "ChildId"])

    with pytest.raises(ValueError):
        _ = process_data(populations_df, parent_tree_df, interpolation=2)


@check_figures_equal('test_pyfish_figure_color_by', extensions=['png'])
def test_pyfish_figure_color_by(ax):
    populations_df = pd.read_csv("tests/populations_new.csv")
    parent_tree_df = pd.read_csv("tests/parent_tree.csv")

    setup_figure()
    fish_plot(*process_data(populations_df, parent_tree_df, absolute=True,
                            interpolation=0, smooth=1, seed=42,
                            color_by="Feature"), ax=ax)
