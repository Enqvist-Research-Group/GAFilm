# GAFilm
gafchromic film analysis repo  
  
[gafchromic film website](http://www.gafchromic.com/)  
A few useful pdfs are saved in ./doc/ herein

## Scanning films
- While the measured difference between the transparency when scanning the shiny versus dull side of a film is gived to be minimal, all analyses herein use the following: (1) shiny side of the film always points towards the radiation source, and (2) both sides of a dosed film should be scanned and saved accordingly (see filname convention below) for redundancy, but for consistency, the shiny-side scan will be used for consistency. 
  
## scanned film tiff filename convention:  
&lt;YYMMDD&gt;\_&lt;source or location&gt;\_&lt;absorbed dose in Gy or exposure time, if known&gt;\_&lt;film type: MD or HD&gt;\_&lt;side of film: shiny or dull&gt;.tiff  
E.g., calibrated dose: 230404_shands_50Gy_HD_dull.tiff  
E.g., unknown dose from UFTR reactor shot: 230301_ShieldTankInsideGlass_1h_HD_dull.tiff  
  
## genFit Useage  
```
$ python ./code_brice/genFit.py -id/--INPUTDIR ./local/path/to/dosed/films/ -rf/--REFFILM ./local/path/to/reference/film.tif
```
