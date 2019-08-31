# Useful extension to dataframe

import pandas as pd
import numpy as np

from sh import sftp
import tempfile
import os
from collections import OrderedDict

from ...s3 import S3

class pp_s3(object):
    """
    PP extension methods to interface with S3

    Integrated into main ppext class
    """
    def read_s3(self, filename, 
                first_index=0, items=1, return_df_only=True,
                aws_credentials='/opt/share/credentials/aws/aws_config',
                **kwargs):
        """
        Read a CSV file from S3
        Input:
            filename -- string to name of file on s3
                        bucket:path/to/optional_file.csv
                        if the filename is given, that is returned,
                        otherwise one or more files from the path
                        are returned depending on index
            first_index -- which file from the path contents in descending order
                           of creation should be chosen
                                     0 - the latest
                                     1 - the one before the latest
                                     etc
            items -- Number of files required after first_index
                        -1: Include all files
            return_df_only -- If true and only one file is selected, a single
                              dataframe will be returned
            aws_credentials -- aws credential file in the pyprofile format
            kwargs -- parameters of the pandas read_csv method to parse
                      the content.
        
        By default, it is comma separated with quotation marks around
        non numeric fields - this seems to work the best but can be changed 
        if desired
        
        Output:
            results -- an ordered dictionary with the key as the filename
                       and the value as the dataframe
                       (except if return_df_only is true and there is only
                        one dataframe)
        """
        
        s3, bucket, file = self._prepare_s3(filename, aws_credentials)
        
        if os.path.basename(file).endswith('.csv'):
            selected_files = [file]
        else:
            if items == -1:
                selected_files = s3.list_files(bucket, file)
                folder_name = file.rstrip('/').split('/')[-1] + '/'
                # Exclude any other folders with the same prefix
                selected_files = [x for x in selected_files if folder_name in x]
                # Do not consider subfolders
                selected_files = [x for x in selected_files if '/' not in x.split(folder_name)[1]]
            else:
                selected_files = s3.list_files(bucket, file)[first_index:first_index+items]
        
        results = OrderedDict()
        
        for f in selected_files:
            results[f] = s3.read_csv(bucket, f, **kwargs)
            context_file=os.path.dirname(f).replace('/', '_')
            try:
                results[f].pp.normalise(('s3', context_file))
            except KeyError:
                print('No context for file: {}'.format(f))
                pass
        
        if len(results) == 1 and return_df_only:
          return next(iter(results.values()))
        return results
            

    def _prepare_s3(self, filename, aws_credentials):
        
        bucket, file = filename.split(':')
        
        # get s3 connection
        s3 = S3(aws_credentials)
        
        return s3, bucket, file