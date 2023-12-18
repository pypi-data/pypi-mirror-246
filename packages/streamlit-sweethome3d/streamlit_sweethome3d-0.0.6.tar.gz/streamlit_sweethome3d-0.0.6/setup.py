import setuptools

import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'streamlit_sweethome3d/pypi_readme.md'), 'r') as f:
  long_des = f.read()

setuptools.setup(
    name="streamlit_sweethome3d",
    version="0.0.6",
    author="Nicola Landro",
    author_email="nicolaxx94@live.it",
    description="This library is created for streamlit framework, it allow to creating house and insert furniture based on sweethome3djs with a good 3D view.",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nicolalandro/streamlit-sweethome3d",
    keywords = ['3d', 'house planner', 'streamlit'],
    project_urls={
        'Source': 'https://gitlab.com/nicolalandro/streamlit-sweethome3d',  
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
