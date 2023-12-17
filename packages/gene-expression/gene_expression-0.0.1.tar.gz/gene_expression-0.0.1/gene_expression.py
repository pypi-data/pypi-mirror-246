import argparse
import concurrent.futures
import gzip
import logging
import os
import re
import statistics
import subprocess
import sys

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = lambda message: logging.info(message)


VERSION = "2023-12-16"
HELP = f"""
compute gene expression (from gtf and bam)
require samtools to be loaded

arguments:
  -g --genes        path to genome annotation file (genes)
                    file format specified by --g-format (may be gzipped)
                    required
  -r --reads        path to aligned reads (bam file)
                    required
  -o --output       output path (will be a tsv file)
                    will be gzipped if path ends with .gz
                    required
  -f --g-format     format of --genes file (gtf or gff3)
                    optional, gtf by default
  -s --read-sens    only quantify reads with proper alignment sens
                    relatively to the gene (forward or reverse)
                    optional, any by default
  -p --parallel     number of parallel trimming processes to spawn
                    optional, 1 by default
"""


GTF_GFF3_ATTRIBUTES = dict(
    gtf=dict(
        attributes_regex=re.compile(r"(\w+)\s+\"([^\"]*)\""),
        gene_id_field="gene_id",
        gene_name_field="gene_name",
        transcript_id_field="transcript_id",
        transcript_parent_field="gene_id",
        exon_id_field="exon_id",
        exon_parent_field="transcript_id"),
    gff3=dict(
        attributes_regex=re.compile(r"(\w+)=([^;]*)"),
        gene_id_field="gene_id",
        gene_name_field="Name",
        transcript_id_field="transcript_id",
        transcript_parent_field="Parent",
        exon_id_field="exon_id",
        exon_parent_field="Parent"))


def z_open(path, mode="r", z="auto", level=6, **open_kargs):
    mode = mode if "b" in mode or "t" in mode else f"{mode[:1]}t{mode[1:]}"
    if z if isinstance(z, bool) else infer_z(path, z):
        return gzip.open(path, mode, level, **open_kargs)
    return open(path, mode, **open_kargs)
    

def infer_z(path, mode="auto"):
    if mode == "extension":
        return path.lower().endswith(".gz")
    if mode == "magic":
        with open(path, "rb") as file:
            return file.read(2) == b"\x1f\x8b"
    if mode == "auto":
        return infer_z(path, "magic" if os.path.isfile(path) else "extension")
    raise ValueError(f"invalid infer mode: {mode} (auto, magic or extension)")


