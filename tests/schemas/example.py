from pandera import DataFrameSchema, Column, Check, Index, MultiIndex

schema = DataFrameSchema(
    checks=None,
    index=None,
    dtype=None,
    coerce=False,
    strict=False,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    add_missing_columns=False,
    title="Schema example",
    description="Description of dataset",
    columns={
        "SAMPLE_ID": Column(
            dtype="str",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description="Unique name of sample",
            title="Sample ID"
        ),
    },
)
