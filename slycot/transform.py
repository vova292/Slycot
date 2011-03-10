#!/usr/bin/env python
#
#       transform.py
#       
#       Copyright 2010-2011 Enrico Avventi <avventi@kth.se>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License version 2 as 
#       published by the Free Software Foundation.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from slycot import _wrapper
import numpy as _np

def tb01id(n,m,p,maxred,a,b,c,job='A'):
    """ s_norm,A,B,C,scale = tb01id(n,m,p,maxred,A,B,C,[job])
    
    To reduce the 1-norm of a system matrix

          S =  ( A  B )
               ( C  0 )

    corresponding to the triple (A,B,C), by balancing. This involves
    a diagonal similarity transformation inv(D)*A*D applied
    iteratively to A to make the rows and columns of
                        -1
               diag(D,I)  * S * diag(D,I)

    as close in norm as possible.

    The balancing can be performed optionally on the following
    particular system matrices

           S = A,    S = ( A  B )    or    S = ( A )
                                               ( C )
    
    Required arguments:
        n : input int
            The order of the matrix A, the number of rows of matrix B and 
            the number of columns of matrix C. It represents the dimension of 
            the state vector.  n > 0.
        m : input int
            The number of columns of matrix B. It represents the dimension of 
            the input vector.  m > 0.
        p : input int
            The number of rows of matrix C. It represents the dimension of 
            the output vector.  p > 0.
        maxred : input float
            The maximum allowed reduction in the 1-norm of S  (in an iteration) 
            if zero rows or columns are encountered.
            If maxred > 0.0, maxred must be larger than one (to enable the norm 
            reduction). 
            If maxred <= 0.0, then the value 10.0 for maxred is used.
        A : input rank-2 array('d') with bounds (n,n)
            The leading n-by-n part of this array must contain the system state 
            matrix A.
        B : input rank-2 array('d') with bounds (n,m)
            The leading n-by-m part of this array must contain the system input 
            matrix B.
        C : input rank-2 array('d') with bounds (p,n)
            The leading p-by-n part of this array must contain the system output 
            matrix C.
    Optional arguments:
        job := 'A' input string(len=1)
            Indicates which matrices are involved in balancing, as follows:
            = 'A':  All matrices are involved in balancing;
            = 'B':  B and A matrices are involved in balancing;
            = 'C':  C and A matrices are involved in balancing;
            = 'N':  B and C matrices are not involved in balancing.
    Return objects:
        s_norm : float
            The 1-norm of the given matrix S is non-zero, the ratio between 
            the 1-norm of the given matrix and the 1-norm of the balanced matrix.
        A : rank-2 array('d') with bounds (n,n)
            The leading n-by-n part of this array contains the balanced matrix 
            inv(D)*A*D.
        B : rank-2 array('d') with bounds (n,m)
            The leading n-by-m part of this array contains the balanced matrix 
            inv(D)*B.
        C : rank-2 array('d') with bounds (p,n)
            The leading p-by-n part of this array contains the balanced matrix C*D.
        scale : rank-1 array('d') with bounds (n)
            The scaling factors applied to S.  If D(j) is the scaling factor 
            applied to row and column j, then scale(j) = D(j), for j = 1,...,n.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['job', 'N', 'M', 'P', 'maxred', 'A', 'LDA'+hidden, 'B', 
        'LDB'+hidden, 'C', 'LDC'+hidden, 'scale', 'INFO'+hidden]
    our = _wrapper.tb01id(n,m,p,maxred,a,b,c,job=job)
    if out[-1] < 0:
        error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
        e = ValueError(error_text)    
        e.info = out[-1]
        raise e
    return out[:-1]

def tb03ad(n,m,p,A,B,C,D,leri,equil='N',tol=0.0,ldwork=None):
    """ A_min,b_min,C_min,nr,index,pcoeff,qcoeff,vcoeff = tb03ad_l(n,m,p,A,B,C,D,leri,[equil,tol,ldwork])
    
    To find a relatively prime left or right polynomial matrix representation
    with the same transfer matrix as that of a given state-space representation, 
    i.e. if leri = 'L'

        inv(P(s))*Q(s) = C*inv(s*I-A)*B + D
        
    or, if leri = 'R'
    
        Q(s)*inv(P(s)) = C*inv(s*I-A)*B + D.
        
    Additionally a minimal realization (A_min,B_min,C_min) of the original 
    system (A,B,C) is returned.

    Required arguments:
        n : input int
            The order of the state-space representation, i.e. the order of 
            the original state dynamics matrix A.  n > 0.
        m : input int
            The number of system inputs.  m > 0.
        p : input int
            The number of system outputs.  p > 0.
        A : input rank-2 array('d') with bounds (n,n)
            The leading n-by-n part of this array must contain the original 
            state dynamics matrix A.
        B : input rank-2 array('d') with bounds (n,max(m,p))
            The leading n-by-m part of this array must contain the original 
            input/state matrix B; the remainder of the leading n-by-max(m,p) 
            part is used as internal workspace.
        C : input rank-2 array('d') with bounds (max(m,p),n)
            The leading p-by-n part of this array must contain the original 
            state/output matrix C; the remainder of the leading max(m,p)-by-n 
            part is used as internal workspace.
        D : input rank-2 array('d') with bounds (max(m,p),max(m,p))
            The leading p-by-m part of this array must contain the original 
            direct transmission matrix D; the remainder of the leading 
            max(m,p)-by-max(m,p) part is used as internal workspace.
        leri : input string(len=1)
            Indicates whether the left polynomial matrix representation or 
            the right polynomial matrix representation is required.
    Optional arguments:
        equil := 'N' input string(len=1)
            Specifies whether the user wishes to balance the triplet (A,B,C), 
            before computing a minimal state-space representation, as follows:
            = 'S':  Perform balancing (scaling);
            = 'N':  Do not perform balancing.
        tol := 0.0 input float
            The tolerance to be used in rank determination when transforming 
            (A, B). If tol <= 0 a default value is used.
        ldwork := max(2*n+3*max(m,p), p*(p+2)) input int
            The length of the cache array.
            ldwork >= max( n + max(n, 3*m, 3*p), pm*(pm + 2))
            where pm = p, if leri = 'L';
                  pm = m, if leri = 'R'.
            For optimum performance it should be larger.
    Return objects:
        A_min : rank-2 array('d') with bounds (n,n)
            The leading nr-by-nr part of this array contains the upper block 
            Hessenberg state dynamics matrix A_min of a minimal realization for 
            the original system.
        B_min : rank-2 array('d') with bounds (n,max(m,p))
            The leading nr-by-m part of this array contains the transformed 
            input/state matrix B_min.
        C_min : rank-2 array('d') with bounds (max(m,p),n)
            The leading p-by-nr part of this array contains the transformed 
            state/output matrix C_min.
        nr : int
            The order of the minimal state-space representation 
            (A_min,B_min,C_min).
        index : rank-1 array('i') with bounds either (p) or (m)
            If leri = 'L', index(i), i = 1,2,...,p, contains the maximum degree 
            of the polynomials in the i-th row of the denominator matrix P(s) 
            of the left polynomial matrix representation. These elements are 
            ordered so that index(1) >= index(2) >= ... >= index(p).
            If leri = 'R', index(i), i = 1,2,...,m, contains the maximum degree 
            of the polynomials in the i-th column of the denominator matrix P(s) 
            of the right polynomial matrix representation. These elements are 
            ordered so that index(1) >= index(2) >= ... >= index(m). 
        pcoeff : rank-3 array('d') with bounds either (p,p,n+1) or (m,m,n+1)
            If leri = 'L' then porm = p, otherwise porm = m.
            The leading porm-by-porm-by-kpcoef part of this array contains 
            the coefficients of the denominator matrix P(s), where 
            kpcoef = max(index) + 1.
            pcoeff(i,j,k) is the coefficient in s**(index(iorj)-k+1) of 
            polynomial (i,j) of P(s), where k = 1,2,...,kpcoef; if leri = 'L' 
            then iorj = I, otherwise iorj = J. Thus for leri = 'L', 
            P(s) = diag(s**index)*(pcoeff(.,.,1)+pcoeff(.,.,2)/s+...).
        qcoeff : rank-3 array('d') with bounds (p,m,n + 1) or (max(m,p),max(m,p))
            If leri = 'L' then porp = m, otherwise porp = p.
            If leri = 'L', the leading porm-by-porp-by-kpcoef part of this array 
            contains the coefficients of the numerator matrix Q(s).
            If leri = 'R', the leading porp-by-porm-by-kpcoef part of this array 
            contains the coefficients of the numerator matrix Q(s).
            qcoeff(i,j,k) is defined as for pcoeff(i,j,k).
        vcoeff : rank-3 array('d') with bounds (p,n,n+1) or (m,n,n+1)
            The leading porm-by-nr-by-kpcoef part of this array contains 
            the coefficients of the intermediate matrix V(s). 
            vcoeff(i,j,k) is defined as for pcoeff(i,j,k).
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['leri', 'equil', 'n', 'm', 'P', 'A', 'LDA'+hidden, 'B', 
        'LDB'+hidden, 'C', 'LDC'+hidden, 'D', 'LDD'+hidden, 'nr', 'index', 
        'pcoeff', 'LDPCO1'+hidden, 'LDPCO2'+hidden, 'qcoeff', 'LDQCO1'+hidden, 
        'LDQCO2'+hidden, 'vcoeff', 'LDVCO1'+hidden, 'LDVCO2'+hidden, 'tol', 
        'IWORK'+hidden, 'DWORK'+hidden, 'ldwork', 'INFO'+hidden]
    if leri == 'L':
        if ldwork is None:
            ldwork = max( 2*n + 3*max(m,p), p*(p+2))
        out = _wrapper.tb03ad_l(n,m,p,A,B,C,D,equil=equil,tol=tol,ldwork=ldwork)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        if out[-1] > 0:
            e = ArithmeticError('a singular matrix was encountered during the computation')
            e.info = out[-1]
            raise e
        return out[:-1]
    if leri == 'R':
        if ldwork is None:
            ldwork = max( 2*n + 3*max(m,p), m*(m+2))
        out = _wrapper.tb03ad_r(n,m,p,A,B,C,D,equil=equil,tol=tol,ldwork=ldwork)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        if out[-1] > 0:
            e = ArithmeticError('a singular matrix was encountered during the computation')
            e.info = out[-1]
            raise e
        return out[:-1]
    raise ValueError('leri must be either L or R')

