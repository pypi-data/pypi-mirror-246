from setuptools import setup, find_packages


VERSION = '0.0.0'
DESCRIPTION = 'BlueMoon AI: Open-source Text to Image Generative AI. Transform text into stunning visuals effortlessly. Free to use and contribute on GitHub.'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="bluemoonai",
    version=VERSION,
    author="bluemoonai",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/BlueMoonAI/BlueMoonAI.git',
    packages=find_packages(),
    keywords=['text-to-image', 'AI model', 'NLP', 'computer vision', 'deep learning', 'ai','machine learning','artificial intelligence','image generation','image generator','bluemoonai','bluemoon'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    install_requires=[],
    license='Apache Software License (Apache 2.0)',
    project_urls={
        'Source Code': 'https://github.com/BlueMoonAI/BlueMoonAI',
        'Bug Tracker': 'https://github.com/BlueMoonAI/BlueMoonAI/issues',
        'Documentation': 'https://github.com/BlueMoonAI/BlueMoonAI#readme',
    },
)

print("Happy Creative!")
