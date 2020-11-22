# A Simple Dash App for Predicting Developer Compensations

This is a very simple applet I've strung together out of prebaked code so users can interface with a predictive model I built around the 2020 Stack Overflow Devloper Survey results. The model used in this app is a boosted simple linear regression.

A NOTE ABOUT THE .LOCK FILE AND HEROKU:
I used pipenv to manage my packages and heroku hated the .lock I used and reverted to using an old version of pip that did not work with some of the packages I was using. I solved this by converting the .lock to a requirements.txt and heroku built the enviornment with a newer version of pip. 
