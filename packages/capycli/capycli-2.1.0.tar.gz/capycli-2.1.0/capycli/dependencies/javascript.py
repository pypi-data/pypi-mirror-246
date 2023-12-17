# -------------------------------------------------------------------------------
# Copyright (c) 2019-23 Siemens
# All Rights Reserved.
# Author: thomas.graf@siemens.com, sameer.panda@siemens.com
#
# SPDX-License-Identifier: MIT
# -------------------------------------------------------------------------------

import json
import logging
import os
import sys

import requests
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashAlgorithm, HashType, Property
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from packageurl import PackageURL

import capycli.common.dependencies_base
import capycli.common.json_support
from capycli import get_logger
from capycli.common.capycli_bom_support import CaPyCliBom, CycloneDxSupport, SbomCreator, SbomWriter
from capycli.common.print import print_red, print_text, print_yellow
from capycli.main.result_codes import ResultCode

LOG = get_logger(__name__)


class GetJavascriptDependencies(capycli.common.dependencies_base.DependenciesBase):
    """
    Determine Javascript components/dependencies for a given project.
    """
    def get_dependency(self, data: dict, sbom: Bom) -> Bom:
        dependencies = data.get("dependencies", {})
        for key in dependencies:
            dep = dependencies[key]
            isdev = False
            if "dev" in dep:
                isdev = dep["dev"]

            if isdev:
                # LOG.debug("Ignoring dev dependency: " + key + "," + dep["version"])
                continue

            LOG.debug("Checking dependency: " + key + "," + dep["version"])
            purl = PackageURL("npm", "", key, dep["version"], "", "").to_string()
            cxcomp = Component(
                name=key.strip(),
                version=dep["version"].strip(),
                purl=purl,
                bom_ref=purl)

            url = dep.get("resolved", "")
            if url:
                ext_ref = ExternalReference(
                    reference_type=ExternalReferenceType.DISTRIBUTION,
                    comment=CaPyCliBom.BINARY_URL_COMMENT,
                    url=url)
                cxcomp.external_references.add(ext_ref)

            url = dep.get("resolved", "").split('/')[-1]
            if url:
                ext_ref = ExternalReference(
                    reference_type=ExternalReferenceType.DISTRIBUTION,
                    comment=CaPyCliBom.BINARY_FILE_COMMENT,
                    url=url)
                # the encoding of the hashes in package-lock.json is incompatible to
                # the encoding in CyloneDX.
                # hash = dep.get("integrity", "")
                # hash_alg = None
                # if hash.startswith("sha512"):
                #     hash_alg = HashAlgorithm.SHA_512
                # if hash.startswith("sha1"):
                #     hash_alg = HashAlgorithm.SHA_1
                # if hash and hash_alg:
                #     ext_ref.hashes.add(HashType(
                #         algorithm=hash_alg,
                #         hash_value=hash))
                cxcomp.external_references.add(ext_ref)

                prop = Property(
                    name=CycloneDxSupport.CDX_PROP_LANGUAGE,
                    value="Javascript")
                cxcomp.properties.add(prop)

            if cxcomp not in sbom.components:
                sbom.components.add(cxcomp)

            if "dependencies" in dep:
                # bomitem = self.get_dependency(dep, sbom)
                pass

        return sbom

    def convert_package_lock(self, package_lock_file: str):
        """Read package-lock.json and convert to bill of material"""
        bom = SbomCreator.create(None, addlicense=True, addprofile=True, addtools=True)
        with open(package_lock_file) as fin:
            data = json.load(fin)
            sbom = self.get_dependency(data, bom)

        return sbom

    def find_package_info(self, pckgName: str, pckgVrsn: str = "", package_source: str = "") -> dict or None:
        hdr = {}
        if not pckgName:
            return None

        if pckgVrsn:
            pckgVrsn = "/" + pckgVrsn
        else:
            pckgVrsn = ""

        if package_source:
            url = package_source + pckgName + pckgVrsn
        else:
            # use default
            url = "https://registry.npmjs.org/" + pckgName + pckgVrsn

        hdr["Accept"] = "application/json"

        try:
            response = requests.get(url, headers=hdr)
            if response.ok:
                res = response.json()

                return res
        except Exception as ex:
            print_yellow(
                "  Error retrieving component meta data: " +
                repr(ex))

        return None

    def try_find_component_metadata(self, bomitem: Component, package_source: str) -> Component:
        """
        Find metadata for a single component.
        """
        info = self.find_package_info(
            pckgName=bomitem.name,
            pckgVrsn=bomitem.version,
            package_source=package_source)
        if not info:
            print_yellow(
                "  No info found for component " +
                bomitem.name +
                ", " +
                bomitem.version)
            return bomitem

        val = info.get("homepage", "")
        if val:
            ext_ref = ExternalReference(
                reference_type=ExternalReferenceType.WEBSITE,
                url=val)
            bomitem.external_references.add(ext_ref)

        repository = info.get("repository")
        url = ""
        if repository is not None and type(repository) == dict:
            url = repository.get("url", "")
            url = url.replace('git+', '')
            url = url.replace('git://', '')
            url = url.replace('git+ssh://git@/', '')
            url = url.replace('ssh://git@', '')
            ext_ref = ExternalReference(
                reference_type=ExternalReferenceType.DISTRIBUTION,
                comment=CaPyCliBom.SOURCE_URL_COMMENT,
                url=url)
            bomitem.external_references.add(ext_ref)
        if "github.com" in url:
            if not str(url).startswith("http"):
                url = "https://" + url
            url = self.find_source_file(url, bomitem.name, bomitem.version)
            CycloneDxSupport.update_or_set_ext_ref(
                bomitem,
                ExternalReferenceType.DISTRIBUTION,
                CaPyCliBom.SOURCE_URL_COMMENT,
                url)
        bomitem.description = info.get("description", "")
        if not CycloneDxSupport.get_binary_file_hash(bomitem):
            ext_ref = CycloneDxSupport.get_ext_ref(
                bomitem,
                ExternalReferenceType.DISTRIBUTION,
                CaPyCliBom.BINARY_FILE_COMMENT)
            hash = info.get("dist", "").get("integrity", "")
            if ext_ref and hash:
                ext_ref.hashes.add(HashType(
                    algorithm=HashAlgorithm.SHA_1,
                    hash_value=hash))

        return bomitem

    def try_find_metadata(self, bom: Bom, package_source: str) -> Bom:
        """
        Find metadata for the whole SBOM.
        """
        for bomitem in bom.components:
            bomitem = self.try_find_component_metadata(bomitem, package_source)

        return bom

    def run(self, args):
        """Main method()"""
        if args.debug:
            global LOG
            LOG = capycli.get_logger(__name__)
        else:
            # suppress (debug) log output from requests and urllib
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

        print_text(
            "\n" + capycli.APP_NAME + ", " + capycli.get_app_version() +
            " - Determine Javascript components/dependencies\n")

        if args.help:
            print("Usage: ")
            print("  CaPyCli getdependencies javascript -i <package-lock.json> -o <bom.json> [-package-source SRC]")
            print("")
            print("Options:")
            print("     -i INPUTFILE                    package lock input file to read from")
            print("     -o OUTPUTFILE                   bom file to write to")
            print("     -package-source PACKAGE_SOURCE  URL of the package manager to use")
            print("     --search-meta-data              search for component meta-data")
            return

        if not args.inputfile:
            print_red("No input file (package-lock.json) specified!")
            sys.exit(ResultCode.RESULT_COMMAND_ERROR)

        if not os.path.isfile(args.inputfile):
            print_red("Input file not found!")
            sys.exit(ResultCode.RESULT_FILE_NOT_FOUND)

        if not args.outputfile:
            print_red("No output SBOM file specified!")
            sys.exit(ResultCode.RESULT_COMMAND_ERROR)

        print_text("Reading input file " + args.inputfile)
        sbom = self.convert_package_lock(args.inputfile)

        if args.search_meta_data:
            print_text("Searching for metadata...")
            sbom = self.try_find_metadata(sbom, args.package_source)

        print_text("Writing new SBOM to " + args.outputfile)
        try:
            SbomWriter.write_to_json(sbom, args.outputfile, True)
        except Exception as ex:
            print_red("Error writing new SBOM: " + repr(ex))
            sys.exit(ResultCode.RESULT_ERROR_WRITING_BOM)

        print_text(" " + self.get_comp_count_text(sbom) + " written to file " + args.outputfile)
        print()
