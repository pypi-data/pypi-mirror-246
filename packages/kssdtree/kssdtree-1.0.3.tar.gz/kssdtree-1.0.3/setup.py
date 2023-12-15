import sys

from setuptools import setup, Extension, find_packages
from os import environ
import platform
import subprocess

# Detect the GCC version
gcc_version_output = subprocess.check_output(['gcc', '-dumpversion']).decode('utf-8')
gcc_version = gcc_version_output.strip()
# print(gcc_version)

if 'darwin' in sys.platform:
    # MacOS
    gcc_command = 'gcc-' + str(gcc_version)
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']
else:
    gcc_command = 'gcc'
    if environ.get('CC') and 'clang' in environ['CC']:
        # clang
        extra_compile_args = ['-fopenmp=libomp']
        extra_link_args = ['-fopenmp=libomp']
    else:
        # GNU
        extra_compile_args = ['-fopenmp']
        extra_link_args = ['-fopenmp']
MOD1 = 'kssdutils'
MOD2 = 'njutils'
MOD3 = 'dnjutils'
MOD4 = 'matrixutils'
sources1 = ['co2mco.c',
            'iseq2comem.c',
            'command_dist_wrapper.c',
            'mytime.c',
            'global_basic.c',
            'command_set.c',
            'command_dist.c',
            'command_shuffle.c',
            'command_composite.c',
            'mman.c',
            'pykssdutils.c']
sources2 = ['align.c',
            'cluster.c',
            'distancemat.c',
            'util.c',
            'tree.c',
            'buildtree.c',
            'sequence.c',
            'pynjutils.c']
sources3 = ['bytescale.c',
            'dnj.c',
            'str.c',
            'pydnjutils.c',
            'tmp.c',
            'phy.c',
            'filebuff.c',
            'nj.c',
            'qseqs.c',
            'vector.c',
            'matrix.c',
            'mman.c',
            'hclust.c',
            'nwck.c',
            'pherror.c']
sources4 = ['pymatrixutils.c']
include_dirs1 = ['kssdheaders']
include_dirs2 = ['njheaders']
include_dirs3 = ['dnjheaders']

require_pakages = [
    'pyqt5',
    'ete3',
    'pandas',
]
setup(
    name='kssdtree',
    version='1.0.3',
    author='yanghang',
    author_email='1090692248@qq.com',
    description='',
    url='',
    download_url='',
    ext_modules=[
        Extension(MOD1, sources=sources1, include_dirs=include_dirs1, libraries=['z'],
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args),
        Extension(MOD2, sources=sources2, include_dirs=include_dirs2),
        Extension(MOD3, sources=sources3, include_dirs=include_dirs3, libraries=['z'],
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args),
        Extension(MOD4, sources=sources4)
    ],
    py_modules=['kssdtree', 'toolutils'],
    packages=find_packages(),
    install_requires=require_pakages,
    dependency_links=['https://pypi.tuna.tsinghua.edu.cn/simple'],
    zip_safe=False,
    include_package_data=True
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload kssdtree-1.0.0.tar.gz
# pip install PyQt5==5.7.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
# pip install kssdtree -i https://pypi.python.org/simple/
'''
PyQt5                    5.7.1  
ete3                     3.1.3  
pyecharts                2.0.4   
Jinja2                   3.1.2   

import kssdtree
kssdtree.sketch(shuf_file='L3K10.shuf', genome_files='26s', output='26s_sketch', set_operation=False)
kssdtree.dist(genome_sketch='dwgsim_ecoli_sketch', dist_output='dwgsim_ecoli_distout')
kssdtree.build(input_dist='distout', output='26s.nwk', method='nj', show='form')
kssdtree.quick(shuf_file='L3K10.shuf', genome_files='26s', output='26s.nwk', method='dnj')

kssdtree.quick(shuf_file='L3K10.shuf', genome_files='bac20000', output='bac20000.nwk', method='dnj')
kssdtree.quick(shuf_file='L3K10.shuf', genome_files='bac10000', output='bac10000.nwk', method='dnj')

kssdtree.sketch(shuf_file='L3K10.shuf', genome_files='Nipponbare.fasta.gz', output='ref_rice00', set_operation=True)
kssdtree.sketch(shuf_file='L3K10.shuf', genome_files='rice_pangenome', output='qry_rice00', set_operation=True)
kssdtree.union(reference_sketch='ref_rice00', output='rice00_union_sketch')
kssdtree.subtract(reference_sketch='rice00_union_sketch', genomes_sketch='qry_rice00', output='rice00_subtract_sketch')
kssdtree.dist(genome_sketch='rice00_subtract_sketch', dist_output='distout')
kssdtree.build(input_dist='distout', output='rice.nwk')
kssdtree.quick(shuf_file='L3K10.shuf', genome_files='rice_pangenome', output='rice.nwk', method='nj', reference='Nipponbare.fasta.gz')
kssdtree.quick(shuf_file='L3K10.shuf', genome_files='hg43', output='hg.nwk', method='nj', reference='hg38.fa.gz')
'''
# kssdtree.quick(shuf_file='shuf_files/L3K10.shuf', genome_files='26s', output='26s.newick', reference=None, method='nj', show='form')
# kssdtree.quick(shuf_file='shuf_files/L3K10.shuf', genome_files='', output='.newick', reference=None, method='nj', show='form')
# kssdtree.quick(shuf_file='shuf_files/L3K10.shuf', genome_files='',
#                output='.newick', reference=None, method='nj', show='form')
# kssdtree.quick(shuf_file='shuf_files/L3K10.shuf', genome_files='',
#                output='.newick', reference=None, method='nj', show='form')
# kssdtree.quick(shuf_file='L3K10.shuf', genome_files='26s', output='26s.newick', method='nj', mode='r', reference=None)

# kssdtree.quick(shuf_file='L3K10.shuf', genome_files='g_rp', output='g_rp.newick', method='nj', mode='r', reference='NIP-T2T.fa.gz')
