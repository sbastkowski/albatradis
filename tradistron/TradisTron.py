'''Driver class'''
from tradistron.PrepareInputFiles import PrepareInputFiles
import logging
import os
import sys
import time

from tradistron.BlockInsertions import BlockInsertions
from tradistron.NormalisePlots import NormalisePlots


class TradisTron:
	def __init__(self, options):
		self.logger            = logging.getLogger(__name__)
		self.plotfiles         = options.plotfiles
		self.minimum_threshold = options.minimum_threshold
		self.window_size       = options.window_size
		self.window_interval   = options.window_interval
		self.verbose           = options.verbose
		self.minimum_logfc     = options.minimum_logfc
		self.pvalue            = options.pvalue
		self.prefix            = options.prefix
		self.minimum_logcpm    = options.minimum_logcpm
		self.iterations        = options.iterations
		self.dont_normalise_plots   = options.dont_normalise_plots
		self.minimum_block     = options.minimum_block
		self.span_gaps         = options.span_gaps
		self.emblfile          = options.emblfile
		self.minimum_proportion_insertions = options.minimum_proportion_insertions
		
		self.genome_length = 0
		
		if self.verbose:
			self.logger.setLevel(logging.DEBUG)
		else:
			self.logger.setLevel(logging.ERROR)
			
		self.blocks = []
	
	def run(self):
		plotfiles = self.plotfiles
		report_decreased_insertions = True
		if self.dont_normalise_plots:
			n = NormalisePlots(self.plotfiles, self.minimum_proportion_insertions)
			report_decreased_insertions = n.decreased_insertion_reporting()
			plotfiles = n.create_normalised_files()
		
		for i in range(1,self.iterations+1):
			bi = BlockInsertions(self.logger, plotfiles, self.minimum_threshold, self.window_size, self.window_interval, self.verbose, self.minimum_logfc, self.pvalue, self.prefix + "_" +str(i), self.minimum_logcpm, self.minimum_block, self.span_gaps, self.emblfile, report_decreased_insertions)
			bi.run()
			self.blocks = bi.blocks
			plotfiles = bi.output_plots.values()
		
		return self
