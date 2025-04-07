import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="1.12.5.0",
    file_description="EasyTARC time management software",
    internal_name="EasyTARC",
    legal_copyright="Copyright 2023 Sebastian Feiert. Licensed under the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)",
    original_filename="EasyTARC.exe",
    product_name="EasyTARC",
    translations=[0, 1200]
)