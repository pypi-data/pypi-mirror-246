.. _basics-2d_hist-label:

========
Basic 2D
========

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be loaded with:

.. code-block:: python

    from plothist import get_dummy_data
    df = get_dummy_data()


Simple plot
===========

To plot a simple 2d histogram:

.. literalinclude:: ../examples/2d_hist/2d_hist_simple.py
    :language: python
    :start-after: ###

.. image:: ../img/2d_hist_simple.svg
   :alt: Simple 2d hist
   :width: 500


Correlations with variable registry
===================================

See :ref:`basics-variable_registry-label` on how to use the variable registry.

The variable registry is a really useful tool to manage and plot the correlation between multiple variables:

.. literalinclude:: ../examples/2d_hist/2d_hist_correlations.py
    :language: python
    :start-after: ###


|img1| |img2| |img3|

.. |img1| image:: ../img/2d_hist_correlations_0.svg
   :alt: 2d correlation plot
   :width: 210

.. |img2| image:: ../img/2d_hist_correlations_1.svg
   :alt: 2d correlation plot
   :width: 210

.. |img3| image:: ../img/2d_hist_correlations_2.svg
   :alt: 2d correlation plot
   :width: 210


Uneven binning
==============

Instead of inputing a number of bins and a range in ``make_2d_hist()``, the bins parameter can be a list of all the edges:

.. literalinclude:: ../examples/2d_hist/2d_hist_uneven.py
    :language: python
    :start-after: ###

.. image:: ../img/2d_hist_uneven.svg
   :alt: 2d hist with uneven binning
   :width: 500



Display 1D distributions
========================

To plot a 2d histogram with x and y projections:

.. literalinclude:: ../examples/2d_hist/2d_hist_with_projections.py
    :language: python
    :start-after: ###

.. image:: ../img/2d_hist_with_projections.svg
   :alt: 2d hist with x and y projections
   :width: 500