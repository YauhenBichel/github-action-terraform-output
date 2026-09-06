# GitHub Actions workflow action for Terraform output

## Author is Yauhen Bichel

## Hot to use

Please find `terraform.yml` workflow file with example of using terraform-output `action.yml` file

```

name: "Terraform"

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

jobs:
  terraform:
    runs-on: ubuntu-latest
    environment: dev
    steps:
    - name: Deploy to dev
      run: |
        echo "Deploying to dev environment"

    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ inputs.aws-region }}
    
    - name: Display commit information
      run: echo "$(git log -1)"
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: ${{ inputs.terraform_version }}

    - name: Terraform Init
      run: terraform init -backend-config="environments/dev/backend.hcl" -input=false
      working-directory: ${{ inputs.working_dir }}

    - name: Terraform Output
      id: terraform-output
      uses: ./.github/actions/terraform-output
      with:
        working-dir: ${{ inputs.working_dir }}


```

---

## Contributors

Thank you to everyone who has helped this project. Your code, reviews, issues, and pull requests are appreciated.

- [@YauhenBichel](https://github.com/YauhenBichel)

See the [full contributor graph](https://github.com/YauhenBichel/github-action-terraform-output/graphs/contributors).

## Contributors

Thank you to everyone who has helped.

<!-- readme: contributors,bots/- -start -->
<!-- readme: contributors,bots/- -end -->

Filled from GitHub commits (bots omitted). Live demo: [readme-contributors](https://github.com/YauhenBichel/readme-contributors#live-demo).
