"""General filtering utilities."""

import numpy as np
import pandas as pd
from annalist.annalist import Annalist

annalizer = Annalist()


def clip(unclipped, low_clip: float, high_clip: float):
    """Clip values in a pandas Series within a specified range.

    Parameters
    ----------
    unclipped : pandas.Series
        Input data to be clipped.
    high_clip : float
        Upper bound for clipping. Values greater than this will be set to NaN.
    low_clip : float
        Lower bound for clipping. Values less than this will be set to NaN.

    Returns
    -------
    pandas.Series
        A Series containing the clipped values with the same index as the
        input Series.
    """
    unclipped_arr = unclipped.to_numpy()

    # Create a boolean condition for values that need to be clipped
    clip_cond = (unclipped_arr > high_clip) | (unclipped_arr < low_clip)

    # Use pandas' where function to clip values to NaN where the condition is
    # True
    clipped_series = unclipped.where(~clip_cond, np.nan)

    return clipped_series


# noinspection SpellCheckingInspection
def fbewma(input_data, span: int):
    """Calculate the Forward-Backward Exponentially Weighted Moving Average (FBEWMA).

    Parameters
    ----------
    input_data : pandas.Series
        Input time series data to calculate the FBEWMA on.
    span : int
        Span parameter for exponential weighting.

    Returns
    -------
    pandas.Series
        A Series containing the FBEWMA values with the same index as the
        input Series.
    """
    # Calculate the Forward EWMA.
    fwd = input_data.ewm(span=span).mean()

    # Calculate the Backward EWMA. (x[::-1] is the reverse of x)
    bwd = input_data[::-1].ewm(span=span).mean()

    # Stack fwd and the reverse of bwd on top of each other.
    stacked_ewma = pd.concat([fwd, bwd[::-1]])

    # Calculate the FB-EWMA by taking the mean between fwd and bwd.
    return stacked_ewma.groupby(level=0).mean()


def remove_outliers(input_data, span: int, delta: float):
    """Remove outliers.

    Remove outliers from a time series by comparing it to the
    Forward-Backward Exponentially Weighted Moving Average (FBEWMA).

    Parameters
    ----------
    input_data : pandas.Series
        Input time series data.
    span : int
        Span parameter for exponential weighting used in the FBEWMA.
    delta : float
        Threshold for identifying outliers. Values greater than this
        threshold will be set to NaN.

    Returns
    -------
    pandas.Series
        A Series containing the time series with outliers removed with
        the same index as the input Series.
    """
    # Calculate the FBEWMA of the time series
    fbewma_series = fbewma(input_data, span)

    # Create a condition to identify outliers based on the absolute difference
    # between input_data and fbewma_series
    delta_cond = np.abs(input_data - fbewma_series) > delta

    # Set values to NaN where the condition is True
    return input_data.where(~delta_cond, np.nan)


def remove_spikes(
    input_data, span: int, low_clip: float, high_clip: float, delta: float
):
    """Remove spikes.

    Remove spikes from a time series data using a combination of clipping and
    interpolation.

    Parameters
    ----------
    input_data : pandas.Series
        Input time series data.
    span : int
        Span parameter for exponential weighting used in outlier detection.
    low_clip : float
        Lower bound for clipping. Values less than this will be set to NaN.
    high_clip : float
        Upper bound for clipping. Values greater than this will be set to NaN.
    delta : float
        Threshold for identifying outliers. Values greater than this threshold
        will be considered spikes.

    Returns
    -------
    pandas.Series
        A Series containing the time series with spikes removed with the same
        index as the input Series.
    """
    # Clip values in the input data within the specified range
    clipped = clip(input_data, low_clip, high_clip)

    # Remove outliers using the remove_outliers function
    gaps_series = remove_outliers(clipped, span, delta)

    # Could use pandas' .interpolate() on the Series
    # interp_series = gaps_series.interpolate()

    return gaps_series


def remove_range(input_series: pd.Series, from_date, to_date):
    """
    Remove data from series in given range.

    Returns the input series without data between from_date and to_date
    inclusive

    Parameters
    ----------
    input_series : pd.Series
        The series to have a section removed
    from_date : str
        Start of removed section
    to_date : str
        End of removed section

    Returns
    -------
    pd.Series
        The series with relevant slice removed
    """
    slice_to_remove = input_series.loc[from_date:to_date]
    return input_series.drop(slice_to_remove.index)
