#CandidateId:8498378

Here is the steps by step approach to have a general idea how the api works.

This application is developed Visual Studio Code

Code structure
    Models.py - Contains all the required models this assignment. It contains the following class
            - AverageMetricDto: Used to collect the Metrics value from the API
            - MetricDto: Contains common fields from all metrics, that is people and prevalence 
            - MetricsDto: MericsDto contains metric value in MetricDto format for five metric categories
            - ConvertedDto: This is a converted in a format of country and its metrics
            - ApiResponseDto: This is a presentable DTO to the browser
    MetricsController.py: This is where the processing of conversion and processing and calculation done. 
        - convertToResponseDto: Convert the raw data that is get from the api to the desired ConvertedDto format.
        - calculate_average_monthly_value: Perform monthly calculation foreach metric
        - calculate_daily_national_estimate: Process the daily national estimate for fcs prevalence
    app.py
        Main pyton to run and consume the api.It has the following definitions.
        - fetchDataFromApi: A reusable component to fetch data from the api. If not successfully, generate the apprpriate error message.
        - isDateValid: A re-usable definition to validate the dates provided stays withing the range specified.
        - getYearFromDate: helper to get a year from date.
    return date.split("-")[0]
        - get_average_monthly_value_metrics_a: API end point to get the average monthly value for the specifc country withing the date range.
        - calculate_daily_national_estimate_metrics_b: API end point to get daily national estimate along with the variance for the specifc country withing the date range.
        - calculate_variance_for_daily_national_estimate_metrics_b: An additional API end point to get the variance.

Deployment 
    -Get the three files (Models.py,MetricsController.py, app.py) above in your python IDE and make sure you keep the reference to each other.
    -In Visual Studio Code, run python app.py to start the webserver.
    -Then use the following link to access API.
        - get_average_monthly_value_metrics_a
            :- http://127.0.0.1:8000/api/metric_a/country/col/2022-06-01/2023-07-01
        - calculate_daily_national_estimate_metrics_b
        -   :-http://127.0.0.1:8000/api/metric_b/country/bfa/2022-06-01/2023-07-01
        - calculate_variance_for_daily_national_estimate_metrics_b
            :- http://127.0.0.1:8000/api/variance_metric_b/country/bfa/2022-06-01/2023-07-01