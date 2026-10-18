def load_data(df, output_path):
    """
    Save transformed data to CSV.
    """

    df.to_csv(output_path, index=False)

    return True