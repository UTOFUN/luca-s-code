# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:51:36 2018

@author: admin
"""

from shapely.geometry import Polygon,Point
import polyline
import pandas as pd
import re
import numpy as np


def boundary():
    df = pd.read_csv(r'C:\Users\admin\Downloads\web.neighborhood_boundary.csv')
    df.boundary = df.boundary.apply(lambda x:x.replace('\\\\','\\'))
    # for some string it does not work, manually process, add r to original string
    
    df['polygon'] = df.boundary.apply(lambda x:Polygon(polyline.decode(x)))
    return tuple(df.neighborhood_name),tuple(df.polygon)

n_name, n_polygon = boundary()

# latitude first, longitude after
def assign_neighborhood(latitude,longitude,neighborhood_name = n_name ,polygon=n_polygon):
    point=Point(float(latitude),float(longitude))
    for i in range(163):
        if polygon[i].contains(point):
            return(neighborhood_name[i])
    return None



    
def polygon2string(list_):
    string='POLYGON(('
    if list_[0]
    list_+=[list_[0]]
    for i in list_:
        string+=str(i[0])+' '+str(i[1])+','
    string=string[:-1]
    string+='))'
    return string

import csv
df = pd.read_csv(r'C:\Users\admin\Downloads\boundary code.txt')
df.code = df.code.apply(lambda x:x.replace('\\\\','\\'))
df.loc[21].code=r'ajpwFzhh`MhBeMf@w@R{@d[_L~NkCsEsO{EzAcA}Dm@R_@aBw@?y@m@_AkFsBiCd@eAr@q@jGiCbG}@nQ{Ax@bGv@GL`@hDXlAg@x@^?hAzIEBzAfGOBzAzFA~Qj@QpBvXyBdIvRp@k@rDbI|BgFjGh[|MuEpCo@Ga@fDs@nD]xFH@b@lJPfBYvCaAl@U?dE_@rDgAjFqBjF_GbJqCzGdTxBdMg@?x\\\\lDRAUtC]FbA??^dGNhO\\\\vAT]dEeBW{Au@aF}FcFtX{AkBsEcB{BoAyEiDqMgFiAbJaJf_@[nDEhDu@KFbDbAnAVlBoBiCgCkB{@Y`EzFoBjB}EwCcBi@sGqFgEbVca@|L}DOeOnCuB}G[k@[GYcA_G~FkAXkFvEqRnMmJpEmAiKkC{Rx@}B}@UQ[QgAQPsEeK_@iDaL_[|@}CgA\\\\{CyKX}@yA}I_@aE}N}~@vAdBe@oDeAqCCuCn@D'
df.loc[27].code=r'on_wF|yaaMVuAKwCHEQsAp@YIm@s@RYkCz@SWgCe@MzBcAAMdA[N_@n@Sf@Eh@g@VGh@c@N?BRXhDhAa@[}CAe@FSj@KnCeA~DqBr@Uj@k@xB~GbNcE{DeQ~BeA`EvQvDmAtk@e[cPcWhWmLoHuRuB_EeIiKZaBEmAQk@{@MrCmGVyCcCiJvF_IDCVKBAlEiEp@cAq@{Aq@cMTQ`AkB|IwGY]pD{Aj@GdAR\\\\g@VAlAi@n@wA?PMTxCxAb@LLVb@?NH@r@`@n@Dx@NF^Cl@n@Bx@\\\\|@|@bAl@VfBDZQN_@Aq@Qa@Lk@Cq@U_AHwCHc@HAXD@VHLZAXZFfAn@z@PtBn@@\\\\^JJ`@JH\\\\Fb@EX`@P@n@QGcBbAeAA[[k@Za@BWu@oB_@i@z@EBKAG_@CyAuAMmAOi@?SJMP?vAdCr@t@t@Rz@BnBYPKtAqBv@y@j@O`C@\\\\Nl@vAd@Zt@nAfAv@lF|@BKRIvAWhAi@rAgBBu@GcAH[Sa@Rs@Ci@Bc@WIGO@c@_@Uc@k@c@wAOgALYHo@n@KlDwAdDmClCk@p@YT@JT^hDa@vC?p@ZnB\\\\x@VLXCFW_@_BGcABg@b@uB@e@[iACk@JqBVIbATd@Bl@T~@z@lA`@NGZaAA_CKe@i@m@w@_@}A[wAeA[HQ`@GBq@o@OBSRcBLe@Ci@Ww@?u@`@oBhBqA~@KXiBnBYLoBWYMgBeCaAwC]iCUi@]mBe@_BYwA[o@W{BLsDZw@`Aa@bBmB`@U~DYl@SlCwCfAm@LO?yAFc@nAkBh@yABe@Ik@}AqBEc@BMNGfABLINsEOsAaA_C?mB`C[nAf@bAKhBXlBFjCc@zBBt@TtBEpBJrCIrA@vAVxAp@nBbBlAdCLj@BrCJj@C^`@bGLrEShBDdANl@?dBc@rE?fADNPH\\\\CPH\\\\v@LxFIfEQx@?`@DF`@BDhIFvA^xCJfBGl@Qh@Er@?lC^|HOfA_A~CKrBOr@e@hAi@xEUzEmAfGG`BHzBi@pCIfGw@tIu@xSLtC]dBKhCL|AWfI\\\\bGCfAO`AFjA@fEMj@a@d@o@Me@Ac@XQ`@@hAs@Hc@V]`@w@tBGt@c@tAaAxA}@lCc@pBBhAQnADl@jAlATdB?~@UtCClALtDM^QFaFU{@ByDc@s@CcAHi@a@m@A}@Do@KYq@MsA_@sAy@iAGUUSs@Iw@w@k@KmB}BIc@YKHq@Km@s@aBa@sALSFq@KcByAiCcAw@[}@wAk@}@IuAk@c@BmA`AWH{EsAIHM|@x@PrCbArCvKt@nFNLh@HnAg@FLOn@DLPCNa@PARNl@`AHrA[tCAxBPrAp@~B`@~@l@l@xBl@`Ax@b@n@bAhDb@f@lA\\\\hBc@l@_@@a@SWMCiB`@o@AQIU]Iw@HOxAN\\\\EVMd@k@f@qAZMpGPtDC`EJx@Bz@f@nDG^KjDJLDEjAr@dACbFK^D~@}GIuEx@{DSA?cAmAk@{BO_BcBDaFdCcBPcNE_B\\\\wB~@_IlJVjEx@t@gJnKo@f@mAw@y@|@mC`BuFjCwE~CoBr@aFsR_Au@o@uC\\\\OkCsJc@DMk@m@Ni@kCx@[gBqFq@n@sBL{QgAyNb@uD^qFfAlA~PcLO}D_@kD_AaFcCuA~FaEzFzDjIz@`@eEzHgHdE_AEuAoCFsAr@oC~@aHM}HiBtBClBiArEwC`CKEYDiAXmA|@MrAw@G_BiB_@O[CUOI@KZECa@[}@uAm@m@]Kc@AsCd@c@G_Bm@iAeBYaAIeA@}ANiA|@wAf@N~@p@fBhBrA~@nAh@xA^h@Kb@{@'
df['polygon'] = df.code.apply(lambda x:polyline.decode(x))
df['string'] = df.polygon.apply(lambda x:polygon2string(x))
df[['city','string']].to_csv(r'C:\Users\admin\Downloads\nassau polygon.csv',index=False,quoting=csv.QUOTE_ALL)        