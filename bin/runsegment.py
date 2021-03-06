#!/usr/bin/python
import os
import numpy as np
import shutil

import common
from segment import normalizefile, segmentfile













def runAll(args):

	print('\n\n\nYou have requested to normalize and segment bincounts files')
	print('\tWARNING:')
	print('\t\tIF USING ANY REFERENCES OTHER THAN THOSE I PROVIDE I CANNOT GUARANTEE RESULT ACCURACY')
	print('\n')
 


	#Set up environment#
	args.AnalysisDirectory = common.fixDirName(args.AnalysisDirectory)

	CountDir = args.AnalysisDirectory + 'BinCounts/' #args.CountDirectory = common.fixDirName(args.CountDirectory)
	if args.bincountdir:
		CountDir = common.fixDirName(args.bincountdir)
		
	lowessDir = args.AnalysisDirectory + 'LowessBinCounts/' #os.path.dirname(args.CountDirectory[:-1]) + '/LowessBinCounts/'
	segmentDir = args.AnalysisDirectory + 'Segments/' #os.path.dirname(args.CountDirectory[:-1]) + '/Segments/'
	tempDir = args.AnalysisDirectory  + 'Temp/' #os.path.dirname(args.CountDirectory[:-1]) + '/Temp/'

	common.makeDir(lowessDir)
	if not args.normalizeonly:
		common.makeDir(segmentDir)
		common.makeDir(tempDir)

	sampleFiles = common.getSampleList(CountDir, args.samples, 'bincounts')
		
		
		
	info = common.importInfoFile(args.infofile, args.columns, 'normalize')
	
	if args.infofile:
		refArray = info
	else:
		thisDtype = info
		refArray = np.array(
			[ (os.path.basename(x)[:-14], 'unk', 1,) for x in sampleFiles],
			dtype=thisDtype)
		
	sampleDict = {x: [y for y in sampleFiles if x == os.path.basename(y)[:len(x)]][0] for x in refArray['name']}

	
	
	
	
	#Run normalization for all samples#
	methodDict = {x: [False,] for x in np.unique(refArray['method'])}	
	methodDict['NA'] = [False]
	sampleNormMethodDict = {x: 'NA' for x in refArray['name']}
	
	if not args.gconly:
		for i in methodDict:
			refSlice = refArray[(refArray['method'] == i) & (refArray['cells'] == 1)]
			methodSamples = [sampleDict[x] for x in refSlice['name']]

			methodDict[i] = normalizefile.runMakeMethodRef(args.species, methodSamples, i, lowessDir)
			
			if methodDict[i][0] != False:
				for j in refSlice['name']:
					sampleNormMethodDict[j] = i

		
	#run multiprocessing for gc (+ method) correction
	normArgs = [(args.species, sampleDict[x], methodDict[sampleNormMethodDict[x]], lowessDir + x + '.lowess.txt') for x in sampleDict.keys()]
	common.daemon(normalizefile.runNormalizeOne, normArgs, 'normalize bincount files')
	
	print('\nNormalization complete\n\n\n')
	
		
		
		
	#Run CBS for all samples#
	if not args.normalizeonly:
		segArgs = [(x, args.species, tempDir, lowessDir, segmentDir) for x in refArray['name']]
		common.daemon(segmentfile.segmentOne, segArgs, 'segment bincount data')
	
	shutil.rmtree(tempDir[:-1])

	print('\nSegmentation complete\n\n\n')

	
	
	
