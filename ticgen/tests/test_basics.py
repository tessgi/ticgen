"""Basic sanity checks to verify that tvguide works.
To run, simply type "py.test".
"""
import numpy as np
import os
import argparse

def test_import():
    """Can we import tvguide successfully?"""
    import ticgen
    from ticgen import calc_star
    from ticgen import ticgen
    from ticgen import Star
    from ticgen import ticgen_csv


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

def test_csv():
    from ticgen import ticgen_csv
    import pandas as pd
    THISDIR = os.path.dirname(os.path.abspath(__file__))
    infn = os.path.join(THISDIR,
        "fromfile_test.csv")
    infn_bad = os.path.join(THISDIR,
        "fromfile_test_badfile.csv")
    outfn = os.path.join(THISDIR,
        "fromfile_test.csv-ticgen.csv")
    knownfile = os.path.join(THISDIR,
        "fromfile_test.csv-ticgen.csv-TEST")
    ticgen_csv(args={'input_fn': infn})
    os.path.isfile(outfn)

    testfile = pd.read_csv(knownfile, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    newfile = pd.read_csv(outfn, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    assert np.allclose(
            testfile.A, newfile.A,
            equal_nan=True)

    try:
        ticgen_csv(args={'input_fn': infn_bad})
        raise 'Should fail here Error'
    except SystemExit:
        pass

    try:
        ticgen_csv(args={'input_fn': 'doesnt_exist'})
        raise 'Should fail here Error'
    except SystemExit:
        pass


def test_space_in_file():
    from ticgen import ticgen_csv
    import pandas as pd
    THISDIR = os.path.dirname(os.path.abspath(__file__))
    infn = os.path.join(THISDIR,
        "fromfile_test_space.csv")
    outfn = os.path.join(THISDIR,
        "fromfile_test_space.csv-ticgen.csv")
    knownfile = os.path.join(THISDIR,
        "fromfile_test.csv-ticgen.csv-TEST")
    ticgen_csv(args={'input_fn': infn})
    os.path.isfile(outfn)

    testfile = pd.read_csv(knownfile, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    newfile = pd.read_csv(outfn, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    assert np.allclose(
            testfile.A, newfile.A,
            equal_nan=True)


def test_nomag():
    from ticgen import ticgen_csv
    import pandas as pd
    THISDIR = os.path.dirname(os.path.abspath(__file__))
    infn = os.path.join(THISDIR,
        "fromfile_test_noTmag.csv")
    outfn = os.path.join(THISDIR,
        "fromfile_test_noTmag.csv-ticgen.csv")
    knownfile = os.path.join(THISDIR,
        "fromfile_test.csv-ticgen.csv-TEST")
    ticgen_csv(args={'input_fn': infn})
    os.path.isfile(outfn)

    testfile = pd.read_csv(knownfile, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    newfile = pd.read_csv(outfn, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    # only search the first 130 rows because the remaining are different
    # from the standard because we removed tmag
    for l in range(10,120,5):
        assert np.allclose(
                testfile.A[l], newfile.A[l],
                equal_nan=True)


def test_case_from_jpl_person():
    from ticgen import ticgen_csv
    import pandas as pd
    THISDIR = os.path.dirname(os.path.abspath(__file__))
    infn1 = os.path.join(THISDIR,
        "fromfile_jpl1.csv")
    outfn1 = os.path.join(THISDIR,
        "fromfile_jpl1.csv-ticgen.csv")
    infn2 = os.path.join(THISDIR,
        "fromfile_jpl2.csv")
    outfn2 = os.path.join(THISDIR,
        "fromfile_jpl2.csv-ticgen.csv")

    ticgen_csv(args={'input_fn': infn1})
    os.path.isfile(outfn1)

    ticgen_csv(args={'input_fn': infn2})
    os.path.isfile(outfn2)

    testfile1 = pd.read_csv(outfn1, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    testfile2 = pd.read_csv(outfn2, names=['A', 'B'],
        skipinitialspace=True,
        skiprows=1)
    assert np.allclose(
            testfile1.A, testfile2.A,
            equal_nan=True)
    assert np.allclose(
            testfile1.B, testfile2.B,
            equal_nan=True)





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


