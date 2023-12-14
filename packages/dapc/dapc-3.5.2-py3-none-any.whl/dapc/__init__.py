import numpy as np
from . import dapc_main

dapc_main.showInformation()

class WaveData:
    def __init__(self):
        self.SampleRate, self.left, self.right, self.bitDepth = 0, np.array([]), np.array([]), np.float32

    # resampleAlgorithm can be "zero","nearest","slinear","linear","quadratic","cubic",etc.
    def resample(self, sample_rate=44100, resample_algorithm="default"):
        self.SampleRate, self.left, self.right = dapc_main.resample(self.SampleRate, sample_rate, self.left, self.right,
                                                               resample_algorithm)

    def reverb(self, reverb_numberOfEcho=3, reverb_maxVolumeDb=2.0, reverb_offsetSecond=0.11,
               CONSTANT_REVERB_RANGE=12.0):
        self.left, self.right = dapc_main.reverb(self.SampleRate, self.left, self.right, echoFunction=dapc_main.reverb_funDefault,
                                            reverb_numberOfEcho=reverb_numberOfEcho,
                                            reverb_maxVolumeDb=reverb_maxVolumeDb,
                                            reverb_offsetSecond=reverb_offsetSecond,
                                            CONSTANT_REVERB_RANGE=CONSTANT_REVERB_RANGE)

    def mix(self, mixer_left_leftRate=1.0, mixer_left_rightRate=-1.0, mixer_right_leftRate=-1.0,
            mixer_right_rightRate=1.0):
        self.left, self.right = dapc_main.mixer(self.left, self.right, mixer_left_leftRate=mixer_left_leftRate,
                                           mixer_left_rightRate=mixer_left_rightRate,
                                           mixer_right_leftRate=mixer_right_leftRate,
                                           mixer_right_rightRate=mixer_right_rightRate)

    # mode = 'factor' or 'DB'.
    def gain(self, leftFactor=1.0, rightFactor=1.0, leftDB=0.0, rightDB=0.0, mode='factor'):
        self.left, self.right = dapc_main.gain(self.left, self.right, leftFactor=leftFactor, rightFactor=rightFactor,
                                          leftDB=leftDB, rightDB=rightDB, mode=mode)

    def pitch(self, pitch_pitchFactor=0.8, pitch_speedFactor=1.0, sonic_library_path=r"./sonic.dll"):
        self.SampleRate, self.left, self.right = dapc_main.pitch(self.left, self.right, np.float32, self.SampleRate,
                                                            self.SampleRate, pitch_pitchFactor=pitch_pitchFactor,
                                                            pitch_speedFactor=pitch_speedFactor, sonic_library_path=sonic_library_path)
        
    def trim(self, start, end, unit="second"):
        self.left, self.right = dapc_main.trim(self.SampleRate, start, end, self.left, self.right, trim_UNIT=unit)

    def addSilence(self, addSilence_start, addSilence_length, addSilence_UNIT="second", addSilence_MODE="insert"):
        self.left, self.right = dapc_main.addSilence(self.SampleRate, addSilence_start, addSilence_length, self.left,
                                                self.right, self.bitDepth, addSilence_UNIT=addSilence_UNIT,
                                                addSilence_MODE=addSilence_MODE)

    def surround3d(self, roundLength=12.75, minimumRangeFactor=0.3, phase=0.0, roundLengthUnit="second"):
        self.left, self.right = dapc_main.surround3d(self.left, self.right, self.SampleRate, self.bitDepth, self.bitDepth,
                                                s3d_roundLength=roundLength, s3d_minimumRangeFactor=minimumRangeFactor,
                                                s3d_phase=phase, s3d_roundLengthUnit=roundLengthUnit)

    # This function is used to implement the fade in and fade out effect. 'fio_fadeMode' can be 'sin','cos','liner'. 'fio_mode' can be 'out','in','both'. 'fio_fadeLengthUnit' can be 'second','sample'.
    def fadeInOut(self, fio_fadeLength=18.5, fio_fadeMode='sin', fio_fadeLengthUnit='second', fio_mode='out'):
        self.left, self.right = dapc_main.fadeInOut(self.left, self.right, self.SampleRate, self.bitDepth, self.bitDepth,
                                               fio_fadeLength, fio_fadeMode, fio_fadeLengthUnit, fio_mode)

    def fftFilter(self, fft_frequency=20000, fft_frequencyRange=180):
        self.left, self.right, self.bitDepth = dapc_main.fftFilter(self.left, self.right, self.SampleRate, self.bitDepth,
                                                              self.bitDepth, fft_frequency=fft_frequency,
                                                              fft_frequencyRange=fft_frequencyRange)

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getSamplerate(self):
        return self.SampleRate

    def getBitdepth(self):
        return self.bitDepth

    def setSamplerate(self, sampleRate):
        self.SampleRate = sampleRate

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def setBitdepth(self, bitdepth):
        self.bitDepth = bitdepth


def ReadWaveFile(filename):
    SampleRate, left, right, bitDepth = dapc_main.readPcmWavData(filename)
    left, right, bitDepth = dapc_main.changeBitRate(left, right, bitDepth, np.float32)
    wave = WaveData()
    wave.setLeft(left)
    wave.setRight(right)
    wave.setBitdepth(bitDepth)
    wave.setSamplerate(SampleRate)
    return wave


def WriteWaveFile(wave, filename, bitdepth=24, isFilter=False, FilterDistance=7):
    bitdepth_dt = np.int16
    if bitdepth==16:
        bitdepth_dt = np.int16
    elif bitdepth == 24:
        bitdepth_dt = np.int32
    else:
        pass
    left, right, samplerate, dataType = wave.getLeft(), wave.getRight(), wave.getSamplerate(), wave.getBitdepth()
    left, right, bitdepth_dt = dapc_main.changeBitRate(left, right, dataType, bitdepth_dt)
    dapc_main.writePcmWavData(filename, left, right, samplerate, bitdepth_dt, isFilter=isFilter, FilterDistance=FilterDistance)

# 'joint_MODE' means splicing mode, it can be 'append' or 'mix'.
def joint(wavfile01, wavfile02, joint_MODE="append"):
    left01, left02, right01, right02 = wavfile01.getLeft(), wavfile02.getLeft(), wavfile01.getRight(), wavfile02.getRight()
    samplerate01, samplerate02, bitdepth01, bitdepth02 = wavfile01.getSamplerate(), wavfile02.getSamplerate(), wavfile01.getBitdepth(), wavfile02.getBitdepth()
    left01, right01, bitdepth01 = dapc_main.changeBitRate(left01, right01, bitdepth01, np.float32)
    left02, right02, bitdepth02 = dapc_main.changeBitRate(left02, right02, bitdepth02, np.float32)
    out_sampleRate = max(samplerate01, samplerate02)
    left, right, bitdepth = dapc_main.joint(left01, left02, right01, right02, samplerate01, samplerate02, out_sampleRate,
                                       bitdepth01, bitdepth02, np.float32, joint_MODE)
    wave = WaveData()
    wave.setLeft(left)
    wave.setRight(right)
    wave.setSamplerate(out_sampleRate)
    wave.setBitdepth(bitdepth)
    return wave

