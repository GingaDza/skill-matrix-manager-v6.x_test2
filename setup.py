from setuptools import setup, find_packages

setup(
    name="skill-matrix-manager",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'skill-matrix-manager=skill_matrix_manager.__main__:main',
        ],
    },
)
