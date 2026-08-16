from unittest.mock import patch

from atlassian.bitbucket.cloud.repositories.pipelines import Pipelines


@patch.object(Pipelines, "post", return_value={"uuid": "{pipeline-uuid}", "type": "pipeline"})
def test_trigger_custom_pipeline_uses_commit_and_pattern(mock_post):
    pipelines = Pipelines("https://api.bitbucket.org/2.0/repositories/workspace/repository/pipelines")

    pipeline = pipelines.trigger(commit="a" * 40, pattern="style-check")

    mock_post.assert_called_once_with(
        None,
        trailing=True,
        data={
            "target": {
                "ref_type": "branch",
                "type": "pipeline_ref_target",
                "ref_name": "master",
                "commit": {"type": "custom", "hash": "a" * 40},
                "selector": {"type": "custom", "pattern": "style-check"},
            }
        },
    )
    assert pipeline.uuid == "{pipeline-uuid}"
