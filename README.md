# Individual-project-in-Bioinformatics
## Abstact 
Code used in Bioinformatics Project written under supervision of Lars Hestbjerg Hansen. The aim was to anwser two questions: 
- What the bacteria causing the blackleg and soft rot in the Danish potato crops are resistant to and what mobile genetic
elements they already had the contact with?
- What are the evolutionary relations between the bacteria collected form the different fields in different parts of Denmark?
  As a starting point I got 59 bacterial & 48 bacteriophage genomes sequenced using combination of Ilumina & ONT and later assembled.
  Most of the files were written specifically for my use and use hardcoded paths to the files I used.
  ## Files description
  _for deep understanding of the code I advise to have a look in a project report sheeet_
  1. compare_spacer_sets.py
     - compares two spacer sets and returns the information about which spacers are shared and which are not (only checks for 100% identity)
  2. extract_spacers.py
     - auxiliary script. It extracts raw spacer sequences from CRISPRDetect files and saves them in a format compatible with the rest of the scripts.
  3. final.py
     - It reads in each BLAST hit for each bacteria separately and compares it with a map to find whether the spacer target can be identified (i.e. matches a genome part assigned as prophage/plasmid). Only positive results (i.e. spacers with known target) are saved to Excel file.
  4. find_plasmid.py
     - Script that aims to find the plasmids in assembled genome files using several assumptions. All contigs with depth <= 0.5x and >=5x are assigned as plasmids. Results were saved into pandas DataFrame. 
  5. find_same_spacers.py
     - Checks every spacer of a given CRISPR system and returns an information whether it is shared by any
of the bacteria and if yes, then at what position. Good at catching slight similarities between distantly related bacteria.
  6. get_GSAlign_out.py
     - Using GSAlign output counts mutations between two assembled genomes and writes it, together with bacteria ID to a _meg_file.txt_ .   
  7. make_distance_matrix.py
     - Makes distance matrix from _meg_file.txt_
  8. proper_prophage_map.py
      - Alyzes whether BLAST a hit is significant or not. It finds all the hits targeting the bacteria and decides on their importance based on the two conditions. If % identity is greater than 99 and alignment length covers at least 95% of the prophage sequence, then start & stop positions, together with the phage ID are added to the pandas DataFrame (separate for each bacteria).
  9. remove_own_hits.py
      - removes self hits from CRISPRDetect & CRISPRCasTyper outputs. 
  10. run_gsalign.sh
      - Bash script used to run GSAlign between all possible sequence pairs between bacteria group.
 
 

 
  
  
