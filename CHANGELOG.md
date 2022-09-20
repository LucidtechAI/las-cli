# Changelog

## Version 9.1.4 - 2022-09-20

- Added CSV support in `datasets create-documents`

## Version 9.1.3 - 2022-09-19

- You may now upload documents without ground truth using `datasets create-documents`
- Improved the caching mechanism of `datasets create-documents`

## Version 9.1.2 - 2022-09-07

- Added `originalFilePath` to `metadata` in `datasets create-documents`

## Version 9.0.1 - 2022-06-30

- Fix bug in datasets create-documents

## Version 9.0.0 - 2022-06-02

- Added optional parameter `--use-cache` to `datasets create-documents`
- Don't use cached data by default in `datasets create-documents`

## Version 8.5.0 - 2022-05-23

- Reduced memory overhead in `datasets create-documents`

## Version 8.4.0 - 2022-05-09

- Optional parameter `--training-id` in `models update` is now nullable

## Version 8.3.0 - 2022-04-22

- Added `payment-methods create`
- Added `payment-methods delete`
- Added `payment-methods get`
- Added `payment-methods list`
- Added `payment-methods update`
- Added optional parameter `--payment-method-id` to `organizations update`

## Version 8.2.0 - 2022-04-12

- Added optional parameter `--sort-by` to `documents list`
- Added optional parameter `--sort-by` to `predictions list`
- Added optional parameter `--order` to `documents list`
- Added optional parameter `--order` to `predictions list`

## Version 8.1.0 - 2022-03-29

- Added `datasets get-documents`. This command will download all documents (PDF, JPEG etc. and JSON ground truth) to directory specified by `output_dir`
- Show help when invoking `las` with no arguments
- Support newer Python versions in setup.py
- Added --version

## Version 8.0.0 - 2022-03-15

- Fix bug in datasets create-documents
- width and height is now optional in models create

## Version 7.1.0 - 2022-03-04

- Added --training-id to predictions create
- Added --training-id to models update

## Version 7.0.0 - 2022-02-23

- Support csv files in datasets create-documents
- Added models list-all-data-bundles
- Added optional parameter --metadata to documents create, documents update, datasets create, datasets update, models create, models update and trainings create
- Removed optional parameter --start-training from models update (Breaking change)
- Changed several optional argument names from --X-path to --X (Breaking change)
- Added models update-training

## Version 6.2.2 - 2022-01-28

- Update argcomplete package

## Version 6.2.1 - 2022-01-26

- Added exception handling to datasets create-documents
- Support specifying ground-truth encoding in datasets create-documents

## Version 6.2.0 - 2021-11-30

- Added models list-trainings
- Added models create-training
- Added plans list
- Added plans get

## Version 6.1.0 - 2021-11-08

- Added optional parameter --postprocess-config to predictions create

## Version 6.0.0 - 2021-10-13

- Removed all support for batches. Use datasets instead.

## Version 5.0.0 - 2021-10-05

- Renamed datasets sync to datasets create-documents and support folder as input and better help functionality

## Version 4.0.0 - 2021-09-10

- Updated version of Python SDK to 4.0.0. API key is no longer needed.

## Version 3.1.1 - 2021-08-31

- Bugfix in datasets sync

## Version 3.1.0 - 2021-08-30

- Added datasets sync for uploading larger datasets

## Version 3.0.0 - 2021-06-29

- Added datasets create
- Added datasets list
- Added datasets update
- Added datasets delete
- Added optional parameter --dataset-id to documents create
- Added optional parameter --document-id to documents delete
- Added optional parameter --dataset-id to documents create
- Added optional parameter --dataset-id to documents list
- Added optional parameter --dataset-id to documents delete
- Added optional parameter --dataset-id to documents update
- Added models create-data-bundle
- Added models list-data-bundles
- Added models update-data-bundle
- Added models delete-data-bundle

### Breaking changes
  `las documents delete` will now require a document id as a positional argument and delete that document only.

  `las documents delete-all` can be used to delete multiple documents. It will by default delete all the documents available.
  Use `--max-results` to restrict the number of documents deleted as before,
  but the default will be to delete everything.


## Version 2.4.1 - 2021-06-18

- Fixed bug causing more log messages than necessary to be printed

## Version 2.4.0 - 2021-06-09

- Added organizations get
- Added organizations update

## Version 2.3.4 - 2021-05-25

- Added --login-urls and --default-login-url to app-clients create

## Version 2.3.3 - 2021-05-11

- Added models create
- Added models update
- Added models get
- Added batches update
- Added app-clients update

## Version 2.3.2 - 2021-05-10

- Added argument app_client_id to users create
