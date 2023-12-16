# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gzip
import logging
import re
from io import StringIO
from os.path import exists

import polars
from packaging import version

from .parsing_error import ParsingError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
Columns of a GTF file:

    seqname   - name of the chromosome or scaffold; chromosome names
                without a 'chr' in Ensembl (but sometimes with a 'chr'
                elsewhere)
    source    - name of the program that generated this feature, or
                the data source (database or project name)
    feature   - feature type name.
                Features currently in Ensembl GTFs:
                    gene
                    transcript
                    exon
                    CDS
                    Selenocysteine
                    start_codon
                    stop_codon
                    UTR
                Older Ensembl releases may be missing some of these features.
    start     - start position of the feature, with sequence numbering
                starting at 1.
    end       - end position of the feature, with sequence numbering
                starting at 1.
    score     - a floating point value indiciating the score of a feature
    strand    - defined as + (forward) or - (reverse).
    frame     - one of '0', '1' or '2'. Frame indicates the number of base pairs
                before you encounter a full codon. '0' indicates the feature
                begins with a whole codon. '1' indicates there is an extra
                base (the 3rd base of the prior codon) at the start of this feature.
                '2' indicates there are two extra bases (2nd and 3rd base of the
                prior exon) before the first codon. All values are given with
                relation to the 5' end.
    attribute - a semicolon-separated list of tag-value pairs (separated by a space),
                providing additional information about each feature. A key can be
                repeated multiple times.

