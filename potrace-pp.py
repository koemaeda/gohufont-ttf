#!/usr/bin/python
#----------------------------------------------------------------------------
#
#   Pixel-perfect potrace for FontForge
#
#	Copyright 2014 by Guilherme Maeda
#	https://github.com/koemaeda/potrace-pixelperfect
#
#----------------------------------------------------------------------------
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#   
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#----------------------------------------------------------------------------
#
# Runs potrace resizing the input image, for pixel perfect tracing in FontForge.
#
# You need to set the AUTOTRACE environment variable with the path to this
#  script for FontForge to use it. Don't forget to set the +x permission.
#
# Use: potrace-pp.py [options] [input file]
#
# Example: ./potrace-pp.py character.bmp
#          ./potrace-pp.py --flat -a 0 -u 1 character.bmp
#
#----------------------------------------------------------------------------

#
# Change this to tweak the scaling
#
scale = 500

import os, sys, math
from subprocess import Popen, PIPE
from PIL import Image

#
# Read the passed image
#
imPath = sys.argv.pop(-1)
imSrc = Image.open(imPath, 'r')
imSrc.putpalette( [255,255,255, 0,0,0] if len(imSrc.getcolors()) > 1 else [0,0,0] )
imBW = imSrc.convert('1') # black & white

#
# Upscale it
#
imBig = imBW.resize((imSrc.size[0]*scale, imSrc.size[1]*scale))

#
# Run potrace passing the big image
#
args = sys.argv
args[0] = 'potrace'

if not '-r' in args: # Add default resolution (72) if not specified
	args += ['-r', '72'] 

args = map(lambda i: # Multiply the resolution parameter (-r)
		str( int(args[i]) * scale ) if args[i-1] == '-r' else args[i],
	range(len(args)))

potrace = Popen(args, stdin=PIPE, stdout=PIPE)
imBig.save(potrace.stdin, imSrc.format)

#
# Output the result to stdout
#
potrace.wait()
output = potrace.communicate()[0]
print output
