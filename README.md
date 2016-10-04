# Confluence Wiki page to tex format
This is programme that takes a Atlassian Confluence wiki page and converts it
to a tex file.

It is set up using Python VirtualEnv

To run the programme you must do the following steps

1. Step into the Virtual Env

> source ./conf-api/bin/activate

2. Change the config.ini file

> To your username / password
> The title of the page you want to convert

When looking at the Confluence website if the title has + symbols in the title within the URL such as D5.2+Work+page then in the config file the +'s must become spaces ( ), and should be D5.2 Work page in the config file.

3. Run the programme with

> behave

4. Should find a file called .tex in the directory.
