"""Worm-like chain models"""
import numpy as np

def WLC(d : np.ndarray, kBT : float, Lc : float, Lp : float) -> np.ndarray:
    r"""Worm-like chain model.

    .. math::
        F = \frac{k_BT}{L_p} \left[\frac{1}{4\left(1-\frac{d}{L_c}\right)^2}-\frac{1}{4}+\frac{d}{L_c}\right]

    Parameters
    ----------
    d : array-like
        Distance between end-points. Units: [um]
    kBT : float
        Boltzman contant times Temperature. Units: [pN*nm]
    Lc : float 
        Contour length. Units: [nm]
    Lp : float
        Persistance length. Units: [nm]

    Outputs
    -------
    F : array-like
        Required force to extend a worm-like chain. Units: [pN]

    Bustamante C, Marko JF, Siggia ED, Smith S. 
    Entropic elasticity of lambda-phage DNA. 
    Science. 1994 Sep 9;265(5178):1599-600. 
    doi: 10.1126/science.8079175. PMID: 8079175.
    """
    # Transform units: [um] to [nm]
    d = d*1000
    
    return (kBT/Lp)*(0.25/(1-d/Lc)**2 - 0.25 + d/Lc)

def bouchiat(d : np.ndarray, kBT : float, Lc : float, Lp : float) -> np.ndarray:
    r"""Bouchiat et al. worm-like chain model with seventh order correction.

    .. math::
        F = \frac{k_BT}{L_p} \left[\frac{1}{4\left(1-\frac{d}{L_c}\right)^2}-\frac{1}{4}+\frac{d}{L_c} +\sum_{n=1}^7 \alpha_n \left(\frac{d}{L_c}\right)^n\right]

    Parameters
    ----------
    d : array-like
        Distance between end-points. Units: [um]
    kBT : float
        Boltzman contant times Temperature. Units: [pN*nm]
    Lc : float 
        Contour length. Units: [nm]
    Lp : float
        Persistance length. Units: [nm]

    Outputs
    -------
    F : array-like
        Required force to extend a worm-like chain. Units: [pN]

    C. Bouchiat, M.D. Wang, J.-F. Allemand, T. Strick, S.M. Block, V. Croquette
    Estimating the Persistence Length of a Worm-Like Chain Molecule from Force-Extension Measurements
    Biophysical Journal
    """
    # Transform units: [um] to [nm]
    d = d*1000
    
    # Correction coefficients
    alpha = np.array([-0.5164228, -2.737418, 16.07497, -38.87607, 39.49944, -14.17718])

    # Compute correction
    corr = 0
    for n in range(len(alpha)): corr += alpha[n]*(d/Lc)**(n+2) 
    
    return (kBT/Lp)*(0.25/(1-d/Lc)**2 - 0.25 + d/Lc + corr)

def odijk(F : np.ndarray, kBT : float, Lc : float, Lp : float, S : float) -> np.ndarray:
    r"""Odidjk worm-like chain model.

    .. math::
        d = L_c \left( 1 - \frac{1}{2}\sqrt{\frac{k_BT}{FL_p}} + \frac{F}{S}

    Parameters
    ----------
    F : array-like
        Required force to extend a worm-like chain. Units: [pN]
    kBT : float
        Boltzman contant times Temperature. Units: [pN*nm]
    Lc : float 
        Contour length. Units: [nm]
    Lp : float
        Persistance length. Units: [nm]
    S : float
        Stretch modulus. Units: [pN]

    Outputs
    -------
    d : array-like
        Distance between end-points. Units: [um]

    Odijk, T. 
    Stiff Chains and Filaments under Tension 
    Macromolecules 1995 28 (20) 
    7016-7018 doi: 10.1021/ma00124a044
    """

    return Lc*(1-0.5*(kBT/(F*Lp))**0.5+F/S)/1000
