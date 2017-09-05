"""Basic sanity checks to verify that tvguide works.
To run, simply type "py.test".
"""


def test_import():
    """Can we import tvguide successfully?"""
    import ticgen
    from ticgen import calc_star
    from ticgen import ticgen
    from ticgen import Star

def test_VJKs():
    from ticgen import Star
    star = Star(Vmag=12, Ksmag=10, Jmag=10.5)
    assert star.Vmag
    assert star.Ksmag
    assert star.Jmag
    assert star.Tmag
    assert star.TmagProvenance == 'V/J/Ks'
