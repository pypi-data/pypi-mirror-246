from setuptools import setup, find_packages

setup(
    name="battleships_solar_sausage",
    version='1.0.0',
    packages=find_packages(),

    # metadata
    author="Solar Sausage",
    description="Battleships game for uni coursework.",
    url="https://github.com/solar-sausage/Battleships-uni-coursework-",
    
    # dependencies
    install_requires=[
        "flask"
    ],

    # entry points
    entry_points={
        'console_scripts': [
            "run_app = battleships.main:main_function",
        ],
    }
)