"""
This script adjust the metadata of a pdf file using the following steps:
- fetch the contents of the first few pages of the pdf file
- use an LLM to parse the contents and extract the following metadata:
    - title
    - author
    - subject
    - keywords
- use the extracted metadata to update the metadata of the pdf file
- save the updated pdf file with a new name
"""

import click
import logging
from textwrap import dedent
from io import StringIO
from pathlib import Path
from dataclasses import dataclass, field
import pikepdf
from openai import OpenAI
from pydantic import BaseModel
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s")

client = OpenAI(
    api_key=settings.keys.openai,
)


@click.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="The pdf file to adjust the metadata of",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="If set, the script will not modify the pdf file, but will print the metadata that would be used to modify the pdf file",
)
@click.option(
    "--no-llm",
    is_flag=True,
    default=False,
    help="If set, the script won't use the LLM to parse the pdf file, but just print the current metadata of the pdf file",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="If set, the script will print more information",
)
@click.option(
    "--num-pages",
    type=int,
    default=3,
    help="The number of pages to extract from the pdf file",
)
def main(path: str, dry_run: bool, no_llm: bool, verbose: bool, num_pages: int):
    """
    Adjust the metadata of a pdf file using the following steps:
    - fetch the contents of the first few pages of the pdf file
    - use an LLM to parse the contents and extract the following metadata:
    """

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.debug(f"Adjusting metadata of {path}")
    logger.debug(f"Dry run: {dry_run}")
    logger.debug(f"No LLM: {no_llm}")
    logger.debug(f"Verbose: {verbose}")

    path = Path(path)

    if not path.exists():
        logger.error(f"The path {path} does not exist")
        return

    run_workflow(path, dry_run, no_llm, num_pages)

    logger.info("Done")


def run_workflow(path: Path, dry_run: bool, no_llm: bool, num_pages: int):
    if path.is_dir():
        run_workflow_for_directory(path, dry_run, no_llm, num_pages)
    else:
        run_workflow_for_file(path, dry_run, no_llm, num_pages)


def run_workflow_for_directory(
    dir_path: Path, dry_run: bool, no_llm: bool, num_pages: int
):
    for path in dir_path.iterdir():
        if path.is_file() and path.suffix.lower() == ".pdf":
            run_workflow(path, dry_run, no_llm, num_pages)
        elif path.is_file() and path.suffix.lower() != ".pdf":
            logger.info(f"Skipping {path} because it is not a pdf file")
        elif path.is_dir():
            logger.info(f"Going into a new dir: {path}")
            run_workflow(path, dry_run, no_llm, num_pages)
        else:
            logger.info(f"Skipping {path}.")


def run_workflow_for_file(file_path: Path, dry_run: bool, no_llm: bool, num_pages: int):
    logger.info(f"Running workflow for {file_path}")
    pdf_contents = extract_pdf_contents(file_path, num_pages)
    if dry_run:
        logger.info("Dry run. Will not modify the pdf file")
        if no_llm:
            logger.info("Will not using LLM to parse the pdf file")
            logger.debug(f"PDF contents: {format_metadata(pdf_contents.metadata)}")
        else:
            logger.info("Using LLM to parse the pdf file")
            logger.debug(f"PDF contents: {format_metadata(pdf_contents.metadata)}")
            logger.debug(f"PDF contents: {pdf_contents.pages}")
            new_metadata = parse_pdf_metadata(pdf_contents)
            logger.debug(f"New metadata: {format_metadata(new_metadata)}")
            comparison = format_comparison(pdf_contents.metadata, new_metadata)
            logger.info(f"Compare metadata: {comparison}")
    else:
        if no_llm:
            logger.info("Will not using LLM to parse the pdf file")
            new_metadata = parse_pdf_metadata(pdf_contents)
            logger.debug(f"New metadata: {format_metadata(new_metadata)}")
        else:
            logger.info("Using LLM to parse the pdf file")
            logger.debug(f"PDF contents: {format_metadata(pdf_contents.metadata)}")
            logger.debug(f"PDF contents: {pdf_contents.pages}")
            new_metadata = parse_pdf_metadata(pdf_contents)
            logger.debug(f"New metadata: {format_metadata(new_metadata)}")
            comparison = format_comparison(pdf_contents.metadata, new_metadata)
            logger.info(f"Compare metadata: {comparison}")
            set_metadata(file_path, new_metadata)
            logger.info(f"Metadata set for {file_path}")


@dataclass
class RawMetadata:
    metadata: pikepdf.Dictionary
    docinfo: pikepdf.Dictionary

    def get_metadata_value(self, xmp_key: str, docinfo_key: str) -> str | None:
        value = self.metadata.get(xmp_key) or self.docinfo.get(docinfo_key)
        if value is not None:
            return str(value).strip()
        return None

    def get_metadata_values(self, xmp_key: str, docinfo_key: str) -> list[str]:
        value = self.get_metadata_value(xmp_key, docinfo_key)
        if value is not None:
            return [item.strip() for item in str(value).split(",")]
        return []


@dataclass
class PdfContents:
    file_name: str
    pages: str
    metadata: "PdfMetadata"


@dataclass
class PdfMetadata:
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    subject: str | None = None
    keywords: list[str] = field(default_factory=list)


class Justifications(BaseModel):
    title: str
    authors: str
    subject: str
    keywords: str


class LLMResponse(BaseModel):
    title: str
    authors: list[str]
    subject: str
    keywords: list[str]
    justifications: Justifications


