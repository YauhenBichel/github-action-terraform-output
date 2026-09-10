# Terraform Output as JSON

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Reads `terraform output -json` from a working directory and hands it back as a
single step output, so a later step can pick values out of it with `jq` or
`fromJSON`.

It validates the JSON before returning it, warns when the directory looks
uninitialised, and writes the value with a heredoc delimiter so multi-line
output survives intact.

## Use it

```yaml
- name: Terraform Output
  id: tf
  uses: YauhenBichel/github-action-terraform-output@v1
  with:
    working-dir: ./terraform

- name: Read one value
  run: echo "The bucket is $BUCKET"
  env:
    BUCKET: ${{ fromJSON(steps.tf.outputs.terraform-output).bucket_name.value }}
```

`terraform init` has to have run in `working-dir` first, in the same job.
Terraform reads state to answer `output`, so this cannot run on its own.

## Inputs

| Name | Default | Description |
|---|---|---|
| `working-dir` | `./terraform` | Directory to run `terraform output` in |

## Outputs

| Name | Description |
|---|---|
| `terraform-output` | The full `terraform output -json` document, as a string |

The value is whatever Terraform prints, so each output is an object with
`value`, `type` and `sensitive`. That is why the example above reaches for
`.bucket_name.value` rather than `.bucket_name`.

Sensitive outputs are included. `terraform output -json` prints them in the
clear, unlike the human-readable form, so treat the result as a secret if any
of your outputs are one, and do not `echo` it.

## A full job

```yaml
name: Terraform

on:
  workflow_call:
    inputs:
      aws-region:
        required: true
        type: string
      terraform_version:
        required: false
        type: string
        default: '1.12.2'
      working_dir:
        required: false
        type: string
        default: './terraform'

permissions:
  contents: read
  id-token: write   # for the OIDC role assumption below

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # OIDC rather than a stored access key: nothing long-lived to leak, and
      # nothing to rotate.
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/github-actions-terraform
          aws-region: ${{ inputs.aws-region }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ inputs.terraform_version }}

      - name: Terraform Init
        run: terraform init -input=false
        working-directory: ${{ inputs.working_dir }}

      - name: Terraform Output
        id: tf
        uses: YauhenBichel/github-action-terraform-output@v1
        with:
          working-dir: ${{ inputs.working_dir }}
```

## Contributing

Issues and pull requests are welcome.

## Licence

[Apache-2.0](LICENSE) — Yauhen Bichel

---

## Contributors

Thank you to everyone who has helped.

<!-- readme: contributors,bots/- -start -->
<!-- readme: contributors,bots/- -end -->

Filled from GitHub commits (bots omitted). Live demo: [readme-contributors](https://github.com/YauhenBichel/readme-contributors#live-demo).
