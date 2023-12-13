from multiprocessing.sharedctypes import Value
import numpy as np
import matplotlib.pyplot as plt
from pyro import param
from scipy.stats.qmc import Sobol, scale
import math
import torch



################################################################################################
######################################## UQ Simple beam example ################################
def  UQ_Simple_beam_F(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):
    """_summary_

    Args:
        parameters (_type_, optional): For evaluation, you can give parameters and get the values. Defaults to None.
        n (int, optional): defines the number of data needed. Defaults to 100.

    Returns:
        _type_: if paramters are given, it returns y, otherwise it returns both X and y
    """

    if random_state is not None:
        np.random.seed(random_state)

    dx = 5
    l_bound = [.1,.2,4,5e+9,1e+4]
    u_bound = [.2,.4,6,35e+9,1.4e+4]

    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    
    # Model with five input parameters  X= [b h L E p]
    #         b:   beam width
    #         h:   beam height
    #         L:   beam span
    #         E:   Young's modulus
    #         p:   uniform load
    # Output:  V = (5/32)*pL^4/(E*b*h^3)
    # See also: UQ_EXAMPLE_PCE_03_SIMPLYSUPPORTEDBEAM
    # This is the output


    if fidelity == 0:
        # mean = 1.2e+04  # Mean of the Gaussian distribution
        # stdd= 1e+03  # Variance of the Gaussian distribution
        # X[..., 4] = np.random.normal(mean, stdd,X[..., 4].shape)
        X[..., 0]=0.15
        X[..., 1]=0.3
        X[..., 2]=5
        X[..., 3]=30e+9
        X[..., 4]=1.2e+04

        y = (5/32)*(X[..., 4]*X[..., 2]**4)/(X[..., 3]*X[..., 0]*X[..., 1]**3)
        
    elif fidelity == 1:
        y = (5/32)*(X[..., 4]*X[..., 2]**4)/(X[..., 3]*X[..., 0]*X[..., 1]**3)
    # elif fidelity == 3:
    #     y =1/(X[..., 0] * X[..., 1]**2  +1)

    else:
        raise ValueError('only 3 fidelities of 0,1,2 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D_Inverse for Calibration ####################################
def  UQ_Simple_beam(X = None,
    n={'0': 50, '1': 100},
    noise_std={'0': 0.0, '1': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2'] and num > 0:
                X, y =  UQ_Simple_beam_F(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
################################################################################################
################################################################################################
################################## Calibration_1D Poly #########################################
def Calibration_1D_Inverse(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):
    """_summary_

    Args:
        parameters (_type_, optional): For evaluation, you can give parameters and get the values. Defaults to None.
        n (int, optional): defines the number of data needed. Defaults to 100.

    Returns:
        _type_: if paramters are given, it returns y, otherwise it returns both X and y
    """

    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound = [-.5, -1]
    u_bound = [.5, 2]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)

    # This is the output
    if fidelity == 0:
        X[..., 0]=.1
        y = 1/(X[..., 0] * X[..., 1]**3 + X[..., 1]**2 + X[..., 1] +1)
    elif fidelity == 1:
        y = 1/(X[..., 0] * X[..., 1]**3 + X[..., 1]**2 + X[..., 1] +1)
    elif fidelity == 2:
        y =1/(X[..., 0] * X[..., 1]**2 + X[..., 1] +1)
    # elif fidelity == 3:
    #     y =1/(X[..., 0] * X[..., 1]**2  +1)

    else:
        raise ValueError('only 3 fidelities of 0,1,2 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D_Inverse for Calibration ####################################
def Calibration_1D_poly_Invers(X = None,
    n={'0': 50, '1': 100, '2': 100},
    noise_std={'0': 0.0, '1': 0.0, '2': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2'] and num > 0:
                X, y = Calibration_1D_Inverse(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    


###############################################################################################
################################## Calibration_1D Poly #########################################
def Calibration_1D(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):


    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound = [-2, -2]
    u_bound = [2, 3]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    # Wp = X[..., 9]
    # This is the output

    if fidelity == 0:
        X[..., 0]=.1
        y = X[..., 0] * X[..., 1]**3 + X[..., 1]**2 + X[..., 1] +1
    elif fidelity == 1:
    # This is the output
        y =X[..., 0] * X[..., 1]**3 + X[..., 1]**2 + X[..., 1] +1

    elif fidelity == 2:
    # This is level 2 in Tammers paper
        y =X[..., 0] * X[..., 1]**3 + X[..., 1]**2 +1

    else:
        raise ValueError('only 3 fidelities of 0,1,2 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D for Calibration ####################################
def Calibration_1D_poly(X = None,
    n={'0': 50, '1': 100, '2': 100, '3': 100},
    noise_std={'0': 0.0, '1': 0.0, '2': 0.0, '3': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2'] and num > 0:
                X, y = Calibration_1D(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(Calibration_1D(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
################################## Calibration_1D Poly #########################################
def Calibration_3_sources_sin(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):

    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound = [0, -1]
    u_bound = [7, 1]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    # Wp = X[..., 9]
    # This is the output

    if fidelity == 0:
        X[..., 0]=1
        y = np.sin(X[..., 0]*X[..., 1]) + np.sin(2*X[..., 0]*X[..., 1])
    elif fidelity == 1:
    # This is the output
        y =np.sin(X[..., 0]*X[..., 1])

    elif fidelity == 2:
    # This is level 2 in Tammers paper
        y =np.sin(X[..., 0]*X[..., 1]) + np.sin(2*X[..., 0]*X[..., 1])

    else:
        raise ValueError('only 3 fidelities of 0,1,2 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D for Calibration ####################################
def Calibration_1D_3_sources_sin(X = None,
    n={'0': 50, '1': 100, '2': 100, '3': 100},
    noise_std={'0': 0.0, '1': 0.0, '2': 0.0, '3': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2'] and num > 0:
                X, y = Calibration_3_sources_sin(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
################################## Calibration_1D_poly_2_Sources #########################################
def Calibration_1D_2_Sources(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):

    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound = [-2, -2]
    u_bound = [2, 3]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    # Wp = X[..., 9]
    # This is the output

    if fidelity == 0:
        mean = 0  # Mean of the Gaussian distribution
        stdd= .1  # Variance of the Gaussian distribution
        X[..., 0] = np.random.normal(mean, stdd,X[..., 0].shape)

        # X[..., 0]=1
        
        y = X[..., 0] * X[..., 1]**3 +X[..., 1]**2 +1
    elif fidelity == 1:
    # This is the output
        y =X[..., 0] * X[..., 1]**3 +X[..., 1]**2 +1
    else:
        raise ValueError('only 3 fidelities of 0,1,2 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D for Calibration ####################################
def Calibration_1D_poly_2_Sources(X = None,
    n={'0': 50, '1': 100},
    noise_std={'0': 0.0, '1': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1'] and num > 0:
                X, y = Calibration_1D_2_Sources(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))

################################# Multi-fidelity-1D for Calibration ####################################
def Calibration_1D_cos(X = None,
    n={'0': 50, '1': 100},
    noise_std={'0': 0.0, '1': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1'] and num > 0:
                X, y =Calibration_f_cos(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
################################## Calibration Cos() #########################################
def Calibration_f_cos(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):

    if random_state is not None:
        np.random.seed(random_state)

    dx = 3
    l_bound =[-2,0,-1]
    u_bound = [2,10,1]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    if fidelity == 0:
        X[..., 0]=1
        X[..., 1]=.5
        # y = X[..., 0]*np.cos(X[..., 1]*X[..., 2]) + 1*np.cos(2*X[..., 1]*X[..., 2])
        
        y = 2*X[..., 0]+np.cos(X[..., 1]*X[..., 2]) + 1*np.cos(10*X[..., 1]*X[..., 2])

    elif fidelity == 1:
        # y = X[..., 0]*np.cos(X[..., 1]*X[..., 2])

        y =  2*X[..., 0] +np.cos(X[..., 1]*X[..., 2])

    else:
        raise ValueError('only 2 fidelities of 0,1 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y

################################## Calibration SIN() #########################################
def Calibration_sin_M(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):

    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound =[.8, -2.5]
    u_bound = [1.6, 2.5]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    if fidelity == 0:
        X[..., 0]=1.2
        # y = np.sin(X[..., 0]*X[..., 1]) + np.sin(10*X[..., 0]*X[..., 1])
        y = np.sin(X[..., 0] * X[..., 1]) + 0.1 * X[..., 1] 

    elif fidelity == 1:
    # This is the output
        y =np.sin(X[..., 0] * X[..., 1]) 

    else:
        raise ValueError('only 2 fidelities of 0,1 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]

    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D for 2 Calibration Parameters####################################
def Calibration_1D_sin_koh_example(X = None,
    n={'0': 50, '1': 100},
    noise_std={'0': 0.0, '1': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1'] and num > 0:
                X, y =Calibration_sin_M(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
################################## Calibration SIN() #########################################
def Calibration_f_sin(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):


    if random_state is not None:
        np.random.seed(random_state)

    dx = 2
    l_bound =[-5, 0]
    u_bound = [15, 1]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    if fidelity == 0:
        X[..., 0]=2
        # y = np.sin(X[..., 0]*X[..., 1]) + np.sin(10*X[..., 0]*X[..., 1])
        y = np.sin(X[..., 0]*X[..., 1]) + np.sin(5*X[..., 0]*X[..., 1])

    elif fidelity == 1:
    # This is the output
        y =np.sin(X[..., 0]*X[..., 1])

    else:
        raise ValueError('only 2 fidelities of 0,1 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Multi-fidelity-1D for 2 Calibration Parameters####################################
def Calibration_1D_sin(X = None,
    n={'0': 50, '1': 100},
    noise_std={'0': 0.0, '1': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1'] and num > 0:
                X, y =Calibration_f_sin(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(UQ_Simple_beam_F(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    
################################## Calibration Wing #########################################
################################## Wing #########################################
def Calibration_f_wing(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):


    if random_state is not None:
        np.random.seed(random_state)

    dx = 10
    # l_bound = [150, 220, 6, -10, 16, 0.5, 0.08, 2.5, 1700, 0.025]
    # u_bound = [200, 300, 10, 10, 45, 1, 0.18, 6, 2500, 0.08]
    l_bound = [150, 220, 6, -10, 16, 0.7, 0.08, 2, 1700, 0.025]
    u_bound = [200, 300, 10, 10, 45, 0.9, 0.20, 3.5, 2500, 0.08]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)
    Sw = X[..., 0]
    Wfw = X[..., 1]
    A = X[..., 2]
    Gama = X[..., 3] * (np.pi/180.0)
    q = X[..., 4]
    lamb = X[..., 5]
    tc = X[..., 6]
    Nz = X[..., 7]
    Wdg = X[..., 8]
    Wp = X[..., 9]
    # This is the output

    if fidelity == 0:
        X[..., 4]=40
        X[..., 5]=0.85
        X[..., 6]=0.17
        X[..., 7]=3
        y = 0.036 * Sw**0.758 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.6 * \
            q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3) *\
            (Nz * Wdg) ** 0.49 + Sw * Wp
    elif fidelity == 1:
    # This is the output
        y = 0.036 * Sw**0.758 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.6 * \
            q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3)\
            * (Nz * Wdg) ** 0.49 + 1 * Wp 

    elif fidelity == 2:
    # This is level 2 in Tammers paper
        y = 0.036 * Sw**0.8 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.6 * \
            q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3)\
            * (Nz * Wdg) ** 0.49 + 1 * Wp

    # elif fidelity == 2:
    # # This is level 2 in Tammers paper
    #     y = 0.006 * Sw**0.8 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.1 * \
    #         q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3)\
    #         * (Nz * Wdg) ** 0.49 + 1 * Wp

    elif fidelity == 3:
    # This is level 2 in Tammers paper
        y = 0.036 * Sw**0.9 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.6 * \
            q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3)\
            * (Nz * Wdg) ** 0.49 + 0 * Wp
    # elif fidelity == 3:
    # This is level 2 in Tammers paper
        # y = 0.01 * Sw**0.9 * Wfw**0.0035 * (A/(np.cos(Gama)) ** 2) ** 0.6 * \
        #     q**0.006*lamb**0.04 * ((100 * tc)/(np.cos(Gama)))**(-0.3)\
        #     * (Nz * Wdg) ** 0.49 + 0 * Wp
    else:
        raise ValueError('only 4 fidelities of 0,1,2,3 have been implemented ')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y




################################# Multi-fidelity ####################################
def Calibration_wing(X = None,
    n={'0': 50, '1': 100, '2': 100, '3': 100},
    noise_std={'0': 0.0, '1': 0.0, '2': 0.0, '3': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2','3'] and num > 0:
                X, y = Calibration_f_wing(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1, l2 or l3')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(Calibration_f_wing(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
    


################################## borehole #########################################
def borehole(n=100, X = None, 
    fidelity = 0,noise_std = 0.0, random_state = None, shuffle = True):
    if random_state is not None:
        np.random.seed(random_state)

    dx = 8
    l_bound = [100, 990, 700, 100, .05,6000, 10, 1000]
    u_bound = [1000, 1110, 820, 10000, .15, 12000,500, 2000]
    out_flag = 0
    if X is None:
        sobolset = Sobol(d=dx, seed = random_state)
        X = sobolset.random(2 ** (np.log2(n) + 1).astype(int))[:n, :]
        X = scale(X, l_bounds=l_bound, u_bounds=u_bound)
        out_flag = 1
    if type(X) != np.ndarray:
        X = np.array(X)

    Tu, Hu, Hl, r, rw, Kw,Tl, L = [X[:, i] for i in range(8)]
    # This is the output

    if fidelity == 0:
        Numer = 2*np.pi*Tu
        Tl=250
        L=1500
        X[:, 6]=Tl
        X[:, 7]=L
        y = (Numer*(Hu-Hl))/(np.log(r/rw)*(1+((2*L*Tu)/(np.log(r/rw)*(rw**2)*Kw))+(Tu/Tl)))
    elif fidelity == 1:
    # This is the output
        Numer = 2*np.pi*Tu
        y = (Numer*(Hu-.8*Hl))/(np.log(r/rw)*(1+((1*L*Tu)/(np.log(r/rw)*(rw**2)*Kw))+(Tu/Tl)))

    elif fidelity == 2:
        Numer = 2*np.pi*Tu
    # This is level 2 in Tammers paper
        y = (Numer*(Hu-Hl))/(np.log(r/rw)*(1+((8*L*Tu)/(np.log(r/rw)*(rw**2)*Kw))+.75*(Tu/Tl)))
    else:
        raise ValueError('only 3 fidelities of 0,1, and 2 have been implemented')

    if X is None:
        if shuffle:
            index = np.random.randint(0, len(y), size = len(y))
            X = X[index,...]
            y = y[index]


    if noise_std > 0.0:
        if out_flag == 1:
            return X, y + np.random.randn(*y.shape) * noise_std
        else:
            return y       
    else:
        if out_flag == 1:
            return X, y
        else:
            return y


################################# Calibration_borehole ####################################
def Calibration_borehole(X = None,
    n={'0': 50, '1': 100, '2': 100},
    noise_std={'0': 0.0, '1': 0.0, '2': 0.0},
    random_state = None, shuffle = True):
    if X is None:
        X_list = []
        y_list = []
        for level, num in n.items():
            if level  in ['0','1','2'] and num > 0:
                X, y = borehole(n=num, fidelity = int(level), 
                    noise_std= noise_std[level], random_state = random_state)
                X = np.hstack([X, np.ones(num).reshape(-1, 1) * float(level)])
                X_list.append(X)
                y_list.append(y)
            else:
                raise ValueError('Wrong label, should be h, l1 or l2')
        return np.vstack([*X_list]), np.hstack(y_list)
    else:
        fidelity = [i for i in n.keys()]
        y_list = []
        if type(X) == np.ndarray:
            X = torch.tensor(X)
        for f in fidelity:
            # Find the index for each fidelity then call the wing
            index = [i[0] for i in torch.argwhere(X[...,-1]== int(f))]
            y_list.append(borehole(X=X[index, 0:-1], fidelity=int(f),  
                noise_std= noise_std[f]))
        return torch.tensor(np.hstack(y_list))
#####################################################################################################


