# python
"""
- Created on: 21.04.2019
- Author:     Ayoub Malek
"""
import os
import subprocess
import numpy as np
from subprocess import Popen, PIPE

class SilenceEliminator:

    def __init__(self):
        pass

    def ffmpeg_silence_eliminator(self, input_path, output_path):
        """
        Eliminate silence from voice file using ffmpeg library.

        Args:
            input_path  (str) : Path to get the original voice file from.
            output_path (str) : Path to save the processed file to.

        Returns:
            (list)  : List including True for successful authentication, False otherwise and a percentage value
                      representing the certainty of the decision.
        """
        # filter silence in mp3 file
        filter_command = ["ffmpeg", "-i", input_path, "-af", "silenceremove=1:0:0.05:-1:1:-36dB", "-ac", "1", "-ss", "0","-t","90", output_path, "-y"]
        out = subprocess.Popen(filter_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out.wait()

        with_silence_duration = os.popen("ffprobe -i '" + input_path + "' -show_format -v quiet | sed -n 's/duration=//p'").read()
        no_silence_duration   = os.popen("ffprobe -i '" + output_path + "' -show_format -v quiet | sed -n 's/duration=//p'").read()

        # print duration specs
        try:
            print("%-32s %-7s %-50s" % ("ORIGINAL SAMPLE DURATION",         ":", float(with_silence_duration)))
            print("%-23s %-7s %-50s" % ("SILENCE FILTERED SAMPLE DURATION", ":", float(no_silence_duration)))
        except:
            print("Cannot convert float to string")

        # convert file to wave and read array
        load_command = ["ffmpeg", "-i", output_path, "-f", "wav", "-" ]
        p            = Popen(load_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        data         = p.communicate()[0]
        audio_np     = np.frombuffer(data[data.find(b'\x00data')+ 9:], np.int16)

        # delete temp silence free file, as we only need the array
        os.remove(output_path)
        return audio_np, no_silence_duration
