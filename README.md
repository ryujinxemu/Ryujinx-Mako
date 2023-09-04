# Ryujinx-Mako

A custom GitHub App to aid Ryujinx with project management and moderation

## Usage

1. Add the following steps to your workflow:

   ```yml
   - name: Checkout Ryujinx-Mako
     uses: actions/checkout@v3
     with:
       repository: Ryujinx/Ryujinx-Mako
       ref: master
       path: '.ryujinx-mako'
   
   - name: Setup Ryujinx-Mako
     uses: ./.ryujinx-mako/.github/actions/setup-mako
   ```
   
2. Execute the available commands like this:
    
   ```yml
   - name: Setup git identity for Ryujinx-Mako
     run: |
        # poetry -n -C .ryujinx-mako run ryujinx-mako <command> [<args>]
        # for example:
        poetry -n -C .ryujinx-mako run ryujinx-mako setup-git
     env:
       MAKO_APP_ID: ${{ secrets.MAKO_APP_ID }}
       MAKO_PRIVATE_KEY: ${{ secrets.MAKO_PRIVATE_KEY }}
       MAKO_INSTALLATION_ID: ${{ secrets.MAKO_INSTALLATION_ID }}
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
