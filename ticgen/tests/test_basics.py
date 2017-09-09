"""Basic sanity checks to verify that tvguide works.
To run, simply type "py.test".
"""
import numpy as np

def test_import():
    """Can we import tvguide successfully?"""
    import ticgen
    from ticgen import calc_star
    from ticgen import ticgen
    from ticgen import Star
    from ticgen import ticgen_fromfile


def test_VJKs():
    from ticgen import Star
    star = Star(Vmag=12, Ksmag=10, Jmag=10.5)
    assert np.allclose(star.Vmag, 12.0)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 10.5)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'V/J/Ks'


def test_VJKs2():
    # test with J-K outside valid region
    from ticgen import Star
    star = Star(Vmag=12, Ksmag=10, Jmag=11.1)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 11.1)
    assert np.allclose(star.Tmag, 12.85) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'J/Ks'


def test_BphJKs():
    from ticgen import Star
    star = Star(Bphmag=12, Ksmag=10, Jmag=10.5)
    assert np.allclose(star.Bphmag, 12.0)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 10.5)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'Bph/J/Ks'


def test_BJKs():
    from ticgen import Star
    star = Star(Bmag=12, Ksmag=10, Jmag=10.5)
    assert np.allclose(star.Bmag, 12.0)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 10.5)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'B/J/Ks'


def test_JKs():
    from ticgen import Star
    # j-k = 0.5
    star = Star(Ksmag=10, Jmag=10.5)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 10.5)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'J/Ks'

    # j-k = 1.5
    star = Star(Ksmag=10, Jmag=11.5)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 11.5)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'J/Ks'

    # j-k = 0.8
    star = Star(Ksmag=10, Jmag=10.8)
    assert np.allclose(star.Ksmag, 10.0)
    assert np.allclose(star.Jmag, 10.8)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'J/Ks'

    # j-k = -1.0
    star = Star(Ksmag=11, Jmag=10)
    assert np.allclose(star.Ksmag, 11.0)
    assert np.allclose(star.Jmag, 10.0)
#    assert np.allclose(star.Tmag,) # todo - calc from the paper
#    assert np.allclose(star.oneSigmaNoise,) # todo - calc from the paper
    assert star.TmagProvenance == 'J/Ks'










