# Changelog

## Version 13.2.3 - 2024-10-09

- Bugfix `transitions update-execution` now supports additional keyword arguments

## Version 13.2.2 - 2024-06-13

- Bugfix `models update-training` now works as intended when specifying `--deployment-environment-id`

## Version 13.2.1 - 2024-02-20

- Bugfix `models update-training` no longer attempts to send `null` for `metadata` when not specified

## Version 13.2.0 - 2023-12-13

- Added optional parameter `--status` to `workflows update`

## Version 13.1.0 - 2023-12-08

- Added optional parameter `--quality` to `documents get`

## Version 13.0.0 - 2023-12-07

- Added `app-clients get`
- Added optional parameter `--status` to `workflows update-execution`
- Added optional parameter `--next-transition-id` to `workflows update-execution`
- Removed mandatory parameter `next_transition_id` from `workflows update-execution`
- Added optional parameter `--statistics-last-n-days` to `models get`

## Version 12.4.0 - 2023-12-05

- Updated default `--preprocess-image` in `create-default` workflow

## Version 12.3.0 - 2023-11-20

- Added optional parameter `--email-config` to `workflows create`
- Added optional parameter `--email-config` to `workflows update`
- Now able to also specify inline JSON for optional parameter `--error-config` in `workflows create`
- Now able to also specify inline JSON for optional parameter `--error-config` in `workflows update`
- Now able to also specify inline JSON for optional parameter `--completed-config` in `workflows create`
- Now able to also specify inline JSON for optional parameter `--completed-config` in `workflows update`

## Version 12.2.0 - 2023-11-02

- Added `models get-data-bundle`
- Added `models get-training`

## Version 12.1.0 - 2023-11-01

- Updated `--create-default-workflow` in `workflows create-default` to use the latest docker images and automatically
add `modelId` to the form config

## Version 12.0.0 - 2023-11-01

- Added `datasets create-transformation`
- Added `datasets delete-transformation`
- Added `datasets list-transformations`
- Added Python 3.11 support
- Removed Python 3.6 and 3.7 support as they have reached end of life

## Version 11.2.0 - 2023-09-14

- Added optional parameter `--model-id` to `predictions list`

## Version 11.1.0 - 2023-09-07

- Added optional parameter `--metadata` to `workflows create`
- Added optional parameter `--metadata` to `workflows update`

## Version 11.0.0 - 2023-08-30

- Added `roles list`
- Added `roles get`
- Added optional parameter `--role-ids` to `app-clients create`
- Added optional parameter `--role-ids` to `app-clients update`
- Added optional parameter `--role-ids` to `users create`
- Added optional parameter `--role-ids` to `users update`
- Removed deprecated optional parameters `--avatar` and `--name` from `users create`
- Removed deprecated optional parameters `--avatar` and `--name` from `users update`

## Version 10.1.0 - 2023-06-27

- Added optional parameter `--width` to `documents get`
- Added optional parameter `--height` to `documents get`
- Added optional parameter `--density` to `documents get`
- Added optional parameter `--page` to `documents get`
- Added optional parameter `--rotation` to `documents get`

## Version 9.5.0 - 2023-04-18

- Added `deployment-environments get`
- Added `deployment-environments list`
- Added `--postprocess-config` to `models create`
- Updated `--preprocess-config` in `models create` to also accept inline JSON
- Added `--postprocess-config` to `models update`
- Updated `--preprocess-config` in `models update` to also accept inline JSON
- Updated `--postprocess-config` in `predictions create` to also accept path to a JSON file

## Version 9.4.0 - 2023-02-23

- Added `--rotation` to `predictions create`

## Version 9.3.0 - 2023-01-30

- Added `--base-model` to `models create`
- Added `--owner` to `models list`

## Version 9.2.4 - 2022-10-13

- Fixed a bug causing `datasets create-documents` to skip creating new documents for documents that have been deleted
from the dataset since last upload.

## Version 9.2.3 - 2022-10-12

- Updated `workflows create-default` to use the default manual transition form component
- Updated default `--preprocess-image` in `workflows create-default`

## Version 9.2.2 - 2022-09-30

- Fixed a bug in `datasets create-documents`.

## Version 9.2.1 - 2022-09-29

- Using a CSV file as input to `datasets create-documents` will now try to locate the document file specified by
`document-path-column` in all sub-directories, e.g. if `document_path=foo/bar/baz.pdf` it will first see if
`foo/bar/baz.pdf` points to an existing and valid file type, then it will check if `bar/baz.pdf` points to an existing
and valid file type and so forth.
- Fixed output bug in `datasets get-documents`. Now only counts number of documents from the dataset you are
downloading, not the number of documents in the outdir_dir

## Version 9.2.0 - 2022-09-28

- Added `--image-url` to `transitions update`
- Added `--secret-id` to `transitions update`
- Added `--cpu` to `transitions update`
- Added `--memory` to `transitions update`
- Now supporting `transitions update --environment null` to clear all environment variables from a transition
- Now supporting `transitions update --environment-secrets null` to clear all environment secrets from a transition
- Added `--from-start-time` to `workflows list-executions`
- Added `--to-start-time` to `workflows list-executions`
- Added shorthand `-p` for `--profile`

## Version 9.1.4 - 2022-09-20

- Added CSV support in `datasets create-documents`
- Removed deprecated `--width` and `--height` from `models create` and `models update`

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
