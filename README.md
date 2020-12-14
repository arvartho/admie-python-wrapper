# AdmieDataCollector
A Python wrapper for the ADMIE data collection API

>[ADMIE](https://www.admie.gr/en/) is Greece's official Independent Power Transmission Operator (IPTO). The mission of ADMIE is the operation, control, maintenance and development of the Hellenic Electricity Transmission System, to ensure the country’s supply with electricity in an adequate, safe, efficient and reliable manner, as well as the operation of the electricity market for transactions outside the Day Ahead Scheduling, pursuant to the principles of transparency, equality and free competition.

ADMIE offers an [official API](https://www.admie.gr/en/market/market-statistics/file-download-api) for downloading data related to the day to day operations of the operator. This wrapper is used to cquery to the ADMIE API and save locally files from the response. 

## Usage

The wrapper is called from any shell with minor dependancies that are covered by Anaconda distribution. 

Here is an example of executing the wrapper:

```
$ python AdmieDataCollector.py  -s 2020-11-10 -e 2020-11-20 -t ISP1DayAheadLoadForecast -d . 
```

The line above will download all the files of type `ISP1DayAheadLoadForecast` for dates starting from `2020-11-10` to `2020-11-20` and save them to the current directory.

The following can be passed as arguments to the wrapper:
* -s | --startDate: starting date for the query with format YYYY-MM-DD
* -e | --endDate: ending date for the query with format YYYY-MM-DD
* -d | --destDir: destination directory, where the files will be stored
* -t | --type: according to the ADMIE API the available file types are the following with the addition of `info` that is used for display purposes:

```['AdhocISPResults', 'CurrentLineOutages', 'CurrentProtectionOutages', 
'CurrentSubstationOutages', 'DailyAuctionsSpecificationsATC', 'DailyEnergyBalanceAnalysis', 
'DayAheadLoadForecast', 'DayAheadRESForecast', 'DayAheadSchedulingRealTimeDeviations', 
'DayAheadSchedulingRequirements', 'DayAheadSchedulingUnitAvailabilities', 'Devit', 
'Devnor', 'DispatchSchedulingResults', 'ExPostImbalancePricingResults', 'HVCUSTCONS', 
'IMBABE', 'InterconnectionsMaintenanceSchedule', 'IntraDayDispatchSchedulingResults', 
'ISP1DayAheadLoadForecast', 'ISP1DayAheadRESForecast', 'ISP1ISPResults', 'ISP1Requirements', 
'ISP1UnitAvailabilities', 'ISP2DayAheadLoadForecast', 'ISP2DayAheadRESForecast', 'ISP2ISPResults', 
'ISP2Requirements', 'ISP2UnitAvailabilities', 'ISP3IntraDayLoadForecast', 'ISP3IntraDayRESForecast', 
'ISP3ISPResults', 'ISP3Requirements', 'ISP3UnitAvailabilities', 'ISP4Requirements', 
'ISPWeekAheadLoadForecast', 'LTPTRsNominationsSummary', 'MonthlyLoadForecast', 'MonthlyNTC',
'MonthlySIPResults', 'ProvisionalLineOutages', 'ProvisionalProtectionOutages', 
'ProvisionalSubstationOutages', 'RealTimeSCADAImportsExports', 'RealTimeSCADARES', 
'RealTimeSCADASystemLoad', 'recovery_cost', 'ReservoirFillingRate', 'RESMV', 'RESMVLVPROD',
'SignificantEvents', 'SYSBOUNDS', 'SystemEstimationsCorrections', 'SystemRealizationSCADA', 
'UA_ANALYSIS', 'UnitAvailabilities', 'UnitProduction', 'UnitsMaintenanceSchedule', 
'WeekAheadLoadForecast', 'WeekAheadWaterUsageDeclaration', 'YearlyLoadForecast', 
'YearlyWaterUsageDeclaration']
```

The `info` value is the only acceptable file type value for the `--type` argument, outside of the ADMIE API, and is used to display information for each acceptable file type value. For instance:

```
$ python AdmieDataCollector.py -t info

Available file types:

         * type: "AdhocISPResults"
            - description: Ημερήσια Αποτελέσματα ΔΕΠ / Daily ISP Results
            - when:



         * type: "CurrentLineOutages"
            - description: Ετήσια Τρέχον Πρόγραμμα Συντήρησης Γραμμών Μεταφοράς / Yearly Current Transmission Lines Outage Planning
            - when:



         * type: "CurrentProtectionOutages"
            - description: Ετήσια Τρέχον Πρόγραμμα Συντήρησης Προστασίας / Yearly Current Protection Outage Planning
            - when:



         * type: "CurrentSubstationOutages"
            - description: Ετήσια Τρέχον Πρόγραμμα Συντήρησης Υποσταθμών / Yearly Current Substations  Outage Planning
            - when:



         * type: "DailyAuctionsSpecificationsATC"
            - description: Ημερήσια Διαθέσιμη Ικανότητα Μεταφοράς ATC / Daily ATC
            - when: 23:00:00



         * type: "DailyEnergyBalanceAnalysis"
            - description:  Ενεργειακό Ισοζύγιο /  Energy Balance
            - when:



         * type: "DayAheadLoadForecast"
            - description: 2 φορές την ημέρα και όποτε άλλοτε χρειαστεί Πρόβλεψη Φορτίου / Twice a day and on demand Load Forecast
            - when: 09:00 και 11:00
```
---

## TODO
* Add option to export data as CSV
   1. Add handle for the most popular ADMIE file types
   2. Collect all files in the selected directory according to ADMIE file type
   3. Open excel files with pandas
   4. Format and transform data
   5. Save to CSV

   