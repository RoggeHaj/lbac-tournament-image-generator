# lbac-tournament-image-generator

Script collection that allows for rapid creation of images suited for social media to
promote beach volleyball tournaments hosted by LBAC (Linköping Beach Arena Club).

## tournament-generator.py

The main python script, tournament-generator.py takes mandatory arguments:
  * --date which is the date for the tournament
  * --level which is the level for the tournament on the Swedish Beach Tour
  * --gender which is the gender for the tournament teams

The optional arguments are:
  * --no-color which prevents colorization of the image according to tournament level
  * --template which points to an alternate template than the default (tournament_template.svg)

## read_file.sh

To allow for batch creation, a small shell script (read_file.sh) that simply reads a text file 
provided as argument and calls the main python program for each line in the file exists.

## Features

The main function of the script is to turn the arguments into correct texts and replace the 
placeholders in the SVG file with those text. Currently, the script expects the following
placeholders:

  * @DATE@ which will expand to the full date of the tournament
  * @SHORT_MONTH@ which will expand to the three letter abbreviation for the month of the tournament date
  * @STARS@ which will expand to the nuber of stars for the tournament (given in the --level arg)
  * @GENDER@ which will expand to the gender for the tournament (given in the --gender arg)
  * @DAY@ which will expand to the weekday name for the tournament date
  * @MONTH@ which will expand to the month name for the tournament date
  * @UC_GENDER@ which will expand to the upper case variant of @GENDER@
  * @TYPE@ which will expand to the textual representation of @STARS@

Once the texts have been replaced, a system call to invoke [inkscape](https://inkscape.org) will be made
to render the image.
