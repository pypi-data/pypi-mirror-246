from setuptools import setup, find_packages

setup(
    name='uas_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Daftar dependensi proyek jika ada
    ],
    entry_points={
        'console_scripts': [
            'uas_project = uas_33423303:main',
        ],
    },
)
