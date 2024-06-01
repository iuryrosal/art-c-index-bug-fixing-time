import pandas as pd
import numpy as np
import math
import duckdb


class CreateFeature():  
    def build_timefixbug(self, dataSetOriginal):
        dataSetOriginal["TimeFixBug"] = ((dataSetOriginal["ResolutionDate"] - dataSetOriginal["CreationDate"]).dt.days)
        return dataSetOriginal

    def _build_no_commits(self, dataSetOriginal):
        # Quantidade de Commits
        quant_commits_commiter_values = dataSetOriginal.groupby(by=["Committer"])["Project"].count().values
        quant_commits_commiter_index = dataSetOriginal.groupby(by=["Committer"])["Project"].count().index
        zip_iterator = zip(quant_commits_commiter_index, quant_commits_commiter_values)
        a_dictionary_commits = dict(zip_iterator)
        return a_dictionary_commits

    def _build_no_assignees(self, dataSetOriginal):
        quant_assignee_commiter_values = dataSetOriginal.groupby(by=["Assignee"])["Priority"].count().values
        quant_assignee_commiter_index = dataSetOriginal.groupby(by=["Assignee"])["Priority"].count().index
        zip_iterator = zip(quant_assignee_commiter_index, quant_assignee_commiter_values)
        a_dictionary_assignee = dict(zip_iterator)
        return a_dictionary_assignee

    def _build_no_reporter(self, dataSetOriginal):
        quant_reporter_commiter_values = dataSetOriginal.groupby(by=["Reporter"])["Priority"].count().values
        quant_reporter_commiter_index = dataSetOriginal.groupby(by=["Reporter"])["Priority"].count().index
        zip_iterator = zip(quant_reporter_commiter_index, quant_reporter_commiter_values)
        a_dictionary_reporter = dict(zip_iterator)
        return a_dictionary_reporter

    def _build_no_comments(self, dataSetOriginal):
        quant_comment_commiter_values = dataSetOriginal.groupby(by=["Author"])["Content"].count().values
        quant_comment_commiter_index = dataSetOriginal.groupby(by=["Author"])["Content"].count().index
        zip_iterator = zip(quant_comment_commiter_index, quant_comment_commiter_values)
        a_dictionary_comment = dict(zip_iterator)
        return a_dictionary_comment

    def _build_median_freq_commits_per_month(self, dataSetOriginal):
        dataSetOriginal["CommitterDate"] = pd.to_datetime(dataSetOriginal["CommitterDate"], utc=True, format='mixed')
        grouped = dataSetOriginal.groupby(['Committer', pd.Grouper(key='CommitterDate', freq='M')])['Project'].count().reset_index().sort_values('CommitterDate')

        grouped = grouped.rename(columns={'Project': "FreqCommitPerM"})

        frequency_commit = grouped.groupby(by=["Committer"]).median()['FreqCommitPerM'].values
        ids_grouped = grouped.groupby(by=["Committer"]).median()['FreqCommitPerM'].index

        zip_iterator = zip(ids_grouped, frequency_commit)
        a_dictionary_median_freq_comment = dict(zip_iterator)
        return a_dictionary_median_freq_comment

    def build_c_index(self, snapshot_file, comment_file, commit_file):
        def cal_comments_weight(num_comments):
            w_comments = 0
            for index_comment in range(1, num_comments+1):
                w_comments += 2/math.sqrt(index_comment)
            return round(w_comments)

        def cal_commits_weight(num_commits):
            w_commits = 0
            for index_commit in range(1, num_commits+1):
                w_commits += 5/math.sqrt(index_commit)
            return round(w_commits)

        def cal_time_weight(DIFF_ANOS):
            return 0.95**abs(DIFF_ANOS)

        bug_per_comment = pd.merge(left=snapshot_file,
                                right=comment_file,
                                how="left",
                                on="Key")[["Key", "Author", "CreationDate_y"]]
        number_comments_per_author_bug = duckdb.sql("""
                                            SELECT Key, Author, COUNT(*) AS 'NUMBER_COMMENTS'
                                            FROM bug_per_comment
                                            GROUP BY Key, Author
                                            """).df()
        number_comments_per_author_bug["w_comments"] = number_comments_per_author_bug.NUMBER_COMMENTS.map(cal_comments_weight)

        commits_per_author_bug = pd.merge(left=snapshot_file, right=commit_file, how="left", on="Key")[["Key", "Committer"]].dropna()

        number_commits_per_author_bug = duckdb.sql("""
                                            SELECT Key, Committer, COUNT(*) AS 'NUMBER_COMMITS'
                                            FROM commits_per_author_bug
                                            GROUP BY Key, Committer
                                            """).df()
        number_commits_per_author_bug["w_commits"] = number_commits_per_author_bug.NUMBER_COMMITS.map(cal_commits_weight)

        time_per_bug = duckdb.sql("""
                            SELECT 
                                Key,
                                EXTRACT(YEAR FROM ResolutionDate::TIMESTAMP) - 2018 AS DIFF_ANOS
                            FROM snapshot_file
                            """).df()

        time_per_bug["w_time"] = time_per_bug.DIFF_ANOS.map(cal_time_weight)

        number_commits_per_author_bug = number_commits_per_author_bug.rename(columns={"Committer": "Author"})

        authors_bug_score = pd.merge(number_comments_per_author_bug, number_commits_per_author_bug, on=['Key', 'Author'], how='inner')

        authors_bug_score = pd.merge(authors_bug_score, time_per_bug, on="Key", how="inner")

        authors_bug_score["score_c"] = round(authors_bug_score["w_comments"] + authors_bug_score["w_commits"] * authors_bug_score["w_time"])

        result = duckdb.sql("""
            WITH RankedScores AS (
                SELECT
                    Author,
                    score_c,
                    ROW_NUMBER() OVER(PARTITION BY Author ORDER BY score_c DESC) AS rank
                FROM
                    authors_bug_score
            ),
            CIndex AS (
                SELECT
                    Author,
                    MAX(rank) AS C_index
                FROM
                    RankedScores
                WHERE
                    rank <= score_c
                GROUP BY
                    Author
            )
            SELECT
                abs.*,
                ci.C_index
            FROM
                authors_bug_score abs
            LEFT JOIN
                CIndex ci
            ON
                abs.Author = ci.Author
        """).df()
        result.drop_duplicates(inplace=True)
        return result

    def build_category_dev(self, dataSetOriginal, snapshot_file, comment_file, commit_file):
        timefixbug_mean = dataSetOriginal[['Committer', 'TimeFixBug']].groupby(by=["Committer"]).median().values
        timefixbug_mean = timefixbug_mean.reshape((139,))

        ids_grouped = dataSetOriginal["Committer"].unique()
        zip_iterator = zip(ids_grouped, timefixbug_mean)
        a_dictionary_commiters = dict(zip_iterator)

        data_items = a_dictionary_commiters.items()
        data_list = list(data_items)

        committers = pd.DataFrame(data_list, columns=['Committer', 'TimeFixBugMean'])

        committers['NoCommits'] = committers['Committer'].map(self._build_no_commits(commit_file))
        committers['NoAssignee'] = committers['Committer'].map(self._build_no_assignees(snapshot_file))
        committers['NoAuthorComment'] = committers['Committer'].map(self._build_no_comments(comment_file))
        committers['NoReporter'] = committers['Committer'].map(self._build_no_reporter(snapshot_file))
        # committers['MedianFreqCommitsPerMonth'] = committers['Committer'].map(self._build_median_freq_commits_per_month(commit_file))

        c_index = self.build_c_index(snapshot_file, comment_file, commit_file)

        contribution_25 = c_index.C_index.quantile(0.25)
        contribution_75 = c_index.C_index.quantile(0.75)

        category_dev = []

        committers_ids = c_index["Author"].values
        metric_engagement = c_index["C_index"].values

        for i in range(0, len(metric_engagement)):
            if metric_engagement[i] <= contribution_25:
                category_dev.append("Low Contribution")
            elif (metric_engagement[i] > contribution_25) and (metric_engagement[i] < contribution_75):
                category_dev.append("Medium Contribution")
            else:
                category_dev.append("High Contribution")
        zip_iterator = zip(committers_ids, category_dev)
        a_dictionary = dict(zip_iterator)
        dataSetOriginal['ContributionLevel'] = dataSetOriginal['Committer'].map(a_dictionary)

        zip_iterator = zip(committers_ids, metric_engagement)
        a_dictionary = dict(zip_iterator)
        dataSetOriginal['CIndex'] = dataSetOriginal['Committer'].map(a_dictionary)

        return dataSetOriginal

    def build_Authors_Freq(self, dataSetOriginal):
        def verify_count_Authors(n_Authors):
            if n_Authors >= 2:
                return ">=2 Authors"
            else:
                return "1 Author"

        dataSetOriginal["AuthorsFreq"] = dataSetOriginal["NoAuthors"].apply(verify_count_Authors)
        return dataSetOriginal

    def build_Comments_Freq(self, dataSetOriginal):
        def verify_count_Comments(n_Comments):
            if n_Comments >= 20:
                return ">= 20 Comments"
            else:
                return "< 20 Comments"

        dataSetOriginal["CommentsFreq"] = dataSetOriginal["NoComments"].apply(verify_count_Comments)
        return dataSetOriginal