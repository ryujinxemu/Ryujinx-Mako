# setup-mako

A small composite action to set up the environment for Mako.

It installs poetry and all module dependencies.

## Usage

Add the following steps to your workflow:

```yml
- name: Checkout Ryujinx-Mako
  uses: actions/checkout@v3
  with:
    repository: Ryujinx/Ryujinx-Mako
    ref: master
    path: ".ryujinx-mako"

- name: Setup Ryujinx-Mako
  uses: .ryujinx-mako/.github/actions/setup-mako
```


