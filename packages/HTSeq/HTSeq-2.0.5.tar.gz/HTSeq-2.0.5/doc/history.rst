.. _history:

***************
Version history
***************

Version 2.0.5
=============
2023-12-13

Fixes installation on some platforms, only upgrade if necessary if you already have 2.0.4 (though it does not hurt).

- Bugfix for poetry and other package managers courtesy of @cameronraysmith.

Version 2.0.4
=============

All users are encouraged to upgrade.

- `htseq-count` now checks if any chromosome names match between the BAM and GFF/GTF file. If not, it shows a warning to stderr.
- Python 3.11 is covered on CI build and deploy (linux only - OSX is not supported by `pysam` yet).

Version 2.0.3
=============
2023-05-16

Bugfix release. All users are encouraged to upgrade.

- `GenomicInterval_from_directional` had a typo (issue #62). Thanks @justinaruda for spotting it.

Version 2.0.2
=============
2022-07-03

Bugfix release. All users are encouraged to upgrade.

Scripts:

- ``htseq-count`` had silently adopted a new logic to handle a corner case where read 1 was missing but read 2 was present. This has now been reverted
  to ensure exact compatibility with ``HTSeq<=0.13.5``.


Version 2.0.1
=============
2022-03-25

Maintenance version. Users are not required to upgrade.

CI:

- Updated docker CI requirements.

Version 2.0.0
=============
2022-03-22

Major release. All users are encouraged to upgrade.

Publication:

- New paper describing HTSeq 2.0 in [Bioinformatics](https://doi.org/10.1093/bioinformatics/btac166). **Please cite the new paper** to help us maintain HTSeq!

API features:

- Support for StretchVector, a data structure for "island-of-data" sparsity
- Added BigWig_Reader
- Added I/O functions for ``GenomicArray`` to/from bedGraph and BigWig files
- ``make_feature_genomicarrayofsets`` now supports multiple primary attributes
- ``make_feature_genomicarrayofsets`` can now add chromosome info as an additional attribute
- Improved context manager support (``with`` statement) for parsers
- Support for ``pathlib.Path`` objects

Scripts:

- Refactoring of ``htseq-count`` for readability
- Added exon-level counting to ``htseq-count``
- Added output formats to ``htseq-count``: loom, h5ad, mtx files
- The above all apply to ``htseq-count-barcodes`` as well.
- Added ``--with-header`` option to ``htseq-count``.

Documentation:

- Modernized template of docs
- Added tutorial on High C analysis
- Added step by step explanation of ``htseq-count`` logic
- Improved API documentation on a number of interfaces
- Improved docstrings throughout

Tests/Infrastructure:

- Better testing infra (e.g. ``test.sh``)
- Many more unit tests

Bug fixes:

- Fixed a bug with templates SAM files
- Fixed a bug about ``ChromVector`` steps.
- Fixed a bug about file opening (thanks @mruffalo)
- Fixed a bug about ambiguous reads (thanks @Mashin6)
- Fixed a typo in the docs (thanks @Tejindersingh1)
- Improved style of code and documentation

Version 0.13.5
==============
2020-12-29

Maintenance and small feature release

- Refactored CI to use Github actions.
- Improved docs and fixed docs building bugs
- Reader classes (e.g. FastaReader, BAM_Reader) can be used with ``with`` (as context managers)
- Fixed a few bugs in ``htseq-count``

Version 0.12.4
==============
2020-04-20

Bugfix release:

- use correct stranded information (thanks gaffneyk)


Version 0.12.3
==============
2020-04-18

New features:

- Negative indices for ``StepVector`` (thanks to shouldsee for the original PR).
- ``htseq-count-barcodes`` counts features in barcoded SAM/BAM files, e.g. 10X Genomics
  single cell outputs. It supports cell barcodes, which result in different columns of
  the output count table, and unique molecular identifiers.
- ``htseq-count`` has new option ``-n`` for multicore parallel processing
- ``htseq-count`` has new option ``-d`` for separating output columns by arbitrary character
  (defalt TAB, ``,`` is also common)
- ``htseq-count`` has new option ``-c`` for output into a file instead of stdout
- ``htseq-count`` has new option ``--append-output`` for output into a file by appending to
  any existing test (e.g. a header with the feature attribute names and sample names)
- ``htseq-count`` has two new values for option ``--nonunique``, namely ``fraction``, which
  will count an N-multimapper as 1/N for each feature, and ``random``, which will assign
  the alignment to a random one of its N-multimapped features. This feature was added by
  ewallace (thank you!).
- ``htseq-qa`` got refactored and now accepts an options ``--primary-only`` which ignores
  non-primary alignments in SAM/BAM files. This means that the final number of alignments
  scored is equal to the number of reads even when multimapped reads are present.

Testing improvements:

- Extensive testing and installation changes for Mac OSX 10.14 and later versions
- Testing Python 2.7, 3.6, 3.7, and 3.8 on OSX
- Testing and deployment now uses conda environments

Numerous bugfixes and doc improvements.

This is the **last** version of ``HTSEQ`` supporting Python 2.7, as it is unmaintained since Jan 1st, 2020. ``HTSeq`` will support Python 3.5+ from the next version.

Version 0.11.4
==============
2020-03-30

Fix a bug with Python3 and no-quality BAM/SAM files.

Version 0.11.3
==============
2020-03-01

Updates in the documentation and new wheels to fix installation bugs.

Version 0.11.2
==============
2019-01-07

Bugfix release for ``htseq-count``:

- fixed bug and changed how to use output SAM files via ``-o``: you now have
  to specify the option once per input/output file

Version 0.11.1
==============
2019-01-03

Bugfix release for ``htseq-count``:

- fixed bug and changed how to use of additional attributes via ``--additional-attr``

Version 0.11.0
==============
2018-08-01

- ``htseq-count`` ignores secondary and supplementary alignments by default
- bugfix in the SAM output of ``htseq-count``
- optional argument name in reverse complement function
- better linting of Cython files

Version 0.10.0
==============
2018-05-08

- flush output of ``htseq-count`` (thanks dcroote)
- pass memmap_dir to ChromVector.create (thanks wkopp)
- ``BAM_Reader`` supports ``check_sq`` for PacBio reads (thanks jbloom)
- a number of Bugfixes

Version 0.9.1
=============
2017-07-26

Bugfix release for ``htseq-count``:

- ``--secondary-alignments`` and ``supplementary-alignments`` should now work for some corner cases of unmapped reads


Version 0.9.0
=============
2017-07-11

This release adds a few options to ``htseq-count``:

- ``--secondary-alignments`` handles secondary alignments coming from the same read
- ``--supplementary-alignments`` handles supplementary alignments (aka chimeric reads)

Raw but fast iterators for FASTA and FASTQ files have been added.

Support for the SAM CIGAR flags ``=`` and ``X`` (sequence match and mismatch) has been added.

``Sequence`` objects can now be pickled/serialized.

Binaries for linux and OSX are now provided on PyPI.

Automation of the release process has been greatly extended, including OSX continuous integration builds.

Several bugs have been fixed, and some parts of the code have been linted or modernized.

Version 0.8.0
=============
2017-06-07

This release adds a few options to ``htseq-count``:

- ``--nonunique`` handles non-uniquely mapped reads
- ``--additional-attr`` adds an optional column to the output (typically for human-readable gene names)
- ``--max-reads-in-buffer`` allows increasing the buffer size when working with paired end, coordinate sorted files

Moreover, ``htseq-count`` can now take more than one input file and prints the output with one column per input file.

Finally, parts of the code have been streamlined or modernized, documentation has been moved to readthedocs,
and other minor changes.

Version 0.7.2
=============

2017-03-24

This release effectively merges the Python2 and Python3 branches.

Enhancements:

- ``pip install HTSeq`` works for both Python 2.7 and 3.4+


Version 0.7.1
=============

2017-03-16

Enhancements:

- installs from PyPI


Version 0.7.0
=============

2017-02-07

Enhancements:

- understands SAMtools optional field B (used sometimes in STAR aligner)
- write fasta files in a single line
- better docstrings thanks to SWIG 3

Bugfixes:

- fixed tests and docs in .rst files

Support bumps:

- supports pysam >=0.9.0

New maintainer: Fabio Zanini.


Version 0.6.1
=============

2014-02-27

- added parser classes for BED and Wiggle format

Patch versions:

- 0.6.1p1 (2014-04-13)

  - Fixed incorrect version tag

- 0.6.1p2 (2014-08-09)

  - some improvements to documentation


Version 0.6.0
=============

2014-02-26

- Several changes and improvements to htseq-count:

  - BAM files can now be read natively. (New option ``--format``)

  - Paired-end SAM files can be used also if sorted by position. No need any mroe to sort by name. (New option ``--order``.)

  - Documentation extended by a FAQ section.

  - Default for ``--minaqual`` is now 10. (was: 0)

- New chapter in documentation, with more information on counting reads.

- New function ``pair_SAM_alignments_with_buffer`` to implement pairing for position-sorted SAM files.


Version 0.5.4
=============

2013-02-20

Various bugs fixed, including

  - GFF_Reader interpreted the constructor's "end_included" flag
    in the wrong way, hence the end position of intervals of
    GFF features was off by 1 base pair before
    
  - htseq-count no longer warns about missing chromosomes, as this
    warning was often misleading. Also, these reads are no properly
    included in the "no_feature" count.
    
  - default for "max_qual" in "htseq-qa" is now 41, to accommodate newer
    Illumina FASTQ files
    
  - BAM_Reader used to incorrectly label single-end reads as paired-end


Patch versions:

* v0.5.4p1 (2013-02-22):

  - changed default for GFF_Reader to end_included=True, which is actually the
    correct style for Ensemble GTF files. Now the behavious should be as it 
    was before.

* v0.5.4p2 (2013-04-18):

  - fixed issue blocking proper built on Windows

* v0.5.4p3 (2013-04-29):

  - htseq-count now correctly skips over "M0" cigar operations

* v0.5.4p4 (2013-08-28):

  - added ``.get_original_line()`` function to ``VariantCall``
  - firex a bug with reads not being read as paired if they were not
    flagged as proper pair

* v0.5.4p5 (2013-10-02/2013-10-10):

  - parsing of GFF attribute field no longer fails on quoted semicolons
  - fixed issue with get_line_number_string

Version 0.5.3
=============

2011-06-29

- added the '--stranded=reverse' option to htseq-count


Patch versions:

* v0.5.3p1 (2011-07-15):

  - fix a bug in pair_sam_Alignment (many thanks for Justin Powell for
    finding the bug and suggesting a patch)
    
* v0.5.3p2 (2011-09-15)

  - fixed a bug (and a documentation bug) in trim_left/right_end_with_quals

* v0.5.3p3 (2011-09-15)

  - p2 was built improperly

* v0.5.3p5 (2012-05-29)

  - added 'to_line' function to VariantCall objects and 'meta_info' function to VCF_Reader objects to print VCF-lines / -headers respectively

* v0.5.3p5b (2012-06-01)
  - added 'flag' field to SAM_Alignment objects and fixed 'get_sam_line' function of those

* v0.5.3p6 (2012-06-11)
  - fixed mix-up between patches p3, p4 and p5

* v0.5.3p7 (2012-06-13)
  - switched global pysam import to on-demand version

* v0.5.3p9ur1 (2012-08-31)
  - corrected get_sam_line: tab isntead of space between optional fields

Version 0.5.2
=============

2011-06-24

- added the '--maxqual' option to htseq-qa


Version 0.5.1
=============

2011-05-03

- added steps method to GenomicArray

Patch versions:

* v0.5.1p1 (2011-05-11):

  - fixed a bug in step_vector.h causing linkage failure under GCC 4.2

* v0.5.1p2 (2011-05-12):

  - fixed pickling

* v0.5.1p3 (2011-05-22):

  - fixed quality plot in htseq-qa (top pixel row, for quality score 40, was cut off)

Version 0.5.0
=============

2011-04-21

- refactoring of GenomicArray class:

  - field ``step_vectors`` replaced with ``chrom_vector``. These now contain
    dicts of dicts of ``ChromVector`` objects rather than ``StepVector`` ones.
    
  - ``chrom_vectors`` is now always a dict of dict, even for unstranded GenomicArrays
    to make it easier to loop over them. (The inner dict has either keys ``"+"``
    and ``"-"``, or just one key, ``"."``.)
    
  - The new ``ChromVector`` class wraps the actual vector and supports three different
    storage modes: ``step``, ``ndarray`` and ``memmap``, the latter two being numpy
    arrays, without and with memory mapping.
    
  - The ``GenomicArray`` constructor now take two new arguments, one for the storage
    class, one for the memmap directory (if needed).
    
  - The ``add_value`` methods had been replaced with an ``__iadd__`` method, to
    enable the ``+=`` semantics.
    
  - Similarily, ``+=`` for ``GenomicArrayOfSets`` adds an element to the sets.
  
  - Instead of ``get_steps``, now use ``steps``.
  
  
- new parser class ``VCF_Reader`` and record class ``VariantCall``

- new parser class ``BAM_Reader``, to add BAM support (including indexed random access)
  (requires PySam to be installed)

- new documentation page :ref:`tss`

- ``Fasta_Reader`` now allows indexed access to Fasta files (requires Pysam to be 
  installed)
  
- peek function removed  

Patch Versions:

- v0.5.0p1  (2011-04-22):

  - build was incomplete; fixed

- v0.5.0p2 (2011-04-22):

  - build was still faulty; new try

- v0.5.0p3 (2011-04-26)

  - fixed regression bug in htseq-count

Version 0.4.7
=============

2010-12-22

- added new option ``-o`` (or ``--samout``) to htseq-count

Patch versions:

* Version 0.4.7p1 (2011-02-14)

  - bug fix: GFF files with empty attribute fiels are now read correctly

* Version 0.4.7p2 (2011-03-13)

  - fixed assertion error in pair_SAM_alignment, triggered by incorrect flags

* Version 0.4.7p3 (2011-03-15)

  - fixed problem due to SAM_Alignment.peek (by removing the method)

* Version 0.4.7p4 (2011-03-18)

  - removed left-over debugging print statement


Version 0.4.6
=============

2010-12-09

- pair_SAM_alignments now handles multiple matches properly

- SAM_Alignments now allows access to optional fields via the new methods
  optional_field and optional_fields
  
- htseq-count now skips reads that are non-uniquely mapped according to the 'NH'
  optional field
  
- updated documentation    

Patch versions:

* Version 0.4.6p1 (2010-12-17)

  - updated htseq-count documentation page

  - htseq-count now accepts '-' as SAM file name

* Version 0.4.6p2 (2012-12-21)

  - corrected a bug in htseq-count regarding the handling of warnings and
    added SAM_Reader.peek.


Version 0.4.5
=============

2010-08-30

- correction to GenomicArray.get_steps() when called without arguments
- correction to FileOrSequence.get_line_number_string
- removed use of urllib's quote and unquote in GFF parsing/writing
- GFF_Reader now stores "meta information"
- qa.py now gives progress report
- auto add chrom now also works on read access
- refactored CIGAR parser
- added bool fields to SAM_Alignment for all flag bits

Patch versions:

* Version 0.4.5p1 (2010-10-08)

  - correction of a mistake in CIGAR checking, misreading symbol "N"

* Version 0.4.5p2 (2010-10-13)

  - Sequence.add_bases_to_count_array and hence htseq-qa now 
    accepts '.' instead of 'N' in a fastq file

* Version 0.4.5p3 (2010-10-20)

  - fixed error reporting for PE in htseq-count

* Version 0.4.5p4 (2010-10-21)

  - fixed another error reporting for PE in htseq-count

* Version 0.4.5p5 (2010-10-28)

  - Not only 'N' but also 'S' was read the wrong way. Fixed.
  
  - Cython had some odd way handling properties overloading attributes,
    which caused issues with 'Alignment.read'. Worked around.

* Version 0.4.5p6 (2010-11-02)

  - write_to_fastq should not break lines. Fixed.

* Version 0.4.5p7 (2010-11-16)

  - added fallback to distutils in case setuptools in unavailable
  
  - fixed documentation of '-a' option to htseq-count

Version 0.4.4
=============

2010-05-19

- StepVectors (and hence also GenomicArrays) now notice if, when setting the
  value of a step, this value is equal to an adjacent step and merge the steps.
  
- GenomicArray's constructor now allows the special value ``"auto"`` for its
  first arguments in order to start without chromosomes and automatically add
  them when first encountered.

Patch versions:

* Version 0.4.4p1 (2010-05-26):

  - minor change to make it run on Python 2.5 again
  - changed 'str' to 'bytes' at various places, now compiles with Cython 0.12
    (but no longer with Cython 0.11 and Python 2.5)

* Version 0.4.4p2 (2010-06-05):

  - change to SAM parser: if flag "query unmapped is set" but RNAME is not
    "*", a warning (rather than an error) is issued

* Version 0.4.4p3 (2010-06-25)

  - again removed an "except sth as e"

* Version 0.4.4p4 (2010-07-12)

  - dto.

* Version 0.4.4p5 (2010-07-13)

  - rebuilt with Cython 0.12.1 (previous one was accidently built with 
    Cython 0.11.1, causing it to fail with Python 2.5)

* Version 0.4.4p6 (2010-07-21)

  - fixed bug in error reporting in count.py
  - losened GFF attribute parsing
  - changed "mio" to "millions" in qa output
  - improved error reporting in GFF parser
  - made SAM parsing more tolerant


Version 0.4.3
=============

2010-05-01

New argument to constructer of GFF_Reader: ``end_include``

* Version 0.4.3-p1 (2010-05-04): version number was messed up; fixed

* Version 0.4.3-p2 (2010-05-15): fixed '-q' option in htseq-count

* Version 0.4.3-p3 (2010-05-15): parse_GFF_attribute_string can now deal with
  empty fields; score treated as float, not int

* Version 0.4.3-p3 (2010-05-15): 
  - parse_GFF_attribute_string can now deal with empty fields; 
  score treated as float, not int
  - fixed bug in SAM_Reader: can now deal with SAM files with 11 columns
  - SAM_Alignment._tags is now a list of strings

* Version 0.4.3-p4 (2010-05-16):
  bumped version number again just to make sure

Version 0.4.2
=============

2010-04-19

Bug fixes to htseq-count and pair_SAM_alignments. Bumped version number to avoid
confusion.

* Version 0.4.2-p1 (2010-04-20): there was still a bug left in htseq-count, fixed.

* Version 0.4.2-p2 (2010-04-26): bug fix: adapter trimming failed if the adapter
  was completely included in the sequence

* Version 0.4.2-p3

* Version 0.4.2-p4 (2010-04-29): bug fix: error in warning when htseq-count
  encountered an unknown chromosome 

* Version 0.4.2-p5 (2010-04-30): bug fixes: error in warning when PE positions
  are mismatched, and misleading error when calling get_steps with unstranded
  interval in a stranded array  


Version 0.4.1
=============

2010-04-19

Bug fixes:

* Fixed bug in ``htseq-count``: CIGAR strings with gaps were not correctly handled

* Fixed bug in Tour (last section, on counting): An wrong indent, and accidental
  change to the ``exons`` variable invalidated data.

* SolexaExportReader no longer complains about multiplexing (indexing) not being supported.

* Mention link to example data in Tour.

* Fix installation instructions. (``--user`` does not work for Python 2.5.)

Enhancements:

* Paired-end support for SAM_Alignment.

* "_as_pos" attributes for GenomicInterval


Version 0.4.0
=============

2010-04-07

First "official" release, i.e., uploaded to PyPI and announced at SeqAnswers

Version 0.3.7
=============

2010-03-12

First version that was uploaded to PyPI
