from .KDE_shape import get_KDE_shape
import zfit


def get_Bu2Ksee_shape(year="2018", trigger="ETOS", preffix=''):
    mass_window = (4500, 6000)
    obs = zfit.Space("B_M", limits=mass_window)
    Bp2Ksee_shape = get_KDE_shape(obs, "bpks", "high", "Bu2Ksee", bandwidth=None, preffix=preffix)
    return Bp2Ksee_shape


def get_Bd2Ksee_shape(year="2018", trigger="ETOS", preffix=''):
    mass_window = (4500, 6000)
    obs = zfit.Space("B_M", limits=mass_window)
    Bd2Ksee_shape = get_KDE_shape(obs, "bdks", "high", "Bd2Ksee", bandwidth=None, preffix=preffix)
    return Bd2Ksee_shape
