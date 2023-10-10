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

## Required environment variables

- `MAKO_APP_ID`: the GitHub App ID
- `MAKO_PRIVATE_KEY`: the contents of the GitHub App private key
- `MAKO_INSTALLATION_ID`: the GitHub App installation ID

## Available commands

```
usage: ryujinx_mako [-h] {setup-git,update-reviewers} ...

A python module to aid Ryujinx with project management and moderation

options:
  -h, --help            show this help message and exit

subcommands:
  {setup-git,update-reviewers}
    setup-git           Configure git identity for Ryujinx-Mako
    update-reviewers    Update reviewers for the specified PR
```

### setup-git

```
usage: ryujinx_mako setup-git [-h] [-l]

Configure git identity for Ryujinx-Mako

options:
  -h, --help   show this help message and exit
  -l, --local  configure the git identity only for the current repository
```

### update-reviewers

```
usage: ryujinx_mako update-reviewers [-h] repo_path pr_number config_path

Update reviewers for the specified PR

positional arguments:
  repo_path    full name of the GitHub repository (format: OWNER/REPO)
  pr_number    the number of the pull request to check
  config_path  the path to the reviewers config file

options:
  -h, --help   show this help message and exit
```
