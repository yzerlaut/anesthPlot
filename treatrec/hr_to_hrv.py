


def build_hrv_limits(spec='horse'):
    """
    return a dico containing HRV limits (VLF, LF, HF)
    input : spec in ['horse', 'man']
    """
    dico = {}
    if spec == 'man':
        # Guidelines. Circulation, 93(5):1043–65, mar 1996.
        vals = [0.001, 0.04, 0.15, 0.4]
    elif spec == 'horse':
        # Ishii et al J. Auton. Nerv. Syst., 8(1):43–8, 1996.
        vals = [0.001, 0.01, 0.07, 0.6]
    else:
        print('spec should be man or horse')
        return dico
    for i, band in enumerate(['VLF', 'LF', 'HF']):
        lims = (vals[i], vals[i+1])
        dico[band] = lims
    return dico

hrv_dico = build_hrv_limits('horse')

#%%
try:
    ekg_df
except:
    print('RR series are not extracted')
    print('run wave_to_hr to build one')
    
#%%
