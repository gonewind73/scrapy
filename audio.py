'''
Created on 2016年5月15日

@author: heguofeng
'''
import unittest
import pyaudio
import wave
from matplotlib  import numpy 
from matplotlib  import pylab 

class recorder():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
    def __init__(self):
        self.pa=pyaudio.PyAudio()
        
        pass
    
    def record(self):
        stream = self.pa.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=1,
                frames_per_buffer=self.CHUNK)
        stream1=self.pa.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=2,
                frames_per_buffer=self.CHUNK)
        print("recording...")
        frames = []
        frames1=  []
 
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            data1= stream1.read(self.CHUNK)
            frames.append(data)
            frames1.append(data1)
        print("finished recording")
        
        self.wavedata=b''.join(frames)
        self.wavedata1=b''.join(frames1)
        self.nframes=int(self.RATE/self.CHUNK*self.RECORD_SECONDS)*self.CHUNK
        # stop Recording
        stream.stop_stream()
        stream.close()
        
        self.savewave(self.WAVE_OUTPUT_FILENAME, self.wavedata)
        self.savewave("file1.wav",self.wavedata1)
        
    def savewave(self,filename,wavedata):
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.pa.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(wavedata)
        waveFile.close()
        return
    
    def loadwave(self,filename):
        wavefile=wave.open(filename,"rb")
        params = wavefile.getparams()  
        self.nchannels, self.sampwidth, self.framerate, self.nframes = params[:4]  
        str_data  = wavefile.readframes(self.nframes)  
        wavefile.close()  
        return str_data
  

    def showwave(self):
        #将波形数据转换成数组  
        #需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组  
        wave_data = numpy.fromstring(self.wavedata,dtype = numpy.short)  
        wave_data.shape = -1,2  
        wave_data = wave_data.T  
        wave_data1 = numpy.fromstring(self.wavedata1,dtype = numpy.short)  
        wave_data1.shape = -1,2  
        wave_data1 = wave_data1.T  
        
        print(self.nframes,len(self.wavedata))
        time = numpy.arange(0,self.nframes)*(1.0/self.RATE)  
        
        len_time = int(len(time)/2) *2 
        print(len_time)
        time = time[0:len_time]  
        #绘制波形  
  
        pylab.subplot(221)  
        print(len(time),len(wave_data[0]))
        
        pylab.plot(time,wave_data[0])  
        
        pylab.subplot(222)  
        pylab.plot(time, wave_data[1],c="r")  
        
        pylab.subplot(223)  
        pylab.plot(time, wave_data1[0])  
        pylab.subplot(224)  
        pylab.plot(time, wave_data1[1],c="r")  
                
        
        pylab.xlabel("time")  
        pylab.show()  
        
    def comparewave(self,wavedata,wavedata1):
        #将波形数据转换成数组  
        #需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组  
        wave_data = numpy.fromstring(wavedata,dtype = numpy.short)  
        wave_data1 = numpy.fromstring(wavedata1,dtype = numpy.short)  
        wave_datac= wave_data-wave_data1
        wave_data.shape = -1,2  
        wave_data = wave_data.T  
        wave_data1 = numpy.fromstring(wavedata1,dtype = numpy.short)  
        wave_data1.shape = -1,2  
        wave_data1 = wave_data1.T  
        
        
        time = numpy.arange(0,self.nframes)*(1.0/self.RATE)  
        
        len_time = int(len(time)/2) *2 
        print(len_time)
        time = time[0:len_time]  
        #绘制波形  
        pylab.subplot(221)  
        pylab.plot(time, wave_data1[0],c="g")  
        pylab.subplot(222)  
        pylab.plot(time, wave_data1[1],c="y")  
                  
        pylab.subplot(221)  
        pylab.plot(time,wave_data[0])  
        
        pylab.subplot(222)  
        pylab.plot(time, wave_data[1],c="r")  
        
        pylab.subplot(223)  
        pylab.plot(time,wave_data[0]-wave_data[1])  
        
        pylab.subplot(224)  
        pylab.plot(time, wave_data[0]-wave_data1[0],c="r")  
        self.savewave("filec.wav", wave_datac)

        
        pylab.xlabel("time")  
        pylab.show()  
  
    def play(self):
        pass
    
    def __del__(self):
        self.pa.terminate()
        pass
    
    def callback(self,in_data, frame_count, time_info, status):
        pass
        
    


class Test(unittest.TestCase):


    def setUp(self):
        self.myrecord=recorder()
        pass


    def tearDown(self):
        pass


    def testRecord(self):
        wavedata=self.myrecord.loadwave("file.wav")
        wavedata1=self.myrecord.loadwave("file2.wav")
        self.myrecord.comparewave(wavedata,wavedata1)
        return True
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()