def iter_gtf_lines(path):
    with z_open(path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            yield line


def read_gtf(path, format="gtf"):
    """
    gene = [0:chr_id, 1:start, 2:end, 3:strand, 4:id, 5:name, 6:transcripts]
    transcript: [0:start, 1:end, 2:id, 3:exons]
    exon: [0:start, 1:end]
    """
    format_attributes = GTF_GFF3_ATTRIBUTES[format]
    attributes_regex, gene_id_field, gene_name_field, transcript_id_field, \
    transcript_parent_field, _, exon_parent_field = format_attributes
    genes = {}
    transcripts = {}
    exons = []
    other_types = set()
    for line in iter_gtf_lines(path):
        try:
            chr_id, _, type, rest = line.split("\t", 3)
            if type == "gene":
                start, end, _, strand, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = dict(
                    match.groups()
                    for match in attributes_regex.finditer(line))
                gene_id = attributes[gene_id_field]
                gene_name = attributes[gene_name_field] \
                    if gene_name_field in attributes \
                    else gene_id
                gene = [chr_id, start, end, strand, gene_id, gene_name, []]
                genes[gene_id] = gene
            elif type == "transcript":
                start, end, _, _, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = dict(
                    match.groups()
                    for match in attributes_regex.finditer(line))
                transcript_id = attributes[transcript_id_field]
                gene_id = attributes[transcript_parent_field]
                if gene_id[:5] == "gene:":
                    gene_id = gene_id[5:]
                transcript = [start, end, transcript_id, []]
                transcripts[transcript_id] = [gene_id, transcript, line]
            elif type == "exon":
                start, end, _, _, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = dict(
                    match.groups()
                    for match in attributes_regex.finditer(line))
                transcript_id = attributes[exon_parent_field]
                if transcript_id[:11] == "transcript:":
                    transcript_id = transcript_id[11:]
                exon = [start, end]
                exons.append([transcript_id, exon, line])
            else:
                other_types.add(type)
        except Exception as error:
            line = line.strip().split("\t")
            raise RuntimeError(f"error on line {line}") from error
    for transcript_id, exon, line in exons:
        try:
            transcripts[transcript_id][1][3].append(exon)
        except KeyError as error:
            line = line.strip().split("\t")
            raise RuntimeError(f"no transcript for exon {line}") from error
    for gene_id, transcript, line in transcripts.values():
        transcript[3].sort(key=lambda exon: exon[1])
        transcript[3].sort(key=lambda exon: exon[0])
        try:
            genes[gene_id][6].append(transcript)
        except KeyError as error:
            line = line.strip().split("\t")
            raise RuntimeError(f"no gene for transcript {line}") from error
    for gene in genes.values():
        gene[6].sort(key=lambda transcript: transcript[1])
        gene[6].sort(key=lambda transcript: transcript[0])
    genes = sorted(genes.values(), key=lambda gene: gene[2])
    genes.sort(key=lambda gene: gene[1])
    genes.sort(key=lambda gene: gene[0])
    info = \
        f"{len(genes):,} genes, " + \
        f"{len(transcripts):,} transcripts, " + \
        f"{len(exons):,} exons " + \
        f" (other types: {', '.join(sorted(other_types))})"
    return genes, info


def write_genes(path, genes):
    header = "chr_id start end strand gene_id gene_name transcripts"
    with z_open(path, "w") as file:
        file.write(header.replace(" ", "\t") + "\n")
        for gene in genes:
            transcripts_string = "|".join(
                f"{transcript[2]}:" + "+".join(
                    f"{exon[0]}-{exon[1]}"
                    for exon in transcript[3])
                for transcript in gene[6])
            file.write(f"{gene[0]}\t{gene[1]}\t{gene[2]}\t{gene[3]}\t")
            file.write(f"{gene[4]}\t{gene[5]}\t{transcripts_string}\n")


def merge_intervals(intervals, already_sorted=False):
    if not already_sorted:
        intervals = sorted(intervals, key=lambda interval: interval[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append([*interval])
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged


def merge_transcripts(genes):
    for gene in genes:
        exons = (
            exon
            for transcript in gene[6]
            for exon in transcript[3])
        exons = merge_intervals(exons)
        transcript_id = f"<{gene[4]}.MERGED>"
        transcript = [exons[0][0], exons[-1][1], transcript_id, exons]
        yield [*gene[:6], transcript]


def get_exons(genes):
    exons_by_chr = {}
    for gene_index, gene in enumerate(genes):
        try:
            chr_exons = exons_by_chr[gene[0]]
        except KeyError:
            chr_exons = []
            exons_by_chr[gene[0]] = chr_exons
        for start, end in gene[6][3]:
            exon = [start, end, gene[3], gene_index]
            chr_exons.append(exon)
    for chr_exons in exons_by_chr.values():
        chr_exons.sort(key=lambda exon: exon[2])
        chr_exons.sort(key=lambda exon: exon[1])
    return dict(sorted(exons_by_chr.items(), key=lambda entry: entry[0]))


def parse_cigar_string(string):
    data = []
    index = len(string) - 1
    while index >= 0:
        symbol = string[index]
        count = 0
        base = 1
        index -= 1
        while index >= 0 and string[index] in "0123456789":
            count += int(string[index]) * base
            base *= 10
            index -= 1
        data.append([symbol, count or 1])
    return reversed(data)


def get_query_length_from_cigar(cigar):
    length = 0
    for symbol, count in cigar:
        if symbol in "MIS=X":
            length += count
    return length


def iter_bam_reads(path, chr_id):
    command = ["samtools", "view", path, chr_id]
    settings = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with subprocess.Popen(command, **settings) as process:
        for line in process.stdout:
            _, flag, _, start, _, cigar, _ = line.split("\t", 6)
            flag = int.from_bytes(flag.encode(), "little")
            if flag & 0x4 or flag & 0x100 or flag & 0x800:
                continue # unaligned, secondary or supplementary alignment
            start = int(start) - 1
            cigar = parse_cigar_string(cigar)
            end = start + get_query_length_from_cigar(cigar)
            strand = "-" if flag & 0x10 else "+"
            yield start, end, strand
        if process.wait():
            raise RuntimeError(process.stderr.read().strip())


def parallelize(tasks, parallel=1):
    parallel = int(min(parallel or os.cpu_count(), len(tasks)))
    if parallel < 2:
        for task in tasks:
            target, args = task[0], task[1:]
            yield target(*args)
    else:
        with concurrent.futures.ProcessPoolExecutor(parallel) as executor:
            futures = [executor.submit(*task) for task in tasks]
        yield from concurrent.futures.as_completed(futures)


def match_reads_per_chr(reads, exons, min_overlap=1, read_sens="any"):
    initial_exon_index = 0
    for read_start, read_end, read_strand in reads:
        read_size = read_end - read_start
        for exon_index in range(initial_exon_index, len(exons)):
            exon_start, exon_end, gene_strand, gene_index = exons[exon_index]
            if exon_end - min_overlap < read_start:
                if exon_index == initial_exon_index + 1:
                    initial_exon_index = exon_index + 1
                continue
            if read_end - min_overlap < exon_start:
                break
            if (read_sens == "forward" and read_strand != gene_strand) \
            or (read_sens == "reverse" and read_strand == gene_strand):
                continue
            exons_size = exon_end - exon_start
            overlap = min(
                read_end - exon_start,
                exon_end - read_start,
                read_size, exons_size)
            if overlap < min_overlap:
                continue
            yield gene_index


def get_read_counts_wrapper(reads_path, chr_id, exons, read_sens):
    reads = iter_bam_reads(reads_path, chr_id)
    min_gene_index = min(exon[4] for exon in exons)
    max_gene_index = max(exon[4] for exon in exons)
    result = [0] * (max_gene_index - min_gene_index + 1)
    for gene_index in match_reads_per_chr(reads, exons, read_sens=read_sens):
        result[gene_index - min_gene_index] += 1
    return min_gene_index, result


def get_read_counts(genes, reads_path, read_sens="any", parallel=1):
    exons = get_exons(genes, by_chr=True)
    submissions = [
        [get_read_counts_wrapper, reads_path, chr_id, chr_exons, read_sens]
        for chr_id, chr_exons in exons.items()]
    read_counts = [0] * len(genes)
    for chr_min_gene_index, counts in parallelize(submissions, parallel):
        for chr_gene_index, count in enumerate(counts):
            read_counts[chr_gene_index + chr_min_gene_index] = count
    return read_counts


def infer_gene_size(genes):
    for gene in genes:
        transcripts_sizes = [
            sum(end - start for start, end in transcript.exons)
            for transcript in gene.transcripts]
        yield int(round(sum(transcripts_sizes) / len(transcripts_sizes)))


def compute_tpms(pseudo_sizes, read_counts):
    read_counts_ratios = [
        count * 1000 / pseudo_size
        for pseudo_size, count in zip(pseudo_sizes, read_counts)]
    total = sum(read_counts_ratios)
    tpms = [
        read_count_ratio * 1e6 / total
        for read_count_ratio in read_counts_ratios]
    median = statistics.median([tpm for tpm in tpms if tpm > 1])
    for tpm in tpms:
        rtpm = tpm / median
        yield tpm, rtpm


def write_genes_with_expression(path, genes, pseudo_sizes, read_counts, tmps_rtpms):
    header = "chr_id start end strand gene_id gene_name"
    header += " pseudo_size read_count tpm rtpm"
    entries = zip(genes, pseudo_sizes, read_counts, tmps_rtpms)
    with z_open(path, "w") as file:
        file.write(header.replace(" ", "\t") + "\n")
        for gene, pseudo_size, read_count, (tpm, rtpm) in entries:
            file.write(f"{gene[0]}\t{gene[1]}\t{gene[2]}\t{gene[3]}\t")
            file.write(f"{gene[4]}\t{gene[5]}\t")
            file.write(f"{pseudo_size}\t{read_count}\t{tpm:.5g}\t{rtpm:.5g}\n")


def genes_expression(genes_path, reads_path, output_path, genes_format="gtf", read_sens="any", parallel=1):
    log(f"--- gene expression (v. {VERSION}) ---")
    log(f"genes: {genes_path}")
    log(f"reads: {reads_path}")
    log(f"read sens: {read_sens}")
    genes, genes_file_info = read_gtf(genes_path, genes_format)
    log(genes_file_info)
    genes = list(genes)
    pseudo_sizes = list(infer_gene_size(genes))
    merged_genes = list(merge_transcripts(genes))
    read_counts = get_read_counts(merged_genes, reads_path, read_sens, parallel)
    tmps_rtpms = compute_tpms(pseudo_sizes, read_counts)
    write_genes_with_expression(output_path, genes, pseudo_sizes, read_counts, tmps_rtpms)
    log("--- gene expression done ---")


def main(raw_args):

    if "-h" in raw_args or "--help" in raw_args:
        sys.stderr.write(f"{HELP.strip()}\n")
        return
    if "-v" in raw_args or "--version" in raw_args:
        sys.stderr.write(f"{VERSION}\n")
        return
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--genes", required=True)
    parser.add_argument("-r", "--reads", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-f", "--genes-format", default="gtf", choices=["gtf", "gff3"])
    parser.add_argument("-s", "--read-sens", default="any", choices=["any", "forward", "reverse"])
    parser.add_argument("-p", "--parallel", default=1, type=int)
    args = vars(parser.parse_args(raw_args)).values()

    return genes_expression(*args)


if __name__ == "__main__":
    main(sys.argv[1:])
