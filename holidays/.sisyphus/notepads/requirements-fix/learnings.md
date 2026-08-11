## dify-plugin Dependency Fix

- Original requirement `dify_plugin~=0.0.1b72` was invalid - no such version exists on PyPI
- Two packages exist on PyPI:
  - `dify-plugin` (hyphen) - latest version 0.9.1
  - `dify_plugin` (underscore) - latest version 0.7.4
- Based on official documentation and GitHub repository names (`dify-plugin-sdks`), the hyphen version is the correct one
- Updated requirements.txt to use `dify-plugin==0.9.1`
- SSL certificate errors encountered during installation testing suggest environmental issues rather than package availability issues