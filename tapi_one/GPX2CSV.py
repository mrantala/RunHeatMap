import glob
import xml.etree.ElementTree as ET

theNS = "{http://www.topografix.com/GPX/1/1}".lower()
theNS2 = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}".lower()

def elementIs(inElement,inTag):
    item1 = inTag.lower()
    item2 = elementName(inElement)
    return (inTag.lower() == elementName(inElement).lower())

def elementName(inElement):
    item1= inElement.tag.lower().replace(theNS,"").replace(theNS2,"")
    return item1

def writeCSV(inSourceFile,inTrkList):
    outFile = inSourceFile.lower().replace(".gpx",".csv")
    tmpfile = open(outFile,"w")
    firstLine="file,segment,vertex,time,ele,hr,lat,lon"
    tmpfile.write(firstLine)
    tmpfile.write("\n")

    iTrkSegIndex = 0
    for iTrkSeg in inTrkList:
        iTrkPtIndex = 0
        for iTrkPtDict in iTrkSeg:
            thisLine = "{0},{1},{2},*time*,*ele*,*hr*,*lat*,*lon*".format(inSourceFile,iTrkSegIndex,iTrkPtIndex)
            for key, value in iTrkPtDict.iteritems():
                thisLine = thisLine.replace("*"+str(key)+"*",str(value))
            tmpfile.write(thisLine)
            tmpfile.write("\n")
            iTrkPtIndex+=1
        iTrkSegIndex+=1

    tmpfile.close()


def mainLoop():
    for iFile in glob.glob("*.gpx"):
        print iFile
        tree = ET.parse(iFile)
        root=tree.getroot()

        theTrkList = []

        for iRoot in root:
            if elementIs(iRoot,"trk"): #"http://www.topografix.com/gpx/1/1}trk" in iRoot.tag.lower():
                for iTrkSeg in iRoot:
                    if not elementIs(iTrkSeg,"trkseg"):
                        continue
                    thisTrk = []

                    pntIndex = 0
                    for iTrkPt in iTrkSeg:
                        if not elementIs(iTrkPt,"trkpt"):
                            continue
                        trkPntDict = dict()
                        trkPntDict["pntIndex"] = pntIndex
                        trkPntDict['lat'] = iTrkPt.get('lat')
                        trkPntDict['lon'] = iTrkPt.get('lon')

                        pntIndex+=1
                        for iElem in iTrkPt:
                            if elementIs(iElem,"extensions"):
                                for iSubElem in iElem:
                                    if (elementIs(iSubElem,"TrackPointExtension")):
                                        for iExtensionElem in iSubElem:
                                            if elementIs(iExtensionElem,"hr"):
                                                trkPntDict[elementName(iExtensionElem)] = iExtensionElem.text
                            else:
                                trkPntDict[elementName(iElem)] = iElem.text

                        #print trkPntDict
                        thisTrk.append(trkPntDict)

                    theTrkList.append(thisTrk)
        writeCSV(iFile.lower(), theTrkList)


        '''for elem in tree.getiterator():
            print "Elem.tag: {0}".format(elem.tag)
            print "   Attrib: {0}".format(elem.attrib)
            print ""'''




theLineList = mainLoop()
