# Graphite-ASAP

This is a graphite-api function for the ASAP dynamic smoothing algorithm

https://arxiv.org/pdf/1703.00983.pdf

# NOTE ABOUT GRAPHITE API

this requires the MAIN BRANCH of graphite-api, the current 1.1.3 version is not really up-to-date

    pip install --upgrade git+https://github.com/brutasse/graphite-api
    
    
## Note On Nulls

If you data as "nulls/Nones" in the data list, it will FORCE them to be 0, otherwise
the algorithm cannot really function, as it needs to be able to dynamically compute windowing layers.


## usage

In the `graphite-api.yaml` file install this package and then add to the functions list

    functions:
        - graphite_asap.functions.ASAPFunctions