def tb04ad(rowcol,n,m,p,A,B,C,D,tol1=0.0,tol2=0.0,ldwork=None):
    """ Ar,Br,Cr,nr,denom_degs,denom_coeffs,num_coeffs = tb04ad(n,m,p,A,B,C,D,lddcoe,lduco1,lduco2,[tol1,tol2,ldwork])

    Convert a state-space system to a tranfer function or matrix of transfer functions.
    
    Required arguments
    ------------------
    
        rowcol : character
            indicates whether the transfer matrix T(s) is output as rows ('R')
            or colums ('C') over common denominators 
        n : integer 
            state dimension
        m : integer 
            input dimension
        p : integer 
            output dimension
        A :  rank-2 array, shape(n,n)
            state dynamics matrix.
        B : rank-2 array, shape (n,m) 
            input matrix
        C : rank-2 array, shape (p,n) 
            output matri
        D : rank-2 array, shape (p,m) 
            direct transmission matrix

     Optional arguments
     ------------------
     
        tol1 = 0.0: double
            tolerance in determining the transfer function coefficients, 
            when set to 0, a default value is used
        tol2 = 0.0: double
            tolerance in separating out a controllable/observable subsystem 
            of (A,B,C), when set to 0, a default value is used
        ldwork : int
            The length of the cache array. The default values is 
            max(1,n*(n+1)+max(n*m+2*n+max(n,p),max(3*m,p)))
     
     Returns
     -------
     
        nr : int
            state dimension of the controllable subsystem for rowcol = 'R', 
            observable subsystem dimension for rowcol = 'C'
        Ar :  rank-2 array, shape(nr,nr)
            state dynamics matrix of the controllable/observable subsystem
        Br : rank-2 array, shape (nr,m) 
            input matrix of the controllable/observable subsystem
        Cr : rank-2 array, shape (p,nr) 
            output matri of the controllable/observable subsystem
        index : rank-1 array, shape (p) or (m)
            array of orders of the denomenator polynomials. Different 
            shapes corresponding to rowcol=='R' and rowcol=='C' 
            respectively.
        dcoeff : rank-2 array, shape (p,max(index)+1) or (m,max(index)+1)
            array of denomenator coefficients. Different shapes 
            corresponding to rowcol=='R' and rowcol=='C' respectively.
        ucoeff : rank-3 array, shape (p,m,max(index)+1) or (max(p,m),max(p,m),max(index)+1)
            array of numerator coefficients. Different shapes 
            corresponding to rowcol=='R' and rowcol=='C' respectively.
            
    Raises
    ------
        ValueError : e
            e.info contains information about the exact type of exception
             < 0:  if info = -i, the i-th argument had an illegal value;
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['rowcol','n','m','p','A','lda'+hidden,'B','ldb'+hidden,'C','ldc'+hidden,'D', 'ldd'+hidden,
        'nr','index','dcoeff','lddcoe'+hidden, 'ucoeff','lduco1'+hidden,'lduco2'+hidden,'tol1','tol2','iwork'+hidden,'dwork'+hidden,'ldwork','info'+hidden]
    if rowcol == 'R':
        mp, pm = m, p
        porm, porp = p, m
        if ldwork is None:
            ldwork = max(1,n*(n+1)+max(n*mp+2*n+max(n,mp),max(3*mp,pm)))
        if B.shape != (n,m):
            e = ValueError("The shape of B is ("+str(B.shape[0])+","+str(B.shape[1])+"), but expected ("+str(n)+","+str(m)+")")
            e.info = -7
            raise e
        if C.shape != (p,n):
            e = ValueError("The shape of C is ("+str(C.shape[0])+","+str(C.shape[1])+"), but expected ("+str(p)+","+str(n)+")")
            e.info = -9
            raise e
        if D.shape != (max(1,p),m):
            e = ValueError("The shape of D is ("+str(B.shape[0])+","+str(B.shape[1])+"), but expected ("+str(max(1,p))+","+str(m)+")")
            e.info = -11
            raise e
        out = _wrapper.tb04ad_r(n,m,p,A,B,C,D,tol1,tol2,ldwork)
    elif rowcol == 'C':
        mp, pm = p, m
        porm, porp = m, p
        if ldwork is None:
            ldwork = max(1,n*(n+1)+max(n*mp+2*n+max(n,mp),max(3*mp,pm)))
        if B.shape != (n,m):
            e = ValueError("The shape of B is ("+str(B.shape[0])+","+str(B.shape[1])+"), but expected ("+str(n)+","+str(max(m,p))+")")
            e.info = -7
            raise e
        _B = _np.zeros((n,max(m,p)))
        _B[:n,:m] = B
        if C.shape != (p,n):
            e = ValueError("The shape of C is ("+str(C.shape[0])+","+str(C.shape[1])+"), but expected ("+str(max([1,m,p]))+","+str(n)+")")
            e.info = -9
            raise e
        _C = _np.zeros((max(1,m,p),n))
        _C[:p,:n] = C
        if D.shape != (p,m):
            e = ValueError("The shape of D is ("+str(B.shape[0])+","+str(B.shape[1])+"), but expected ("+str(max([1,m,p]))+","+str(max(m,p))+")")
            e.info = -11
            raise e
        _D = _np.zeros((max(1,m,p),max(m,p)))
        _D[:p,:m] = D
        out = _wrapper.tb04ad_c(n,m,p,A,_B,_C,_D,tol1,tol2,ldwork)
    else:
        e = ValueError("Parameter rowcol had an illegal value")
        e.info = -1
        raise e

    if out[-1] < 0:
        error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
        e = ValueError(error_text)
        e.info = out[-1]
        raise e
    
    A,B,C,Nr,index,dcoeff,ucoeff = out[:-1]
    kdcoef = max(index)+1
    return A[:Nr,:Nr],B[:Nr,:m],C[:p,:Nr],Nr,index,dcoeff[:porm,:kdcoef],ucoeff[:porm,:porp,:kdcoef]

def td04ad(rowcol,m,p,index,dcoeff,ucoeff,tol=0.0,ldwork=None):
    """ nr,A,B,C,D = td04ad(m,p,index,dcoeff,ucoeff,[tol,ldwork])

    Convert a tranfer function or matrix of transfer functions to 
    a minimum state space realization.
    
    Required arguments
    ------------------
    
        rowcol : character 
            indicates whether the transfer matrix T(s) is given 
            as rows ('R') or colums ('C') over common denominators.
        m : integer 
            input dimension
        p : integer 
            output dimension
        index : rank-1 array, shape (p) or (m) 
            array of orders of the denomenator polynomials. Different 
            shapes corresponding to rowcol=='R' and rowcol=='C' 
            respectively.
        dcoeff : rank-2 array, shape (p,max(index)+1) or (m,max(index)+1)
            array of denomenator coefficients. Different shapes 
            corresponding to rowcol=='R' and rowcol=='C' respectively.
        ucoeff : rank-3 array, shape (p,m,max(index)+1) or (max(p,m),max(p,m),max(index)+1)
            array of numerator coefficients. Different shapes 
            corresponding to rowcol=='R' and rowcol=='C' respectively.

    Optional arguments
    ------------------
    
        tol : float 
            tolerance in determining the state space system, 
            when set to 0, a default value is used.
        ldwork : int
            The length of the cache array. The default values is 
            max(1,sum(index)+max(sum(index),max(3*m,3*p)))
     
    Returns
    -------
    
        nr : int
            minimal state dimension
        A :  rank-2 array, shape(nr,nr)
            state dynamics matrix.
        B : rank-2 array, shape (nr,m) 
            input matrix
        C : rank-2 array, shape (p,nr) 
            output matri
        D : rank-2 array, shape (p,m) 
            direct transmission matrix
            
    Raises
    ------

        ValueError : e
            e.info contains information about the exact type of exception
             < 0:  if info = -i, the i-th argument had an illegal value;
             > 0:  if info = i, then i is the first integer for which
                abs( dcoeff(i,1) ) is so small that the calculations
                would overflow (see SLICOT Library routine TD03AY);
                that is, the leading coefficient of a polynomial is
                nearly zero; no state-space representation is
                calculated.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['rowcol','m','p','index','dcoeff','lddcoe'+hidden, 'ucoeff', 'lduco1'+hidden,'lduco2'+hidden,
        'nr','A','lda'+hidden,'B','ldb'+hidden,'C','ldc'+hidden,'D', 'ldd'+hidden,
        'tol','iwork'+hidden,'dwork'+hidden,'ldwork','info'+hidden]
    if ldwork is None:
        n = sum(index)
        ldwork = max(1,n+max(n,max(3*m,3*p)))
    
    kdcoef = max(index)+1
    if rowcol == 'R':
        porm = p
        if ucoeff.ndim != 3:
            e = ValueError("The numerator is not a 3D array!")
            e.info = -7
            raise e
        if ucoeff.shape != (max(1,p),max(1,m),kdcoef):
            e = ValueError("The numerator shape is ("+str(ucoeff.shape[0])+","+str(ucoeff.shape[1])+","+str(ucoeff.shape[2])+"), but expected ("+str(max(1,p))+","+str(max(1,m))+","+str(kdcoef)+")")
            e.info = -7
            raise e
        if dcoeff.shape != (max(1,p),kdcoef):
            e = ValueError("The denominator shape is ("+str(dcoeff.shape[0])+","+str(dcoeff.shape[1])+"), but expected ("+str(max(1,p))+","+str(kdcoef)+")")
            e.info = -5
            raise e
        out = _wrapper.td04ad_r(m,p,index,dcoeff,ucoeff,n,tol,ldwork)
    elif rowcol == 'C':
        porm = m
        if ucoeff.ndim != 3:
            e = ValueError("The numerator is not a 3D array!")
            e.info = -7
            raise e
        if ucoeff.shape != (max([1,m,p]),max([1,m,p]),kdcoef):
            e = ValueError("The numerator shape is ("+str(ucoeff.shape[0])+","+str(ucoeff.shape[1])+","+str(ucoeff.shape[2])+"), but expected ("+str(max([1,m,p]))+","+str(max([1,m,p]))+","+str(kdcoef)+")")
            e.info = -7
            raise e
        if dcoeff.shape != (max(1,m),kdcoef):
            e = ValueError("The denominator shape is ("+str(dcoeff.shape[0])+","+str(dcoeff.shape[1])+"), but expected ("+str(max(1,m))+","+str(kdcoef)+")")
            e.info = -5
            raise e
        out = _wrapper.td04ad_c(m,p,index,dcoeff,ucoeff,n,tol,ldwork)
    else:
        e = ValueError("Parameter rowcol had an illegal value")
        e.info = -1
        raise e

    if out[-1] < 0:
        error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
        e = ValueError(error_text)
        e.info = out[-1]
        raise e
    if out[-1] > 0:
        error_text = "The leading coefficient of a denominator polynomial is nearly zero; calculations would overflow; no state-space representation was calculated. ABS(DCOEFF("+str(out[-1])+",1))="+str(abs(dcoeff(out[-1],1)))+" is too small."    
        e.info = out[-1]
        raise e
    Nr, A, B, C, D = out[:-1]    
    return Nr, A[:Nr,:Nr], B[:Nr,:m], C[:p,:Nr], D[:p,:m] 

