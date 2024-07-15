import pandas as pd


class TransformData():
  def data_transformation(self, dataSetOriginal):
    columns_selected = ["Owner", "Manager_x", "Manager_y", "Category_x", "Category_y", 
                        "AffectsVersions", "FixVersions", "NoWatchers", "CommitHash", 
                        "InwardIssueLinks", "OutwardIssueLinks", "IsMergeCommit", 
                        "Project_y", "Status", "HasMergeCommit"]
    data_set_transformed = dataSetOriginal.drop(columns=columns_selected, inplace=False)

    data_set_transformed.NoAuthors = data_set_transformed.NoAuthors.astype("int")
    data_set_transformed.NoCommitters = data_set_transformed.NoCommitters.astype("int")
    data_set_transformed.CreationDate = pd.to_datetime(data_set_transformed.CreationDate, utc=True)
    data_set_transformed.ResolutionDate = pd.to_datetime(data_set_transformed.ResolutionDate, utc=True)
    data_set_transformed.CommittersLastCommitDate = pd.to_datetime(data_set_transformed.CommittersLastCommitDate, utc=True)
    data_set_transformed.CommittersFirstCommitDate = pd.to_datetime(data_set_transformed.CommittersFirstCommitDate, utc=True)
    data_set_transformed.CommitterDate = pd.to_datetime(data_set_transformed.CommitterDate, utc=True)
    data_set_transformed.AuthorDate = pd.to_datetime(data_set_transformed.AuthorDate, utc=True)
    data_set_transformed.ResolutionDate = pd.to_datetime(data_set_transformed.ResolutionDate, utc=True)

    data_set_transformed = data_set_transformed.rename(columns={"Project_x": "Project"})

    return data_set_transformed

  def remove_outlier_timefixbug(self, dataSetOriginal):
    data_set_transformed = dataSetOriginal[dataSetOriginal.BFT <= 95] 
    return data_set_transformed