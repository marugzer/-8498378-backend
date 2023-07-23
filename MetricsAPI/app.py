#CandidateId:8498378

import requests
import json
from itertools import groupby

from flask import Flask, jsonify, request
from MetricsController import MetricsController
from datetime import datetime, timedelta


def fetchDataFromApi(api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Check for any request errors
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch data from the API: {e}")
        
def isDateValid(start_date_str, end_date_str):
    today = datetime.now().date()
    startdate = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    enddate = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    mindate = today - timedelta(days=500)
    
    startValidation = startdate >= mindate and startdate <= today
    endValidation = enddate >= mindate and enddate <= today
    
    return startValidation and endValidation

def getYearFromDate(date):
    return date.split("-")[0]

app = Flask(__name__)
#output the average monthly value for each value
@app.route('/api/metric_a/country/<string:country>/<start_date>/<end_date>', methods=['GET'])
def get_average_monthly_value_metrics_a(country, start_date, end_date):   
     if  not isDateValid(start_date, end_date):    
          return jsonify("Invalid date range. Start date should not be before 500 days ago, and end date should not be later than today.")
     else:
        try:
            api_url = f"https://api.hungermapdata.org/v1/foodsecurity/country/{country}/region?date_start={start_date}&date_end={end_date}"       
            metric_data = fetchDataFromApi(api_url)
            controller = MetricsController(metric_data)
            result = controller.calculate_average_monthly_value(country, start_date, end_date)
            api_response_data = {            
                "Country": country,
                "StartDate": start_date,
                "EndDate": end_date,         
                "MetricA": [] 
            }   
            # Loop through each month in the result.ResultMetrics and format the data
            for month, metrics in result.ResultMetrics.items():
                 formatted_data = {
                    "name": month,
                    "Fcs": metrics.Fcs,
                    "HealthAccess": metrics.HealthAccess,
                    "LivelihoodCoping": metrics.LivelihoodCoping,
                    "MarketAccess": metrics.MarketAccess,
                    "Rcsi": metrics.Rcsi
                 }
                 api_response_data["MetricA"].append(formatted_data)

            return jsonify(api_response_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#outout daily national estimate for the Fcs prevalance and also the variance of this metric
@app.route('/api/metric_b/country/<string:country>/<start_date>/<end_date>', methods=['GET'])
def calculate_daily_national_estimate_metrics_b(country, start_date, end_date):
    if  not isDateValid(start_date, end_date):    
          return jsonify("Invalid date range. Start date should not be before 500 days ago, and end date should not be later than today.")
    else:
        try:
            api_url = f"https://api.hungermapdata.org/v1/foodsecurity/country/{country}/region?date_start={start_date}&date_end={end_date}"       
            metric_data = fetchDataFromApi(api_url)

            controller = MetricsController(metric_data)        
            result = controller.calculate_daily_national_estimate(country, start_date, end_date)
            grouped_metrics = [
                {"Date": date, "Daily national estimate": value}
                for date, value in result.ResultMetrics.items()
            ]
            grouped_metrics.sort(key=lambda x: x["Date"])  # Sort by date
            grouped_metrics_by_year = {
                year: list(data)
                for year, data in groupby(grouped_metrics, key=lambda x: getYearFromDate(x["Date"]))
            }
            api_response_data = {            
                "Country": country,
                "StartDate": start_date,
                "EndDate": end_date, 
                "Variance" : result.variance,
                #"MetricsB" :grouped_metrics
                "MetricsB" :grouped_metrics_by_year
            }
            return jsonify(api_response_data)     
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500


#Output the variance. This is added if needed, but there is an output for variance on metric B when we
#calcuate the daily national estimate for the fcs prevalence
@app.route('/api/variance_metric_b/country/<string:country>/<start_date>/<end_date>', methods=['GET'])
def calculate_variance_for_daily_national_estimate_metrics_b(country, start_date, end_date):    
    if  not isDateValid(start_date, end_date):    
          return jsonify("Invalid date range. Start date should not be before 500 days ago, and end date should not be later than today.")
    else:
        try:
            api_url = f"https://api.hungermapdata.org/v1/foodsecurity/country/{country}/region?date_start={start_date}&date_end={end_date}"       
            metric_data = fetchDataFromApi(api_url)
            controller = MetricsController(metric_data)   
            
            result = controller.calculate_daily_national_estimate(country, start_date, end_date)
            api_response_data = {            
                    "Country": country,
                    "StartDate": start_date,
                    "EndDate": end_date, 
                    "Variance" : result.variance,            
            }
            return jsonify(api_response_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)


