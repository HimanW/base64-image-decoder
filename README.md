# JSON Image Decoder

Decode base64-encoded images from JSON response files into real image
files with a small, CLI-friendly Python tool.

This script walks through a folder of `.json` files, looks for an
`annotated_image` block with a base64 string, and writes out the decoded
images to an output directory.

------------------------------------------------------------------------

## Features

-   Scan a folder for JSON files
-   Extract `annotated_image.base64` from each file
-   Decode and save the image to disk
-   Uses the original filename and MIME type to decide the image
    extension
-   Simple command-line interface

------------------------------------------------------------------------

## Requirements

-   Python 3.8+
-   Standard library only:
    -   `argparse`
    -   `base64`
    -   `json`
    -   `dataclasses`
    -   `pathlib`
    -   `typing`

No external dependencies are required for the basic decoder.

------------------------------------------------------------------------

## Installation

Clone the repository:

``` bash
git clone https://github.com/<your-username>/json-image-decoder.git
cd json-image-decoder
```

(Replace `<your-username>` and repo name with your actual GitHub
details.)

------------------------------------------------------------------------

## JSON Format

The script expects each JSON file to have a structure like:

``` json
{
  "job_id": "cae61e75-ab11-4504-b643-98c6647163ca",
  "status": "completed",
  "annotated_image": {
    "filename": "cae61e75-ab11-4504-b643-98c6647163ca_IMG_20251117_132353.jpg",
    "mime": "image/jpeg",
    "base64": "<very long base64 string>"
  }
}
```

The important part is the `annotated_image` block with:

-   filename\
-   mime\
-   base64

------------------------------------------------------------------------

## Usage

Place your JSON files in a folder, for example:

    json-input/
      response_1764238955577.json
      response_1764239179541.json

Run the decoder:

``` bash
python decoder.py json-input/ -o png-output
```

-   `json-input/` --- folder containing your `.json` files\
-   `-o png-output` --- folder where decoded images will be saved\
    (it will be created if it doesn't exist)

### Example output:

    [INFO] Found 2 JSON file(s) in C:\Users\Kavinda\Documents\GitHub\decoder-model\json-input
    [INFO] Output images will be written to C:\Users\Kavinda\Documents\GitHub\decoder-model\png-output
    ------------------------------------------------------------
    [OK] response_1764238955577.json  ->  349b8fbb-0202-4766-bb8c-c01e91eabe86_IMG_20251117_132353.jpg
    [OK] response_1764239179541.json  ->  cae61e75-ab11-4504-b643-98c6647163ca_IMG_20251117_132353.jpg

Decoded images will be saved in:

    png-output/
      349b8fbb-0202-4766-bb8c-c01e91eabe86_IMG_20251117_132353.jpg
      cae61e75-ab11-4504-b643-98c6647163ca_IMG_20251117_132353.jpg

------------------------------------------------------------------------

## Notes

-   The script uses the MIME type to determine the file extension
    (`image/jpeg` → `.jpg`, `image/png` → `.png`).\
-   If the MIME type is unknown, it falls back to the original
    filename's extension or `.bin`.\
-   You can customize the behavior in `decoder.py` if your JSON
    structure changes or if you want to force a specific output format.
