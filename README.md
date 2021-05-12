# Streamlit GLVis viewer

This is a initial attempt of a port of the [GLVis/glvis-js](https://github.com/GLVis/glvis-js) code to be a streamlit component.

# To run 

You are required to have streamlit and node installed.

    $ pip install streamlit

Node is required if the frontend is to be used, otherwise you will see some minor errors. But the `components.html` do not require them. In one terminal run

    $ cd streamlit-glvis/streamlit-glvis/frontend
    $ node install
    $ node run start

In another

    $ cd streamlit-glvis
    $ streamlit run streamlit-glvis/__init__.py

Then go to the Local URL that streamlit tells you to go.

# Notes

ESlint was disabled in package.json as one attempt to get the glvis code working with the ReactJS backend, but to no avail.

# GLVis/glvis-js License

Code taken from GLVis/glvis-js is under a BSD3 License. Code used from this project is attributed the appropriate license indicated in code.
