import setuptools

setuptools.setup(
    name="Turtle",
    version="v1.3",
    author="Nicolas Elger",
    author_email="nicolas.elger@free.fr",
    description="A turtle made with pygame",
    long_description="Controls:\nSPACE to show/hide the turtle, F1 key to zoom-in, F2 key to zoom-out, ARROWS to move arround, ESCAPE key or closing button to close the window.",
    url="https://github.com/Nico-hub856/Turtle",
    packages=setuptools.find_packages(exclude=("tests")),
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6'
)
