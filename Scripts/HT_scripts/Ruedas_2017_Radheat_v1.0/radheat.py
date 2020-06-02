#!/usr/bin/env python
# coding: utf-8

# NOTE: This Python script was generated from the Jupyter notebook file
# radheat.ipynb and was slightly edited (reformatted) by hand.

# # radheat - Calculation of radioactive heat production of $^{26}$Al, $^{40}$K, $^{60}$Fe, $^{232}$Th, $^{235}$U, and $^{238}$U
# ### Thomas Ruedas (t dot ruedas at uni-muenster dot de) - radheat v. 1.0, 18/10/2017
# #### Citation info
# If you use this program for your work, please acknowledge it and cite the following paper:
# 
# Ruedas, T. (2017): Radioactive heat production of six geologically important nuclides. *Geochem. Geophys. Geosys.*, 18(9), 3530-3541, doi:10.1002/2017GC006997.
#
# This software is released under the GNU General Public License v.3.
# 
# ## Purpose
# The purpose of this program is to calculate the energy available as heat or for chemical reactions and the specific heat production of six nuclides ($^{26}$Al, $^{40}$K, $^{60}$Fe, $^{232}$Th, $^{235}$U, and $^{238}$U), which are geologically important as heat sources, especially in the context of the formation, evolution, and geodynamics of terrestrial planetary bodies.
# 
# ## Unit conventions and data sources
# All half-lives are converted into years, with the relation between seconds and years defined as in NUBASE2016 (Audi *et al.*, 2017). Energy calculations use energies in keV. Atomic masses of isotopes are taken from AME2016 (Wang *et al.*, 2017), the elemental averages and isotopic abundances from IUPAC 2013 (Meija *et al.*, 2016a,b), and the half-lives are from NUBASE2016.
# 
# The nuclide-specific decay data (energies and intensities) were obtained from the [NuDat v.2.7$\beta$ website of the National Nuclear Data Center (NNDC) of the Brookhaven National Laboratory, USA](http://www.nndc.bnl.gov/nudat2/index.jsp), and the [Recommended Data site of the Laboratoire National Henri Becquerel, Saclay, France](http://www.nucleide.org/DDEP_WG/DDEPdata.htm). In general, the newest available data were used.
# 
# ## General procedure
# The decay chain of the nuclide is followed through most of its branches, leaving out only very minor (improbable) ones in some instances. Total decay energies $Q$ are calculated from the mass difference of parent and decay products of the step in the chain. For $\alpha$ decay, this is equivalent to the energy available for heating. For $\beta^-$ and $\beta^+$ decay, the energy carried by (anti)neutrinos is subtracted; for the latter, the annihilation of the positron and an electron are taken into account as an additional heat-effective energy term. For electron capture (ec), only the radiative part is converted into heat. As all decay series happen to start with nuclides whose half-lives $T_{1/2}$ are orders of magnitude longer than that of any of the daughters, it is the parent half-life that is used for power calculations; the `lambda_s` decay constants written out for each step are for informational purposes only.

from math import log
# physical and unit conversion constants
clight0=299792458.  # m/s, speed of light, CODATA2014
c2=clight0*clight0
amu=1.660539040e-27  # kg, atomic mass unit, CODATA2014
ec0=1.6021766208e-19  # C, elementary charge, CODATA2014
yr2s=31556926  # yr->s conversion factor (1 yr = 365.2422 d), NUBASE2016
yr2d=365.2422
yr2h=yr2d*24
yr2m=yr2h*60
u_He4=4.00260325413 # AME2016
u_el=9.10938356e-31/amu  # m_el/amu, CODATA2014
E_ep0=c2*2*u_el*1e-3*amu/ec0 # electron-positron annihilation energy (in keV)

# 
rU85=137.794 # ratio of U-238 to U-235 (Goldmann et al., 2015)
rU84=0.992742/0.000054 # ratio of U-238 to U-234 (IUPAC 2013)
rK19=0.067302/0.932581 # ratio of K-41 to K-39 (IUPAC 2013)


# ## Energy calculation functions
# At the core of the calculation is the energy balance of the decay. The following helper functions calculate energies; all include conversions from SI units into keV where necessary, as keV is the commonly used energy unit in nuclear physics.
# 
# In $\alpha$ decays, the entire decay energy is converted into heat, which follows from the mass difference between the parent nuclide and the daughter nuclide plus the $^4$He atom that eventually forms from the $\alpha$ particle:
# \begin{equation}
# E=c_0^2(m_\mathrm{P}-m_\mathrm{D}-m_{^4\mathrm{He}}).
# \end{equation}

def Qa(P,D):
    """Q-value for alpha decay in keV"""
    global u
    return c2*(u[P]-u[D]-u_He4)*1e-3*amu/ec0


# The following is a helper function that calculates the total decay energy for use in $\beta$ or $\epsilon$ (ec) decays according to
# \begin{equation}
# E=c_0^2(m_\mathrm{P}-m_\mathrm{D}).
# \end{equation}

def Qb(P,D):
    """Q-value for beta/ec decay in keV"""
    global u
    return c2*(u[P]-u[D])*1e-3*amu/ec0


# The heat energies are converted into power per mass using the decay constants $\lambda_{1/2}=\frac{\ln 2}{T_{1/2}}$ of the parent nuclide. 
# \begin{equation}
# H=\frac{E_H\lambda_{1/2}}{m_\mathrm{P}}.
# \end{equation}
# The following function includes a conversion back to SI units.

def EtoH_W(lam,EH,P):
    """Energy to power conversion in W, with conversion keV->J, yr->s"""
    global u
    return 1e3*lam*EH*ec0/(u[P]*amu*yr2s)


# The decay calculation yields the power per mass of the isotope under consideration, but it is often convenient to know the power per mass of the element, which usually has several isotopes with different total decay heat energies (if they are radioactive). This value changes with time as the proportions of the different isotopes in the isotopic composition of the element change due to the different decay rates. The values for extant isotopes calculated here are present-day values based on observed isotopic abundances and masses:
# \begin{equation}
# H_\mathrm{elm}=\frac{1}{\bar{u}}\sum H_i X_i u_i,
# \end{equation}
# where $\bar{u}=\sum X_i u_i$ indicates the mean value for the element and the sum is over all of its isotopes.
# 
# It must be ensured that $\bar{u}$ and $\sum X_i u_i$ are consistent with each other within the accuracy of the values for $\bar{u}$ from the IUPAC 2013 reports and for the $u_i$ from the AME2016 evaluations. This is the case if the values can be taken from one self-consistent database, in particular if one is interested in present-day values and chooses the isotopic abundances from Meija *et al.* (2016b); for Th, ${}^{232}$Th is the only isotope with significant abundance, and so its power per mass of isotope can be used for the bulk element. However, if data for the abundances are from different sources, additional considerations are necessary to guarantee internal consistency.
# 
# One such case are the extinct isotopes ${}^{26}$Al and ${}^{60}$Fe, for which abundances must be set. Assuming that they are the only radioactive isotopes of their respective elements, one can take the tabulated mean atomic mass as the mean of the stable isotopes, $\bar{u}_\mathrm{st}$. Then the mean of the element in presence of the radionuclide is constrained by the closure condition for the abundances $X_i$, i.e., $\sum X_i=1$, to be
# \begin{equation}
# \bar{u}=(1-X_\mathrm{rad})\bar{u}_\mathrm{st}+X_\mathrm{rad}u_\mathrm{rad},
# \end{equation}
# where the subscript "rad" indicates the radioactive nuclide.
# 
# In the case of K, there are the two stable isotopes ${}^{39}$K and ${}^{41}$K in addition to the radioactive isotope ${}^{40}$K. The calculation for present-day proportions, which does not need further assumptions, is described further below. If $X_{40}$ is set to a different value, the default for the ratio $r_{40}=X_{40}/X_{39}$ becomes obsolete, and we make instead the additional assumption that $r_{41}=X_{41}/X_{39}$ is constant and given by the IUPAC 2013 value. Then the mean atomic mass of the stable isotopes is given by
# \begin{equation}
# \bar{u}_\mathrm{st}=\frac{u_{39}+r_{41}u_{41}}{1+r_{41}}
# \end{equation}
# and is inserted into the previous general equation.

def uelem(Xiso,iso):
    """Mean element atomic mass for elements with 1 radionuclide"""
    global u,Xiso_def
    # get element name from isotope name
    j=iso.find('-')
    el=iso[0:j]
    # mean of stable isotopes from (present-day) default values
    if el == 'K':
        ust=(u['K-39']+rK19*u['K-41'])/(1+rK19)
    elif Xiso_def == 0.:
        ust=u[el] # Al-26, Fe-60: extinct
    return (1-Xiso)*ust+Xiso*u[iso]


# For U, we assume the existence of three radioactive isotopes and use the recent reevaluation of the ratio $r_5$ of ${}^{238}$U to ${}^{235}$U by Goldmann *et al.* (2015), which gave $r_5=137.794$, slightly less than the value of 137.804 derived from the IUPAC abundances, which were derived excluding meteoritic materials. In order to determine the isotopic fractions, an additional assumption is necessary to construct a unique solution. The choice made here is to set the ratio $r_4$ of ${}^{238}$U to ${}^{234}$U to the value given by the IUPAC data, based on the assumption that all ${}^{234}$U, which appears only in minute amounts, always stems from ${}^{238}$U, of whose decay chain it is a part, and that the relative amounts of these two coupled isotopes are consistent with each other; this implies that $r_4$ is always the same, even if a different $r_5$ is used. With $r_4=18384.111$ and the closure condition $\sum X_i=1$, we have
# \begin{align}
# X_{238}&=\left(\frac{1}{r_4}+\frac{1}{r_5}+1\right)^{-1}\\
# \bar{u}_\mathrm{U}&=X_{234}u_{234}+X_{235}u_{235}+X_{238}u_{238}=
# \left(\frac{u_{234}}{r_4}+\frac{u_{235}}{r_5}+u_{238}\right)X_{238}.
# \end{align}
# For the purpose of calculating bulk element power we treat ${}^{234}$U together with ${}^{238}$U.

