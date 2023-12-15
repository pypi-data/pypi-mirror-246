# system modules
import argparse
import os
import sys
import glob
import re
import itertools
from pathlib import Path
import shutil
import tempfile
import logging
from pathlib import Path
from zipfile import ZipFile

# external modules
import rich
from rich.syntax import Syntax
from rich.panel import Panel
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def formatstr(x):
    try:
        x.format(1)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"{x!r} can not be format()ed with a single argument: {e!r}"
        )
    return x.format


def present_latex(code, title=None):
    if hasattr(code, "decode"):
        code = code.decode(errors="ignore")
    output = Syntax(code, lexer="latex")
    if title:
        output = Panel(output, title=title)
    console.log(output)


parser = argparse.ArgumentParser(
    description="Turn your latex LaTeX project into a flat structure or ZIP file"
)
parser.add_argument(
    "texfiles",
    nargs="*",
    default=(_ := glob.glob("*.tex")),
    help="TeX files to process. " f"Defaults to {', '.join(map(repr,_))}.",
)

behaviourgroup = parser.add_argument_group(
    title="Processing", description="Options changing the processing behaviour"
)
behaviourgroup.add_argument(
    "--plos",
    help="activate PLoS settings (shorthand for --replace-bib --sequential-figures --hide-figures)",
    action="store_true",
)
behaviourgroup.add_argument(
    "--replace-bib",
    help=r"replace \bibliography with .bbl contents (needed for PLoS)",
    action="store_true",
)
behaviourgroup.add_argument(
    "--sequential-figures",
    metavar="FORMATSTR",
    const=(
        default_sequential_figures := (
            default_sequential_figures_format := "fig{}"
        ).format
    ),
    type=formatstr,
    help=f"[RUDIMENTARY] Rename figure files sequentially (default e.g. {default_sequential_figures(3)+'.ext'!r}). "
    "Can be set to a Python format string where {} is replaced with the figure number. "
    f"Default format is {default_sequential_figures_format!r}. "
    f"Note that the resulting figure numbers might not correspond to the actual figure labels.",
    nargs="?",
)
behaviourgroup.add_argument(
    "--hide-figures",
    help="[RUDIMENTARY] Hide graphics (by not \includegraphics{}ing them). "
    f"The source files are still included. "
    f"Note that also graphics that are not actually figures might be hidden. ",
    action="store_true",
)


outputgroup = parser.add_argument_group(
    title="Output", description="Options changing the output behaviour"
)
outputgroup.add_argument(
    "--inplace",
    help=r"modify TeX files in-place and place source files around it.",
    action="store_true",
)
outputgroup.add_argument(
    "-d",
    "--outdir",
    help=r"output directory for files (if --inplace is not given). "
    "By default, a temporary directory is used that is later removed.",
)
outputgroup.add_argument(
    "-z",
    "--zip",
    help=r"Make a ZIP file next to the .tex file with the adjusted .tex file "
    "and its dependencies in a flat structure as in --outdir. ",
    action="store_true",
)
outputgroup.add_argument(
    "--keep-other-files",
    help="Also include .aux etc. files",
    action="store_true",
)
outputgroup.add_argument(
    "--copy",
    help="Copy files instead of symlinking.",
    action="store_true",
)
outputgroup.add_argument(
    "--force",
    help="Just do it. Potentially overwrites files and loses data.",
    action="store_true",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)


