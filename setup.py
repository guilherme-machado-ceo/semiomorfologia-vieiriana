from setuptools import setup, find_packages

setup(
    name="semiomorfologia-vieiriana",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["numpy>=1.21.0", "scipy>=1.7.0", "scikit-learn>=1.0.0"],
    extras_require={"embeddings": ["sentence-transformers>=2.2.0"]},
)
