import time
import numpy as np
from numba import njit, prange
from spins2 import functions

def iteration3(latt, X_s, Y_s, J0, J1, Ja, J_1, J_a, Aa, Ab, val, nequilibrium, nworks):
    t0 = time.time()
    Ns = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    for i in range(nequilibrium):
        laRn = functions.NormalrandNNN(2, 2, 2, Y_s, X_s)
        randvals = np.random.rand(2, 2, 2, Y_s, X_s)
        latZ = energy_A(latt, Aa, Ab)
        laRZ = energy_A(laRn, Aa, Ab)
        E0   = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, J0, J1, Ja, J_1, J_a, val)
    for i in range(nworks):
        laRn = functions.NormalrandNNN(2, 2, 2, Y_s, X_s)
        randvals = np.random.rand(2, 2, 2, Y_s, X_s)
        latZ = energy_A(latt, Aa, Ab)
        laRZ = energy_A(laRn, Aa, Ab)
        E0   = update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, J0, J1, Ja, J_1, J_a, val)
        Ew[i] = E0 / 2.0
        Ns[i] = functions.Average(np.sign(latt[0,0,0,:,:,2])), functions.Average(np.sign(latt[0,1,0,:,:,2])), functions.Average(np.sign(latt[0,0,1,:,:,2])), functions.Average(np.sign(latt[0,1,1,:,:,2])),\
                functions.Average(np.sign(latt[1,0,0,:,:,2])), functions.Average(np.sign(latt[1,1,0,:,:,2])), functions.Average(np.sign(latt[1,0,1,:,:,2])), functions.Average(np.sign(latt[1,1,1,:,:,2]))
    t = time.time() - t0
    return t, Ns, Ew

def energy_A(latt, Aa, Ab):
    latt_2 = latt ** 2
    if Aa < 0:
        if Aa == Ab:
            L_x_2 = latt_2[:,:,:,:,:,0]
            return ( -Aa * L_x_2 )
        else:
            L_y_2 = latt_2[:,:,:,:,:,1]
            L_z_2 = latt_2[:,:,:,:,:,2]
            return ( Aa * L_y_2 + Ab * L_z_2 )
    else:
        if Aa == Ab:
            L_z_2 = latt_2[:,:,:,:,:,2]
            return ( -Aa * L_z_2 )
        else:
            L_x_2 = latt_2[:,:,:,:,:,0]
            L_y_2 = latt_2[:,:,:,:,:,1]
            return ( Aa * L_x_2 + Ab * L_y_2 )

