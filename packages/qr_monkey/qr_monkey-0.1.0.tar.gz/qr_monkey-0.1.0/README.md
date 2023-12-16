# qr_monkey

An API Client for qrcode-monkey API that integrates custom and unique looking QR codes into your system or workflow.

## Installation

```bash
$ pip install qr_monkey
```

## Usage

#### 1. Import qr_monkey

After installing the package, import it into your project.

import qr_monkey

#### 2. Create base_url

Use the provided custom function to create a custom QR code with the specified parameters:

base_url = "specify the url you want to link to the QR code"

#### 3. Set parameters 

You can set these according to the ['QRCode-Monkey website'](https://www.qrcode-monkey.com/qr-code-api-with-logo/?utm_source=google_c&utm_medium=cpc&utm_campaign=&utm_content=&utm_term=qr%20code%20monkey_e&gad_source=1&gclid=CjwKCAiAg9urBhB_EiwAgw88mV1GL6kx3Cywp8JgtxcCjZTneJc8gj1J8w3LLS3TB8Z28A1QCTLNNhoCrq4QAvD_BwE)

For example:

params = {
    "data": base_url,
    "config": {
        "body": "circle",
    },
    "size": 300,
    "download": False,
    "file": "png"
}

#### 4. Create custom QR code  

qr_monkey.custom(base_url,params)


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`qr_monkey` was created by Vansh Murad Kalia. It is licensed under the terms of the MIT license.

## Credits

`qr_monkey` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
