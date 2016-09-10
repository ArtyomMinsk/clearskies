import urllib2

airport="KRDU"
address="1600+Amphitheatre+Parkway,+Mountain+View,+CA"
key="AIzaSyBJRBQ0vUyLij18oHW8A_mwdsJbyYnlDUk"
url="https://maps.googleapis.com/maps/api/geocode/json?airport=%s&key=%s" % (airport, key)

response = urllib2.urlopen(url)
jsongeocode = response.read()
