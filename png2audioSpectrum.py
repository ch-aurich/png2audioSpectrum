#base of this file from: http://codingmess.blogspot.com/2010/02/how-to-make-wav-file-with-python.html
import sys
import wave
import numpy as N
from PIL import Image


def get_signal_data(frequency=440, duration=1, volume=32768, samplerate=44100):
    """Outputs a numpy array of intensities"""
    samples = duration * samplerate
    period = samplerate / float(frequency)
    omega = N.pi * 2 / period
    t = N.arange(samples, dtype=N.float)
    y = volume * N.sin(t * omega)
    return y

def numpy2string(y):
    """Expects a numpy vector of numbers, outputs a string"""
    signal = "".join((wave.struct.pack('h', item) for item in y))
    # this formats data for wave library, 'h' means data are formatted
    # as short ints
    return signal

class SoundFile:
    def  __init__(self, signal, filename, duration=1, samplerate=44100):
        self.file = wave.open(filename, 'wb')
        self.signal = signal
        self.sr = samplerate
        self.duration = duration
  
    def write(self):
        self.file.setparams((1, 2, self.sr, self.sr*self.duration, 'NONE', 'noncompressed'))
        # setparams takes a tuple of:
        # nchannels, sampwidth, framerate, nframes, comptype, compname
        self.file.writeframes(self.signal)
        self.file.close()

def getPngBwPicture(filename,ySize):
    """reads png from filename, resizes to have width of ySize and returns resized image - does not change the file!"""
    im = Image.open(filename)
    size = im.size
    #convert to b/w picture - ie only contain 0 and 1 in array
    #im = im.convert('P')
    #resizes the image to have a width of ySize
    im = im.resize((size[0]*ySize/size[1],ySize))
    #get array of picture that will be returned
    pix = im.load()
    return pix

def getSignalMix(duration,freqlow,freqstep,pix,iteration,ydim):
    """produces an signal of $duration seconds lenght that consists of multiple sines that are specified by the given image array."""
    sumsignal = get_signal_data(1, duration, 0);
    for f in range(0,ydim):
	if (pix[f,iteration]==1):
            sumsignal += get_signal_data(f*freqstep + freqlow, duration,(32000)/ydim)
    return sumsignal


if __name__ == '__main__':
    #time one spectrum will be held
    stepDuration = 0.5			

    #output filename - TODO: read from script arguments
    myfilename = 'png2audioSpectrum.wav'

    #number of distinct frequencies used to make up the image - TODO: calculate that by the parameters given
    #eg calculate by frequency bounds and minimum resolution (50Hz is good)
    numSteps = 400

    #lowest used frequency - TODO:make this accessible by an external parameter
    minfrequency = 100

    #reads image from fixed filename - TODO: make filename accessible by external parameter
    pix = getPngBwPicture('img.png',numSteps)

    #initialize array sumsignal by calling getSignalMix for the first bunch of pixels
    sumsignal = getSignalMix(stepDuration,minfrequency,50,pix,0,numSteps)
    #start looping through image at the second bunch of pixels
    for n in range(1,numSteps - 1):
        sumsignal1 = getSignalMix(stepDuration,minfrequency,50,pix,n,numSteps)
	sumsignal = N.concatenate((sumsignal, sumsignal1))
	#if an real number for progress in % is reached update display
	if ((1000*n/numSteps)%10==0):
            #update display - delete previous output and print new progress
	    print '\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r',"reading: %2d percent done" % (100*n/numSteps),
            sys.stdout.flush()

    print '\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r', "finished reading image"

    print "converting to wave"
    signal = numpy2string(sumsignal)
    f = SoundFile(signal, myfilename, stepDuration*numSteps)
    print "saving wave"
    f.write()
    print 'file written successfully'
