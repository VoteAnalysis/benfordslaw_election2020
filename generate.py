import os
import os.path

import numpy as np
import matplotlib.pyplot as plt

NAMES = ['biden', 'trump']
COLORS = ['blue', 'red']
LEADINGDIGITS = list(range(10)[1:])

SRCDATA = "source_data"
README = 'readme.txt'

def getRawDataset(name, basePath):
   filePath = os.path.join(basePath, name + ".txt")
   rows = [i.strip() for i in open(filePath).read().strip().replace(',','').split('\n')]
   return rows

def getNames(name, basePath):
   names = [i.split('#')[1].strip() for i in getRawDataset(name, basePath)]
   return names

def getDataset(name, basePath):
   return [int(i.split('#')[0].strip()) for i in getRawDataset(name, basePath)]

def getLeadingDigits(votes):
   return [sum([1 for i in votes if str(i).startswith(str(leadingDigit))])
      for leadingDigit in LEADINGDIGITS]

def getBenfordsLawSample(numItems):
   standardBenfordsLawPercents = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
   return [int(p * numItems / 100) for p in standardBenfordsLawPercents]

dataDirNames = []
with open('index.html', 'w') as f:
   f.write(open("templates/explanation.html").read())

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

      votesArray = [getDataset(name, basePath) for name in NAMES]
      subNames = getNames(NAMES[0], basePath)
      for nameIdx in range(len(NAMES)):
         name = NAMES[nameIdx]
         for rowIdx in range(len(votesArray[0])):
            subName = subNames[rowIdx]
            if votesArray[nameIdx][rowIdx] == 0 and votesArray[1 - nameIdx][rowIdx] != 0:
               f.write(f'<span style="color: red">Zero votes for {name} in "{subName}" when {NAMES[1 - nameIdx]} has {votesArray[1 - nameIdx][rowIdx]}</span><br/>')

      fig = plt.figure()
      for nameIdx in range(len(NAMES)):
         name = NAMES[nameIdx]

         N = len(LEADINGDIGITS)
         width = 0.3
         plot = fig.add_subplot(121 + nameIdx)
         y_pos = np.arange(N)

         votesWithZeros = getDataset(name, basePath)
         votes = [x for x in votesWithZeros if x > 0]
         numVotes = len(votes)

         seriesValsBenford = getBenfordsLawSample(numVotes)
         plot.bar(y_pos - width/2, seriesValsBenford, width, color='gray')
         plot.xaxis.set_ticks([i - 1 for i in LEADINGDIGITS])
         plot.set_xticklabels([str(x) for x in LEADINGDIGITS])

         seriesVals = getLeadingDigits(votes)
         plot.bar(y_pos + width/2, seriesVals, width, color=COLORS[nameIdx])

         f.write(f'<a href="source_data/{dataDirName}/{name}.txt">Source data for {name}<a>; ')
         f.write(f'Nonzero counts: {numVotes}')
         if 0 in votesWithZeros:
            f.write(f'; <span style="color: red">Zero votes: {len([x for x in votesWithZeros if x == 0])}</span>')
         f.write(f'<br/>')
      
      f.write("<br/>")

      imagePath = os.path.join(basePath, f"{dataDirName}.png")
      plt.savefig(imagePath, dpi=150)

      f.write(open(readMePath).read().replace('\n', '<br/>'))

      f.write(f'There are a total of {numVotes} vote subtotals represented<br/>')
      f.write('\n')
      f.write(f'<img src="{imagePath}" />')

contents = open('index.html').read()
with open('index.html', 'w') as f:
   f.write('<h1>All Cities/Counties Included</h1>')
   for dataDirName in dataDirNames:
      f.write(f'<a href="#{dataDirName}">{dataDirName}</a><br/>')
   f.write(contents)
