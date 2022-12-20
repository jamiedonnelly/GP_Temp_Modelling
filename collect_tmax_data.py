import requests
import os 
from lxml import etree
import json

# Base url page 
url = "https://dap.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.1.0.0/60km/tasmax/day/v20220310/{file}"
response = requests.get(url.format(file=""))
tree = etree.HTML(response.text)

# OS cmd to execute
base_cmd = "curl {url} --output '/Users/jamie/Documents/GP Stochastic Volatiltiy Model /data/tmax/{fname}'"

# Collecting data
xpath = '/html/body/pre/a[{value}]/text()'
for i in range(2,746):
    file = tree.xpath(xpath.format(value=i))[0]
    furl = url.format(file=file)
    os.system(base_cmd.format(url=furl,fname=file))