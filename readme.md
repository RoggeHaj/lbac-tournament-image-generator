# Introduction

This is a small python hack that allows one to quickly generate PNG images with social media format friendly
ads for LBAC ranked tournaments.

The script is simply performing search and replace of a few anchors in an SVG template and also sets the
background image according to the gender for the tournament.

## Background image

When updating the SVG template, there's a few things to take into account if you want things to work smoothly.

1. Do not embed the background images in the SVG. Always use xlink attribute to link to an external image
   in the assets directory.

2. Make sure that no image is visible when you are done editing. look for `style="display:none"` in the
   image tags. The script will select an appropriate image tag and change the style to `display:normal`
   when generating the PNG export

3. The background images are selected based on the id tag in the SVG file, *not the filename*. This means
   you are free to name the asset anything as long as you include the gender `{herr, dam}` in the id
   field in the SVG. The script will collect all image tags under the `Background` layer whose name
   includes the selected gender and randomly select an image from that collection for the background.
