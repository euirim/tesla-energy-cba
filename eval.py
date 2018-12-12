import math
import numpy as np
import pandas as pd

def FtoC(temp):
	return (temp - 32) * 5 / 9

def calc_price_normal(I, tax_credit, watt_discount, A, usage_ph):

	area = A * 10.76 # convert to feet squared
	discounted = 0 
	r = 0.0269

	generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
	#F = 0
	if (generated > usage_ph):
		F = usage_ph / generated
	else:
		F = 1


	for i in range(0, 9):
		discounted += (1 / (1 + r)) ** i

		final = ((1 - tax_credit) * (21.85 * F * area + 2 * 8700 + discounted * (500 + 300)) - watt_discount * 200 * F * area * 0.197) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.9)
	return final


def calc_price_low(I, tax_credit, watt_discount, A, usage_ph):

	area = A * 10.76 # convert to feet squared
	discounted = 0
	r = 0.0269

	generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
	if (generated > usage_ph):
		F = usage_ph / generated
	else:
		F = 1

	for i in range(0, 11):
		discounted += (1 / (1 + r)) ** i


	final = ((1 - tax_credit) * (21.85 * F * area + 2 * 7200 + discounted * (100 + 100)) - watt_discount * 200 * F * area * 0.197) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.9)
	return final

def calc_price_lease_low(I, A, usage_ph):

	area = A * 10.76
	discounted = 0
	r = 0.0269
	s = 0

	generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
	if (generated > usage_ph):
		F = usage_ph / generated
	else:
		F = 1

	for i in range(0, 9):
		s += (1 + 0.029) ** i
		discounted += (1 / (1 + r)) ** i

	final = (25 * 12 * s + 2 * 7200 + discounted * (100 + 100)) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.9)
	return final

def calc_price_lease_normal(I, A, usage_ph):

        area = A * 10.76
        discounted = 0
        r = 0.0269
        s = 0

        generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
        if (generated > usage_ph):
                F = usage_ph / generated
        else:
                F = 1

        for i in range(0, 9):
                s += (1 + 0.029) ** i
                discounted += (1 / (1 + r)) ** i

        final = (125 * 12 * s + 2 * 8700 + discounted * (500 + 300)) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.9)
        return final

def calc_price_lease_high(I, A, usage_ph):

        area = A * 10.76
        discounted = 0
        r = 0.0269
        s = 0

        generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
        if (generated > usage_ph):
                F = usage_ph / generated
        else:
                F = 1

        for i in range(0, 9):
                s += (1 + 0.029) ** i
                discounted += (1 / (1 + r)) ** i

        final = (250 * 12 * s + 2 * 11700 + discounted * (1000 + 500)) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.8)
        return final

def calc_price_high(I, tax_credit, watt_discount, A, usage_ph):

	area = A * 10.76
	discounted = 0
	r = 0.0269

	generated = 365 * area * 0.093 * discounted * I * 0.197 * 0.9
	if (generated > usage_ph):
		F = usage_ph / generated
	else:
		F = 1

	for i in range(0, 11):
		discounted += (1 / (1 + r)) ** i

	final = ((1 - tax_credit) * (21.85 * F * area + 2 * 11700 + discounted * (1000 + 500)) - watt_discount * 200 * F * area * 0.197) / (365 * F * area * 0.093 * discounted * I * 0.197 * 0.9)
	return final

def price_helper(base, rate, years):
	s = 0
	for i in range(0, years):
		s += base * ((1 + rate) ** years)	
	return s / years

state_df = pd.read_csv("~/Downloads/state-usage.csv")
df = pd.read_csv("~/Downloads/preprocessed_data.csv")
df['mean_annual_dni']=df['mean_annual_dni'].replace(0,df['mean_annual_dni'].mean())
df = df.fillna(method='ffill')
df = pd.merge(df, state_df, on='state_name')

#df = df.fillna(method='ffill')
#df = df.fillna(df.mean())
df['mean_annual_dni'] = df['mean_annual_dni'].replace(to_replace=0, method='ffill')

#df['interpolate'] = (df['avg_price_per_kwh_2017'] - df['avg_price_per_kwh_2013']) * 2 + df['avg_price_per_kwh_2017']  
df = df.fillna(method='ffill')
#df.to_csv("output.csv")
#df['low'] = df.apply(lambda row: calc_price_low(row.mean_annual_dni, 0), axis = 1)
df['low_no_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_high(row.mean_annual_dni, 0, 0, row.roof_area_in_msq,float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['low_fed_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_high(row.mean_annual_dni, 0.1, 0, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['low_fed_state_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_high(row.mean_annual_dni, 0.1, 0.2, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['low_lease'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_lease_high(row.mean_annual_dni, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['normal_no_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_normal(row.mean_annual_dni, 0, 0, row.roof_area_in_msq,float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['normal_fed_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_normal(row.mean_annual_dni, 0.1, 0, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['normal_fed_state_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_normal(row.mean_annual_dni, 0.1, 0.2, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['normal_lease'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_lease_normal(row.mean_annual_dni, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['high_no_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_low(row.mean_annual_dni, 0, 0, row.roof_area_in_msq,float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['high_fed_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_low(row.mean_annual_dni, 0.1, 0, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['high_fed_state_incentive'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_low(row.mean_annual_dni, 0.1, 0.2, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)
df['high_lease'] = df.apply(lambda row: price_helper(row['avg_price_per_kwh_2017'], 0.04, 8) - calc_price_lease_low(row.mean_annual_dni, row.roof_area_in_msq, float(row.kWh_capita.replace(',', '')) * 2.58), axis = 1)

#df['high'] = df.apply(lambda row: calc_price_high(row.mean_annual_dni, 0), axis = 1)
#df = df.fillna(method='ffill')
df.to_csv("output.csv")