def tc04ad(m,p,index,pcoeff,qcoeff,leri,ldwork=None):
    """ n,rcond,a,b,c,d = tc04ad_l(m,p,index,pcoeff,qcoeff,leri,[ldwork])

    To find a state-space representation (A,B,C,D) with the same
    transfer matrix as that of a given left or right polynomial
    matrix representation, i.e.

        C*inv(sI-A)*B + D = inv(P(s))*Q(s) 

    or

        C*inv(sI-A)*B + D = Q(s)*inv(P(s))

    respectively.
        
    Required arguments:
        m : input int
            The number of system inputs.  m > 0.
        p := len(index) input int
            The number of system outputs.  p > 0.
        index : input rank-1 array('i') with bounds (p) or (m)
            If leri = 'L', index(i), i = 1,2,...,p, must contain the maximum 
            degree of the polynomials in the I-th row of the denominator matrix 
            P(s) of the given left polynomial matrix representation.
            If leri = 'R', index(i), i = 1,2,...,m, must contain the maximum 
            degree of the polynomials in the I-th column of the denominator 
            matrix P(s) of the given right polynomial matrix representation.
        pcoeff : input rank-3 array('d') with bounds (p,p,*) or (m,m,*)
            If leri = 'L' then porm = p, otherwise porm = m. The leading 
            porm-by-porm-by-kpcoef part of this array must contain 
            the coefficients of the denominator matrix P(s). pcoeff(i,j,k) is 
            the coefficient in s**(index(iorj)-K+1) of polynomial (I,J) of P(s), 
            where k = 1,2,...,kpcoef and kpcoef = max(index) + 1; if leri = 'L' 
            then iorj = i, otherwise iorj = j. Thus for leri = 'L', 
            P(s) = diag(s**index)*(pcoeff(.,.,1)+pcoeff(.,.,2)/s+...).
            If leri = 'R', pcoeff is modified by the routine but restored on exit.
        qcoeff : input rank-3 array('d') with bounds (p,m,*) or (max(m,p),max(m,p),*)
            If leri = 'L' then porp = m, otherwise porp = p. The leading 
            porm-by-porp-by-kpcoef part of this array must contain 
            the coefficients of the numerator matrix Q(s). 
            qcoeff(i,j,k) is defined as for pcoeff(i,j,k).
            If leri = 'R', qcoeff is modified by the routine but restored on exit.
        leri : input string(len=1)
            Indicates whether a left polynomial matrix representation or a right 
            polynomial matrix representation is input as follows:
            = 'L':  A left matrix fraction is input;
            = 'R':  A right matrix fraction is input.
    Optional arguments:
        ldwork := max(m,p)*(max(m,p)+4) input int
            The length of the cache array. ldwork >= max(m,p)*(max(m,p)+4)
            For optimum performance it should be larger.
    Return objects:
        n : int
            The order of the resulting state-space representation.
            That is, n = sum(index).
        rcond : float
            The estimated reciprocal of the condition number of the leading row 
            (if leri = 'L') or the leading column (if leri = 'R') coefficient 
            matrix of P(s).
            If rcond is nearly zero, P(s) is nearly row or column non-proper.
        A : rank-2 array('d') with bounds (n,n)
            The leading n-by-n part of this array contains the state dynamics matrix A.
        B : rank-2 array('d') with bounds (n,max(m,p))
            The leading n-by-n part of this array contains the input/state matrix B; 
            the remainder of the leading n-by-max(m,p) part is used as internal 
            workspace.
        C : rank-2 array('d') with bounds (max(m,p),n)
            The leading p-by-n part of this array contains the state/output matrix C; 
            the remainder of the leading max(m,p)-by-n part is used as internal 
            workspace.
        D : rank-2 array('d') with bounds (max(m,p),max(m,p))
            The leading p-by-m part of this array contains the direct transmission 
            matrix D; the remainder of the leading max(m,p)-by-max(m,p) part is 
            used as internal workspace.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['leri', 'm', 'P', 'index', 'pcoeff', 'LDPCO1'+hidden, 
    'LDPCO2'+hidden, 'qcoeff', 'LDQCO1'+hidden, 'LDQCO2'+hidden, 'N', 'rcond', 
    'A', 'LDA'+hidden, 'B', 'LDB'+hidden, 'C', 'LDC'+hidden, 'D', 'LDD'+hidden, 
    'IWORK'+hidden, 'DWORK'+hidden, 'ldwork', 'INFO'+hidden]
    if ldwork is None:
        ldwork = max(m,p)*(max(m,p)+4)
    n = sum(index)
    if leri == 'L':
        out = _wrapper.tc04ad_l(m,p,index,pcoeff,qcoeff,n)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        if out[-1] == 1:
            e = ArithmeticError('P(s) is not row proper')
            e.info = out[-1]
            raise e
        return out[:-1]
    if leri == 'R':
        out = _wrapper.tc04ad_r(m,p,index,pcoeff,qcoeff,n)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        if out[-1] == 1:
            e = ArithmeticError('P(s) is not column proper')
            e.info = out[-1]
            raise e
        return out[:-1]
    raise ValueError('leri must be either L or R')
    
def tc01od(m,p,indlin,pcoeff,qcoeff,leri):
    """ pcoeff,qcoeff = tc01od_l(m,p,indlim,pcoeff,qcoeff,leri)
    
    To find the dual right (left) polynomial matrix representation of a given 
    left (right) polynomial matrix representation, where the right and left 
    polynomial matrix representations are of the form Q(s)*inv(P(s)) and 
    inv(P(s))*Q(s) respectively.
    
    Required arguments:
        m : input int
            The number of system inputs.  m > 0.
        p : input int
            The number of system outputs.  p > 0.
        indlim : input int
            The highest value of k for which pcoeff(.,.,k) and qcoeff(.,.,k) 
            are to be transposed.
            k = kpcoef + 1, where kpcoef is the maximum degree of the polynomials 
            in P(s).  indlim > 0.
        pcoeff : input rank-3 array('d') with bounds (p,p,indlim) or (m,m,indlim)
            If leri = 'L' then porm = p, otherwise porm = m. 
            On entry, the leading porm-by-porm-by-indlim part of this array 
            must contain the coefficients of the denominator matrix P(s).
            pcoeff(i,j,k) is the coefficient in s**(indlim-k) of polynomial 
            (i,j) of P(s), where k = 1,2,...,indlim.
        qcoeff : input rank-3 array('d') with bounds (max(m,p),max(m,p),indlim)
            On entry, the leading p-by-m-by-indlim part of this array must 
            contain the coefficients of the numerator matrix Q(s).
            qcoeff(i,j,k) is the coefficient in s**(indlim-k) of polynomial 
            (i,j) of Q(s), where k = 1,2,...,indlim.
        leri : input string(len=1)
    Return objects:
        pcoeff : rank-3 array('d') with bounds (p,p,indlim)
            On exit, the leading porm-by-porm-by-indlim part of this array 
            contains the coefficients of the denominator matrix P'(s) of 
            the dual system.
        qcoeff : rank-3 array('d') with bounds (max(m,p),max(m,p),indlim)
            On exit, the leading m-by-p-by-indlim part of the array contains 
            the coefficients of the numerator matrix Q'(s) of the dual system.
        info : int
            = 0:  successful exit;
            < 0:  if info = -i, the i-th argument had an illegal value.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['leri', 'M', 'P', 'indlim', 'pcoeff', 'LDPCO1'+hidden, 
        'LDPCO2'+hidden, 'qcoeff', 'LDQCO1'+hidden, 'LDQCO2'+hidden, 
        'INFO'+hidden]
    if leri == 'L':
        out = _wrapper.tc01od_l(m,p,indlin,pcoeff,qcoeff)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        return out[:-1]
    if leri == 'R':
        out = _wrapper.tc01od_r(m,p,indlin,pcoeff,qcoeff)
        if out[-1] < 0:
            error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
            e = ValueError(error_text)
            e.info = out[-1]
            raise e
        return out[:-1]
    raise ValueError('leri must be either L or R')