(from ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/README)
"""

REQUIRED_COLUMNS = [
    "seqname",
    "source",
    "feature",
    "start",
    "end",
    "score",
    "strand",
    "frame",
    "attribute",
]


def parse_gtf(
    filepath_or_buffer,
    restrict_attribute_columns=None,
    expand_attribute_column=True,
    features=None,
):
    """Parse lines into column->values dictionary and then expand the
    'attribute' column into multiple columns. This expansion happens by
    replacing strings of semi-colon separated key-value values in the
    'attribute' column with one column per distinct key, with a list of values
    for each row (using None for rows where key didn't occur).

    Parameters
    ----------
    filepath_or_buffer : str or buffer object

    restrict_attribute_columns : list/set of str or None
        If given, then only use these attribute columns.

    features : set or None
        Ignore entries which don't correspond to one of the supplied features
    """
    # use a global string cache so that all strings get intern'd into
    # a single numbering system
    if version.parse(polars.__version__) >= version.parse("0.17.0"):
        polars.enable_string_cache(True)
    else:
        polars.toggle_string_cache(True)

    kwargs = dict(
        has_header=False,
        comment_char="#",
        null_values=".",
        dtypes={
            "seqname": polars.Categorical,
            "source": polars.Categorical,
            "start": polars.Int64,
            "end": polars.Int64,
            "score": polars.Float32,
            "feature": polars.Categorical,
            "strand": polars.Categorical,
            "frame": polars.UInt32,
        },
    )
    if version.parse(polars.__version__) >= version.parse("0.16.14"):
        kwargs["separator"] = "\t"
    else:
        kwargs["sep"] = "\t"

    try:
        if type(filepath_or_buffer) is StringIO:
            df = polars.read_csv(
                filepath_or_buffer, new_columns=REQUIRED_COLUMNS, **kwargs
            ).lazy()
        elif filepath_or_buffer.endswith(".gz") or filepath_or_buffer.endswith(
            ".gzip"
        ):
            with gzip.open(filepath_or_buffer) as f:
                df = polars.read_csv(
                    f, new_columns=REQUIRED_COLUMNS, **kwargs
                ).lazy()
        else:
            df = polars.scan_csv(
                filepath_or_buffer,
                with_column_names=lambda cols: REQUIRED_COLUMNS,
                **kwargs
            ).lazy()
    except polars.ShapeError:
        raise ParsingError("Wrong number of columns")

    if features is not None:
        features = sorted(set(features))
        df = df.filter(polars.col("feature").is_in(features))

    df = df.with_columns(
        [
            polars.col("frame").fill_null(0),
            # polars.col("attribute").str.replace_all('"', "'")
        ]
    )

    # convert lazyDataFrame to DataFrame
    df = df.collect()
    if expand_attribute_column:
        if isinstance(restrict_attribute_columns, str):
            restrict_attribute_columns = {restrict_attribute_columns}
        elif restrict_attribute_columns:
            restrict_attribute_columns = set(restrict_attribute_columns)
        else:
            restrict_attribute_columns = set()

        def extract_attributes(gtf_attr):
            records = re.findall(r"(\S+) \"([^\"]+)\";", gtf_attr)
            return dict(records)

        # Apply the function to each row
        annot_df = (
            df["attribute"]
            .apply(lambda x: extract_attributes(x))
            .struct.unnest()
        )
        df = polars.concat([df, annot_df], how="horizontal")
        df = df.drop("attribute")

    return df


def parse_gtf_and_expand_attributes(*args, **kwargs):
    kwargs["expand_attribute_column"] = True
    return parse_gtf(*args, **kwargs)


def parse_gtf_pandas(*args, **kwargs):
    return parse_gtf(*args, **kwargs).to_pandas()


def read_gtf(
    filepath_or_buffer,
    expand_attribute_column=True,
    infer_biotype_column=False,
    column_converters={},
    usecols=None,
    features=None,
    result_type="pandas",
):
    """Parse a GTF into a dictionary mapping column names to sequences of
    values.

    Parameters
    ----------
    filepath_or_buffer : str or buffer object
        Path to GTF file (may be gzip compressed) or buffer object
        such as StringIO

    expand_attribute_column : bool
        Replace strings of semi-colon separated key-value values in the
        'attribute' column with one column per distinct key, with a list of
        values for each row (using None for rows where key didn't occur).

    infer_biotype_column : bool
        Due to the annoying ambiguity of the second GTF column across multiple
        Ensembl releases, figure out if an older GTF's source column is actually
        the gene_biotype or transcript_biotype.

    column_converters : dict, optional
        Dictionary mapping column names to conversion functions. Will replace
        empty strings with None and otherwise passes them to given conversion
        function.

    usecols : list of str or None
        Restrict which columns are loaded to the give set. If None, then
        load all columns.

    features : set of str or None
        Drop rows which aren't one of the features in the supplied set

    result_type : One of 'polars', 'pandas', or 'dict'
        Default behavior is to return a Polars DataFrame, but will convert to
        Pandas DataFrame or dictionary if specified.
    """
    if isinstance(filepath_or_buffer, str) and not exists(filepath_or_buffer):
        raise ValueError("GTF file does not exist: %s" % filepath_or_buffer)

    result_df = parse_gtf(
        filepath_or_buffer,
        restrict_attribute_columns=usecols,
        expand_attribute_column=expand_attribute_column,
        features=features,
    )

    for column_name, column_type in column_converters.items():
        result_df = result_df.with_columns(
            polars.col(column_name).apply(
                lambda x: column_type(x) if len(x) > 0 else None
            )
        )

    # Hackishly infer whether the values in the 'source' column of this GTF
    # are actually representing a biotype by checking for the most common
    # gene_biotype and transcript_biotype value 'protein_coding'
    if infer_biotype_column:
        unique_source_values = set(result_df["source"])
        if "protein_coding" in unique_source_values:
            column_names = set(result_df.columns)
            # Disambiguate between the two biotypes by checking if
            # gene_biotype is already present in another column. If it is,
            # the 2nd column is the transcript_biotype (otherwise, it's the
            # gene_biotype)
            if "gene_biotype" not in column_names:
                logging.info(
                    "Using column 'source' to replace missing 'gene_biotype'"
                )
                result_df = result_df.with_columns(
                    polars.col("source").alias("gene_biotype")
                )
            if "transcript_biotype" not in column_names:
                logging.info(
                    "Using column 'source' to replace missing 'transcript_biotype'"
                )
                result_df = result_df.with_columns(
                    polars.col("source").alias("transcript_biotype")
                )

    if usecols is not None:
        column_names = set(result_df.columns)
        valid_columns = [c for c in usecols if c in column_names]
        result_df = result_df.select(valid_columns)

    if result_type == "pandas":
        return result_df.to_pandas()
    elif result_type == "dict":
        return result_df.to_dict()
    return result_df
