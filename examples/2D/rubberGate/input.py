# %% Input Parameters

def getParam(path):

    # Metafor and PFEM solvers
    
    param = dict()
    param['inputS'] = 'input_meta'
    param['inputF'] = path+'/input_pfem.lua'
    
    # Algorithm parameters

    param['RBF'] = 'C0'
    param['radius'] = 1
    param['interp'] = 'RBF'
    param['algo'] = 'IQN_MVJ'
    param['omega'] = 0.5
    param['maxIt'] = 25
    param['tol'] = 1e-8

    # Time Parameters

    param['dt'] = 5e-4
    param['dtWrite'] = 1e-3
    param['tEnd'] = 0.4

    return param