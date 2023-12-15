﻿# -*- coding: UTF-8 -*-
from setuptools import setup
import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

alllist = [
        ('', ['algorithmLib/DLLs/p563.dll']),
        ('', ['algorithmLib/DLLs/g160.dll']),
        ('', ['algorithmLib/DLLs/cygwin1.dll']),
        ('', ['algorithmLib/DLLs/peaqb.exe']),
        ('', ['algorithmLib/DLLs/PY_PESQ.dll']),
        ('', ['algorithmLib/DLLs/matchsig.dll']),
        ('', ['algorithmLib/DLLs/snr_music.dll']),
        ('', ['algorithmLib/DLLs/snr_transient.dll']),
        ('', ['algorithmLib/DLLs/agcDelay.dll']),
        ('', ['algorithmLib/DLLs/attackrelease.dll']),
        ('', ['algorithmLib/DLLs/gaintable.dll']),
        ('', ['algorithmLib/DLLs/musicStability.dll']),
        ('', ['algorithmLib/DLLs/matchsig_aec.dll']),
        ('', ['algorithmLib/DLLs/ERLE_estimation.dll']),
        ('', ['algorithmLib/DLLs/pcc.dll']),
        ('', ['algorithmLib/DLLs/p563.dylib']),
        ('', ['algorithmLib/DLLs/g160.dylib']),
        ('', ['algorithmLib/DLLs/PY_PESQ.dylib']),
        ('', ['algorithmLib/DLLs/matchsig.dylib']),
        ('', ['algorithmLib/DLLs/snr_music.dylib']),
        ('', ['algorithmLib/DLLs/snr_transient.dylib']),
        ('', ['algorithmLib/DLLs/agcDelay.dylib']),
        ('', ['algorithmLib/DLLs/attackrelease.dylib']),
        ('', ['algorithmLib/DLLs/gaintable.dylib']),
        ('', ['algorithmLib/DLLs/musicStability.dylib']),
        ('', ['algorithmLib/DLLs/matchsig_aec.dylib']),
        ('', ['algorithmLib/DLLs/ERLE_estimation.dylib']),
        ('', ['algorithmLib/DLLs/pcc.dylib']),
        ('', ['algorithmLib/DLLs/p563.so']),
        ('', ['algorithmLib/DLLs/g160.so']),
        ('', ['algorithmLib/DLLs/matchsig.so']),
        ('', ['algorithmLib/DLLs/snr_music.so']),
        ('', ['algorithmLib/DLLs/snr_transient.so']),
        ('', ['algorithmLib/DLLs/agcDelay.so']),
        ('', ['algorithmLib/DLLs/attackrelease.so']),
        ('', ['algorithmLib/DLLs/gaintable.so']),
        ('', ['algorithmLib/DLLs/musicStability.so']),
        ('', ['algorithmLib/DLLs/matchsig_aec.so']),
        ('', ['algorithmLib/DLLs/ERLE_estimation.so']),
        ('', ['algorithmLib/DLLs/pcc.so']),
        ('', ['algorithmLib/DLLs/SC_res_retrain_220316_185754125621__ep_007.tar']),
        ('', ['algorithmLib/DLLs/silero_vad.jit']),
]
setup(
    name='AlgorithmLib',
    version='1.19.29',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author=' MA JIANLI',
    author_email='majianli@corp.netease.com',
    description='audio algorithms to compute and test audio quality of speech enhencement',
    long_description='long_description',
    long_description_content_type="text/markdown",
    install_requires=[
    'numpy',
    'wave',
    'matplotlib',
    'datetime',
    'scipy',
    'pystoi',
    'paramiko',
    'moviepy',
    'torch',
    'torchaudio',
    'librosa',
    'requests',
    'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[
            ('', ['algorithmLib/DLLS/audio.dll'])],
    python_requires='>=3.6',
)



