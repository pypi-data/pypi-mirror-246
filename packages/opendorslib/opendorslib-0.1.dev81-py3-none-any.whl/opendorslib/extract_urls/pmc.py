# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

import json
import re

from jsonpath_ng import parse

from opendorslib.abc import WorkflowRule
from opendorslib.metadata import Repository, IdType, DataSource, Corpus, Mention
from opendorslib.urls import canonical_url


_SOURCE = DataSource.EXTRACT_URLS_PMC
_ID_TYPE = IdType.PMC


# ######################################################################################################################
# ############################ Class
# ######################################################################################################################


class ExtractURLPMCRetriever(WorkflowRule):
    def __init__(
        self,
        input_json: str,
        output_json: str,
        log_file: str,
        log_level: str,
        indent: int = 0,
    ):
        """
        A retriever for publication metadata from the PMC subset of the Extract URLs dataset.

        :param input_json: The input data JSON file
        :param output_json: The path string for the target OpenDORS JSON file
        :param log_file: The path string to the log file that logging output should be written to
        """
        super().__init__(__name__, log_file, log_level, indent)
        self.input_json = input_json
        self.output_json = output_json

    def _extract_pmc_id(self, pdf_file: str) -> str:
        """
        Extracts the PMC ID from a PDF file path in the Extract-URLs PMC data.

        :param pdf_file: The pdf file path string to extract the ID from
        :return: the PMC ID
        """
        # Assert that the PDF file name ends with the default string '<PMC ID>.pdf'.
        split_name = pdf_file.split(".")
        id_candidate = split_name[-2]
        try:
            assert re.match(r"^PMC\d+$", id_candidate)
        except AssertionError as ae:
            self.log.error(f"Could not find PMC id in '{pdf_file}'.")
            raise ae
        return id_candidate.replace("PMC", "")

    def run(self) -> None:
        """
        Extracts repository URLs from Extract-URLs parsed PMC data JSON files,
        checks whether URLs can be transformed into canonical repository URLs,
        and if so, adds them to a corpus of repositories of canonical URLs
        and their mentions in the PMC part of the dataset.
        The corpus is then written into a JSON file.
        """
        c = Corpus()
        with open(self.input_json, "r") as json_in:
            data = json.load(json_in)
            expr = "$.*.files.*.url_count"
            jsonpath_expression = parse(expr)

            for datum in jsonpath_expression.find(data):
                if int(datum.value) > 0:
                    all_urls = datum.context.value["all_urls"]
                    for url in all_urls:
                        if canon_url := canonical_url(url):
                            # Get PMC ID for the paper and map it.
                            # The match can only have exactly one context, and that is the parent field,
                            # i.e., the PDF name, which contains the PMC ID.
                            pdf_file = str(datum.context.path)
                            pmc_id = self._extract_pmc_id(pdf_file)
                            self.log.debug(
                                f"Mapping PMC ID {pmc_id} to URL {canon_url}."
                            )
                            m = Mention(
                                data_source=DataSource.EXTRACT_URLS_PMC,
                                id=pmc_id,
                                id_type=IdType.PMC,
                                orig_urls={url},
                            )
                            c.add_repository(Repository(url=canon_url, mentions=[m]))
                        else:
                            self.log.info(f"Could not get a canonical URL for {url}")

        with open(self.output_json, "w") as mj:
            self.log.info(f"Writing corpus for extract_urls-pmc to {self.output_json}.")
            mj.write(c.model_dump_json(indent=self.indent))