def tf01md(n,m,p,N,A,B,C,D,u,x0):
    """ xf,y = tf01md(n,m,p,N,A,B,C,D,u,x0)
    
    To compute the output sequence of a linear time-invariant
    open-loop system given by its discrete-time state-space model
    
    Required arguments:
        n : input int
            Order of the State-space representation.
        m : input int
            Number of inputs.
        p : input int
            Number of outputs.
        N : input int
            Number of output samples to be computed. 
        A : input rank-2 array('d') with bounds (n,n)
            State dynamics matrix.
        B : input rank-2 array('d') with bounds (n,m)
            Input/state matrix.
        C : input rank-2 array('d') with bounds (p,n)
            State/output matrix.
        D : input rank-2 array('d') with bounds (p,m)
            Direct transmission matrix.
        u : input rank-2 array('d') with bounds (m,N)
            Input signal.
        x0 : input rank-1 array('d') with bounds (n)
            Initial state, at time 0.
    Return objects:
        xf : rank-1 array('d') with bounds (n)
            Final state, at time N+1.
        y : rank-2 array('d') with bounds (p,N)
            Output signal.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['n','m','p','ny','A','lda'+hidden,'B','ldb'+hidden,
        'C','ldc'+hidden,'D','ldd'+hidden,'u','ldu'+hidden,'x0',
        'y'+hidden,'ldy'+hidden,'dwork'+hidden,'info'+hidden]
        
    out = _wrapper.tf01md(n,m,p,N,A,B,C,D,u,x0)
    if out[-1] < 0:
        error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
        e = ValueError(error_text)
        e.info = out[-1]
        raise e
    return out[:-1]
    
def tf01rd(n,m,p,N,A,B,C,ldwork=None): 
    """ H = tf01rd(n,m,p,N,A,B,C,[ldwork])
    
    To compute N Markov parameters M_1, M_2,..., M_N from the
    parameters (A,B,C) of a linear time-invariant system, where each
    M_k is an p-by-m matrix and k = 1,2,...,N.

    All matrices are treated as dense, and hence TF01RD is not
    intended for large sparse problems.

    
    Required arguments:
        n : input int
            Order of the State-space representation.
        m : input int
            Number of inputs.
        p : input int
            Number of outputs.
        N : input int
            Number of Markov parameters to be computed.
        A : input rank-2 array('d') with bounds (n,n)
            State dynamics matrix. 
        B : input rank-2 array('d') with bounds (n,m)
            Input/state matrix.
        C : input rank-2 array('d') with bounds (p,n)
            State/output matrix.
    Optional arguments:
        ldwork := 2*na*nc input int
    Return objects:
        H : rank-2 array('d') with bounds (p,N*m)
            H[:,(k-1)*m : k*m] contains the k-th Markov parameter, 
            for k = 1,2...N.
    """
    hidden = ' (hidden by the wrapper)'
    arg_list = ['n','m','p','N','A','lda'+hidden,'B','ldb'+hidden,'C',
        'ldc'+hidden,'H','ldh'+hidden,'dwork'+hidden,'ldwork','info'+hidden]
        
    if ldwork is None:
        out = _wrapper.tf01rd(n,m,p,N,A,B,C)
    else:
        out = _wrapper.tf01rd(n,m,p,N,A,B,C,ldwork=ldwork)
    if out[-1] < 0:
        error_text = "The following argument had an illegal value: "+arg_list[-out[-1]-1]
        e = ValueError(error_text)
        e.info = out[-1]
        raise e
    return out[0]

    
# to be replaced by python wrappers
