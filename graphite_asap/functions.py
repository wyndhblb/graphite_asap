import six

from graphite_api.evaluator import evaluateTokens
from graphite_api.render.datalib import TimeSeries
from graphite_api.render.attime import parseTimeOffset
from graphite_api.utils import to_seconds

from datetime import timedelta

from .asap import smooth


def ASAP(requestContext, seriesList, resolution=1000):
    '''
    use the ASAP smoothing on a series

    https://arxiv.org/pdf/1703.00983.pdf
    https://raw.githubusercontent.com/stanford-futuredata/ASAP/master/ASAP.py


    :param requestContext:
    :param seriesList:
    :param resolution: either number of points to keep or a time resolution
    :return: smoothed(seriesList)
    '''

    if not seriesList:
        return []

    windowInterval = None
    if isinstance(resolution, six.string_types):
        delta = parseTimeOffset(resolution)
        windowInterval = to_seconds(delta)

    if windowInterval:
        previewSeconds = windowInterval
    else:
        previewSeconds = max([s.step for s in seriesList]) * int(resolution)

    # ignore original data and pull new, including our preview
    # data from earlier is needed to calculate the early results
    newContext = requestContext.copy()
    newContext['startTime'] = (requestContext['startTime'] -
                               timedelta(seconds=previewSeconds))
    previewList = evaluateTokens(newContext, requestContext['args'][0])
    result = []
    for series in previewList:

        if windowInterval:
            # the resolution here is really the number of points to maintain
            # so we need to convert the "seconds" to num points
            windowPoints = round((series.end - series.start) / windowInterval)
        else:
            use_res = int(resolution)
            if len(series) < use_res:
                use_res = len(series)
            windowPoints = use_res

        if isinstance(resolution, six.string_types):
            newName = 'asap(%s,"%s")' % (series.name, resolution)
        else:
            newName = "asap(%s,%s)" % (series.name, resolution)

        step_guess = (series.end - series.start) / \
            windowPoints  # seems float "steps" are approved

        newSeries = TimeSeries(
            newName,
            series.start,
            series.end,
            step_guess,
            []
        )
        newSeries.pathExpression = newName

        # detect "none" lists
        if len([v for v in series if v is not None]) <= 1:
            newSeries.extend(series)
        else:
            # the "resolution" is a suggestion,
            # the algo will alter it some inorder
            # to get the best view for things
            new_s = smooth(series, windowPoints)
            # seems float "steps" are approved
            new_step = round((series.end - series.start) / len(new_s))
            newSeries.step = new_step
            newSeries.extend(smooth(series, windowPoints))
        result.append(newSeries)

    return result


ASAPFunctions = {
    'asap': ASAP
}
