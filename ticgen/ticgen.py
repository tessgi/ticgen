from __future__ import absolute_import
import numpy as np
import argparse
from . import Highlight
from . import logger
import pandas as pd
import sys


class Star(object):
    """
    class to contain and calculate star brightness and noise giving
    various other parameters

    integration: integration time in minutes
    """

    def __init__(self, Tmag=None, Vmag=None,
                 Jmag=None, Ksmag=None, Bphmag=None, Bmag=None,
                 Gmag=None, Hmag=None,
                 integration=60.):
        self.integration = integration
        if Tmag is not None:
            self.TmagProvenance = 'Tmag was provided'
            self.Tmag = Tmag
            self.oneSigmaNoise = self.get_oneSigmaNoise()
        else:
            if ((Vmag is not None) & (Jmag is not None) &
                    (Ksmag is not None)):
                if (((Jmag - Ksmag) <= 1.0) &
                        ((Jmag - Ksmag) >= -0.1)):
                    self.set_VJKs(Vmag, Jmag, Ksmag)
                elif (Bphmag is not None):
                    self.set_BphJKs(Bphmag, Jmag, Ksmag)
                elif (Bmag is not None):
                    self.set_BJKs(Bmag, Jmag, Ksmag)
                else:
                    self.set_JKs(Jmag, Ksmag)
            elif ((Bphmag is not None) & (Jmag is not None) &
                  (Ksmag is not None)):
                self.set_BphJKs(Bphmag, Jmag, Ksmag)
            elif (Bmag is not None) & (Jmag is not None) & (Ksmag is not None):
                self.set_BJKs(Bmag, Jmag, Ksmag)
            elif (Jmag is not None) & (Ksmag is not None):
                self.set_JKs(Jmag, Ksmag)
            elif (Jmag is not None) & (Gmag is not None):
                self.set_GJ(Gmag, Jmag)
            elif (Vmag is not None) & (Jmag is not None) & (Hmag is not None):
                self.TmagProvenance = 'V/J/H'
                self.Vmag = Vmag
                self.Jmag = Jmag
                self.Hmag = Hmag
                self.Tmag = self.TESS_Mag_VJH()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            elif (Jmag is not None) & (Hmag is not None):
                self.TmagProvenance = 'J/H'
                self.Jmag = Jmag
                self.Hmag = Hmag
                self.Tmag = self.TESS_Mag_JH()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            elif (Vmag is not None):
                self.TmagProvenance = 'V'
                self.Vmag = Vmag
                self.Tmag = self.TESS_Mag_V()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            elif (Jmag is not None):
                self.TmagProvenance = 'J'
                self.Jmag = Jmag
                self.Tmag = self.TESS_Mag_J()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            elif (Hmag is not None):
                self.TmagProvenance = 'H'
                self.Hmag = Hmag
                self.Tmag = self.TESS_Mag_H()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            elif (Ksmag is not None):
                self.TmagProvenance = 'Ks'
                self.Ksmag = Ksmag
                self.Tmag = self.TESS_Mag_Ks()
                self.oneSigmaNoise = self.get_oneSigmaNoise()
            else:
                self.Tmag = None
                self.TmagProvenance = 'Could not calculate'
                self.oneSigmaNoise = np.nan

    def set_VJKs(self, Vmag, Jmag, Ksmag):
        self.TmagProvenance = 'V/J/Ks'
        self.Vmag = Vmag
        self.Jmag = Jmag
        self.Ksmag = Ksmag
        self.Tmag = self.TESS_Mag_VJKs()
        self.oneSigmaNoise = self.get_oneSigmaNoise()

    def set_BphJKs(self, Bphmag, Jmag, Ksmag):
        self.TmagProvenance = 'Bph/J/Ks'
        self.Bphmag = Bphmag
        self.Jmag = Jmag
        self.Ksmag = Ksmag
        self.Tmag = self.TESS_Mag_BphJKs()
        self.oneSigmaNoise = self.get_oneSigmaNoise()

    def set_BJKs(self, Bmag, Jmag, Ksmag):
        self.TmagProvenance = 'B/J/Ks'
        self.Bmag = Bmag
        self.Jmag = Jmag
        self.Ksmag = Ksmag
        self.Tmag = self.TESS_Mag_BJKs()
        self.oneSigmaNoise = self.get_oneSigmaNoise()

    def set_JKs(self, Jmag, Ksmag):
        self.TmagProvenance = 'J/Ks'
        self.Jmag = Jmag
        self.Ksmag = Ksmag
        self.Tmag = self.TESS_Mag_JKs()
        self.oneSigmaNoise = self.get_oneSigmaNoise()

    def set_GJ(self, Gmag, Jmag):
        self.TmagProvenance = 'J/Gaia'
        self.Jmag = Jmag
        self.Gmag = Gmag
        self.Tmag = self.TESS_Mag_GJ()
        self.oneSigmaNoise = self.get_oneSigmaNoise()

    def get_oneHourNoiseLnsigma(self):
        """
        TESS photometric error estimate [ppm] based on
        magnitude and Eq. on bottom of P24 of
        arxiv.org/pdf/1706.00495.pdf
        """
        F = 4.73508403525e-5
        E = -0.0022308015894
        D = 0.0395908321369
        C = -0.285041632435
        B = 0.850021465753
        lnA = 3.29685004771

        return (lnA + B * self.Tmag + C * self.Tmag**2 + D * self.Tmag**3 +
                E * self.Tmag**4 + F * self.Tmag**5)

    def get_oneSigmaNoise(self):
        return (np.exp(self.get_oneHourNoiseLnsigma()) *
                np.sqrt(self.integration / 60.))

    def TESS_Mag_VJKs(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on bottom of p4 of arxiv.org/pdf/1706.00495.pdf
        """
        assert ((self.Jmag is not None) & (self.Ksmag is not None) &
                (self.Vmag is not None))
        if self.Jmag - self.Ksmag > 1.0:
            return self.Jmag + 1.75
        elif self.Jmag - self.Ksmag < -0.1:
            return self.Jmag + 0.5
        else:
            X = self.Vmag - self.Ksmag
            return (self.Jmag + 0.00152 * X**3 - 0.01862 * X**2 +
                    0.38523 * X + 0.0293)

    def TESS_Mag_BphJKs(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf
        """
        assert ((self.Jmag is not None) & (self.Ksmag is not None) &
                (self.Bphmag is not None))
        X = self.Bphmag - self.Ksmag
        return (self.Jmag + 0.00178 * X**3 - 0.01780 * X**2 +
                0.31926 * X + 0.0381)

    def TESS_Mag_BJKs(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
        assert ((self.Jmag is not None) & (self.Ksmag is not None) &
                (self.Bmag is not None))
        X = self.Bmag - self.Ksmag
        return (self.Jmag + 0.00226 * X**3 - 0.02313 * X**2 +
                0.29688 * X + 0.0407)

    # def TESS_Mag_JKs_lt0p7(J, Ks, debug=False):
    #     """ TESS magnitude estimate based on magnitude and
    #     Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
    #     X = J - Ks
    #     return J + 1.22163 * X**3 - 1.74299 * X**2 + 1.89115 * X + 0.0563

    # def TESS_Mag_JKs_gt0p7(J, Ks, debug=False):
    #     """ TESS magnitude estimate based on magnitude and
    #     Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
    #     X = J - Ks
    #     return J + 269.372 * X**3 + 668.453 * X**2 - 545.64 * X + 147.811

    def TESS_Mag_JKs(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
        assert ((self.Jmag is not None) & (self.Ksmag is not None))
        X = self.Jmag - self.Ksmag
        if (X > 0.7) and (X <= 1.0):
            return (self.Jmag - 269.372 * X**3 +
                    668.453 * X**2 - 545.64 * X + 147.811)
        elif (X <= 0.7) & (X >= -0.1):
            return (self.Jmag + 1.22163 * X**3 - 1.74299 * X**2 +
                    1.89115 * X + 0.0563)
        elif (X > 1.0):
            return self.Jmag + 1.75
        elif (X < -0.1):
            return self.Jmag + 0.5

    def TESS_Mag_GJ(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
        assert ((self.Jmag is not None) & (self.Gmag is not None))
        X = self.Gmag - self.Jmag
        return (self.Gmag + 0.00106 * X**3 + 0.01278 * X**2 -
                0.46022 * X + 0.0211)

    def TESS_Mag_VJH(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf"""
        assert ((self.Jmag is not None) & (self.Hmag is not None) &
                (self.Vmag is not None))
        X = self.Jmag - self.Hmag
        return (self.Vmag - 0.28408 * X**3 + 0.75955 * X**2 -
                1.96827 * X - 0.1140)

    def TESS_Mag_JH(self):
        """ TESS magnitude estimate based on magnitude and
        Eq. on p5 of arxiv.org/pdf/1706.00495.pdf
        """
        assert ((self.Jmag is not None) & (self.Hmag is not None))
        X = self.Jmag - self.Hmag
        return (self.Jmag - 0.99995 * X**3 - 1.49220 * X**2 +
                1.93384 * X + 0.1561)

    def TESS_Mag_V(self):
        assert (self.Vmag is not None)
        return self.Vmag - 0.6

    def TESS_Mag_J(self):
        assert (self.Jmag is not None)
        return self.Jmag + 0.5

    def TESS_Mag_H(self):
        assert (self.Hmag is not None)
        return self.Hmag + 0.7

    def TESS_Mag_Ks(self):
        assert (self.Ksmag is not None)
        return self.Ksmag + 0.8


def ticgen(args=None):
    """
    exposes ticgen to the command line
    """
    if args is None:
        parser = argparse.ArgumentParser(
            description="Calculate TESS noise level and TESS magnitude. "
                        "This work is all based upon the TESS Input v5 catalog "
                        "paper by Stassun, et al (https://arxiv.org/abs/1706.00495). "
                        "The user can input various magnitudes and the "
                        "code will calculate a TESS magnitude, if possible. "
                        "The order of priority in which magnitudes to use "
                        "follows the priority from the TIC paper. "
                        "The code will also calculate the 1-sigma noise level "
                        "based on the algorithm in the same paper. The user can specify "
                        "the baseline to integrate the noise over. This assumes "
                        "Poisson statistics, which is naive.")
        parser.add_argument('-T', '--Tmag', type=float,
                            help="TESS magnitude of the source")
        parser.add_argument('-J', '--Jmag', type=float,
                            help="J magnitude of the source")
        parser.add_argument('-K', '--Ksmag', type=float,
                            help="Ks magnitude of the source")
        parser.add_argument('-V', '--Vmag', type=float,
                            help="V magnitude of the source")
        parser.add_argument('-G', '--Gmag', type=float,
                            help="Gaia magnitude of the source")
        parser.add_argument('-H', '--Hmag', type=float,
                            help="H magnitude of the source")
        parser.add_argument('-B', '--Bmag', type=float,
                            help="B magnitude of the source")
        parser.add_argument('--Bphmag', type=float,
                            help="B photgraphic magnitude of the source")
        parser.add_argument('-i', '--integration', type=float,
                            default=60,
                            help="Specify the integration time in minutes time "
                            "to calculate the noise on. This assumes "
                            "noise scales with the inverse square-root "
                            "of the integration time. "
                            "(default: 60")
        args = parser.parse_args(args)
        args = vars(args)

    _output = calc_star(args)


def ticgen_csv(args=None):
    """
    exposes ticgen_csv to the command line
    """
    if args is None:
        parser = argparse.ArgumentParser(
            description="Calculate TESS noise level and TESS magnitude. "
                        "This work is all based upon the TESS Input v5 catalog "
                        "paper by Stassun, et al (https://arxiv.org/abs/1706.00495). "
                        "A user must give a filepath for a csv file with "
                        "columns containing magnitudes. The code reads the headers. "
                        "Header options are Tmag, Vmag, Jmag, Bmag, Bphmag, "
                        "Ksmag, Hmag, and Gmag. The code will return a file "
                        "with columns Tmag and one-sigma noise in "
                        "parts-per-million. The user can optionally "
                        "supply an integration time to calculate the noise on "
                        "(the default is 60 minutes)")
        parser.add_argument('input_fn',
                            help="Path to a csv file that lists known "
                                 "magnitudes of targets (one target per line). "
                                 "The file should contain a header with "
                                 "columns listing the magnitudes")
        parser.add_argument('-i', '--integration', type=float,
                            default=60,
                            help="Specify the integration time in minutes time "
                            "to calculate the noise on. This assumes "
                            "noise scales with the inverse square-root "
                            "of the integration time. "
                            "(default: 60")
        args = parser.parse_args(args)
        args = vars(args)
    else:
        if 'integration' not in args.keys():
            args['integration'] = 60

    mags = parse_file(args['input_fn'])

    output_arr = np.zeros([mags.shape[0], 2])
    for i in range(mags.shape[0]):
        magdict = mags.iloc[i].to_dict()
        # change nans to None
        for k, v in magdict.items():
            if np.isnan(v):
                magdict[k] = None
        star = Star(integration=args['integration'],
                                        **magdict)
        output_arr[i] = star.Tmag, star.oneSigmaNoise
    output_fn = args['input_fn'] + '-ticgen.csv'
    np.savetxt(output_fn, output_arr, delimiter=', ',
               fmt=['%10.3f', '%10.3f'])


def parse_file(infile):
    """Parse a comma-separated file.
    """
    try:
        mags = pd.read_csv(infile,)
    except FileNotFoundError as e:
        logger.error("There seems to be a problem with the input file, "
                     "please check the filename and location")
        sys.exit(1)
    except Exception as e:
        logger.error("There seems to be a problem with the input file, "
                     "please check the file format")
        raise e

    good_cnames = np.array(['Tmag', 'Vmag',
                            'Jmag', 'Bmag', 'Bphmag',
                            'Ksmag', 'Hmag', 'Gmag'])
    for cname in mags.columns.values:
        if cname not in good_cnames:
            logger.error("Unrecognized column {} found. ".format(cname) +
                         "Column names can only be be "+
                         "Tmag, Vmag, Jmag, Bmag, Bphmag, "+
                         "Ksmag, Hmag, Gmag")
            sys.exit(1)
    return mags


def calc_star(args):
    """Returns the TESS magnitude and 1-sigma noise in ppm.

    Parameters
    ----------
    Tmag : float
        Right Ascension (J2000) in decimal degrees.

    dec_deg : float
        Declination (J2000) in decimal degrees.

    padding : float
        Target must be at least `padding` pixels away from the edge of the
        superstamp. (Note that CCD boundaries are not considered as edges
        in this case.)

    Returns
    -------
    Tmag : float
        The TESS magnitude of the target.
    oneSigmaNoise : float
        The one-sigma scatter of the target in parts-per-million.
    """
    star = Star(**args)
    if star.Tmag is not None:
        print(Highlight.GREEN +
              "TESS mag = {:.2f}, ".format(star.Tmag) +
              "calculated using {}.".format(star.TmagProvenance) +
              Highlight.END)
        print(Highlight.GREEN +
              "1-sigma scatter in {:.0f} min = {:.0f} ppm.".format(
                  star.integration,
                  star.oneSigmaNoise) +
              Highlight.END)
    else:
        print(Highlight.RED +
              "TESS mag could not be calculated " +
              "You need to supply some magnitudes" +
              Highlight.END)

    return star.Tmag, star.oneSigmaNoise
