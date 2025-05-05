from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

class VLEModel:
    def __init__(self, T, x1, y1, P, A1, B1, C1, A2, B2, C2):
        self.T = T  # Температура в Кельвинах
        self.x1 = np.array(x1)  # Мольные доли компонента 1 в жидкости
        self.y1 = np.array(y1)  # Мольные доли компонента 1 в паре
        self.P = np.array(P)  # Давление в барах
        self.A1, self.B1, self.C1 = A1, B1, C1  # Параметры Антуана для компонента 1
        self.A2, self.B2, self.C2 = A2, B2, C2  # Параметры Антуана для компонента 2
        self.R = 8.314  # Универсальная газовая постоянная

    def calculate_saturation_pressure(self, A, B, C):
        P_mmHg = np.exp(A - B / (self.T + C))
        P_bar = P_mmHg / 750.062
        return P_bar

    def calculate_activity_coefficients(self):
        P1_0 = self.calculate_saturation_pressure(self.A1, self.B1, self.C1)
        P2_0 = self.calculate_saturation_pressure(self.A2, self.B2, self.C2)
        self.gam1 = self.y1 * self.P / (P1_0 * self.x1)
        self.gam2 = (1 - self.y1) * self.P / (P2_0 * (1 - self.x1))
        self.gE_exp = (self.x1 * np.log(self.gam1) + (1 - self.x1) * np.log(self.gam2)) * (self.R * self.T)

    def wilson_parameters(self, params):
        Lambda12, Lambda21 = params
        gE_wilson = (-self.x1 * np.log(self.x1 + Lambda12 * (1 - self.x1)) - (1 - self.x1) * np.log(
            Lambda21 * self.x1 + (1 - self.x1))) * (self.R * self.T)
        return np.sum(np.abs(self.gE_exp - gE_wilson))

    def optimize_wilson_parameters(self):
        initial_guess = [0.1, 0.1]
        result = minimize(self.wilson_parameters, initial_guess, method='Nelder-Mead')
        self.Lambda12, self.Lambda21 = result.x

    def print_results(self):
        print("Оптимизированные параметры модели Вильсона:")
        print(f"Lambda12 = {self.Lambda12}, Lambda21 = {self.Lambda21}")

    def calculate_vle(self):
        x_range = np.linspace(0, 1, 100)
        x2_range = 1 - x_range

        P1_0 = self.calculate_saturation_pressure(self.A1, self.B1, self.C1)
        P2_0 = self.calculate_saturation_pressure(self.A2, self.B2, self.C2)

        gamma1 = np.exp(-np.log(x_range + self.Lambda12 * x2_range) + x2_range * (self.Lambda12 / (x_range + self.Lambda12 * x2_range) - self.Lambda21 / (self.Lambda21 * x_range + x2_range)))
        gamma2 = np.exp(-np.log(x2_range + self.Lambda21 * x_range) - x_range * (self.Lambda12 / (x_range + self.Lambda12 * x2_range) - self.Lambda21 / (self.Lambda21 * x_range + x2_range)))

        P_total = x_range * gamma1 * P1_0 + x2_range * gamma2 * P2_0
        y1_calc = (x_range * gamma1 * P1_0) / P_total
        y2_calc = (x2_range * gamma2 * P2_0) / P_total
        assert np.allclose(y1_calc + y2_calc, 1), "y1 + y2 должно быть равно 1"

        return x_range, x2_range, y1_calc, y2_calc, P_total

    def plot_diagrams(self):
        x_range, x2_range, y1_calc, y2_calc, P_total = self.calculate_vle()

        plt.figure(figsize=(15, 6))

        plt.subplot(1, 2, 1)
        plt.plot(x_range, y1_calc, label='Calculated y1')
        plt.plot(x_range, x_range, label='x = y', color='black', linestyle='--')
        plt.scatter(self.x1, self.y1, color='red', label='Experimental Data')
        plt.xlabel('Mole Fraction of Acetone in Liquid (x1)')
        plt.ylabel('Mole Fraction of Acetone in Vapor (y1)')
        plt.title('y-x Diagram for Acetone + n-Hexane at T = 298.15 K')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(x_range, P_total, label='Calculated Pressure', color = "blue")
        plt.plot(y1_calc, P_total, label='Calculated Pressure', color = "blue")
        plt.scatter(self.x1, self.P, color='red', label='Experimental Data')
        plt.fill_betweenx(P_total, x_range, y1_calc, color='green', alpha=0.5, label='Double phase area')
        # plt.fill_betweenx(P_total, np.maximum(x_range, y1_calc), 1, color='lightblue', alpha=0.2, label='High Pressure')
        # plt.fill_betweenx(P_total, 0, np.minimum(x_range, y1_calc), color='lightcoral', alpha=0.2, label='Low Pressure')
        plt.xlabel('Mole Fraction of Acetone in Liquid (x1)')
        plt.ylabel('Pressure (bar)')
        plt.title('P-xy Diagram for Acetone + n-Hexane at T = 298.15 K')
        plt.legend()
        plt.grid(True)

        # plt.subplot(2, 2, 3)
        # plt.plot(x2_range, y2_calc, label='Calculated y2')
        # # plt.plot(x2_range, y2_calc, label='P(x2) — Liquid Phase', color='green', linestyle='-.')
        # plt.scatter(self.x1, self.y1, color='red', label='Experimental Data')
        # plt.xlabel('Mole Fraction of Acetone in Liquid (x2)')
        # plt.ylabel('Mole Fraction of Acetone in Vapor (y2)')
        # plt.title('y-x Diagram for Acetone + n-Hexane at T = 298.15 K')
        # plt.legend()
        # plt.grid(True)
        #
        # plt.subplot(2, 2, 4)
        # plt.plot(x2_range, P_total, label='Calculated Pressure')
        # plt.plot(y2_calc, P_total, label='Calculated Pressure')
        # plt.scatter(self.x1, self.P, color='red', label='Experimental Data')
        # plt.xlabel('Mole Fraction of Acetone in Liquid (x2)')
        # plt.ylabel('Pressure (bar)')
        # plt.title('P-x Diagram for Acetone + n-Hexane at T = 298.15 K')
        # plt.legend()
        # plt.grid(True)

        plt.tight_layout()
        plt.show()

T = 298.15
x1 = [0.100, 0.300, 0.500, 0.700, 0.900]
y1 = [0.402, 0.536, 0.620, 0.635, 0.782]
P = [0.3065, 0.3680, 0.3832, 0.3850, 0.3604]
A1, B1, C1 = 16.65, 2940.4, -35.93
A2, B2, C2 = 15.84, 2697.55, -48.78

# Создание экземпляра класса и выполнение расчетов
vle_model = VLEModel(T, x1, y1, P, A1, B1, C1, A2, B2, C2)
vle_model.calculate_activity_coefficients()
vle_model.optimize_wilson_parameters()
vle_model.plot_diagrams()
vle_model.print_results()