def XisoU():
    """Isotope fractions of U isotopes 234, 235, 238"""
    global u
    X_U238=1/(1+1/rU84+1/rU85)
    X_U235=X_U238/rU85
    X_U234=X_U238/rU84
    u['U']=(u['U-234']/rU84+u['U-235']/rU85+u['U-238'])*X_U238
    return [X_U234,X_U235,X_U238]


# A conversion of energy to mass is needed in order to determine the mass of an excited nuclear isomer from the mass of the ground state. Such a conversion is needed in the calculations for the decay chain of $^{238}$U, which includes $^{234}$Pa and its isomer $^{234}$Pa$^\mathrm{m}$.

def keV2u(E):
    """Conversion of energy in keV to mass in u"""
    return 1e3*E*ec0/(c2*amu)


# The energy available for heating of a decay to the $k$-th level of the daughter consists of the mean energy of the $\beta^-$ emission and the entire radiative (electromagnetic) energy released in the de-excitation of the $k$-th level. The latter is calculated as the difference between the total decay energy and the maximum $\beta^-$ energy rather than read from tabulated observations. The terms of the sum are weighted by the intensity/probability of decay to the $k$-th level.

def getEHb(Qs,Eb_endp_i,Eb_mean_i,Ib_i):
    """Beta decay energy available for heating"""
    EHb=0.
    k=0
    while (k < len(Ib_i)):
        EHb+=(Eb_mean_i[k]+Qs-Eb_endp_i[k])*Ib_i[k]
        k+=1
    return EHb


# As stated above, in $\alpha$ decays, the entire decay energy is converted to heat. The following function returns the $Q$ value of $\alpha$ decays. The weight factor `wa` is for use in a multi-branch decay, where it would be $<1$ and represents the probability of the $\alpha$ branch.

def QHalpha(P,D,lmbd,wa=1):
    """Energies and power of alpha decay"""
    # In alpha decays, the entire decay energy is converted to heat. In a
    # multi-branch decay, wa < 1 is the probability of the alpha branch.
    global Etot,Qgstot,silent
    Qgs=Qa(P,D)
    if (wa == 1):
        Etot+=Qgs
        Qgstot+=Qgs
    else:
        Etot+=wa*Qgs
        Qgstot+=wa*Qgs
    if silent == 1: return
    print ("\t(lambda_s=%.4e 1/yr)\tI=%f%%\n"
               "\tQ_gs=%.3f keV (%.3e J)\n" \
               "\tE_H (per atom)=%.6f keV (%.3e J)") % \
               (lmbd,wa*100,Qgs,1e3*Qgs*ec0,Qgs,1e3*Qgs*ec0)


# In a $\beta^-$ decay, we have to determine how much energy is carried off by neutrinos, for each target (daughter isotope) energy level. In a multi-branch decay, `wb` $<1$ is the probability of the $\beta^-$ branch. This weight factor `wb` thus corresponds to the sum of all $\beta^-$ intensities in a multi-branch decay and ensures that the energies are weighted correctly in the total sum. The $\beta^-$ intensities from the original sources, which do not always sum exactly to 1 even in single-branch decays, are normalized in this function to ensure that the decays to the different target levels of the daughter have the correct relative proportions.

def QHbetam(P,D,lmbd,Ib_i,Eb_endp_i,Eb_mean_i,wb=1):
    """Energies and power of beta- decay"""
    global Etot,Qgstot,silent
    Qgs=Qb(P,D)
    if (len(Eb_endp_i) == 0): Eb_endp_i=[Qgs]
    # normalize intensities to 1
    Ib=sum(Ib_i)
    for i in range(len(Ib_i)):
        Ib_i[i]/=Ib
    Eb_endp=sum(EI[0]*EI[1] for EI in zip(Eb_endp_i,Ib_i))
    Eb_mean=sum(EI[0]*EI[1] for EI in zip(Eb_mean_i,Ib_i))
    fr_b=Eb_mean/Eb_endp
    EHb=getEHb(Qgs,Eb_endp_i,Eb_mean_i,Ib_i)
    if (wb == 1):
        Qgstot+=Qgs
        Etot+=EHb
    else:
        Qgstot+=wb*Qgs
        Etot+=wb*EHb
    if silent == 1: return
    print ("\t(lambda_s=%.4e 1/yr)\tI=%f%%\tX_b=%.6f\n"
               "\tQ_gs=%.3f keV (%.3e J)\n" \
               "\tE_H (per atom)=%.6f keV (%.3e J)") % \
               (lmbd,wb*100,fr_b,Qgs,1e3*Qgs*ec0,EHb,1e3*EHb*ec0)


# ## Individual nuclide decay functions
# The following six functions implement the decay of the six nuclides under consideration.

# ### $^{26}$Al
# $^{26}$Al was probably the most important heat source during the early formation stages of planets and is now extinct in planetary bodies. It decays with a half-life of $\sim 717$ ky into the stable $^{26}$Mg, either by $\beta^+$ decay with a probability $I$ of 0.8173 or by ec with a probability of 0.1827 (NuDat v.2.7$\beta$, Basunia & Hurst, 2016). Almost one quarter of the total decay energy is carried off by neutrinos and does not contribute to heat production. - As the isotope is extinct, the power calculation for bulk Al returns zero by default; this can be changed by assigning a non-zero value to `Xiso`.

# nuclides
# Aluminum-26 #################################################################
def calc_Al26(Xiso):
    """Decay energy and power of Al-26"""
    global u,Xiso_def
    u={'Al-26': 25.986891863,'Al': 26.9815385,'Mg-26': 25.982592971}
    Xiso_def=0.
    if Xiso == "":
        Xiso=Xiso_def # default: extinct
        ubar=u['Al']
    else:
        ubar=uelem(Xiso,'Al-26')
    Qgs=Qb('Al-26','Mg-26') # ground-state energy difference
#   intensities and energies from NuDat v.2.7b
#   beta+ branch
    print "beta+ decay: Al-26 -> Mg-26"
    Ib=0.8173  # beta+ intensity (NuDat v.2.7b)
    thalf_b=717e3 # yr
    lambda_b=log(2.)/thalf_b
    Eb_endp=1173.42
    Eb_mean=543.29
    fr_b=Eb_mean/Eb_endp
    Egb=Qgs-Eb_endp # total gamma from beta+, Mg-26 exc1->gs + e-e' annihilation
    EHb=Ib*(Eb_mean+Egb) # total heat from beta+
#   electron capture branch
    print "electron capture: Al-26 -> Mg-26"
    # ec branches to Mg-26 excited states
    Ie_i={'1': 0,'2': 0.0274}
    Ie_i['1']=1-(Ib+Ie_i['2'])  # applying closure condition
    thalf_e=thalf_b
    lambda_e=log(2.)/thalf_e
    # gamma levels
    Eg_i={'2-0': 2938, '1-0': Egb-E_ep0, '2-1': 0}
    Eg_i['2-1']=Eg_i['2-0']-Eg_i['1-0']
    # total heat from ec
    EHe=(Eg_i['2-0']+Eg_i['2-1'])*Ie_i['2']+Eg_i['1-0']*Ie_i['1']
#   total heat and power
    EH=EHb+EHe
    He=EtoH_W(lambda_e,EH,'Al-26')
    He_Altot=He*Xiso*u['Al-26']/ubar
    print ("  lambda=%.4e 1/yr\tX_b=%.6f\n"
               "  Q_gs=%.3f keV (%.3e J)\n" \
               "  E_H (per atom)=%.3f keV (%.3e J)") % \
               (lambda_e,fr_b,Qgs,1e3*Qgs*ec0,EH,1e3*EH*ec0)
    print "  H(Al-26)=%.6e W/kg\tH(Al)=%.6e W/kg" % (He,He_Altot)
    if Xiso != Xiso_def: print ("  Mean u_Al used with Xiso=%.3e: %.7f amu") % (Xiso,ubar)


# ### $^{40}$K
# $^{40}$K is the most abundant of the four still extant nuclides considered here and is of special interest because it is assumed to contribute most of the radiogenic heat of the core; its present-day fraction in K is $1.1668\times 10^{-4}$ (Naumenko *et al.*, 2013). It has two important decay branches, both of which produce stable daughters: the most likely ($I=0.8928$) decay is a $\beta^-$ decay directly to the ground state of $^{40}$Ca, the other ($I=0.1072$) produces $^{40}$Ar by electron capture, as does the third, very low-probability $\beta^+$ branch (NuDat v.2.7$\beta$, Chen, 2017). As the branch leading to $^{40}$Ca decays directly into the ground state, there is no $\gamma$ contribution. Note that up to now, the mean $\beta$ energy in the $\beta^-$ decay to $^{40}$Ca was underestimated in nuclear data evaluations. The value of 583.55 keV adopted here is a recent recalculation that overcomes limitations in older evaluations related to the correct treatment of 3rd forbidden unique transitions such as this one (Mougeot, 2015 and pers.comm. 2017); it is the mean of a calculation with the full calculated $\beta$ spectrum and a calculation based on an experimental shape factor, using $Q$ as derived from AME2016.
# 
# The present-day isotopic fraction of ${}^{40}$K and the ratio $r_{40}=X_{40}/X_{39}$ were recently redetermined by Naumenko *et al.* (2013). The fraction was found to be the same as the four decades old one given in Meija *et al.* (2016b) within error, but for consistency we recalculate the mean atomic mass using the best estimates from Naumenko *et al.* (2013), $X_{40}=1.1668\times 10^{-4}$ and $r_{40}=1.25116\times 10^{-4}$, and the tabulated masses of the three relevant isotopes, of which two are stable:
# \begin{equation}
# \bar{u}_\mathrm{K}=\left(u_{40}-u_{41}+\frac{u_{39}-u_{41}}{r_{40}}\right)X_{40}+u_{41}.
# \end{equation}
# The result agrees with the IUPAC value if rounded to the same accuracy.

