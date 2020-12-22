import os
import json
import csv
import time
import requests
import argparse
import datetime
from tqdm import tqdm

class AdmieDataCollector():

   def __init__(self):
      # API query variables
      self.baseQueryURL = 'https://www.admie.gr/getOperationMarketFilewRange'
      self.fileInfoURL = 'https://www.admie.gr/getFiletypeInfo'
      self.all_filetypes = ['AdhocISPResults', 'CurrentLineOutages', 'CurrentProtectionOutages', 
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
      self.downloadedFiles = {'date': [], 'filepath': [], 'description': []}

      # Initialize argument parser      
      self.parser = argparse.ArgumentParser(description='Wraps the ADMIE data collection API', prog='ADMIE API Wrapper')
      self.parser.add_argument('-s','--startDate', type=datetype, help='''Select start date for the query, date format: YYYY-MM-DD''')
      self.parser.add_argument('-e','--endDate', type=datetype, help='''Select end date for the query, date format: YYYY-MM-DD''')
      self.parser.add_argument('-d','--destDir', help='''Select directory to save the data''')      
      self.parser.add_argument('-f','--file', help='''Select a file as input for executing batch API queries. The file should be CSV file with have the following format:
         startDate1,endDate1,filetype1
         startDate2,endDate2,filetype2
         ...
         startDateN,endDateN,filetypeN
         ''')      
      self.parser.add_argument('-t','--type', help='''Select file type from the available file types according to the ADMIE API:''', 
            choices=self.all_filetypes + ['info'])

      self.parser.add_argument('--version', action='version', version='%(prog)s  1.0')
      self.args = self.parser.parse_args()
      # Apply argument constrains
      self.checkArgConstrains()
   

   # Executes the API queries
   def run(self,): 
      if self.args.file and os.path.isfile(self.args.file):
         self.executeBatchQuery()
      else:
         self.executeQuery()


   # Query process
   def executeQuery(self, params={}):      
      if not params:
         params = {'dateStart': self.args.startDate,
                   'dateEnd': self.args.endDate,
                   'FileCategory': self.args.type}

      if 'info' in params['FileCategory']:
         self.showAllFileTypes()
      else:
         self.checkApiParams(params)
         req = requests.get(self.baseQueryURL, params=params)
         self.downloadFiles(req)      
      

   # Batch query process
   def executeBatchQuery(self,):
      with open(self.args.file, 'r') as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=',')
         for i,row in enumerate(csv_reader, start=1):
            try:
               params = {'dateStart': row[0],
                         'dateEnd': row[1],
                         'FileCategory': row[2]}
               self.executeQuery(params=params)
            except:
               self.parser.error('\nATTENTION: Error in CSV file format in line %s' % i)


   # Check query parameters constrains      
   def checkApiParams(self, params):
      datetype(params['dateStart'])
      datetype(params['dateEnd'])
      if params['FileCategory'] not in self.all_filetypes:
         raise Exception()


   # Check argument constrains      
   def checkArgConstrains(self,):
      if self.args.file:         
         self.checkConfigFileConstains()

      if self.args.startDate or self.args.endDate:
         self.checkDateConstains()

      if list(self.args.__dict__.values()) == [None, None, None, None, None]:
         self.parser.error('\nATTENTION: No arguments were selected')

   # Check date argument constrains
   def checkDateConstains(self,):
      if self.args.startDate and not self.args.endDate:
         self.parser.error('\nATTENTION: -e/--endDate is required when -s/--startDate is set.')
      if self.args.endDate and not self.args.startDate:
         self.parser.error('\nATTENTION: -s/--startDate is required when -e/--endDate is set.')
      if self.args.endDate < self.args.startDate:
         self.parser.error('\nATTENTION: Start date cannot be after end date')


   # Check input file argument constrains
   def checkConfigFileConstains(self,):
      if self.args.startDate or self.args.endDate or self.args.type:
            self.parser.error('\nATTENTION: Only destination (-d|--destDir) argument is needed with input file (-f|--file) argument')
      if not os.path.isfile(self.args.file):
         self.parser.error('\nATTENTION: File does not exist')
         

   # Display all file types and available information
   def showAllFileTypes(self,):
      # Fetch request
      jsonResp = requests.get(self.fileInfoURL).json()
      print('Available file types:')
      for element in jsonResp:
         filetype = element['filetype']
         time_gate = element['EN'][0]['time_gate']

         publication_frequencyGR = element['GR'][0]['publication_frequency']
         publication_frequencyEN = element['EN'][0]['publication_frequency']

         data_typeGR = element['GR'][0]['data_type']
         data_typeEN = element['EN'][0]['data_type']

         print('''
         * type: "%s"
            - description: %s %s / %s %s
            - when: %s

         ''' % (filetype, 
                publication_frequencyGR, data_typeGR,
                publication_frequencyEN, data_typeEN,
                time_gate))


   # Download query results   
   def downloadFiles(self, req):
      # Begin counting
      start_time = time.time() 

      jsonResp = req.json() 
      # Create destination path
      destDir = self.args.destDir      
      if not os.path.exists(destDir):
         os.makedirs(destDir)

      if len(jsonResp) == 0:
         print('No results found for request: %s' % req.url)
      else:
         print('Starting files downloading...')
         processBar = tqdm(jsonResp)
         for element in processBar:            
            try:
               # element attributes
               url = element['file_path']
               description = element['file_description']
               
               # file destination
               filename = url.split('/')[-1]
               filepath = os.path.join(destDir, filename)
               
               # initiate file request
               processBar.set_description("  Downloading file: %s" % filename)
               req = requests.get(url, allow_redirects=True)

               # save file locally
               with open(filepath, 'wb') as f:
                  f.write(req.content)
                  self.downloadedFiles['filepath'].append(filepath)
                  self.downloadedFiles['description'].append(description)
                  self.downloadedFiles['date'].append(filename.split('_')[0])

            except Exception as e:
               print('Error in request: %s' % str(e))
      print("--- Finished in %s seconds ---" % round(time.time() - start_time, 2))


# Handle date type arguments
def datetype(dateString):
   try:
      date = datetime.datetime.strptime(dateString, '%Y-%m-%d')  # accept only dates with specific format
   except:
      print('Error for value %s. -s/--startDate and -e/--endDate arguments have to follow the format YYYY-MM-DD' % dateString)
   return date


if __name__ == "__main__":
   admie = AdmieDataCollector()
   admie.run()
