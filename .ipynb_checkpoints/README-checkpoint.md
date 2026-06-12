# TWISTER: Telling Where to Increase, StrengThen, and Expand Radars
Data analysis pipeline to identify where the addition of new NEXRAD weather radars would fill current radar coverage gaps and assist in early warnings of tornado producing storms.

**Background:** Tornados are a highly damaging and dangerous weather phenomenon that appear with minimal warning beforehand. Alerts for potential tornadoes from the National Weather Service are highly dependent on reading the output from radars all across the country. To ensure these alerts are recieved by affected parties in a timely manner, high quality and high convergae data is a necessity. Unfortunately the convergae by available WSR-88D radars is limited in some areas where, historically, damaging tornadoes are more common. Identifying these high-risk low-coverage areas and installing new weather radars can increase the liklihood that the National Weather Service can issue alerts accurently and save lives.

**Goal:** Identify where new NEXRAD-class weather radars would most reduce the risk of unwarned tornado strikes on populated areas.

**Strategy:** Using KDE mapping based on tornado intensity ratings (F and EF scale), clustering of previous tornadoes, and population, determine the best locations to build 5 new WSR-88D weather radars. Ensuring that these new radar placements most optimally fill in gaps in existing radar coverage.

**Data:** Raw data can be re-downloaded using the download.py script in the src directory.

(1) NOAA Storm Events -- Detailed CSVs containing information on severe storms available from 1990 to 2025. This contains information about tornado events such as severity scale (i.e. EF0 - EF5 or F0 - F5 before 2007), estimated start coordinates for the storm, date and time, human impact (injuries/deaths), etc.

(2) NEXRAD WSR-88D site list -- From the NWS radar API, contains the locations of all existing WSR-88D weather radars. Will be used, along with estimated effective range of these radars in detecting storms, to determine where there are gaps in radar coverage.

(3) US Census 2020 -- County population estimates to determine population density in the regions of interest. Higher population regions with radar gaps should be prioritized. 

(4) Census TIGER simplified county boundaries -- File containing county boundaries to map the population densities to a map of the CONUS. Used to integrate the storm event data with the population data.



## Dependencies
For data download: requests

For main analysis code: ...

