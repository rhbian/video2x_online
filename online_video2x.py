import os

import subprocess
import multiprocessing

import tempfile
import pathlib

import bentoml
from bentoml.adapters import FileInput
from bentoml.adapters import JsonOutput

@bentoml.env()
class Video2x(bentoml.BentoService):
    
    @bentoml.api(input=FileInput(), output=JsonOutput())
    def predict(self, input_fd):
        with tempfile.TemporaryDirectory() as directory_name:
            abs_input_file_name = os.path.join(pathlib.Path(directory_name), input_fd.name)
            abs_output_file_name = os.path.join(pathlib.Path(directory_name), "_"+input_fd.name)
            with open(abs_input_file_name, "wb") as f:
                f.write(input_fd.read())
            shell_str = "/usr/local/bin/waifu2x-converter-cpp -i {input_name} -o {output_name} --noise-level {noise} --scale-ratio {scale}".format(input_name=abs_input_file_name, output_name=abs_output_file_name, noise=2, scale=2)
            shell_str = shell_str.split(" ")
            completed = subprocess.Popen(shell_str)
            completed.wait()
            """pictures to bytes, supported format: jpg/png/webp, default=ext/png"""
            with open(abs_output_file_name, "rb") as f:
                return f.read()
service = Video2x()
service.save()
