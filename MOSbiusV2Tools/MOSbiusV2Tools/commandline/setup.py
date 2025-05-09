from setuptools import setup, find_packages

setup(
    name='mosbiusv2tools',
    version='1.0.0',
    description='Tools for generating SPICE subcircuits from JSON circuit descriptions and sizing files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Peter Kinget',
    author_email='peter@kinget.net',
    url='https://github.com/peterkinget/MOSbiusCADFlow',
    license='MIT',
    packages=find_packages(where="MOSbiusV2Tools/MOSbiusV2Tools/commandline/src"),
    # install_requires=open('commandline/requirements.txt').read().splitlines(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'generate_sizes_probe_subckt=commandline.src.generate_sizes_probe_subckt:main',
            'generate_switch_matrix_probe_subckt=commandline.src.generate_switch_matrix_probe_subckt:main',
            'generate_pin_to_RBUS_SBUS_subckt=commandline.src.generate_pin_to_RBUS_SBUS_subckt:main',
            'generate_nodes_to_subckt=commandline.src.generate_nodes_to_subckt:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)