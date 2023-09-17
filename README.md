# Ryujinx-Mako

A custom GitHub App to aid Ryujinx with project management and moderation

## Usage

Add the following step to your workflow:

```yml
- name: Run Ryujinx-Mako
  uses: Ryujinx/Ryujinx-Mako@master
  with:
    command: <Mako subcommand>
    args: <subcommand args>
    app_id: ${{ secrets.MAKO_APP_ID }}
    private_key: ${{ secrets.MAKO_PRIVATE_KEY }}
    installation_id: ${{ secrets.MAKO_INSTALLATION_ID }}
```

## Available commands

```
usage: ryujinx_mako [-h] {setup-git,update-reviewers} ...

A python module to aid Ryujinx with project management and moderation

options:
  -h, --help            show this help message and exit

subcommands:
  setup-git             Set git identity to Ryujinx-Mako
  
  update-reviewers      Update reviewers for the specified PR
```

### setup-git

```
usage: ryujinx_mako setup-git [-h] [-l]

Set git identity to Ryujinx-Mako

options:
  -h, --help   show this help message and exit
  -l, --local  Set git identity only for the current repository.
```

### update-reviewers

```
usage: ryujinx_mako update-reviewers [-h] repo_path pr_number config_path

Update reviewers for the specified PR

positional arguments:
  repo_path
  pr_number
  config_path

options:
  -h, --help   show this help message and exit
```