def extract_pdf_contents(file_path: Path, num_pages: int) -> PdfContents:
    """
    Extract the contents of the first few pages of the pdf file.
    Metadata is extracted either from the XMP metadata or from the docinfo dictionary.
    """
    return PdfContents(
        file_name=file_path.name,
        pages=extract_text(file_path, num_pages),
        metadata=extract_pdf_metadata(file_path),
    )


def extract_text(file_path: Path, num_pages: int) -> str:
    output_string = StringIO()
    with open(file_path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page_number, page in enumerate(PDFPage.create_pages(doc)):
            if page_number >= num_pages:
                break
            interpreter.process_page(page)

    return output_string.getvalue().strip()


def extract_pdf_metadata(file_path: Path) -> PdfMetadata:
    with pikepdf.open(file_path) as pdf:
        raw_metadata = RawMetadata(pdf.open_metadata(), pdf.docinfo)
        return PdfMetadata(
            title=raw_metadata.get_metadata_value("dc:title", "/Title"),
            authors=raw_metadata.get_metadata_values("dc:creator", "/Author"),
            subject=raw_metadata.get_metadata_value("dc:subject", "/Subject"),
            keywords=raw_metadata.get_metadata_values("dc:keywords", "/Keywords"),
        )


def parse_pdf_metadata(pdf_contents: PdfContents) -> PdfMetadata:
    """
    Use OpenAI to extract missing or incorrect metadata from the pdf contents.
    """
    system_message = """
        You are a helpful assistant that extracts and corrects metadata from PDF files of books. You are provided with three key pieces of information: the filename, the contents of the first few pages of the PDF, and the existing metadata. Your task is to infer, correct, or add metadata by analyzing the provided content. You must always provide values for mandatory metadata fields, even if they need to be inferred with limited data. For optional fields, include them when sufficient context allows.

        Mandatory metadata fields:
        - title: the name of the book, derived from clear indications in the file content or inferred if necessary.
        - authors: a comma-separated list of authors' names.
        - subject: a general knowledge area that categorizes the book (e.g., Mathematics, Computer Science, Sociology).

        Optional metadata field:
        - keywords: specific topics covered in the book, inferred from context (e.g., Category Theory, Semiconductor Physics).

        You must justify each metadata field you assign in a dedicated 'justifications' section. Be logical, thorough, and strive to use contextual evidence. If information is ambiguous or missing, rely on reasonable inference from your general knowledge and the visible text content.

        Always respond in JSON format, containing the fields: `title`, `authors`, `subject`, `keywords`, and `justifications`. Do not include additional commentary or unrelated content. Clarify only if essential details are missing to fulfill the metadata extraction task effectively.
        """

    user_message = f"""
    Please extract the following metadata from the pdf file:
        - title: mandatory
        - authors: mandatory
        - subject: mandatory
        - keywords: nice to have
    Justify your choices!
    ---
    The file name is: {pdf_contents.file_name}
    ---
    The pdf file is:
    {pdf_contents.pages}
    ---
    The current metadata of the pdf file is:
    Title: {pdf_contents.metadata.title}
    Author: {pdf_contents.metadata.authors}
    Subject: {pdf_contents.metadata.subject}
    Keywords: {pdf_contents.metadata.keywords}
    """
    logger.debug(f"System message: {system_message}")
    logger.debug(f"User message: {user_message}")
    try:
        # Use OpenAI to get structured output
        response = client.responses.parse(
            model="gpt-4.1-nano",
            input=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            text_format=LLMResponse,
        )

        # Parse the JSON response
        output = response.output_parsed
        logger.info(f"Justification for title: {output.justifications.title}")
        logger.info(f"Justification for authors: {output.justifications.authors}")
        logger.info(f"Justification for subject: {output.justifications.subject}")
        logger.info(f"Justification for keywords: {output.justifications.keywords}")
        return PdfMetadata(
            title=output.title,
            authors=output.authors,
            subject=output.subject,
            keywords=output.keywords,
        )
    except Exception as e:
        logger.error(f"Error using OpenAI: {str(e)}")
        return pdf_contents.metadata  # Return original metadata if there's an error


def set_metadata(file_path: Path, new_metadata: PdfMetadata):
    """
    Set the metadata of the pdf file
    """
    with pikepdf.open(file_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata() as meta:
            meta["dc:title"] = new_metadata.title
            meta["dc:creator"] = ", ".join(new_metadata.authors)
            meta["dc:subject"] = new_metadata.subject
            meta["dc:keywords"] = ", ".join(new_metadata.keywords)
        pdf.docinfo["/Title"] = new_metadata.title
        pdf.docinfo["/Author"] = ", ".join(new_metadata.authors)
        pdf.docinfo["/Subject"] = new_metadata.subject
        pdf.docinfo["/Keywords"] = ", ".join(new_metadata.keywords)
        pdf.save()


def format_metadata(metadata: PdfMetadata) -> str:
    """
    Format the metadata of the pdf file
    """
    output = ""
    try:
        if metadata.title:
            output += f"Title: {metadata.title}\n"
        if metadata.authors:
            output += f"Author: {', '.join(metadata.authors)}\n"
        if metadata.subject:
            output += f"Subject: {metadata.subject}\n"
        if metadata.keywords:
            output += f"Keywords: {', '.join(metadata.keywords)}\n"
    except Exception as e:
        print(metadata)
        logger.error(f"Error formatting metadata: {str(e)}")
        raise e

    return output


def format_comparison(meta: PdfMetadata, new_meta: PdfMetadata) -> str:
    return dedent(f"""
    title: {meta.title} -> {new_meta.title}
    authors: {meta.authors} -> {new_meta.authors}
    subject: {meta.subject} -> {new_meta.subject}
    keywords: {meta.keywords} -> {new_meta.keywords}
    """)


if __name__ == "__main__":
    main()
