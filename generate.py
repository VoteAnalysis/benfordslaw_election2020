import os
import os.path

import numpy as np
import matplotlib.pyplot as plt

NAMES = ['biden', 'trump']
COLORS = ['blue', 'red']
LEADINGDIGITS = list(range(10)[1:])

SRCDATA = "source_data"
README = 'readme.txt'

def getDataset(name, basePath):
   filePath = os.path.join(basePath, name + ".txt")
   votes = [int(i.split('#')[0].strip()) for i in open(filePath).read().strip().replace(',','').split('\n')]
   return votes

def getLeadingDigits(votes):
   return [sum([1 for i in votes if str(i).startswith(str(leadingDigit))])
      for leadingDigit in LEADINGDIGITS]

def getBenfordsLawSample(numItems):
   standardBenfordsLawPercents = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
   return [int(p * numItems / 100) for p in standardBenfordsLawPercents]

dataDirNames = []
with open('index.html', 'w') as f:
   for dataDirName in next(os.walk(SRCDATA))[1]:
      dataDirNames += [dataDirName]
      basePath = os.path.join(SRCDATA, dataDirName)
      readMePath = os.path.join(basePath, README)
      if not (os.path.isfile(readMePath) and \
            all([os.path.isfile(os.path.join(SRCDATA, dataDirName, f"{name}.txt")) for name in NAMES])):
         print(f"Didn't find expected data in {dataDirName}")
         continue

      print(f"Processing {dataDirName}...")

      f.write('<hr>\n')
      f.write(f'<h1 id="{dataDirName}">{dataDirName}</h1>\n')

      fig = plt.figure()
      for nameIdx in range(len(NAMES)):
         name = NAMES[nameIdx]

         N = len(LEADINGDIGITS)
         width = 0.3
         plot = fig.add_subplot(121 + nameIdx)
         y_pos = np.arange(N)

         votes = getDataset(name, basePath)

         seriesValsBenford = getBenfordsLawSample(len(votes))
         plot.bar(y_pos - width/2, seriesValsBenford, width, color='gray')
         plot.xaxis.set_ticks([i - 1 for i in LEADINGDIGITS])
         plot.set_xticklabels([str(x) for x in LEADINGDIGITS])

         seriesVals = getLeadingDigits(votes)
         plot.bar(y_pos + width/2, seriesVals, width, color=COLORS[nameIdx])

         f.write(f'<a href="source_data/{dataDirName}/{name}.txt">Source data for {name}<a><br/>')
      
      f.write("<br/>")

      imagePath = os.path.join(basePath, f"{dataDirName}.png")
      plt.savefig(imagePath, dpi=150)

      f.write(open(readMePath).read().replace('\n', '<br/>'))
      f.write('\n')
      f.write(f'<img src="{imagePath}" />')

contents = open('index.html').read()
with open('index.html', 'w') as f:
   f.write('<h1>All Cities/Counties Included</h1>')
   for dataDirName in dataDirNames:
      f.write(f'<a href="#{dataDirName}">{dataDirName}</a><br/>')
   f.write(contents)