def cli():
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO - (args.verbose - args.quiet) * 5,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    if args.plos:
        args.replace_bib = True
        args.sequential_figures = default_sequential_figures
        args.hide_figures = True

    if args.sequential_figures:
        logger.warning(
            f"--sequential-figures is implemented rudimentally and might not reflect the actual figure number correctly."
        )

    if args.hide_figures:
        logger.warning(
            f"--hide-figures is implemented rudimentally and might also hide graphics that are not actually figures."
        )

    # make the most out of given command-line arguments
    expanded_texfiles = []
    for texfile in args.texfiles:
        path = Path(texfile)
        if path.is_dir():
            if texfiles_here := list(map(str, path.glob("*.tex"))):
                expanded_texfiles.extend(texfiles_here)
                logger.info(
                    f"Found {len(texfiles_here)} .tex files {texfiles_here} in given directory {texfile!r}, using those instead."
                )
            else:
                logger.warning(
                    f"No .tex files in given directory {texfile!r}. Skipping."
                )
        elif path.is_file():
            expanded_texfiles.append(texfile)
        else:
            logger.warning(
                f"Given path {texfile!r} is neither an existing file nor a directory containing .tex files. Skipping."
            )
    args.texfiles = expanded_texfiles
    if not args.texfiles:
        logger.info(f"😴 No TeX files. Nothing to do.")
        sys.exit(0)

    if not (args.inplace or args.outdir or args.zip):
        logger.warning(
            f"If neither --inplace, --outdir or --zip is given, you won't see much of an effect. Continuing anyway."
        )

    if len(args.texfiles) > 1 and args.outdir:
        logger.critical(
            f"Giving an --outdir while specifying {len(args.texfiles)} .tex files {tuple(args.texfiles)} is not sensible. "
            "Use --force to do it anyway."
        )
        sys.exit(2)

    logger.debug(f"{args = }")

    logger.info(
        f"{len(args.texfiles)} TeX files to process. {', '.join(map(repr,args.texfiles))}"
    )

    def readInputFiles(texfile):
        texfile = Path(texfile)
        pattern = re.compile(r"^INPUT\s+(?P<file>.*)$")
        if (flsfile := texfile.parent / Path(f"{texfile.stem}.fls")).exists():
            logger.debug(f"{str(texfile)!r}: Found {str(flsfile)!r} for dependencies")
            with flsfile.open() as fh:
                for line in fh:
                    if m := pattern.search(line):
                        yield m.groupdict()["file"]
        pattern = re.compile(
            r"""^\s+"(?P<file>.*?)"\s+(\d+)\s+(\d+)\s+([a-f0-9]+)\s+"([^"]*)"\s+$"""
        )
        if (fdbfile := texfile.parent / Path(f"{texfile.stem}.fdb_latexmk")).exists():
            logger.debug(f"{str(texfile)!r}: Found {str(fdbfile)!r} for dependencies")
            with fdbfile.open() as fh:
                for line in fh:
                    if m := pattern.search(line):
                        yield m.groupdict()["file"]

    #
    # Loop over all given/found tex files
    #
    for texfile in map(Path, args.texfiles):
        #
        # Get the --outdir in order
        #
        outdir_remove_after = False
        if args.inplace:
            if args.outdir:
                logger.warning(f"Ignore --outdir {args.outdir!r} as --inplace is given")
            outdir = Path(texfile).parent
        elif args.outdir:
            outdir = Path(args.outdir)
            if outdir.exists():
                if args.force:
                    shutil.rmtree(str(outdir))
                    logger.warning(f"🗑️ Removed existing --outdir {str(outdir)!r}")
                else:
                    logger.critical(
                        f"--outdir {str(outdir)!r} exists. Remove it or add --force."
                    )
                    sys.exit(1)
            if not outdir.exists():
                logger.info(f"Creating --outdir {args.outdir!r}")
                try:
                    outdir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.critical(f"Couldn't create --outdir {args.outdir!r}: {e!r}")
                    sys.exit(1)
        else:
            outdir = Path(tempfile.mkdtemp(prefix=f"latex-flatten-"))
            outdir_remove_after = True

        def put_next_to_texfile(path, name=None):
            path = Path(path)
            if name is None:
                name = path.name
            is_texfile = path.resolve() == texfile.resolve()
            if not path.is_absolute() and not is_texfile:
                path = texfile.parent / path
            try:
                target = outdir / name
                if args.copy or is_texfile:
                    shutil.copy(str(from_ := path), str(target))
                    logger.info(f"🖇️ Copied {str(from_)!r} to {str(target)!r}")
                else:
                    # TODO: relative absolute target path might be more elegant
                    os.symlink(str(from_ := path.resolve()), str(target))
                    logger.info(f"🔗 Symlinked {str(from_)!r} to {str(target)!r}")
            except shutil.SameFileError as e:
                return None
            except Exception as e:
                logger.error(
                    f"💥 Couldn't {'copy' if args.copy else 'link'} {str(path)!r} next to {texfile.name!r}: {e!r}"
                )
                return False
            return True

        # all found, unique input files, including global LaTeX ones
        inputFiles = set()
        inputFilesResolved = set()
        for inputfile in map(Path, readInputFiles(texfile)):
            if (resolved := inputfile.resolve()) not in inputFilesResolved:
                inputFiles.add(inputfile)
            inputFilesResolved.add(resolved)
        logger.debug(f"{str(texfile)!r} has {len(inputFiles)} dependent files in total")
        if logger.getEffectiveLevel() < logging.DEBUG - 10:
            logger.debug(inputFiles)

        if not inputFiles:
            logger.warning(
                f"No input files detected (from *.fls or *.fdb_latexmk files next to {str(texfile)!r})! "
                f"Apparently, you didn't run 'latexmk' or 'pdflatex -recorder' on {str(texfile)!r}? "
                f"Continuing anyway, but the result might be unexpected."
            )

        # files to include in outdir or ZIP file
        # mapping of original input file to target name
        inputFilesToInclude = {f: f.name for f in inputFiles}

        # drop all absolute paths (those are the global TeX dependencies)
        inputFilesToInclude = {
            f: n for f, n in inputFilesToInclude.items() if not f.is_absolute()
        }
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(
                f"{str(texfile)!r}: dependencies inclusion list after dropping absolute paths:\n{inputFilesToInclude}"
            )

        def dont_include_file(path=None, glob=None):
            toremove = set()
            if path is not None:
                path = Path(path)
                if not path.is_absolute():
                    path = texfile.parent / path
            for inputfile in inputFilesToInclude:
                inputfile_ = inputfile
                if not inputfile_.is_absolute():
                    inputfile_ = texfile.parent / inputfile_
                if path is not None:
                    if inputfile_.resolve() == path.resolve():
                        toremove.add(inputfile)
                try:
                    if Path(inputfile).match(glob):
                        toremove.add(inputfile)
                except Exception:
                    pass
            if path and not toremove:
                logger.debug(
                    f"Instruction to not include {str(path)!r} explicitly didn't change anything."
                )
            for f in toremove:
                logger.debug(
                    f"Remove {str(f)!r} from dependency inclusion list for {str(texfile)!r}"
                )
                del inputFilesToInclude[f]

        if not args.keep_other_files:
            for pattern in (
                "*.aux *.log *.toc *.fdb_latexmk *.fls *.bbl *.blg *.fff "
                "*.lof *.lot *.ttt *.spl *.out *.bcf *.tdo *.run.xml"
            ).split():
                dont_include_file(glob=pattern)

        logger.debug(
            f"{str(texfile)!r} has {len(inputFilesToInclude)} dependent files to include"
        )
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(inputFilesToInclude)

        # Make sure the texfile is actually in outdir
        put_next_to_texfile(texfile)
        dont_include_file(Path(texfile.name))

        texfile_edit = outdir / texfile.name

        #
        # Replace \input{FILE} with contents of FILE
        #
        logger.info(
            rf"{str(texfile_edit)!r}: Searching occurences of \input{{FILE}} to replace with contents of FILE"
        )
        with texfile_edit.open("rb") as fh:
            texcode = fh.read()
        for n, (inputline, inputfile) in enumerate(
            re.findall(rb"^(\\input\{([^}]+)\})$", texcode, flags=re.MULTILINE)
        ):
            logger.info(rf"{str(texfile_edit)!r}: Found \input line #{n}")
            if logger.getEffectiveLevel() < logging.INFO:
                present_latex(inputline)
            inputfilepath = Path(inputfile.decode(errors="ignore"))
            inputfile = inputfilepath
            if not inputfile.is_absolute():
                inputfile = Path(texfile).parent / inputfile
            try:
                with open(str(inputfile), "rb") as fh:
                    inputfilecontent = fh.read()
                logger.debug(
                    f"Read {len(inputfilecontent)} bytes ({len(inputfilecontent.splitlines())} lines) from {str(inputfile)!r}"
                )
            except Exception as e:
                logger.error(f"💥 Couldn't read contents of {str(inputfile)!r}: {e!r}")
                continue
            logger.info(
                f"{str(texfile_edit)!r}: ✂️  Replacing {inputline!r} with contents of {str(inputfile)!r} ({len(inputfilecontent.splitlines())} lines)"
            )
            texcode_before = texcode
            texcode = texcode.replace(inputline, inputfilecontent)
            if texcode_before == texcode:
                logger.error(
                    f"{str(texfile_edit)!r}: Replacing {inputline} with contents of {str(inputfile)!r} didn't change anything!? 🤨"
                )
            with open(texfile_edit, "wb") as fh:
                fh.write(texcode)
                logger.info(f"💾 Saved {str(texfile_edit)!r}")
            dont_include_file(inputfilepath)

        #
        # Adjust all \includegraphics{} paths
        #
        logger.info(
            rf"{str(texfile_edit)!r}: Searching for \includegraphics{{...}} for adjusting include paths"
        )
        with texfile_edit.open("rb") as fh:
            texcode = fh.read()
        graphicscounter = itertools.count(start=1)
        for fullline, includegraphicsline, includegraphicspath in re.findall(
            rb"(^.*?(\\includegraphics\s*(?:\[[^\]]+\])?\s*\{\s*([^}]+)\s*\}).*?$)",
            texcode,
            flags=re.MULTILINE,
        ):
            if re.search(rb"^\s*%", fullline):  # skip comments
                logger.debug(
                    rf"{str(texfile_edit)!r}: Ignore commented \includegraphics line {fullline.decode()!r}"
                )
                # console.log(Syntax(fullline.decode(), lexer="latex"))
                continue
            graphicsnumber = next(graphicscounter)
            logger.info(
                rf"{str(texfile_edit)!r}: Found \includegraphics line #{graphicsnumber}"
            )
            if logger.getEffectiveLevel() < logging.INFO:
                present_latex(includegraphicsline)
            # console.log(Syntax(fullline.decode(), lexer="latex"))
            includegraphicspath = Path(includegraphicspath.decode(errors="ignore"))
            if not includegraphicspath.suffixes:
                logger.warning(
                    rf"\includegraphics path {str(includegraphicspath)!r} has no suffix. This might cause issues."
                )
            if args.sequential_figures:
                includegraphicspath_new = args.sequential_figures(graphicsnumber)
                # add old suffix
                includegraphicspath_new = "".join(
                    [includegraphicspath_new] + includegraphicspath.suffixes
                )
                inputFilesToInclude[includegraphicspath] = includegraphicspath_new
                logger.info(
                    rf"Will include \includegraphics file {str(includegraphicspath)!r} as {includegraphicspath_new!r}"
                )
            else:
                includegraphicspath_new = includegraphicspath.name
            includegraphicslinenew = includegraphicsline
            # update the included path
            includegraphicslinenew = includegraphicslinenew.replace(
                str(includegraphicspath).encode(errors="ignore"),
                includegraphicspath_new.encode(errors="ignore"),
            )  # TODO: encoding weirdness possible!!
            if args.hide_figures:
                # comment it out
                includegraphicslinenew = re.sub(
                    rb"(^|[\r\n])", rb"\1% ", includegraphicslinenew
                )
            logger.info(rf"✂️  Adjusted \includegraphics line #{graphicsnumber}")
            if logger.getEffectiveLevel() < logging.INFO:
                present_latex(includegraphicslinenew)
            texcode = texcode.replace(includegraphicsline, includegraphicslinenew)
            with open(texfile_edit, "wb") as fh:
                fh.write(texcode)

        if args.replace_bib:
            bblfile = texfile.parent / Path(f"{Path(texfile).stem}.bbl")
            logger.debug(
                rf"{str(texfile_edit)!r}: Replacing \bibliography{{}} with contents of the .bbl file (assumed to be {str(bblfile)!r})"
            )
            bbllinecounter = itertools.count(start=1)
            for fullline, bibliographyline, bibfile in re.findall(
                rb"(^.*?(\\bibliography\s*\{\s*([^}]+)\s*\}).*?$)",
                texcode,
                flags=re.MULTILINE,
            ):
                if re.search(rb"^\s*%", fullline):  # skip comments
                    logger.debug(
                        rf"{str(texfile_edit)!r}: Ignore commented \bibiliography line {fullline.decode()!r}"
                    )
                    # console.log(Syntax(fullline.decode(), lexer="latex"))
                    continue
                bbllinenumber = next(bbllinecounter)
                logger.info(
                    rf"{str(texfile_edit)!r}: Found \bibiliography line #{bbllinenumber}"
                )
                if logger.getEffectiveLevel() < logging.INFO:
                    present_latex(bibliographyline)

                try:
                    with bblfile.open("rb") as fh:
                        bblcontent = fh.read()
                        logger.info(
                            f"Read {len(bblcontent)} bytes from {str(bblfile)!r}"
                        )
                except Exception as e:
                    logger.error(
                        rf"Couldn't replace {bibliographyline!r} call with contents of {str(bblfile)!r}: {e!r}. "
                        rf"Maybe you need to recompile your document, e.g. with `latexmk {str(texfile_edit)!r}`?"
                    )
                    continue
                texcode = texcode.replace(fullline, bblcontent)
                with texfile_edit.open("wb") as fh:
                    fh.write(texcode)
                logger.info(
                    rf"Replaced \bibiliography line #{bbllinenumber} with contents of {str(bblfile)!r}"
                )
                if args.keep_other_files:
                    dont_include_file(bblfile.name)

        logger.info(
            rf"{str(texfile)!r}: Copying all local input dependencies next to {str(texfile_edit)!r}"
        )
        for inputfile, name in inputFilesToInclude.items():
            put_next_to_texfile(inputfile, name=name)

        if args.zip:
            try:
                with ZipFile(
                    str(zipfilepath := Path(f"{texfile.stem}.zip")), "w"
                ) as zipfile:
                    logger.info(f"🗃️  Writing ZIP file {str(zipfilepath)!r}")
                    logger.info(
                        f"🗃️  {str(zipfilepath)!r}: Adding {str(texfile_edit)!r}"
                    )
                    zipfile.write(str(texfile_edit), arcname=str(texfile_edit.name))
                    for inputfile, name in inputFilesToInclude.items():
                        inputfile = outdir / name
                        logger.info(
                            f"🗃️  {str(zipfilepath)!r}: Adding {str(inputfile)!r}"
                        )
                        zipfile.write(str(inputfile), arcname=name)
            except Exception as e:
                logger.error(
                    f"{str(texfile)!r}: Couldn't finish ZIP file {str(zipfilepath)!r}: {e!r}"
                )

        logger.info(f"✅ Done with {str(texfile)!r}")

        if outdir_remove_after:
            try:
                shutil.rmtree(str(outdir))
                logger.info(f"🗑️ Removed temporary --outdir {str(outdir)!r}")
            except Exception as e:
                logger.error(
                    f"Couldn't remove temporary --outdir {str(outdir)!r}: {e!r}"
                )
        else:
            try:
                _outdir = outdir.resolve()
                _outdir = outdir.relative_to(".")
                _outdir = outdir.relative_to(".", walk_up=True)
            except Exception:
                pass
            logger.info(
                f"Have a look into {str(_outdir)!r} and try to compile {texfile_edit.name!r} there (e.g. with `latexmk`)"
            )


if __name__ == "__main__":
    cli()
