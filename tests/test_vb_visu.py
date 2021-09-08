import pytest
import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import bayes.vb
import bayes.vb_visu
from imageio import imread


def test_vb_visu(generate_ref_img=False):
    mvn = bayes.vb.MVN(mean=[2, 30, 100], precision=[[1, 1, 1], [1, 2, 0], [1, 0, 3]])
    gamma0 = bayes.vb.Gamma.FromSD(5, shape=3)
    gamma1 = bayes.vb.Gamma.FromSD(1, shape=8.5)

    axes = bayes.vb_visu.visualize_vb_marginal_matrix(mvn, [gamma0, gamma1], label="VB")
    bayes.vb_visu.format_axes(axes)

    ref_img_name = Path(__file__).absolute().parent / "test_vb_visu_ref.png"
    if generate_ref_img:
        plt.savefig(ref_img_name, dpi=300)
        return

    with tempfile.TemporaryDirectory() as tmpdirname:
        test_img_name = Path(tmpdirname) / "test_visu.png"
        plt.savefig(test_img_name, dpi=300)

        test_img = imread(test_img_name)
        ref_img = imread(ref_img_name)

        assert np.linalg.norm(test_img - ref_img) == pytest.approx(0)


if __name__ == "__main__":
    test_vb_visu(generate_ref_img=False)