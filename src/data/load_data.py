import pandas as pd
import streamlit as st


class DataSet():
    def __init__(self):
        self.changelog_file = pd.read_csv("data/raw/new_changelog_file.csv", sep = ";")
        self.commit_file = pd.read_csv("data/raw/new_commit_file.csv", sep = ";")
        self.comment_file = pd.read_csv("data/raw/new_comment_file.csv", sep = ";")
        self.final_list_of_contributors = pd.read_csv("data/raw/final_list_of_contributors_after.csv", sep = ";")
        self.snapshot_file = pd.read_csv("data/raw/new_snapshot_file.csv", sep = ";")
        self.commit_snapshot = self.merge_commit_snapshot()

    def merge_commit_snapshot(self):
        return pd.merge(self.commit_file, self.snapshot_file, on='Key')
