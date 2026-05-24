from setuptools import setup, find_packages

setup(
    name="semiomorfologia-vieiriana",
    version="3.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.0.0",
    ],
    extras_require={
        "embeddings": ["sentence-transformers>=2.2.0"],
        "api": [
            "fastapi>=0.100.0", "uvicorn>=0.22.0", "typer>=0.9.0",
            "httpx>=0.24.0", "networkx>=3.0", "pyvis>=0.3.0",
            "sparqlwrapper>=2.0.0", "requests>=2.28.0",
        ],
        "visualization": ["networkx>=3.0", "pyvis>=0.3.0"],
        "knowledge": ["sparqlwrapper>=2.0.0", "requests>=2.28.0"],
        "quantum": ["qiskit>=1.0.0", "qiskit-aer>=0.13.0"],
        "all": [
            "sentence-transformers>=2.2.0",
            "fastapi>=0.100.0", "uvicorn>=0.22.0", "typer>=0.9.0",
            "httpx>=0.24.0", "networkx>=3.0", "pyvis>=0.3.0",
            "sparqlwrapper>=2.0.0", "requests>=2.28.0",
            "qiskit>=1.0.0", "qiskit-aer>=0.13.0",
        ],
    },
)
