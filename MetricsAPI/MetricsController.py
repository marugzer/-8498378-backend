#CandidateId:8498378

import json
from datetime import datetime
from dataclasses import dataclass
import calendar

from flask import Flask, jsonify, request
from models import AverageMetricDto, MetricDto,ConvertedDto,MetricsDto,ApiResponseDto
import statistics


class MetricsController:        
    def __init__(self, data):
        self.data = data   
        
    def convertToResponseDto(self, data):
        # Extract nested dictionary safely
        metrics_data = data.get("metrics", {})
        fcs_data = metrics_data.get("fcs", {})
        rcsi_data = metrics_data.get("rcsi", {})
        health_data = metrics_data.get("healthAccess", {})
        market_data = metrics_data.get("marketAccess", {})
        livelihood_data = metrics_data.get("livelihoodCoping", {})

        metrics = MetricsDto(
            Fcs=MetricDto(People=fcs_data.get("people", 0), Prevalence=fcs_data.get("prevalence", 0.0)),
            Rcsi=MetricDto(People=rcsi_data.get("people", 0), Prevalence=rcsi_data.get("prevalence", 0.0)),
            HealthAccess=MetricDto(People=health_data.get("people", 0), Prevalence=health_data.get("prevalence", 0.0)),
            MarketAccess=MetricDto(People=market_data.get("people", 0), Prevalence=market_data.get("prevalence", 0.0)),
            LivelihoodCoping=MetricDto(People=livelihood_data.get("people", 0), Prevalence=livelihood_data.get("prevalence", 0.0))
        )
        convertedDto =ConvertedDto(
            Country=data.get("country", {}),            
            Date=data.get("date", ""),            
            Metrics=metrics
        )
        return convertedDto
        
    def calculate_average_monthly_value(self,country, start_date, end_date):

        survey_data = [self.convertToResponseDto(data) for data in self.data]
        
        print(len(survey_data))

        average_monthly_metrics = {}
        ordered_data = sorted(survey_data, key=lambda x: x.Date)

        for data in ordered_data:                
            date = datetime.strptime(data.Date, "%Y-%m-%d")
            month_year_key = date.strftime("%Y-%m")

            if month_year_key not in average_monthly_metrics:
                average_monthly_metrics[month_year_key] = AverageMetricDto()

            average_monthly_metrics[month_year_key].Fcs += data.Metrics.Fcs.People
            average_monthly_metrics[month_year_key].Rcsi += data.Metrics.Rcsi.People
            average_monthly_metrics[month_year_key].HealthAccess += data.Metrics.HealthAccess.People
            average_monthly_metrics[month_year_key].MarketAccess += data.Metrics.MarketAccess.People
            average_monthly_metrics[month_year_key].LivelihoodCoping += data.Metrics.LivelihoodCoping.People

        # Calculate the average for each month
        for month_year_key in average_monthly_metrics.keys():
            total_days_in_month = 32 - datetime.strptime(month_year_key, "%Y-%m").day
            year, month = map(int, month_year_key.split('-'))
            total_days_in_month = calendar.monthrange(year, month)[1]

            average_monthly_metrics[month_year_key].MonthYear = month_year_key
            average_monthly_metrics[month_year_key].Fcs /= total_days_in_month
            average_monthly_metrics[month_year_key].Fcs /= total_days_in_month
            average_monthly_metrics[month_year_key].Rcsi /= total_days_in_month
            average_monthly_metrics[month_year_key].HealthAccess /= total_days_in_month
            average_monthly_metrics[month_year_key].MarketAccess /= total_days_in_month
            average_monthly_metrics[month_year_key].LivelihoodCoping /= total_days_in_month
    
        apiResponseDto = ApiResponseDto(Country=country, StartDate=start_date, EndDate=end_date)
        apiResponseDto.ResultMetrics= average_monthly_metrics            
        return apiResponseDto       
    
    def calculate_daily_national_estimate(self,country, start_date, end_date):
        daily_fcs_prevalence = {}
        ordered_data =sorted(self.data, key=lambda x: x["date"])

        for data in ordered_data:
            date_val = data["date"]
            prevalence  = data["metrics"]["fcs"]["prevalence"]
            if date_val in daily_fcs_prevalence:
                daily_fcs_prevalence[date_val].append(prevalence)
            else:
                daily_fcs_prevalence[date_val] = [prevalence]

        print(len(daily_fcs_prevalence))
        
        #Calculate the average FCS prevalence for each day
        daily_national_estimate_prevalence = {}

        for date_val, prevalences in daily_fcs_prevalence.items():
            average_prevalence = sum(prevalences) / len(prevalences)
            daily_national_estimate_prevalence[date_val] = average_prevalence

        daily_fcs_prevalence_list = list(daily_national_estimate_prevalence.values())

        variance_fcs_prevalence = statistics.variance(daily_fcs_prevalence_list)

        apiResponseDto = ApiResponseDto(Country=country, StartDate=start_date, EndDate=end_date)
        apiResponseDto.variance = variance_fcs_prevalence
        apiResponseDto.ResultMetrics= daily_national_estimate_prevalence

        return apiResponseDto    

# ##test metric-a for bfa
# api_url = "https://api.hungermapdata.org/v1/foodsecurity/country/bfa/region?date_start=2022-06-01&date_end=2023-07-01"        
# # #metric_data = fetch_data_from_api(api_url)
# file_path = 'bfa.json'        
# with open(file_path, 'r') as file:
#     metric_data = json.load(file)

# controller = MetricsController(metric_data)
# country="bfa"
# start_date="2022-06-01"
# end_date="2023-07-01"
# result = controller.calculate_average_monthly_value(country, start_date, end_date)
# for month, metrics in result.ResultMetrics.items():
#             formatted_data = {
#                 "name": month,
#                 "Fcs": metrics.Fcs,
#                 "HealthAccess": metrics.HealthAccess,
#                 "LivelihoodCoping": metrics.LivelihoodCoping,
#                 "MarketAccess": metrics.MarketAccess,
#                 "Rcsi": metrics.Rcsi
#             }

# api_response_data = {            
#     "Country": country,
#     "StartDate": start_date,
#     "EndDate": end_date,         
#     "MetricA": []              
#     #"MetricsA" :grouped_metrics_by_year
# }             
# api_response_data["MetricA"].append(formatted_data)

# api_response_json = json.dumps(api_response_data, indent=4)
# # Print the JSON data
# print(api_response_json)


#////////////////////////////////////////

#test metric- b for bfa
# api_url = "https://api.hungermapdata.org/v1/foodsecurity/country/bfa/region?date_start=2022-06-01&date_end=2023-07-01"        
# #metric_data = fetch_data_from_api(api_url)
file_path = 'bfa.json'        
with open(file_path, 'r') as file:
    metric_data = json.load(file)

controller = MetricsController(metric_data)
country="bfa"
start_date="2022-06-01"
end_date="2023-07-01"
result = controller.calculate_daily_national_estimate(country, start_date, end_date)
api_response_data = {            
            "Country": country,
            "StartDate": start_date,
            "EndDate": end_date,    
            "Variance" : result.variance,         
            "MetricsA" :[]
        }
for year, metrics in result.ResultMetrics.items():
                 formatted_data = {
                    "name": year,
                    #"Fcs": metrics.Fcs,
                    #"HealthAccess": metrics.HealthAccess,                    
                 }
# Convert the dictionary to JSON format
api_response_json = json.dumps(api_response_data, indent=4)
# Print the JSON data
print(api_response_json)