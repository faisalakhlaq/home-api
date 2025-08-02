from textwrap import dedent

property_count_doc = dedent(
    """
    Returns the number of properties that match the applied filters.

    This endpoint applies the same filtering logic as the list view. By default,
    it returns the count of active properties. If a 'status' query parameter
    is provided, the count will reflect the number of properties in the specified
    status(es).
    """
)
