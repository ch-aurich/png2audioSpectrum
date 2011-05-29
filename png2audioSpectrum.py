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

#load B/W PNG image as array
def getPngBwPicture(filename,ySize):
    im = Image.open(filename)
    size = im.size
    #im = im.convert('P')
    #print im.mode
    im = im.resize((size[0]*ySize/size[1],ySize))
    pix = im.load()
    return pix

def getSignalMix(duration,freqlow,freqstep,pix,iteration,ydim):
    sumsignal = get_signal_data(1, duration, 0);
    for f in range(0,ydim):
	if (pix[f,iteration]==1):
            sumsignal += get_signal_data(f*freqstep + freqlow, duration,(32000)/ydim)
    return sumsignal



if __name__ == '__main__':
    stepDuration = 0.5
    myfilename = 'png2audioSpectrum.wav'
    numSteps = 400
    minfrequency = 100
    pix = getPngBwPicture('img.png',numSteps)

    sumsignal = getSignalMix(stepDuration,minfrequency,50,pix,0,numSteps)
    for n in range(1,numSteps - 1):
        sumsignal1 = getSignalMix(stepDuration,minfrequency,50,pix,n,numSteps)
	sumsignal = N.concatenate((sumsignal, sumsignal1))
	if ((1000*n/numSteps)%10==0):
	    print '\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r',"reading: %2d percent done" % (100*n/numSteps),
            sys.stdout.flush()

    print "\nconverting and saving to wave"
    signal = numpy2string(sumsignal)
    f = SoundFile(signal, myfilename, stepDuration*numSteps)
    f.write()
    print 'file written'
