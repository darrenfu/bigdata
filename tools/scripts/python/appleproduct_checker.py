#!/usr/bin/python

# python lib dependency: 
# sudo pip install twilio
import sys
import os

class IParser:
  def __init__():
    pass

  def parse(self, doc, out_file):
    self._doc = doc
    self._out_file = out_file

class JSONParser(IParser):

  def __init__(self):
    pass

  def parse(self, doc, out_file, model):
    import json
    out_arr = []
    IParser.parse(self, doc, out_file)
    jobj = json.load(doc)
    nodes = jobj['body']['stores']
    model_txt = None
    for node in nodes:
      if model_txt == None:
        model_txt = node['partsAvailability'][model]['storePickupProductTitle']
      if node['partsAvailability'][model]['pickupDisplay'] == 'available' and node['storedistance'] < 100:
        line = "%s, %s, %s, %s, %s, %s" % (node['address']['address'], node['address']['address2'], node['city'], node['state'], node['address']['postalCode'], node['storeDistanceWithUnit'])
        out_arr.append(line)
        print line
        self._out_file.write(line)
        self._out_file.write("\n")
    return {"productTitle":model_txt, "availableStores":out_arr}

def send_request(url):
  import urllib2
  print "Downloading %s" % url
  res = urllib2.urlopen(url)
  return res

# main flow starts from here
def check_iphone(model, *args):
  zipcode = '98004'
  uri = 'https://www.apple.com/shop/retail/pickup-message?pl=true&cppart=UNLOCKED/US&parts.0=%s&location=%s'
  url = uri % (model, zipcode)

  res = send_request(url)

  if len(args) < 0:
    print('Usage: .py [zkhost:port=localhost:2181]')
    sys.exit(1)

  outfile = "/tmp/applestore_list.dat"
  print "Generating available appstore list to: " + outfile
  out = open(outfile, 'a')

  # Download interesting grid batch ids via QMS service
  parser = JSONParser()
  jresult = parser.parse(res, out, model)
  out.close()
  res.close()

  if len(jresult['availableStores']) > 0:
    print("Detect an available iphone! SMS ...")
    from twilio.rest import Client
    account_sid='...'
    auth_token='...'
    recipient_mobile='+1...'
    sender_mobile='+1...'
    msg_body = "%s\n\n%s" % (jresult['productTitle'], ";\n".join(jresult['availableStores']))

    client = Client(account_sid, auth_token)
    client.api.account.messages.create(to=recipient_mobile, from_=sender_mobile, body=msg_body)

if __name__ == "__main__":
  product_code_dict = {
    'iphone8p 64gb gray': 'MQ8D2LL/A',
    'iphone8p 64gb silver': 'MQ8E2LL/A',
    'iphone8p 64gb gold': 'MQ8F2LL/A',
    'iphone8p 256gb gray': 'MQ8G2LL/A',
    'iphone8p 256gb silver': 'MQ8H2LL/A',
    'iphone8p 256gb gold': 'MQ8J2LL/A',
    'iphone8 64gb gray': 'MQ6K2LL/A',
    'iphone8 64gb silver': 'MQ6L2LL/A',
    'iphone8 64gb gold': 'MQ6M2LL/A',
    'iphone8 256gb gray': 'MQ7F2LL/A',
    'iphone8 256gb gilver': 'MQ7G2LL/A',
    'iphone8 256gb gold': 'MQ7H2LL/A',
  }
  check_iphone(product_code_dict['iphone8p 64gb gray'], *sys.argv)
  #check_iphone(product_code_dict['iphone8p 64gb silver'], *sys.argv)
