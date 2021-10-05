# Changelog

## Version 4.0.1 - 2021-10-05

- Extended method datasets sync to support folder as input and better help functionality, and re-name to create-documents
  
## Version 4.0.0 - 2021-09-10

- Updated version of Python SDK to 4.0.0. API key is no longer needed.

## Version 3.1.1 - 2021-08-31

- Bugfix in sync method

## Version 3.1.0 - 2021-08-30

- Added method datasets sync for uploading larger datasets

## Version 3.0.0 - 2021-06-29

- Added method datasets create
- Added method datasets list
- Added method datasets update
- Added method datasets delete
- Added optional parameter --dataset-id to documents create
- Added optional parameter --document-id to documents delete
- Added optional parameter --dataset-id to documents create
- Added optional parameter --dataset-id to documents list
- Added optional parameter --dataset-id to documents delete
- Added optional parameter --dataset-id to documents update
- Added method models create-data-bundle
- Added method models list-data-bundles
- Added method models update-data-bundle
- Added method models delete-data-bundle

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
