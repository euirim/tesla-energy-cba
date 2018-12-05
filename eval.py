import math

def FtoC(temp):
	return (temp - 32) * 5 / 9

def calc_price_normal(theta, n, T_f):
	T_c = FtoC(T_f)
	theta_rad = math.radians(theta)

	discounted = 0 
	r = 0.0269

	for i in range(0, 11):
		discounted += (1 / (1 + r)) ** i


	I = 127 * (0.768 ** (1 / math.cos(theta_rad))) * math.cos(theta_rad) / 0.768
	E_wh = (1 - 0.75 * (n ** 3)) * (1 - (T_c + 273 - 294) / 249)


	final = (21.85 * 3000 + 8700 + discounted * (500 + 300)) / (2.78 * (10 ** (-7)) * 365 * 3000 * discounted * 0.85 * 44640 * 0.24 * I * E_wh)
	return final


def calc_price_low(theta, n, T_f):
	T_c = FtoC(T_f)
        theta_rad = math.radians(theta)

        discounted = 0
        r = 0.0269

        for i in range(0, 11):
                discounted += (1 / (1 + r)) ** i


        I = 127 * (0.768 ** (1 / math.cos(theta_rad))) * math.cos(theta_rad) / 0.768
        E_wh = (1 - 0.75 * (n ** 3)) * (1 - (T_c + 273 - 294) / 249)


        final = (21.85 * 4500 + 7200 + discounted * (100 + 100)) / (2.78 * (10 ** (-7)) * 365 * 4500 * discounted * 0.925 * 44640 * 0.24 * I * E_wh)
        return final


def calc_price_high(theta, n, T_f):
	T_c = FtoC(T_f)
        theta_rad = math.radians(theta)

        discounted = 0
        r = 0.0269

        for i in range(0, 11):
                discounted += (1 / (1 + r)) ** i


        I = 127 * (0.768 ** (1 / math.cos(theta_rad))) * math.cos(theta_rad) / 0.768
        E_wh = (1 - 0.75 * (n ** 3)) * (1 - (T_c + 273 - 294) / 249)


        final = (21.85 * 1500 + 11700 + discounted * (1000 + 500)) / (2.78 * (10 ** (-7)) * 365 * 1500 * discounted * 0.775 * 44640 * 0.24 * I * E_wh)
        return final

theta = 47.6 # latitude in degrees
n = 0.587 # cloud cover
T_f = 59.5 # temperature in F

print(calc_price_low(theta, n, T_f))
print(calc_price_normal(theta, n, T_f))
print(calc_price_high(theta, n, T_f))