# Potassium-40 ################################################################
def calc_K40(Xiso):
    """Decay energy and power of K-40"""
    global u,Etot,Qgstot,Xiso_def
    # mean element atomic mass of K is calculated from default isotope ratios
    u={'Ar-40': 39.96238312378,\
        'K-39': 38.96370648661,'K-40': 39.963998166,\
        'K-41': 40.96182525796,'K': 0.,\
        'Ca-40': 39.962590865}
    # default: Naumenko et al. (2013)
    Xiso_def=1.1668e-4  # K-40/K
    r09=1.25116e-4  # K-40/K-39
    if Xiso == "":
        Xiso=Xiso_def
        u['K']=(u['K-40']-u['K-41']+(u['K-39']-u['K-41'])/r09)*Xiso_def+u['K-41']
        ubar=u['K']
    else:
        ubar=uelem(Xiso,'K-40')
    thalf_tot=1.248e9 # yr
    # branching ratio from NuDat v.2.7b
    lambda_eff=log(2.)/thalf_tot
    xb=0.8928
    xe_i=[0.1067,0.0005]
    xe=sum(xe_i)
    br=xe/xb
    print "beta- decay: K-40 -> Ca-40"
    lambda_s=lambda_eff/(1+br)
    # beta energy from Mougeot (2015 and pers.comm., 2017)
    Ib_i=[1.]
    Eb_endp_i=[] # same as ground-state Q because of absence of gammas
    Eb_mean_i=[583.55]
    QHbetam('K-40','Ca-40',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    print "electron capture: K-40 -> Ar-40"
    # a beta+ component with an intensity of 1e-5 is neglected here
    lambda_s=lambda_s*br
    Qgs=Qb('K-40','Ar-40')
    Qgstot+=xe*Qgs
    Ig=xe_i[0]/xe # most but not all decays entail a gamma
    Eg=1460.82*Ig # NuDat v.2.7b
    Etot+=xe*Eg
    fr_g=Eg/Qgs
    Htot=EtoH_W(lambda_eff,Etot,'K-40')
    print ("\tlambda_s=%.4e 1/yr\tX_g=%.6f\n"
               "\tQ_gs=%.3f keV (%.3e J)\n" \
               "\tE_H (per atom)=%.6f keV (%.3e J)") % \
               (lambda_s,fr_g,Qgs,1e3*Qgs*ec0,Eg,1e3*Eg*ec0)
    print "total K-40 decay (weighted mean)"
    print ("  Q_gs=%.3f keV (%.3e J)\n  E_H (per atom)=%.6f keV (%.3e J)\n"       "  H(K-40)=%.6e W/kg\tH(K)=%.6e W/kg") % \
      (Qgstot,1e3*Qgstot*ec0,Etot,1e3*Etot*ec0,Htot,Htot*Xiso*u['K-40']/ubar)
    print ("  Mean u_K used with Xiso=%.4e: %.4f amu") % (Xiso,ubar)


# ### $^{60}$Fe
# The other major radiogenic heat source during the earliest part of Solar System history may have been $^{60}$Fe ($T_{1/2}\approx 2.62$ Myr), which transmutes by two $\beta^-$ decays via $^{60}$Co ($T_{1/2}\approx 5.2712$ yr) to $^{60}$Ni (NUBASE2016) and is now extinct in planetary bodies; the initial concentrations of this nuclide are very uncertain, and recent work suggests that older studies have overestimated its abundance and hence its importance as a heat source (Boehnke et al., Trappitsch et al., 2017). As the half-life of the intermediate step is more than six orders of magnitude shorter than that of $^{60}$Fe, the $T_{1/2}$ of the latter is assumed to apply to the entire chain. However, it is the second decay step that contributes more than 95% of the total heat. - As the isotope is extinct, the power calculation for bulk Fe returns zero by default; this can be changed by assigning a non-zero value to `Xiso`.

# Iron-60 #####################################################################
def calc_Fe60(Xiso):
    """Decay energy and power of the Fe-60 chain"""
    global u,Etot,Qgstot,Xiso_def
    u={'Fe-60': 59.934070411,'Fe': 55.845,\
        'Co-60': 59.933815667,'Ni-60': 59.930785256}
    Xiso_def=0.
    if Xiso == "":
        Xiso=Xiso_def # default: extinct
        ubar=u['Fe']
    else:
        ubar=uelem(Xiso,'Fe-60')
    print "  Step 1, beta- decay: Fe-60 -> Co-60"
    thalf_b=2.62e6 # yr
    lambda_eff=log(2.)/thalf_b
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[1.]
    Eb_endp_i=[178.]
    Eb_mean_i=[50.2]
    QHbetam('Fe-60','Co-60',lambda_eff,Ib_i,Eb_endp_i,Eb_mean_i)
    print "  Step 2, beta- decay: Co-60 -> Ni-60 (T1/2=5.2712 yr)"
    thalf_s=5.2712 # yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    # T1/2(Co-60) << T1/2(Fe-60), hence lambda_b for Fe-60 is rate-limiting
    # an intermediate level with Eb_endp=664.19 keV and I=2e-5 is neglected
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[0.9988,0.0012]
    Eb_endp_i=[317.05,1490.29]
    Eb_mean_i=[95.77,625.87]
    QHbetam('Co-60','Ni-60',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    Htot=EtoH_W(lambda_eff,Etot,'Fe-60')
    print "Total heat energy/power for combined Fe-60 -> Co-60 -> Ni-60 decay"
    print "  Q_gs=%.3f keV (%.3e J)\n  E_H (per atom)=%.6f keV (%.3e J)" %       (Qgstot,1e3*Qgstot*ec0,Etot,1e3*Etot*ec0)
    print "  Htot(Fe-60)=%.6e W/kg\tHtot(Fe)=%.6e W/kg" % \
      (Htot,Htot*Xiso*u['Fe-60']/ubar)
    if Xiso != Xiso_def: print ("  Mean u_Fe used with Xiso=%.3e: %.3f amu") % (Xiso,ubar)


# ### $^{232}$Th
# Of the six radionuclides considered, $^{232}$Th is the one with the longest half-life ($T_{1/2}\approx 14$ Gy), and it is the only isotope of Th that exists today in appreciable amounts. It has a long decay chain consisting of several $\alpha$ and $\beta^-$ decays, but as the half-lives of all unstable daughters are between 9 and 18 orders of magnitude shorter, $T_{1/2}=14$ Gy is used for all rate calculations. While heat production calculation from the $\alpha$ decays is straightforward and requires only the masses of the parent and daughter, care must be taken with the $\beta^-$ decays of $^{228}$Ra (Luca, 2009 2012), $^{228}$Ac (NuDat v.2.7$\beta$, Abusaleem, 2014), $^{212}$Pb (Nichols, 2011b,c), $^{212}$Bi (Nichols, 2011a,d), and $^{208}$Tl (Nichols, 2010, 2016), all of which feed several different excited energy levels of their respective daughters. Moreover, $^{212}$Bi has two decay branches: it can decay via the $\alpha$ branch ($I=0.3593$) to $^{208}$Tl or via the $\beta^-$ branch ($I=0.6407$) to $^{212}$Po (Nichols, 2011d), and the decay energies of the daughters have to be weighted accordingly. Note that in some cases the $\beta^-$ branch of $^{212}$Bi leads to a $^{212}$Po$^\mathrm{m}$ state that proceeds directly via $\alpha$ decay to $^{208}$Pb, i.e., without passing through the $^{212}$Po ground state by $\gamma$ emission; this branch is not accounted for explicitly in the energy calculation, but it is in fact included in the final sum, because it is energetically equivalent to the path through the ground state.
# 
# Apart from the final stable daughter $^{208}$Pb, each decay of $^{232}$Th eventually also produces 6 atoms of $^{4}$He.

# Thorium-232 #################################################################
def calc_Th232():
    """Decay energy and power of the Th-232 series"""
    global u,Etot,Qgstot
    u={'Tl-208': 207.982017992,\
        'Pb-208': 207.976651918,'Pb-212': 211.991895975,\
        'Bi-212': 211.991285016,\
        'Po-212': 211.988867896,'Po-216': 216.001913506,\
        'Rn-220': 220.011392534,\
        'Ra-224': 224.020210453,'Ra-228': 228.031068657,\
        'Ac-228': 228.031019767,\
        'Th-228': 228.028739835,'Th-232': 232.038053689}
    print "decay chain: Th-232 -> Pb-208"
    # Th-232 -> Ra-228
    print "  Step 1, alpha decay: Th-232 -> Ra-228"
    thalf_Th232=14e9 # yr, AME2016
    lambda_eff=log(2.)/thalf_Th232
    QHalpha('Th-232','Ra-228',lambda_eff)
    #  Ra-228 -> Ac-228
    print "  Step 2, beta- decay: Ra-228 -> Ac-228"
#   T1/2(daughters) << T1/2(Th-232), hence lambda_Th232 is rate-limiting for all
    thalf_s=5.75 # yr
    lambda_s=log(2.)/thalf_s
    # beta energies from NuDat v.2.7b, intensities from Luca (2009a, 2012)
    Ib_i=[0.3,0.087,0.49,0.12]
    Eb_endp_i=[12.7,25.6,39.1,39.5]
    Eb_mean_i=[3.22,6.48,9.94,10.04]
    QHbetam('Ra-228','Ac-228',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # Ac-228 -> Th-228
    print "  Step 3, beta- decay: Ac-228 -> Th-228"
    thalf_s=6.15/yr2h # conversion h->yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[4.2e-05,6.2e-05,0.00019,0.00054,2.9e-05,0.0028,0.00038,3.3e-05,\
              0.00251,0.00046,0.00056,0.00034,0.00077,0.00117,0.00045,5e-05,\
              0.00119,0.00062,0.00389,0.00133,0.0176,0.0243,0.00164,0.0112,\
              0.0419,0.03,0.0115,0.00095,0.076,0.006,0.012,0.0006,0.00217,\
              0.00058,0.0067,0.0017,2.5e-05,0.0311,0.058,0.059,0.0026,0.0007,\
              0.0311,0.0033,0.0014,0.299,0.00041,0.0021,0.,0.0059,0.1165,\
              0.00116,0.006,0.07]
    Eb_endp_i=[11.,97.,104.,111.,120.,124.,147.,175.,189.,197.,205.,227.,234.,\
                   241.,336.,338.,374.,376.,390.,398.,410.,446.,450.,451.,\
                   488.,491.,496.,516.,603.,684.,702.,718.,790.,837.,907.,\
                   959.,960.,966.,981.,1011.,1043.,1074.,1111.,1118.,1154.,\
                   1165.,1190.,1260.,1615.,1806.,1738.,1756.,1947.,2076.]
    Eb_mean_i=[2.73,25.15,26.94,29.04,31.51,32.44,38.72,46.79,50.75,52.94,\
              55.39,61.79,63.71,65.77,94.51,95.13,106.17,106.77,111.29, \
              113.94,117.50,129.00,130.51,130.82,142.79,143.73,145.32, \
              152.1,181.0,208.9,215.3,220.9,246.4,260.3,288.8,307.6, \
              307.9,310.2,315.7,327.0,338.9,350.6,364.7,367.0,381.0, \
              385.0,394.4,421.2,536.9,609.3,609.7,616.9,694.3,747.0]
    QHbetam('Ac-228','Th-228',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # Th-228 -> Ra-224
    print "  Step 4, alpha decay: Th-228 -> Ra-224"
    thalf_s=1.9124 # yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    QHalpha('Th-228','Ra-224',lambda_s)
    #  Ra-224 -> Rn-220
    print "  Step 5, alpha decay: Ra-224 -> Rn-220"
    thalf_s=3.6319/yr2d # conversion d->yr, NUBASE2012
    lambda_s=log(2.)/thalf_s
    QHalpha('Ra-224','Rn-220',lambda_s)
    # Rn-220 -> Po-216
    print "  Step 6, alpha decay: Rn-220 -> Po-216"
    thalf_s=55.6/yr2s # conversion s->yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    QHalpha('Rn-220','Po-216',lambda_s)
    # Po-216 -> Pb-212
    print "  Step 7, alpha decay: Po-216 -> Pb-212"
    thalf_s=0.145/yr2s # conversion s->yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    QHalpha('Po-216','Pb-212',lambda_s)
    # Pb-212 -> Bi-212
    print "  Step 8, beta- decay: Pb-212 -> Bi-212"
    thalf_s=10.64/yr2h # conversion h->yr, NUBASE2016
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from Nichols (2011)
    Ib_i=[0.0499,0.817,0.133]
    Eb_endp_i=[154.6,331.3,569.9]
    Eb_mean_i=[41.1,93.5,171.7]
    QHbetam('Pb-212','Bi-212',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # two decay branches for Bi-212
    # branching ratio from Nichols (2011)
    thalf_tot=60.55/yr2m # min (NUBASE2016)
    lambda_tot=log(2.)/thalf_tot
    xb=0.6407
    xa=0.3593
    br=xa/xb
    # Bi-212 -> Po-212
    # Some Po-212m levels decay directly to Pb-208; these are not treated separately
    # but are covered equivalently by the gamma emission to Po-212 and the subsequent alpha
    # decay Po-212 -> Pb-208 (step 10a below).
    print "  Step 9a, beta- decay: Bi-212 -> Po-212"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from Nichols (2011)
    Ib_i=[0.0068,0.00032,0.0021,0.019,0.0144,0.045,0.5531]
    Eb_endp_i=[446.1,451.2,572.7,631.4,739.4,1524.8,2252.1]
    Eb_mean_i=[130.1,131.7,172.4,192.7,230.8,533.1,834.2]
    QHbetam('Bi-212','Po-212',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    #  Bi-212 -> Tl-208
    print "  Step 9b, alpha decay: Bi-212 -> Tl-208"
    lambda_s=lambda_s*br
    QHalpha('Bi-212','Tl-208',lambda_s,wa=xa)
    # Po-212 -> Pb-208
    print "  Step 10a, alpha decay: Po-212 -> Pb-208"
    thalf_s=294.7e-9/yr2s # s, NUBASE2016
    lambda_s=log(2.)/thalf_s
    # weight xb is used b/c this continues the original beta- branch
    QHalpha('Po-212','Pb-208',lambda_s,wa=xb)
    # Tl-208 -> Pb-208
    print "  Step 10b, beta- decay: Tl-208 -> Pb-208"
    thalf_s=3.053/yr2m # min (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from Nichols (2016)
    Ib_i=[0.00052,0.00017,0.00045,5e-05,0.00102,2e-05,0.00231,0.00174,7e-05,\
              0.0317,0.00048,0.0063,0.241,0.221,0.492]
    Eb_endp_i=[518.3,615.7,640.3,675.1,702.4,737.1,818.6,873.7,1003.6,1037.8,\
                   1052.4,1079.0,1290.5,1523.9,1801.3]
    Eb_mean_i=[154.3,187.7,196.4,208.6,218.3,230.8,260.4,280.8,329.7,342.8,\
                   348.4,358.6,441.5,535.4,649.5]
    # weight xa is used b/c this continues the original alpha branch
    QHbetam('Tl-208','Pb-208',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xa)
    print "Total heat energy/power for Th-232 decay series"
    print "  Q_gs=%.3f keV (%.3e J)\n  E_H (per atom)=%.6f keV (%.3e J)" %       (Qgstot,1e3*Qgstot*ec0,Etot,1e3*Etot*ec0)
    print "  Htot=%.6e W/kg" % EtoH_W(lambda_eff,Etot,'Th-232')


# ### $^{235}$U
# $^{235}$U is the less abundant and shorter-lived ($T_{1/2}=704$ My; Huang & Wang, 2014) of the two major uranium isotopes. Its decay chain is even longer and more complicated than that of $^{232}$Th and yields $^{207}$Pb as well as 7 atoms of $^{4}$He as final products. The decay branch from $^{223}$Fr to $^{219}$At has a very low probability, and therefore the subsequent steps of that branch are omitted from the calculation; they merge with the main decay path at different points. With regard to the energy balance, the $\beta^-$ decays of $^{231}$Th (NuDat v.2.7$\beta$, Browne & Tuli, 2013a), $^{227}$Ac (NuDat v.2.7$\beta$, Kondev *et al.*, 2016), $^{223}$Fr (Huang & Wang, 2009, 2012), $^{211}$Pb (NuDat v.2.7$\beta$, Singh *et al.*, 2013), and $^{207}$Tl (NuDat v.2.7$\beta$, Kondev & Lalkovski, 2011) require attention because of the neutrino component. A possible, very low-probability $\beta^-$ decay path from $^{207}$Tl$^\mathrm{m}$ to $^{207}$Pb is not treated individually but as if it were identical to the path via the $^{207}$Tl ground state.

# Uranium-235 #################################################################
def calc_U235():
    """Decay energy and power of the U-235 series"""
    global u,Etot,Qgstot,HtotU,silent
    # mean element atomic mass of U is calculated from isotope ratios
    u={'Tl-207': 206.977418586,\
           'Pb-207': 206.975896735,'Pb-211': 210.988735356,\
           'Bi-211': 210.987268698,\
           'Po-211': 210.986653085,'Po-215': 214.999418454,\
           'At-219': 219.011160647,\
           'Rn-219': 219.009478753,\
           'Fr-223': 223.019734313,\
           'Ra-223': 223.018500719,\
           'Ac-227': 227.027750666,\
           'Th-227': 227.027702618,'Th-231': 231.036302853,\
           'Pa-231': 231.035882575,\
           'U-234': 234.040950370,'U-235': 235.043928190,\
           'U-238': 238.050786996,'U': 0}
    if silent == 0: print "decay chain: U-235 -> Pb-207"
    # U-235 -> Th-231
    if silent == 0: print "  Step 1, alpha decay: U-235 -> Th-231"
    thalf_U235=704e6 # yr (NUBASE2016)
    lambda_eff=log(2.)/thalf_U235
    QHalpha('U-235','Th-231',lambda_eff)
    #  Th-231 -> Pa-231
    if silent == 0: print "  Step 2, beta- decay: Th-231 -> Pa-231"
#   T1/2(daughters) << T1/2(U-235), hence lambda_U235 is rate-limiting for all
    thalf_s=25.52/yr2h # h (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[3e-5,0.00065,7.8e-6,0.026,0.003,0.121,0.013,0.12,0.4,0.32,0.0017,\
              0.0017,0.00022]
    Eb_endp_i=[39.8,71.4,73.6,144.3,173.4,208.1,217.4,289.3,290.2,307.4,313.9,\
                   333.0,391.6]
    Eb_mean_i=[9.8,18.1,18.7,37.8,46.0,55.9,58.6,79.8,80.1,85.3,87.3,93.1,111.4]
    QHbetam('Th-231','Pa-231',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # Pa-231 -> Ac-227
    if silent == 0: print "  Step 3, alpha decay: Pa-231 -> Ac-227"
    thalf_s=3.276e4 # yr (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Pa-231','Ac-227',lambda_eff)
    # two decay branches for Ac-227 (Kondev et al., 2016)
    thalf_tot=21.772 # yr (NUBASE2016)
    lambda_tot=log(2.)/thalf_tot
    xb=0.9862
    xa=0.0138
    br=xa/xb
    #  Ac-227 -> Th-227
    if silent == 0: print "  Step 4a, beta- decay: Ac-227 -> Th-227"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[0.002999990814,0.0999996938,0.3499989283,0.53999834652]
    Eb_endp_i=[6.9,20.3,35.5,44.8]
    Eb_mean_i=[1.73,5.11,8.98,11.37]
    QHbetam('Ac-227','Th-227',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    # Ac-227 -> Fr-223
    if silent == 0: print "  Step 4b, alpha decay: Ac-227 -> Fr-223"
    lambda_s=lambda_s*br
    QHalpha('Ac-227','Fr-223',lambda_eff,wa=xa)
    # Th-227 -> Ra-223
    if silent == 0: print "  Step 5a, alpha decay: Th-227 -> Ra-223"
    lambda_s=18.697/yr2d # d, NUBASE2016
    # weight xb is used b/c this continues the original beta- branch
    QHalpha('Th-227','Ra-223',lambda_eff,wa=xb)
    # two decay branches for Fr-223 (Huang & Wang, 2012)
    thalf_tot=22./yr2m # min, NUBASE2016
    lambda_tot=log(2.)/thalf_tot
    xb_a=0.9998
    xa_a=0.0002
    br=xa_a/xb_a
    # Fr-223 -> Ra-223
    if silent == 0: print "  Step 5b-1, beta- decay: Fr-223 -> Ra-223"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from Huang & Wang (2012)
    Ib_i=[0.000012,0.000004,0.0000046,0.0002,0.000082,0.000051,0.00106,\
              0.000011,0.00025,0.00088,0.00035,0.0054,0.00014,0.00004,0.0014,\
              0.00019,0.0000111,0.00013,0.000046,0.018,0.00037,0.00042,0.00049,\
              0.00032,0.00004,0.091,0.0024,0.15,0.0027,0.67,0.06,0.01]
    Eb_endp_i=[120.3,124.6,129.9,191.5,205.9,208.4,222.6,243.3,281.9,302.8,\
                   306.9,323.3,326.0,343.8,345.4,362.1,366.7,555.3,773.1,\
                   779.9,806.7,814.9,819.4,863.1,869.0,914.5,1025.5,1069.6,\
                   1087.8,1099.1,1119.3,1149.2]
    Eb_mean_i=[31.5,32.7,34.1,51.5,55.6,56.3,60.5,66.6,78.1,84.4,85.7,90.7,\
                   91.5,97.0,97.5,102.7,104.1,165.6,241.3,243.7,253.3,256.3,\
                   257.9,273.8,275.9,292.6,333.9,350.5,357.4,361.7,369.4,380.8]
    # continuation of orig. alpha branch, beta- fork
    QHbetam('Fr-223','Ra-223',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xa*xb_a)
    # Fr-223 -> At-219
    if silent == 0: print "  Step 5b-2, alpha decay: Fr-223 -> At-219"
    lambda_s=lambda_s*br
    # continuation of orig. alpha branch, alpha fork
    QHalpha('Fr-223','At-219',lambda_eff,wa=xa*xa_a)
    # Ra-223 -> Rn-219
    if silent == 0: print "  Step 6, alpha decay: Ra-223 -> Rn-219"
    thalf_s=11.4377/yr2d # d (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Ra-223','Rn-219',lambda_eff)
    # Rn-219 -> Po-215
    if silent == 0: print "  Step 7, alpha decay: Rn-219 -> Po-215"
    thalf_s=3.96/yr2s # s (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Rn-219','Po-215',lambda_eff)
    # Po-215 -> Pb-211
    # a very low-probability beta- decay Po-215 -> At-215 is omitted
    if silent == 0: print "  Step 8, alpha decay: Po-215 -> Pb-211"
    thalf_s=1.781e-3/yr2s # s (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Po-215','Pb-211',lambda_eff)
    # Pb-211 -> Bi-211
    if silent == 0: print "  Step 9, beta- decay: Pb-211 -> Bi-211"
    thalf_s=36.164/yr2m # min (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[0.000186,1.3e-05,0.00017,0.0083,4.6e-05,0.00056,0.00022,0.0628,\
              0.0163,0.9132]
    Eb_endp_i=[96.,133.,171.,258.,264.,287.,416.,535.,962.,1367.]
    Eb_mean_i=[25.3,35.3,45.9,71.3,73.1,80.2,120.7,160.2,313.7,471.3]
    QHbetam('Pb-211','Bi-211',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # two decay branches for Bi-211
    # branching ratio from NuDat v.2.7b
    thalf_tot=2.14/yr2m # min, NUBASE2016
    lambda_tot=log(2.)/thalf_tot
    xb=0.00276
    xa=0.99724
    br=xa/xb
    # Bi-211 -> Po-211
    if silent == 0: print "  Step 10a, beta- decay: Bi-211 -> Po-211"
    lambda_s=lambda_tot/(1+br)
    # beta intensity and energy from NuDat v.2.7b
    Ib_i=[0.00276]
    Eb_endp_i=[574.]
    Eb_mean_i=[172.9]
    QHbetam('Bi-211','Po-211',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    #  Bi-211 -> Tl-207
    # An intermediate state Tl-207m may decay with very low probability via beta decay into
    # Pb-207; this branch is not treated as a beta decay here but lumped together with the
    # decay path through the ground state of Tl-207.
    if silent == 0: print "  Step 10b, alpha decay: Bi-211 -> Tl-207"
    lambda_s=lambda_s*br
    QHalpha('Bi-211','Tl-207',lambda_eff,wa=xa)
    # Po-211 -> Pb-207
    if silent == 0: print "  Step 11a, alpha decay: Po-211 -> Pb-207"
    thalf_s=516e-3/yr2s # s (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # weight xb is used b/c this continues the original beta- branch
    QHalpha('Po-211','Pb-207',lambda_eff,wa=xb)
    # Tl-207 -> Pb-207
    if silent == 0: print "  Step 11b, beta- decay: Tl-207 -> Pb-207"
    thalf_s=4.77/yr2m # min (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from NuDat v.2.7b; one level with very low
    # probability omitted
    Ib_i=[0.00271,0.99729]
    Eb_endp_i=[520.,1418.]
    Eb_mean_i=[155.0,492.5]
    # weight xa is used b/c this continues the original alpha branch
    QHbetam('Tl-207','Pb-207',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xa)
    Htot=EtoH_W(lambda_eff,Etot,'U-235')
    X_Ui=XisoU()
    if silent == 0:
        print "Total heat energy/power for U-235 decay series"
        print "  Q_gs=%.3f keV (%.3e J)\n  E_H (per atom)=%.6f keV (%.3e J)" % \
          (Qgstot,1e3*Qgstot*ec0,Etot,1e3*Etot*ec0)
        HtotU+=X_Ui[1]*Htot*u['U-235']/u['U']
        print "  Htot(U-235)=%.6e W/kg\tHtot(U)=%.6e W/kg" % (Htot,HtotU)
        print "  Isotope fractions: X_U234=%.5f%%   X_U235=%.5f%%   X_U238=%.5f%%" %  (X_Ui[0]*100,X_Ui[1]*100,X_Ui[2]*100)
        print "  Mean u_U: %.5f amu" % u['U']
    else:
        HtotU=X_Ui[1]*Htot*u['U-235']/u['U']


# ### $^{238}$U
# The other, much more abundant isotope $^{238}$U has a half-life close to the age of the Solar System, $T_{1/2}=4468$ My, and a similarly long and complex decay chain. It yields $^{206}$Pb as well as 8 atoms of $^{4}$He as final products. The isomeric transition (IT) of $^{234}$Pa was treated separately because of the slightly different $\beta^-$ energies, but the very low-probability $\beta^-$ branch of $^{218}$At and two similar branches of $^{210}$Pb to $^{206}$Hg and of $^{210}$Bi to $^{206}$Tl are not included. Energy is lost by neutrinos in the $\beta^-$ decays of $^{234}$Th (Luca, 2009b, 2010), $^{234}$Pa$^\mathrm{m}$ and $^{234}$Pa (Huang & Wang, 2011a-d), $^{218}$Po (Chisté & Bé, 2007a, 2010c), $^{214}$Pb (Chisté & Bé, 2010a,b), $^{214}$Bi (NuDat v.2.7$\beta$, Wu, 2009), $^{210}$Tl, $^{210}$Pb (NuDat v.2.7$\beta$, Basunia, 2014), and $^{210}$Bi (Chisté *et al.*, 2014). The mass of the excited isomer $^{234}$Pa$^\mathrm{m}$ is determined from the mass of the ground state of $^{234}$Pa and the energy of the $\gamma$ photon emitted upon decay to the ground level, which is determined to be 73.92 keV (Luca, 2010); this calculation is done on the fly with the function `keV2u`.

# Uranium-238 #################################################################
def calc_U238():
    """Decay energy and power of the U-238 series"""
    # Pa-234m is a long-lived Pa-234 excited isomeric state
    # mean element atomic mass of U is calculated from isotope ratios
    global u,Etot,Qgstot,HtotU,silent
    u={'Tl-210': 209.990072970,\
           'Pb-206': 205.974465124,'Pb-210': 209.984188301,\
           'Pb-214': 213.999803788,\
           'Bi-210': 209.984120156,'Bi-214': 213.998710938,\
           'Po-210': 209.982873601,'Po-214': 213.995201208,\
           'Po-218': 218.008971502,\
           'At-218': 218.008693735,\
           'Rn-222': 222.017576286,\
           'Ra-226': 226.025408455,\
           'Th-230': 230.033132358,'Th-234': 234.043599860,\
           'Pa-234': 234.043305615,'Pa-234m': 0,\
           'U-234': 234.040950370,'U-235': 235.043928190,\
           'U-238': 238.050786996,'U': 0}
    if silent == 0: print "decay chain: U-238 -> Pb-206"
    # U-238 -> Th-234
    if silent == 0: print "  Step 1, alpha decay: U-238 -> Th-234"
    thalf_U238=4.468e9 # yr (NUBASE2016)
    lambda_eff=log(2.)/thalf_U238
    QHalpha('U-238','Th-234',lambda_eff)
    #  Th-234 -> Pa-234m
    if silent == 0: print "  Step 2, beta- decay: Th-234 -> Pa-234m"
#   T1/2(daughters) << T1/2(U-238), hence lambda_U238 is rate-limiting for all
    thalf_s=24.1/yr2d # d (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    # beta intensities and energies from Luca (2010)
    Ib_i=[0.016,0.00016,0.065,0.141,0.778]
    Eb_endp_i=[85.,95.,105.,106.,198.]
    Eb_mean_i=[22.,25.,27.,28.,53.]
    # mass of excited isomer from ground state mass and excitation energy
    Eexc=73.92 # keV
    u['Pa-234m']=u['Pa-234']+keV2u(Eexc)
    QHbetam('Th-234','Pa-234m',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # two decay branches for Pa-234m (Huang & Wang, 2011)
    thalf_tot=1.159/yr2m # minutes
    lambda_tot=log(2.)/thalf_tot
    xb=0.9985
    xIT=0.0015
    br=xIT/xb
    # Pa-234m -> U-234
    if silent == 0: print "  Step 3a, beta- decay: Pa-234m -> U-234"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from Huang & Wang (2011)
    Ib_i=[0.0000389,0.000108,0.000452,0.000258,0.0000311,0.000146,0.000021,\
              0.000357,0.000024,0.000061,0.0000127,0.000249,0.0000231,\
              0.00032,0.000131,0.000092,0.000121,0.000046,0.01006,0.00945,\
              0.00049,0.97599]
    Eb_endp_i=[299.,332.,358.,394.,406.,460.,473.,488.,575.,602.,667.,677.,\
                   698.,715.,768.,834.,1032.,1095.,1224.,1459.,1483.,2269.]
    Eb_mean_i=[83.0,93.0,101.0,112.3,116.0,133.3,137.4,142.3,171.2,180.1,\
                   202.5,205.8,213.3,219.2,237.6,261.1,333.1,356.7,405.6,\
                   496.0,505.3,820.5]
    QHbetam('Pa-234m','U-234',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    # Pa-234m -> Pa-234 -> U-234
    if silent == 0:
        print "  Step 3b, isomeric transition, then beta- decay: Pa-234m -> Pa-234 -> U-234"
    lambda_s=lambda_s*br
    Qgs=Eexc
    Qgstot+=xIT*Qgs
    Etot+=xIT*Qgs
    # beta intensities and energies from Huang & Wang (2011)
    Ib_i=[0.0042,0.0021,0.00064,0.004,0.0014,0.00055,0.009,0.00112,0.00122,\
              0.0059,0.00044,0.0044,0.0035,0.0022,0.0021,0.0025,0.00029,\
              0.0017,0.0143,0.0041,0.00061,0.08,0.00129,0.028,0.0078,0.0116,\
              0.36,0.084,0.069,0.0095,0.0018,0.00035,0.007,0.0005,0.196,\
              0.00078,0.001,0.009,0.0021,0.0025,0.027,0.0012,0.0011,0.00109,\
              0.003,0.015,0.019,0.0069,0.08,0.015,0.05,0.031,0.025,0.004,\
              0.008,0.008,0.05]
    Eb_endp_i=[51.,79.,94.,126.,129.,158.,161.,175.,195.,214.,226.,236.,254.,\
                   267.,279.,313.,332.,351.,383.,402.,411.,412.,424.,433.,\
                   457.,458.,472.,472.,502.,542.,545.,576.,606.,613.,642.,\
                   647.,651.,658.,662.,693.,699.,709.,747.,883.,980.,1000.,\
                   1067.,1104.,1126.,1171.,1171.2,1206.,1227.,1232.,1247.,\
                   1346.,2052.]
    Eb_mean_i=[13.0,20.4,24.2,33.1,33.8,41.9,42.9,46.7,52.2,57.8,61.3,64.3,\
                   69.7,73.5,76.9,87.3,93.0,98.9,108.9,114.8,117.6,118.1,\
                   121.8,124.7,132.3,132.5,137.1,137.2,146.8,160.1,164.6,\
                   171.4,181.7,184.1,194.0,195.6,197.1,199.3,200.6,211.3,\
                   213.5,216.9,230.3,278.7,314.2,312.6,346.5,360.2,368.3,\
                   385.4,385.4,398.5,406.4,408.7,414.4,452.1,732.2]
    QHbetam('Pa-234','U-234',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xIT)
    # U-234 -> Th-230
    if silent == 0: print "  Step 4, alpha decay: U-234 -> Th-230"
    # save total heat energy released up to here for later use with U-234 power
    dEH234=Etot
    thalf_s=245.5e3 # yr (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('U-234','Th-230',lambda_s)
    # Th-230 -> Ra-226
    if silent == 0: print "  Step 5, alpha decay: Th-230 -> Ra-226"
    thalf_s=75.4e3 # yr (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Th-230','Ra-226',lambda_s)
    # Ra-226 -> Rn-222
    if silent == 0: print "  Step 6, alpha decay: Ra-226 -> Rn-222"
    thalf_s=1600. # yr (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Ra-226','Rn-222',lambda_s)
    # Rn-222 -> Po-218
    if silent == 0: print "  Step 7, alpha decay: Rn-222 -> Po-218"
    thalf_s=3.8215/yr2d # d (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Rn-222','Po-218',lambda_s)
    # two decay branches for Po-218
    # branching ratio from Chisté & Bé (2010)
    thalf_tot=3.098/yr2m # min (NUBASE2016)
    lambda_tot=log(2.)/thalf_tot
    xb=0.00022
    xa=0.99978
    br=xa/xb
    # Po-218 -> At-218
    if silent == 0: print "  Step 8a, beta- decay: Po-218 -> At-218"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from Chisté & Bé (2010)
    Ib_i=[0.00022]
    Eb_endp_i=[] # same as ground-state Q because of absence of gammas
    Eb_mean_i=[73.]
    QHbetam('Po-218','At-218',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    #  Po-218 -> Pb-214
    if silent == 0: print "  Step 8b, alpha decay: Po-218 -> Pb-214"
    lambda_s=lambda_s*br
    QHalpha('Po-218','Pb-214',lambda_s,wa=xa)
    # At-218 -> Bi-214
    # a low-probability beta- branch to Rn-218 is neglected
    if silent == 0: print "  Step 9a, alpha decay: At-218 -> Bi-214"
    lambda_s=1.5/yr2s # s (NUBASE2016)
    # weight xb is used b/c this continues the original beta- branch
    QHalpha('At-218','Bi-214',lambda_s,wa=xb)
    # Pb-214 -> Bi-214
    if silent == 0: print "  Step 9b, beta- decay: Pb-214 -> Bi-214"
    lambda_s=27.06/yr2m # min (NUBASE2016)
    # beta intensities and energies from Chisté & Bé (2010)
    Ib_i=[0.02762,0.000196,0.01047,0.4652,0.4109,0.092]
    Eb_endp_i=[180.,222.,485.,667.,724.,1019.]
    Eb_mean_i=[50.,62.,145.,207.,227.,337.]
    # weight xa is used b/c this continues the original alpha branch
    QHbetam('Pb-214','Bi-214',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xa)
    # two decay branches for Bi-214
    # branching ratio from NuDat v.2.7b
    thalf_tot=19.9/yr2m # min (NUBASE2016)
    lambda_tot=log(2.)/thalf_tot
    xb=0.99979
    xa=0.00021
    br=xa/xb
    # Bi-214 -> Po-214
    if silent == 0: print "  Step 10a, beta- decay: Bi-214 -> Po-214"
    lambda_s=lambda_tot/(1+br)
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[1e-05,1.4e-06,7.9e-06,9e-07,2.1e-05,7e-06,7.3e-05,0.00038,0.00043,\
              7e-05,0.000104,4e-05,0.000168,4e-06,0.00041,2.17e-05,1.1e-05,\
              0.0002225,1.4e-05,4.5e-05,0.000108,0.000114,0.00014,0.00032,\
              0.00033,0.00047,0.0005,0.00538,0.00267,0.00104,0.00292,0.00127,\
              0.00036,0.0015,1.8e-06,1e-06,0.00044,0.00123,0.00173,0.01244,\
              0.0278,0.00074,6e-05,0.00557,0.00196,0.056,0.00855,0.00444,\
              0.04345,0.00102,0.0245,0.01431,0.01177,0.01588,0.0814,0.1696,\
              0.00163,0.00125,0.1757,0.0061,0.0312,0.0089,0.0735,0.0058,0.191]
    Eb_endp_i=[86.,97.,110.,121.,127.,176.,188.,216.,256.,267.,270.,284.,291.,\
                   307.,329.,335.,341.,348.,351.,373.,376.,390.,400.,409.,\
                   443.,484.,500.,541.,551.,571.,575.,608.,639.,665.,708.,\
                   717.,725.,762.,765.,788.,822.,847.,909.,977.,1004.,1066.,\
                   1077.,1122.,1151.,1182.,1253.,1259.,1275.,1380.,1423.,\
                   1505.,1557.,1527.,1540.,1609.,1727.,1855.,1892.,2661.,3270.]
    Eb_mean_i=[22.3,25.1,28.6,31.7,33.5,47.1,50.6,58.7,70.5,73.7,74.7,78.9,\
                   81.1,86.0,92.8,94.8,96.6,98.7,99.4,106.5,107.6,111.8,115.2,\
                   118.1,129.1,142.5,147.9,161.8,164.9,171.9,173.3,184.4,\
                   195.4,204.5,219.5,222.8,225.7,238.9,239.9,248.2,260.9,\
                   269.8,293.0,318.2,328.4,352.1,356.5,373.7,385.1,396.8,\
                   424.6,427.1,433.5,474.9,492.0,525.3,529.7,534.0,539.4,\
                   567.2,615.4,668.1,683.7,1007.5,1268.8]
    QHbetam('Bi-214','Po-214',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xb)
    #  Bi-214 -> Tl-210
    if silent == 0: print "  Step 10b, alpha decay: Bi-214 -> Tl-210"
    lambda_s=lambda_s*br
    QHalpha('Bi-214','Tl-210',lambda_s,wa=xa)
    # Po-214 -> Pb-210
    if silent == 0: print "  Step 11a, alpha decay: Po-214 -> Pb-210"
    lambda_s=163.72e-6/yr2s # s (NUBASE2016)
    # weight xb is used b/c this continues the original beta- branch
    QHalpha('Po-214','Pb-210',lambda_s,wa=xb)
    # Tl-210 -> Pb-210
    if silent == 0: print "  Step 11b, beta- decay: Tl-210 -> Pb-210"
    lambda_s=1.3/yr2m # min (NUBASE2016)
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[0.02,0.07,0.24,0.1,0.1,0.3,0.2]
    Eb_endp_i=[1380.,1600.,1860.,2020.,2413.,4210.,4386.]
    Eb_mean_i=[477.,568.,674.,743.,877.1,1635.,1762.6]
    # weight xa is used b/c this continues the original alpha branch
    QHbetam('Tl-210','Pb-210',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i,wb=xa)
    # Pb-210 -> Bi-210
    # a very weak alpha decay branch to Hg-206 is neglected
    if silent == 0: print "  Step 12, beta- decay: Pb-210 -> Bi-210"
    lambda_s=22.2 # yr (NUBASE2016)
    # beta intensities and energies from NuDat v.2.7b
    Ib_i=[0.84,0.16]
    Eb_endp_i=[17.,63.5]
    Eb_mean_i=[4.16,16.16]
    QHbetam('Pb-210','Bi-210',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # Bi-210 -> Po-210
    # a very weak alpha decay branch to Tl-206 is neglected
    if silent == 0: print "  Step 13, beta- decay: Bi-210 -> Po-210"
    lambda_s=5.012/yr2d # d (NUBASE2016)
    # beta intensities and energies from Chisté et al. (2014)
    Ib_i=[1.]
    Eb_endp_i=[] # same as ground-state Q because of absence of gammas
    Eb_mean_i=[317.]
    QHbetam('Bi-210','Po-210',lambda_s,Ib_i,Eb_endp_i,Eb_mean_i)
    # Po-210 -> Pb-206
    if silent == 0: print "  Step 14, alpha decay: Po-210 -> Pb-206"
    thalf_s=138.376/yr2d # d (NUBASE2016)
    lambda_s=log(2.)/thalf_s
    QHalpha('Po-210','Pb-206',lambda_s)
    Htot=EtoH_W(lambda_eff,Etot,'U-238')
    # H(U-234) uses lambda_eff, because supply from U-238 is still the rate-limiting factor
    H234=EtoH_W(lambda_eff,Etot-dEH234,'U-234')
    X_Ui=XisoU()
    if silent == 0:
        print "Total heat energy/power for U-238 decay series"
        print "  Q_gs=%.3f keV (%.3e J)\n  E_H (per atom)=%.6f keV (%.3e J)" %           (Qgstot,1e3*Qgstot*ec0,Etot,1e3*Etot*ec0)
        # weighted mean with U-234, which releases a bit less heat
        HtotU+=(X_Ui[0]*H234*u['U-234']+X_Ui[2]*Htot*u['U-238'])/u['U']
        print "  Htot(U-238+U-234)=%.6e W/kg\tHtot(U)=%.6e W/kg" % (Htot,HtotU)
        print "  Isotope fractions: X_U234=%.5f%%   X_U235=%.5f%%   X_U238=%.5f%%" %             (X_Ui[0]*100,X_Ui[1]*100,X_Ui[2]*100)
        print "  Mean u_U: %.5f amu" % u['U']
    else:
        # weighted mean with U-234, which releases a bit less heat
        HtotU=(X_Ui[0]*H234*u['U-234']+X_Ui[2]*Htot*u['U-238'])/u['U']


# ## Main program (wrapper)
# The main program is merely a wrapper that reads user input and calls the corresponding function.
# 
# Initialize the total heat energy and $Q$ value and prompt the user for the nuclide to be calculated as well as isotope fractions or ratios as applicable:

Etot=0.; Qgstot=0.
silent=0
nuc=raw_input("Known nuclides: Al-26, K-40, Fe-60, Th-232, U-235, U-238\n"               "Enter nuclide for calculation: ")
if nuc == "Al-26":
    Xiso=raw_input("Fraction of isotope in element (0<=Xiso<=1; hit ENTER for default):")
    if Xiso != "": Xiso=float(Xiso)
    calc_Al26(Xiso)
elif nuc == "K-40":
    Xiso=raw_input("Fraction of isotope in element (0<=Xiso<=1; hit ENTER for default):")
    if Xiso != "": Xiso=float(Xiso)
    calc_K40(Xiso)
elif nuc == "Fe-60":
    Xiso=raw_input("Fraction of isotope in element (0<=Xiso<=1; hit ENTER for default):")
    if Xiso != "": Xiso=float(Xiso)
    calc_Fe60(Xiso)
elif nuc == "Th-232":
    calc_Th232()
elif nuc == "U-235":    
    buf=raw_input("Ratio r=U-238/U-235; hit ENTER for default (r=%.3f):" % rU85)
    if buf != "": rU85=float(buf)
    silent=1
    calc_U238()
    Etot=0.; Qgstot=0.
    silent=0
    calc_U235()
elif nuc == "U-238": 
    buf=raw_input("Ratio r=U-238/U-235; hit ENTER for default (r=%.3f):" % rU85)
    if buf != "": rU85=float(buf)
    silent=1
    calc_U235()
    Etot=0.; Qgstot=0.
    silent=0
    calc_U238()
else:
    print "Unknown nuclide."

# #### Version history
# - 1.0 (18/10/2017) - Updated publication info (final), added table of contents and internal links for better navigation (notebook only)
# - 1.0d (06/09/2017) - Corrected $E_H$ output for $^{26}$Al in J; the values of $E_H$ in keV and of $H$ are unaffected.
# - 1.0c (25/08/2017) - Updated publication info (no change to the code; pre-publication).
# - 1.0b (15/08/2017) - Update concerning importance of $^{60}$Fe (no change to the code; pre-publication).
# - 1.0a (19/07/2017) - First public release (pre-publication).
#

# ### References
# Abusaleem, K. (2014): Nuclear data sheets for $A=228$. *Nucl. Data Sheets 116*, 163-262, [doi:10.1016/j.nds.2014.01.002](http://dx.doi.org/10.1016/j.nds.2014.01.002).
# 
# Audi, G.; Kondev, F. G.; Wang, M.; Huang, W. J.; Naimi, S. (2017): The NUBASE2016 evaluation of nuclear properties. *Chin. Phys. C 41*(3), 030001, [doi: 10.1088/1674-1137/41/3/030001](http://dx.doi.org/10.1088/1674-1137/41/3/030001); https://www-nds.iaea.org/amdc/
# 
# Basunia, M.S. (2014): Nuclear data sheets for $A=210$. *Nucl. Data Sheets 121*, 561-694, [doi:10.1016/j.nds.2014.09.004](http://dx.doi.org/10.1016/j.nds.2014.09.004).
# 
# Basunia, M.S., Hurst, A.M. (2016): Nuclear data sheets for $A=26$.
#   *Nucl. Data Sheets 132*, 1-148, [doi:10.1016/j.nds.2016.04.001](http://dx.doi.org/10.1016/j.nds.2016.04.001).
#
# Boehnke, P.; McKeegan, K. D.; Stephan, T.; Steele, R. C. J.; Trappitsch, R.; Davis, A. M. (2017): The rise and fall of iron-60. *Meteorit. Planet. Sci. 52*(S1), [6243](https://www.hou.usra.edu/meetings/metsoc2017/pdf/6243.pdf), [doi:10.1111/maps.12934](http://dx.doi.org/10.1111/maps.12934)
#  
# Browne, E., Tuli, J.K. (2013a): Nuclear data sheets for $A=231$. *Nucl. Data Sheets 114*(6-7), 751-840, [doi:10.1016/j.nds.2013.05.002](http://dx.doi.org/10.1016/j.nds.2013.05.002).
# 
# Browne, E., Tuli, J.K. (2013b): Nuclear data sheets for $A=60$. *Nucl. Data Sheets 114*(12), 1849-2022, [doi:10.1016/j.nds.2013.11.002](http://dx.doi.org/10.1016/j.nds.2013.11.002).
# 
# Chen, J. (2017): Nuclear data sheets for $A=40$. *Nucl. Data Sheets 140*, 1-376, [doi:10.1016/j.nds.2017.02.001](http://dx.doi.org/10.1016/j.nds.2017.02.001)
# 
# Chisté, V., Bé, M.M. (2007): [$^{218}$Po - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Po-218_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Chisté, V., Bé, M.M. (2010a): [$^{214}$Pb - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Pb-214_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Chisté, V., Bé, M.M. (2010b): [${}_{82}^{214}\mathrm{Pb}_{132}$](http://www.nucleide.org/DDEP_WG/Nuclides/Pb-214_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Chisté, V., Bé, M.M. (2010c): [${}_{84}^{218}\mathrm{Po}_{134}$](http://www.nucleide.org/DDEP_WG/Nuclides/Po-218_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Chisté, V., Bé, M.M., Kellett, M.A. (2014a): [$^{210}$Bi - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Bi-210_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Chisté, V., Bé, M.M., Kellett, M.A. (2014b): [${}_{83}^{210}\mathrm{Bi}_{127}$](http://www.nucleide.org/DDEP_WG/Nuclides/Bi-210_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Goldmann, A., Brennecka, G., Noordman, J., Weyer, S., Wadhwa, M. (2015): The uranium isotopic composition of the Earth and the Solar System. *Geochim. Cosmochim. Acta 148*, 145-158, [doi:10.1016/j.gca.2014.09.008](http://dx.doi.org/10.1016/j.gca.2014.09.008).
# 
# Huang, X., Wang, B. (2009): [$^{223}$Fr - Comments on evaluation of the decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Fr-223_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2011a): [$^{234}$Pa - Comments on evaluation of the decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Pa-234_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2011b): [$^{234}$Pa$^\mathrm{m}$ - Comments on evaluation of the decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Pa-234m_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2011c): [${}_{91}^{234}\mathrm{Pa}_{143}$](http://www.nucleide.org/DDEP_WG/Nuclides/Pa-234_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2011d): [${}_{91}^{234}\mathrm{Pa}_{143}^\mathrm{m}$](http://www.nucleide.org/DDEP_WG/Nuclides/Pa-234m_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2012): [${}_{87}^{223}\mathrm{Fr}_{136}$](http://www.nucleide.org/DDEP_WG/Nuclides/Fr-223_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Huang, X., Wang, B. (2014): [${}_{92}^{235}\mathrm{U}_{143}$](http://www.nucleide.org/DDEP_WG/Nuclides/U-235_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Kondev, F.G., Lalkovski, S. (2011): Nuclear data sheets for $A=207$. *Nucl. Data Sheets 112*(3), 707-853, [doi:10.1016/j.nds.2011.02.002](http://dx.doi.org/10.1016/j.nds.2011.02.002).
#   
# Kondev, F., McCutchan, E., Singh, B., Tuli, J. (2016): Nuclear data sheets for $A=227$. *Nucl. Data Sheets 132*, 257-354, [doi:10.1016/j.nds.2016.01.002](http://dx.doi.org/10.1016/j.nds.2016.01.002).
#   
# Luca, A. (2009a): [$^{228}$Ra - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Ra-228_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Luca, A. (2009b): [$^{234}$Th - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Th-234_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Luca, A. (2010): [${}_{90}^{234}\mathrm{Th}_{144}$](http://www.nucleide.org/DDEP_WG/Nuclides/Th-234_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Luca, A. (2012): [${}_{88}^{228}\mathrm{Ra}_{140}$](http://www.nucleide.org/DDEP_WG/Nuclides/Ra-228_tables.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Meija, J., Coplen, T.B., Berglund, M., Brand, W.A., De Bièvre, P., Gröning, M., Holden, N.E., Irrgeher, J., Loss, R.D., Walczyk, T., Prohaska, T. (2016a): Atomic weights of the elements 2013 (IUPAC Technical Report). *Pure Appl. Chem. 88*(3), 265-291, [doi:10.1515/pac-2015-0305](http://dx.doi.org/10.1515/pac-2015-0305).
# 
# Meija, J., Coplen, T.B., Berglund, M., Brand, W.A.,De Bièvre, P., Gröning, M., Holden, N.E., Irrgeher, J., Loss, R.D., Walczyk, T., Prohaska, T. (2016b): Isotopic compositions of the elements 2013 (IUPAC Technical Report), *Pure Appl. Chem., 88*(3), 293-306, [doi:10.1515/pac-2015-0503](http://dx.doi.org/10.1515/pac-2015-0503).
# 
# Mohr, P.J., Newell, D.B., Taylor, B.N. (2016): CODATA recommended values of the fundamental physical constants: 2014. *J. Phys. Chem. Ref. Data 45*(4), 043102, [doi:10.1063/1.4954402](http://dx.doi.org/10.1063/1.4954402).
# 
# Mougeot, X. (2015): Reliability of usual assumptions in the calculation of $\beta$ and $\nu$ spectra. Phys. Rev. C 91(5), 055504, [doi: 10.1103/PhysRevC.91.055504](http://dx.doi.org/10.1103/PhysRevC.91.055504)
# 
# Naumenko, M.O., Mezger, K., Nägler, T.F., Villa, I.M. (2013): High precision determination of the terrestrial $^{40}$K abundance. *Geochim. Cosmochim. Acta 122*, 353-362, [doi:10.1016/j.gca.2013.08.019](http://dx.doi.org/10.1016/j.gca.2013.08.019).
# 
# Nichols, A.L. (2010): [$^{208}$Tl - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Tl-208_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Nichols, A.L. (2011a): [$^{212}$Bi - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Bi-212_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
#   
# Nichols, A.L. (2011b): [$^{212}$Pb - Comments on evaluation of decay data](http://www.nucleide.org/DDEP_WG/Nuclides/Pb-212_com.pdf). In *Table de Radionucléides*, CEA/LNHB, Gif-sur-Yvette, France.
# 
# Nichols, A.L. (2011c): [${}_{82}^{212}\mathrm{Pb}_{130}$](http://www.nucleide.org/DDEP_WG/Nuclides/Pb-212_tables.pdf). In *Table de Radionucléides*, LNHB/CEA, Gif-sur-Yvette, France.
# 
# Nichols, A.L. (2011d): [${}_{83}^{212}\mathrm{Bi}_{129}$](http://www.nucleide.org/DDEP_WG/Nuclides/Bi-212_tables.pdf). In *Table de Radionucléides*, LNHB/CEA, Gif-sur-Yvette, France.
# 
# Nichols, A.L. (2016): [${}_{81}^{208}\mathrm{Tl}_{127}$](http://www.nucleide.org/DDEP_WG/Nuclides/Tl-208_tables.pdf). In *Table de Radionucléides*, LNHB/CEA, Gif-sur-Yvette, France.
# 
# Singh, B., Abriola, D., Baglin, C., Demetriou, V., Johnson, T., McCutchan, E., Mukherjee, G., Singh, S., Sonzogni, A., Tuli, J. (2013): Nuclear data sheets for $A=211$. *Nucl. Data Sheets 114*(6-7), 661-749, [doi:10.1016/j.nds.2013.05.001](http://dx.doi.org/10.1016/j.nds.2013.05.001).
#
# Trappitsch, R.; Boehnke, P.; Stephan, T.; Telus, M.; Savina, M. R.; Pardo, O.; Davis, A. M.; Dauphas, N.; Huss, G. R. (2017): The life and death of iron-60. *Meteorit. Planet. Sci. 52*(S1), [6299](https://www.hou.usra.edu/meetings/metsoc2017/pdf/6299.pdf), [doi:10.1111/maps.12934](http://dx.doi.org/10.1111/maps.12934)
# 
# Wang, M.; Audi, G.; Kondev, F. G.; Huang, W. J.; Naimi, S.; Xu, X. (2017): The AME2016 atomic mass evaluation. (II). Tables, graphs and references. *Chin. Phys. C 41*(3), 030003, [doi: 10.1088/1674-1137/41/3/030003](http://dx.doi.org/10.1088/1674-1137/41/3/030003); https://www-nds.iaea.org/amdc/
# 
# Wu, S.-C. (2009): Nuclear data sheets for $A=214$. *Nucl. Data Sheets 110*(3), 681-748, [doi:10.1016/j.nds.2009.02.002](http://dx.doi.org/10.1016/j.nds.2009.02.002).

# ### Acknowledgments
# Shamsuzzoha Basunia (LBL), Jun Chen (NSCL, MSU), Xavier Mougeot (CEA Saclay), Balraj Singh (McMaster U), and Alejandro Sonzogni (BNL) kindly answered questions and gave advice concerning the evaluations for some nuclides.
