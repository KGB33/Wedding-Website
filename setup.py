import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='WeddingWebsite',  
     version='0.1',
     author="Kelton Bassingthwaite",
     author_email="weddingWebsite@bassingthwaite.org",
     description="A Website for my Wedding",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
     ],
 )