#!/usr/bin/env python3

"""
The MappingTemplate executes RML rules to generate high quality Linked Data
from multiple originally (semi-)structured data sources.
"""

import os
import psutil
import time
from typing import Optional
from timeout_decorator import timeout, TimeoutError  # type: ignore
from bench_executor.logger import Logger
from bench_executor.container import Container

VERSION = 'kgc2024-tra'
TIMEOUT = 6 * 3600  # 6 hours


class MappingTemplate(Container):
    """MappingTemplate container for executing MTL mappings."""

    def __init__(self, data_path: str, config_path: str, directory: str,
                 verbose: bool, expect_failure: bool = False):
        """Creates an instance of the MappingTemplate class.

        Parameters
        ----------
        data_path : str
            Path to the data directory of the case.
        config_path : str
            Path to the config directory of the case.
        directory : str
            Path to the directory to store logs.
        verbose : bool
            Enable verbose logs.
        expect_failure : bool
            If a failure is expected, default False.
        """
        self._data_path = os.path.abspath(data_path)
        self._config_path = os.path.abspath(config_path)
        self._logger = Logger(__name__, directory, verbose)
        self._verbose = verbose

        os.makedirs(os.path.join(self._data_path, 'mapping-template'), exist_ok=True)
        super().__init__(f'cefriel/mapping-template:{VERSION}', 'MappingTemplate',
                         self._logger, expect_failure=expect_failure,
                         volumes=[f'{self._data_path}/mapping-template:/data',
                                  f'{self._data_path}/shared:/data/shared'])

    @property
    def root_mount_directory(self) -> str:
        """Subdirectory in the root directory of the case for MappingTemplate.

        Returns
        -------
        subdirectory : str
            Subdirectory of the root directory for MappingTemplate.

        """
        return __name__.lower()

    @timeout(TIMEOUT)
    def _execute_with_timeout(self, arguments: list) -> bool:
        """Execute a mapping with a provided timeout.

        Returns
        -------
        success : bool
            Whether the execution was successfull or not.
        """

        cmd = 'java -jar /mapping-template/mapping-template.jar'
        if self._verbose:
            cmd += ' --verbose'
        cmd += f' {" ".join(arguments)}'

        print(cmd)
        
        self._logger.debug(f'Executing MappingTemplate with arguments '
                           f'{" ".join(arguments)}')

        return self.run_and_wait_for_exit(cmd)

    def execute(self, arguments: list) -> bool:
        """Execute MappingTemplate with given arguments.

        Parameters
        ----------
        arguments : list
            Arguments to supply to MappingTemplate.

        Returns
        -------
        success : bool
            Whether the execution succeeded or not.
        """
        try:
            return self._execute_with_timeout(arguments)
        except TimeoutError:
            msg = f'Timeout ({TIMEOUT}s) reached for MappingTemplate'
            self._logger.warning(msg)

        return False

    def execute_mapping(self,
                        mapping_file: str,
                        output_file: str,
                        input_format: Optional[str] = None,
                        input_file: Optional[str] = None,
                        output_formatter: Optional[str] = None,
                        serialization: Optional[str] = None,
                        rdb_username: Optional[str] = None,
                        rdb_password: Optional[str] = None,
                        rdb_host: Optional[str] = None,
                        rdb_port: Optional[int] = None,
                        rdb_name: Optional[str] = None,
                        rdb_type: Optional[str] = None) -> bool:
        """Execute a mapping file with MappingTemplate.

        Parameters
        ----------
        input_file : Optional[str]
            File used as input for a mapping.
        mapping_file : str
            Path to the mapping file to execute.
        output_file : str
            Name of the output file to store the triples in.
        formatter : str
            Formatter format to use.
        rdb_username : Optional[str]
            Username for the database, required when a database is used as
            source.
        rdb_password : Optional[str]
            Password for the database, required when a database is used as
            source.
        rdb_host : Optional[str]
            Hostname for the database, required when a database is used as
            source.
        rdb_port : Optional[int]
            Port for the database, required when a database is used as source.
        rdb_name : Optional[str]
            Database name for the database, required when a database is used as
            source.
        Returns
        -------
        success : bool
            Whether the execution was successfull or not.
        """

        arguments = [ '-b', '/data/shared/',
                      '-t', mapping_file,
                      '-o', output_file,
                      '-iri', 'http://example.com/base/',
                      '-rml', '-fir', '--trim'] #, '-f', 'nq']

        if input_format is not None:
            arguments.append(f'-if {input_format}')

        if input_file is not None:
            arguments.append('-i')
            arguments.append(os.path.join('/data/shared/', input_file))

        if rdb_username is not None and rdb_password is not None \
           and rdb_port is not None and rdb_name is not None \
           and rdb_host is not None:

            arguments.append('--username')
            arguments.append(rdb_username)
            arguments.append('--password')
            arguments.append(rdb_password)

            rdb_url = f'{rdb_host}:{rdb_port}'
            
            arguments.append('-url')
            arguments.append(rdb_url)
            arguments.append('-id')
            arguments.append(rdb_name)

        print(arguments)

        return self.execute(arguments)

