import apache_beam as beam
import json
from datetime import datetime

class CheckAbandonedCartsFn(beam.DoFn):
# Implements the verification of abandoned carts

  def process(self, element):

    abandonments = []
    firstTimestamp = True # flag to indicate that no timestamp was read
    lastTimestamp = None # variable to hold the last read timestamp
    currentBasket = [] # variable to hold the current product in the basket
    gap = 0 # indicates the gap between consecutive events from the same user

    for event in element[1]:

        presentTimestamp = datetime.strptime(event["timestamp"], '%Y-%m-%d %H:%M:%S') # converting the timestamp string to standard format

        if(not firstTimestamp):
            # calculate the seconds between two events
            gap = (presentTimestamp - lastTimestamp).seconds

            if(gap >= 600 and currentBasket): # 600 s = 10 min; flow is interrupted with a product in the cart

                #abandoned cart!
                abandonment = {}
                abandonment["timestamp"] = event["timestamp"] # it is a string; does not require treatment
                abandonment["customer"] = element[0]
                abandonment["product"] = ', '.join(currentBasket)
                abandonment = json.dumps(abandonment)

                abandonments.append(abandonment)

                # abandonment format
                # { "timestamp": "2019-01-01 14:20:00", "customer": "customer-3", "product": "product-4" }

                # clean up
                firstTimestamp = True
                currentBasket = []
                gap = 0

            elif(event["page"] == "basket"):
                currentBasket.append(event["product"]) # a cart can hold one or more items

            elif(event["page"] == "checkout"):
                # clean up (completed purchase)
                firstTimestamp = True
                currentBasket = []
                gap = 0

        firstTimestamp = False
        lastTimestamp = presentTimestamp
#        abandonments.append('a')

    if currentBasket: # if it is not empty, it was abandoned

        abandonment = {}
        abandonment["timestamp"] = lastTimestamp.strftime('%Y-%m-%d %H:%M:%S') # it is a datetime; requires a conversion
        abandonment["customer"] = element[0]
        abandonment["product"] = ', '.join(currentBasket)
        abandonment = json.dumps(abandonment)

        abandonments.append(abandonment)

    yield abandonments

inputs = 'input/*'
output = 'output/abandoned-carts.json'

with beam.Pipeline() as pipeline:
  (
      pipeline
      | "Read lines" >> beam.io.ReadFromText(inputs)
      # output: lines (str)
      | "Find events" >> beam.Map( lambda line: ( json.loads(line)["customer"], json.loads(line) ) )
      # output: [(str, {str: str, str: str, ...}), ...]
      | "Group events per customer" >> beam.GroupByKey()
      # output: [(str, [{str: str, str: str, ...}, ...]), ...]
      | "Sort customer events by timestamp" >> beam.Map( lambda x: ( x[0], sorted(x[1], key=lambda a: a["timestamp"] ) ) )
      # output: [(str, [{str: str, str: str, ...}, ...] <- SORTED), ...]
      | "Check if any cart has been abandoned" >> beam.ParDo(CheckAbandonedCartsFn())
      # output: array of JSON arrays: [ [ { "timestamp": "2019-01-01 14:20:00", "customer": "customer-3", "product": "product-4" }, ... ], ... ]
      # or [ [ { str: str, str: str, str: str }, ... ], ... ]
      | "Format results" >> beam.FlatMap(lambda x: x)
      # output: JSON array: { "timestamp": "2019-01-01 14:20:00", "customer": "customer-3", "product": "product-4" }, ...
      | "Write results" >> beam.io.WriteToText(output, num_shards = 1, shard_name_template='')
  )
