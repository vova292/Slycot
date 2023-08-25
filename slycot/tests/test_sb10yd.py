from slycot import synthesis
import numpy as np
from scipy import signal

class Test_sb10yd():

    def test_sb10yd_cont_exec(self):
        """A simple execution test.
        """

        A = np.array([[0.0, 1.0], [-0.5, -0.1]])
        B = np.array([[0.0], [1.0]])
        C = np.array([[1.0, 0.0]])
        D = np.zeros((1,1))

        sys_tf = signal.ss2tf(A,B,C,D)
        num, den = sys_tf

        omega, H = signal.freqs(num.squeeze(), den)

        real_H_resp = np.real(H)
        imag_H_resp = np.imag(H)

        n = 2
        dico = 0 # 0 for continuous time
        flag = 0 # 0 for no constraints on the poles
        n_id, *_ = synthesis.sb10yd(
            dico, flag, len(omega), 
            real_H_resp, imag_H_resp, omega, n, tol=0)

        # Because flag = 0, we expect n == n_id
        np.testing.assert_equal(n, n_id)

    def test_sb10yd_cont_allclose(self):
        """Compare given and identified frequency response.
        """

        A = np.array([[0.0, 1.0], [-0.5, -0.1]])
        B = np.array([[0.0], [1.0]])
        C = np.array([[1.0, 0.0]])
        D = np.zeros((1,1))

        sys_tf = signal.ss2tf(A,B,C,D)
        num, den = sys_tf

        omega, H = signal.freqs(num.squeeze(), den)

        real_H_resp = np.real(H)
        imag_H_resp = np.imag(H)

        n = 2
        dico = 0 # 0 for continuous time
        flag = 0 # 0 for no constraints on the poles
        n_id, A_id, B_id, C_id, D_id = synthesis.sb10yd(
            dico, flag, len(omega), 
            real_H_resp, imag_H_resp, omega, n, tol=0)
        
        sys_tf_id = signal.ss2tf(A_id,B_id,C_id,D_id)
        num_id, den_id = sys_tf_id
        w_id, H_id = signal.freqs(num_id.squeeze(), den_id, worN=omega)

        #print(np.max(abs(H)-abs(H_id)), np.max(abs(H_id)-abs(H)))
        #print(np.max(abs(H_id)/abs(H)))

        # Compare given and identified frequency response up to some toleration.
        # absolute(a-b) <= atol + rtol*abolute(b), element-wise true
        # absolute(a-b) or absolute(b-a) <= atol, for rtol=0 element-wise true
        np.testing.assert_allclose(abs(H_id),abs(H),rtol=0,atol=0.1)

    def test_sb10yd_disc_exec(self):
        """A simple execution test.
        """

        A = np.array([[0.0, 1.0], [-0.5, -0.1]])
        B = np.array([[0.0], [1.0]])
        C = np.array([[1.0, 0.0]])
        D = np.zeros((1,1))

        sys_tf = signal.ss2tf(A,B,C,D)
        num, den = sys_tf

        dt = 0.1
        num, den, dt = signal.cont2discrete((num, den), dt, method="zoh")
        print(den)

        omega, H = signal.freqz(num.squeeze(), den)

        real_H_resp = np.real(H)
        imag_H_resp = np.imag(H)

        n = 2
        dico = 1 # 0 for discrete time
        flag = 0 # 0 for no constraints on the poles
        n_id, *_ = synthesis.sb10yd(
            dico, flag, len(omega), 
            real_H_resp, imag_H_resp, omega, n, tol=0)

        # Because flag = 0, we expect n == n_id
        np.testing.assert_equal(n, n_id)

    def test_sb10yd_disc_allclose(self):
        """Compare given and identified frequency response.
        """

        A = np.array([[0.0, 1.0], [-0.5, -0.1]])
        B = np.array([[0.0], [1.0]])
        C = np.array([[1.0, 0.0]])
        D = np.zeros((1,1))

        sys_tf = signal.ss2tf(A,B,C,D)
        num, den = sys_tf

        dt = 0.01
        num, den, dt = signal.cont2discrete((num, den), dt, method="zoh")

        omega, H = signal.freqz(num.squeeze(), den)

        real_H_resp = np.real(H)
        imag_H_resp = np.imag(H)

        n = 2
        dico = 1 # 0 for discrete time
        flag = 0 # 0 for no constraints on the poles
        n_id, A_id, B_id, C_id, D_id = synthesis.sb10yd(
            dico, flag, len(omega), 
            real_H_resp, imag_H_resp, omega, n, tol=0)
        
        sys_id = signal.dlti(A_id,B_id,C_id,D_id, dt=dt)
        sys_tf_id = signal.TransferFunction(sys_id)
        num_id, den_id = sys_tf_id.num, sys_tf_id.den
        w_id, H_id = signal.freqz(num_id.squeeze(), den_id, worN=omega)

        #print(np.max(abs(H)-abs(H_id)), np.max(abs(H_id)-abs(H)))
        #print(np.max(abs(H_id)/abs(H)))

        # Compare given and identified frequency response up to some toleration.
        # absolute(a-b) <= atol + rtol*abolute(b), element-wise true
        # absolute(a-b) or absolute(b-a) <= atol, for rtol=0 element-wise true
        np.testing.assert_allclose(abs(H_id),abs(H),rtol=0,atol=1.0)