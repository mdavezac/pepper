salt packages:
  pip.installed:
    - pkgs:
      - pip
      - salt
      - jupyter
      - mako
      - jinja2
    - upgrade: True
    - bin_env: {{pillar['condiment_build_dir']}}/salt-env/bin/pip

{{grains['userhome']}}/.salted:
  file.directory:
    - makedirs: True
