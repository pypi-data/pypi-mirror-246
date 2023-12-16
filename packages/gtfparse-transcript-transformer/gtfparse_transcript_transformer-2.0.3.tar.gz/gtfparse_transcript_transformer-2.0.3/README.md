Temporary fix for gtfparse to work with polars>0.16, based on https://github.com/y9c/gtfparse

gtfparse
========
Parsing tools for GTF (gene transfer format) files.

# Example usage

## Parsing all rows of a GTF file into a Pandas DataFrame

```python
from gtfparse import read_gtf

# returns GTF with essential columns such as "feature", "seqname", "start", "end"
# alongside the names of any optional keys which appeared in the attribute column
df = read_gtf("gene_annotations.gtf")

# filter DataFrame to gene entries on chrY
df_genes = df[df["feature"] == "gene"]
df_genes_chrY = df_genes[df_genes["seqname"] == "Y"]
```


## Getting gene FPKM values from a StringTie GTF file

```python
from gtfparse import read_gtf

df = read_gtf(
    "Transcripts.gtf",
    column_converters={"FPKM": float})

gene_fpkms = {
    gene_name: fpkm
    for (gene_name, fpkm, feature)
    in zip(df["seqname"], df["FPKM"], df["feature"])
    if feature == "gene"
}
```