@njit(cache=True, parallel=True)
def update3(latt, latZ, laRn, laRZ, randvals, X_s, Y_s, J0, J1, Ja, J_1, J_a, val):
    nn_sum = 0
    for h in prange(2):
        for g in range(2):
            for f in range(2):
                for j in range(Y_s):
                    for i in range(X_s):
                        ipp = (i + 1) if (i + 1) < X_s else 0
                        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                        jpp = (j + 1) if (j + 1) < Y_s else 0
                        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
                        ho = 1 - h
                        go = 1 - g
                        fo = 1 - f
                        hx0 = inn if g == 0 else ipp
                        if f == 0:
                            vy0 = jnn
                            vx0 = inn if g == 0 else i
                        else:
                            vy0 = jpp
                            vx0 = i   if g == 0 else ipp
                        if h == 0:
                            x_0 = inn if g == 0 else i
                            if f == 0:
                                gp = go
                                y_0 = j
                                y_1 = jnn
                                x_1 = inn if g == 0 else i
                                y_2 = j
                            else:
                                gp  = g
                                y_0 = jpp
                                y_1 = j
                                x_1 = i
                                y_2 = jpp
                        else:
                            x_0 = i   if g == 0 else ipp
                            if f == 0:
                                gp  = g
                                y_0 = jnn
                                y_1 = j
                                x_1 = i
                                y_2 = jnn
                            else:
                                gp = go
                                y_0 = j
                                y_1 = jpp
                                x_1 = i   if g == 0 else ipp
                                y_2 = j

                        energy  = ( -J0 * ( latt[ho,g ,f ,j  ,i  ,0] + latt[ho,go,f ,j  ,x_0,0] +
                                            latt[ho,gp,fo,y_0,i  ,0] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,0] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,0] + latt[ho,go,fo,y_2,hx0,0] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,0] + latt[h ,g ,fo,vy0,i  ,0] +
                                            latt[h ,go,fo,j  ,vx0,0] + latt[h ,go,fo,vy0,vx0,0] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,0] + latt[h ,go,f ,j  ,hx0,0] )
                                   ) * latt[h,g,f,j,i,0] + (
                                    -J0 * ( latt[ho,g ,f ,j  ,i  ,1] + latt[ho,go,f ,j  ,x_0,1] +
                                            latt[ho,gp,fo,y_0,i  ,1] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,1] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,1] + latt[ho,go,fo,y_2,hx0,1] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,1] + latt[h ,g ,fo,vy0,i  ,1] +
                                            latt[h ,go,fo,j  ,vx0,1] + latt[h ,go,fo,vy0,vx0,1] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,1] + latt[h ,go,f ,j  ,hx0,1] )
                                   ) * latt[h,g,f,j,i,1] + (
                                    -J0 * ( latt[ho,g ,f ,j  ,i  ,2] + latt[ho,go,f ,j  ,x_0,2] +
                                            latt[ho,gp,fo,y_0,i  ,2] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,2] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,2] + latt[ho,go,fo,y_2,hx0,2] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,2] + latt[h ,g ,fo,vy0,i  ,2] +
                                            latt[h ,go,fo,j  ,vx0,2] + latt[h ,go,fo,vy0,vx0,2] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,2] + latt[h ,go,f ,j  ,hx0,2] )
                                   ) * latt[h,g,f,j,i,2]

                        Erandn  = ( -J0 * ( latt[ho,g ,f ,j  ,i  ,0] + latt[ho,go,f ,j  ,x_0,0] +
                                            latt[ho,gp,fo,y_0,i  ,0] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,0] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,0] + latt[ho,go,fo,y_2,hx0,0] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,0] + latt[h ,g ,fo,vy0,i  ,0] +
                                            latt[h ,go,fo,j  ,vx0,0] + latt[h ,go,fo,vy0,vx0,0] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,0] + latt[h ,go,f ,j  ,hx0,0] )
                                   ) * laRn[h,g,f,j,i,0] + (
                                    -J0 * ( latt[ho,g ,f ,j  ,i  ,1] + latt[ho,go,f ,j  ,x_0,1] +
                                            latt[ho,gp,fo,y_0,i  ,1] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,1] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,1] + latt[ho,go,fo,y_2,hx0,1] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,1] + latt[h ,g ,fo,vy0,i  ,1] +
                                            latt[h ,go,fo,j  ,vx0,1] + latt[h ,go,fo,vy0,vx0,1] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,1] + latt[h ,go,f ,j  ,hx0,1] )
                                   ) * laRn[h,g,f,j,i,1] + (
                                    -J0 * ( latt[ho,g ,f ,j  ,i  ,2] + latt[ho,go,f ,j  ,x_0,2] +
                                            latt[ho,gp,fo,y_0,i  ,2] ) -
                                     J1 *   latt[ho,gp,fo,y_1,x_1,2] -
                                     J_1* ( latt[ho,go,fo,y_2,i  ,2] + latt[ho,go,fo,y_2,hx0,2] ) -
                                     Ja * ( latt[h ,g ,fo,j  ,i  ,2] + latt[h ,g ,fo,vy0,i  ,2] +
                                            latt[h ,go,fo,j  ,vx0,2] + latt[h ,go,fo,vy0,vx0,2] ) -
                                     J_a* ( latt[h ,go,f ,j  ,i  ,2] + latt[h ,go,f ,j  ,hx0,2] )
                                   ) * laRn[h,g,f,j,i,2]

                        ez = latZ[h,g,f,j,i]
                        Ez = laRZ[h,g,f,j,i]
                        if val == 0:
                            if energy < 0:
                                pass
                                DeltaE = ez + energy - Ez - Erandn
                            else:
                                latt[h,g,f,j,i] *= -1
                                DeltaE = ez - energy - Ez - Erandn
                            if DeltaE < 0:
                                pass
                            else:
                                latt[h,g,f,j,i] = laRn[h,g,f,j,i]
                        else:
                            if energy < 0:
                                if randvals[h,g,f,j,i] < np.exp( 2.0 * val * energy ):
                                    latt[h,g,f,j,i] *= -1
                                    DeltaE = ez - energy - Ez - Erandn
                                else:
                                    DeltaE = ez + energy - Ez - Erandn
                            else:
                                latt[h,g,f,j,i] *= -1
                                DeltaE = ez - energy - Ez - Erandn
                            if DeltaE < 0:
                                if randvals[h,g,f,j,i] < np.exp( val * DeltaE ):
                                    latt[h,g,f,j,i] = laRn[h,g,f,j,i]
                            else:
                                latt[h,g,f,j,i] = laRn[h,g,f,j,i]

                        nn_sum += ( -J0 * ( np.sign(latt[ho,g ,f ,j  ,i  ,2]) + np.sign(latt[ho,go,f ,j  ,x_0,2]) +
                                            np.sign(latt[ho,gp,fo,y_0,i  ,2]) ) -
                                     J1 *   np.sign(latt[ho,gp,fo,y_1,x_1,2]) -
                                     J_1* ( np.sign(latt[ho,go,fo,y_2,i  ,2]) + np.sign(latt[ho,go,fo,y_2,hx0,2]) ) -
                                     Ja * ( np.sign(latt[h ,g ,fo,j  ,i  ,2]) + np.sign(latt[h ,g ,fo,vy0,i  ,2]) +
                                            np.sign(latt[h ,go,fo,j  ,vx0,2]) + np.sign(latt[h ,go,fo,vy0,vx0,2]) ) -
                                     J_a* ( np.sign(latt[h ,go,f ,j  ,i  ,2]) + np.sign(latt[h ,go,f ,j  ,hx0,2]) )
                                   ) * np.sign(latt[h,g,f,j,i,2])

    return nn_sum
