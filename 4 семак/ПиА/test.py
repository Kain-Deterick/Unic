import sys
import numpy as np
from scipy.integrate import odeint
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
import matplotlib.pyplot as plt

def func_ode(y, t, k, b):
    dydt = k*y + b
    return dydt
class MainWindow():
    def __init__(self):
        #Переменные
        self.tmax = 10
        self.M = 500
        self.C1 = 4200
        self.C2 = 4200
        self.G1 = 400
        self.G2 = 1000
        self.T1 = 90
        self.T2 = 20
        self.k = 0.0
        self.t = 0.0
        self.T_out_0 = 0.0  # initial value
        self.ntime = 101  # number of time nodes
        self.T_out = np.ndarray((self.ntime, 1, 1, 1, 1))  # result array

    def clickGraphClicked(self):
        global t
        t = np.linspace(0, self.tmax, self.ntime)
        if self.G1 == 0 and self.G2 == 0:
            self.k = -0.5 * (self.C1 + self.C2) / self.M
            self.b = -0.5 * (self.T1 * (self.C1 + 1.0) + self.T2 * (self.C2 + 1.0)) / self.M
        else:
            self.k = -(self.C1 * self.G1 + self.C2 * self.G2) / (self.M * (self.G1 + self.G2))
            self.b = (self.T1 * self.G1 * (self.C1 + 1.0) + self.T2 * self.G2 * (self.C2 + 1.0)) / (
                        self.M * (self.G1 + self.G2))
        sol = odeint(func_ode, self.T_out_0, t, args=(self.k, self.b)).reshape(self.ntime, )
        print(sol)
        self.T_out[:, 0, 0, 0, 0] = sol
        df = pd.DataFrame(self.T_out[:, 0, 0, 0, 0].reshape((1, self.ntime)))
        df.insert(0, 'T2', self.T2)
        df.insert(0, 'T1', self.T1)
        df.insert(0, 'G2', self.G2)
        df.insert(0, 'G1', self.G1)
        df.insert(0, 'C2', self.C2)
        df.insert(0, 'C1', self.C1)
        df.insert(0, 'M', self.M)
        df.insert(0, 'tmax', self.tmax)

        # The database URL must be in a specific format
        db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
        # Replace the values below with your own
        # DB username, password, host and database name
        db_url = db_url.format(
            USER="Kain",
            PWD="Uxninitcroom13",
            HOST="localhost:3306",
            DBNAME="unic"
        )
        engine = create_engine(db_url, echo=False)

        with engine.begin() as conn:
            df.to_sql(
                name='temperature',
                con=conn,
                if_exists='append',
                index=False
            )

MainWindow().clickGraphClicked()