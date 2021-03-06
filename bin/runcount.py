#!/usr/bin/python
import os

from count import countfile 
import common










def runAll(args):
  
	print('\n\n\nYou have requested to count unique sam files')
	print('\tWARNING:')
	print('\t\tIF USING ANY REFERENCES OTHER THAN THOSE I PROVIDE I CANNOT GUARANTEE RESULT ACCURACY')
	print('\n')
  


	#set up environment#
	args.AnalysisDirectory = common.fixDirName(args.AnalysisDirectory)
	
	
	SamDir = args.AnalysisDirectory + '/Sam/' #args.SamDirectory = common.fixDirName(args.SamDirectory)
	if args.mapdir:
		SamDir = common.fixDirName(args.mapdir)
	
	countDir = args.AnalysisDirectory + '/BinCounts/' #os.path.dirname(args.SamDirectory[:-1]) + '/BinCounts/'
	
	statsDir =  args.AnalysisDirectory + '/PipelineStats/' #os.path.dirname(args.SamDirectory[:-1]) + '/PipelineStats/'
	if args.statdir:
		statsDir = common.fixDirName(args.statdir)
			
	for i in [countDir, statsDir]:
		common.makeDir(i)

	samFiles = common.getSampleList(SamDir, args.samples, 'sam')
		
		
	
	#run multiprocessing of all bin counting commands#	
	argList = [(x, countDir, statsDir, args.species) for x in samFiles]
	common.daemon(countfile.runOne, argList, 'count sam files')
	
	
	
	print('\nBin counts complete\n\n\n')

	
	
	
	
