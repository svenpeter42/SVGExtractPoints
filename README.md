# SVGExtractPoints
Tiny tool to extract values from SVG plots usually found inside PDF files. Useful to extract results from research papers to accurately compare with your work.

# Installation
```
pip install git+https://github.com/svenpeter42/SVGExtractPoints@master
```

# Usage
* Open the PDF in Inkscape, make sure to select "import via poppler" to make the paths nicer
* Save as SVG
* Find two X and Y ticks each for which you can easily read the coordinates. Click on them and write down the pathid and the coordinate.
* Click on the curve you want to extract and write down the path id
* Run the following command

```
SVGExtractPoints
    -svg filename.svg
    -x0 *pathNNN for first x coordinate*,*first x coordinate*
    -x1 *pathNNN for second x coordinate*,*second x coordinate*
    -y0 *pathNNN for first y coordinate*,*first y coordinate*
    -y1 p*pathNNN for second y coordinate*,*second y coordinate*
    -path *descriptive name*,*pathNNN of the first curve* *descriptive name*,*pathNNN of the second curve* .... 
    -output points.yml
```
