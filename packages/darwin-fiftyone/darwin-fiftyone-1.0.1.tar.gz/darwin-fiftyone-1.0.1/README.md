# darwin_fiftyone

Provides integration between Voxel51 and V7 Darwin. This enables Voxel51 users to send subsets of their datasets to Darwin for annotation and review. The annotated data can then be imported back into Voxel51.

## Example Usage

To illustrate, let's upload all files from the zoo dataset "quickstart" into a Darwin dataset named "quickstart-example". If the dataset doesn't already exist in Darwin, it will be created.

```python
import fiftyone.zoo as foz
dataset = foz.load_zoo_dataset("quickstart", dataset_name="quickstart-example")
dataset.annotate(
    "annotation_job_key",
    label_field="ground_truth",
    atts=["iscrowd"],
    launch_editor=True,
    backend="darwin",
    dataset_slug="quickstart-example",
    external_storage="example-darwin-storage-slug",
    base_url="https://darwin.v7labs.com/api/v2/teams",
)
```

After the annotations and reviews are completed in Darwin, you can fetch the updated data as follows:

```python
dataset.load_annotations("annotation_job_key")
```


## Configuration

To integrate with the Darwin backend:

1. Install the backend:

```bash
pip install darwin-fiftyone
```

2. Configure voxel51 to use it.

```bash
cat ~/.fiftyone/annotation_config.json
```

```json
{
  "backends": {
    "darwin": {
      "config_cls": "darwin_fiftyone.DarwinBackendConfig",
      "api_key": "d8mLUXQ.**********************"
    }
  }
}
```

**Note**: Replace the api_key placeholder with a valid API key generated from Darwin.


## API

In addition to the standard arguments provided by dataset.annotate(), we also support:

- `backend=darwin`, Indicates that the Darwin backend is being used.
- `atts`, Specifies attribute subannotations to be added in the labelling job
- `dataset_slug`, Specifies the name of the dataset to use or create on Darwin.
- `external_storage`, Specifies the sluggified name of the Darwin external storage and indicates that all files should be treated as external storage

## Supported Annotation Types

The integration supports bounding boxes, polygons (closed polylines), keypoints, and tags (classifications). It also supports attribute subtypes as previously mentioned.

Future development work will focus on the addition of annotation and subannotation types so do reach out if you are interested


## License and Usage
Please see the terms in [LEGAL](LEGAL) and [LICENSE](LICENSE).

# Development

## Install

For development installation, checkout the repo and

```bash
pip install . 
```

## Testing 
Set up your environment with FiftyOne and Darwin integration settings. To find your team slug check the [Darwin documentation on dataset identifiers](https://docs.v7labs.com/reference/datasetidentifier) which has a section called "Finding Team Slugs:"

You'll also need an [API Key](https://docs.v7labs.com/docs/use-the-darwin-python-library-to-manage-your-data)

```bash
export FIFTYONE_ANNOTATION_BACKENDS=*,darwin
export FIFTYONE_DARWIN_CONFIG_CLS=darwin_fiftyone.DarwinBackendConfig
export FIFTYONE_DARWIN_API_KEY=******.*********
export FIFTYONE_DARWIN_TEAM_SLUG=your-team-slug-here
```
## TODO

- Video support in progress
- Support for read only external data storage
- Support for mask and keypoint skeleton types