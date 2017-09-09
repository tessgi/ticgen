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
    assert np.allclose(star.Tmag, 11.23744) # calculated from the paper
    assert np.allclose(star.oneSigmaNoise, 382.6877864019419) # calced from the paper
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


def test_noise():
    from ticgen import Star
    for i, Tmag in enumerate(range(0, 30, 1)):
        star = Star(Tmag=Tmag)
        assert np.allclose(star.oneSigmaNoise, Tmag_arr[i])


# array of Tmags range(0,30,1)
# in ppm per hour integration
Tmag_arr = [
    27.027369769,
    49.3647823676,
    62.7573377878,
    65.4511161846,
    63.2746707005,
    61.7745189948,
    64.3399722724,
    73.6472423282,
    93.6058029111,
    131.64622144,
    202.512525689,
    336.023245221,
    595.006926982,
    1122.44295407,
    2285.13069356,
    5190.45752548,
    13956.8518637,
    48658.6105895,
    250067.359628,
    2248605.33024,
    44088886.7696,
    2480504666.32,
    559607639017.0,
    7.55557557376e+14,
    9.78672050295e+18,
    2.10592707293e+24,
    1.41615211158e+31,
    6.11648153921e+39,
    3.83170364726e+50,
    8.68820707807e+63,
    ]


