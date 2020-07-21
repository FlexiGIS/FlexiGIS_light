

def shape_legend(node, ax, handles, labels, reverse=False, **kwargs):
    """Plot legend manipulation. This code is copied from the oemof example script
    see link here: https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.3.x/plotting_examples
    """
    handels = handles
    labels = labels
    axes = ax
    parameter = {}

    new_labels = []
    for label in labels:
        label = label.replace('(', '')
        label = label.replace('), flow)', '')
        label = label.replace(node, '')
        label = label.replace(',', '')
        label = label.replace(' ', '')
        new_labels.append(label)
    labels = new_labels

    parameter['bbox_to_anchor'] = kwargs.get('bbox_to_anchor', (1, 0.5))
    parameter['loc'] = kwargs.get('loc', 'center left')
    parameter['ncol'] = kwargs.get('ncol', 1)
    plotshare = kwargs.get('plotshare', 0.9)
    if reverse:
        handels = handels.reverse()
        labels = labels.reverse()
    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * plotshare, box.height])
    parameter['handles'] = handels
    parameter['labels'] = labels
    axes.legend(**parameter)

    return axes
