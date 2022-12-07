
import os
import tarfile
import wget


def get_sst_data(data_dir=None):
    if data_dir is None:
        data_dir = os.path.join(os.path.expanduser('~'), '.xarray_tutorial_data')
    
    os.makedirs(data_dir, exist_ok=True)

    remote = 'http://ldeo.columbia.edu/~rpa/sst.tar.gz'

    # download the data
    filename = wget.download(remote, out=data_dir)

    # un tar/zip the file
    cwd = os.getcwd()
    os.chdir(data_dir)
    try:
        with tarfile.open(filename, "r:gz") as file:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(file)
    finally:
        os.chdir(cwd)

    # remove tar.gz file
    os.remove(filename)

    print(f'\nsst data is in {data_dir}/sst')
