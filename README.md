# Graphite-ASAP

This is a graphite-api function for the ASAP dynamic smoothing algorithm

https://arxiv.org/pdf/1703.00983.pdf

# NOTE ABOUT GRAPHITE API

this requires the MAIN BRANCH of graphite-api, the current 1.1.3 version is not really up-to-date

    pip install --upgrade git+https://github.com/brutasse/graphite-api
    
    
## Note On Nulls

If you data as "nulls/Nones" in the data list, it will FORCE them to be 0, otherwise
the algorithm cannot really function, as it needs to be able to dynamically compute windowing layers.

## Note on the Algo

This is a dynamic windowing algorithm, meaning that the returned vector is NOT necessarily going to be the same
length as the one you wish.  If you want a 500 point vector back you can easily get much lower then that if
the windowing deems it ok.  For very "flat" data (i.e. sigma^4 is very small) you may even just get a few points.

In your graphing world it's recommended you use "connected" lines, not just points, as the returned data can be
very sparse.

## usage

In the `graphite-api.yaml` file install this package and then add to the functions list

    functions:
        - graphite_asap.functions.ASAPFunctions

And in your favorite query engine
    
    # attempt to get a vector with 10second steps
    http://xxx/render?target=asap(path.to.metric, '10s')
    
    # attempt to get a vector that has roughly this number of points
    http://xxx/render?target=asap(path.to.metric, 100)
