import pandas as pd
import numpy as np


def match_age_sex(df_cases, df_controls, age_tolerance=1, max_controls_per_case=1, random_state=None, sex_label=[0, 1]):
    
    """
    Match cases and controls based on age and sex.

    :param df_cases: DataFrame containing case subjects.
    :param df_controls: DataFrame containing control subjects.
    :param age_tolerance: The age difference tolerance for matching.
    :param max_controls_per_case: Maximum number of controls to match per case.
    :param random_state: Random state for reproducibility.
    :sex_label: label for male and female sex
    :return: DataFrame with matched cases and controls.
    """

    matched_cases = []

    for sex in sex_label:
        case_subset = df_cases[(df_cases['sex'] == sex) & (df_cases['label'] == 1)]
        control_subset = df_controls[df_controls['sex'] == sex]

        temp = []

        for _, case_row in case_subset.iterrows():
            age = case_row['age']
            age_range = (age - age_tolerance, age + age_tolerance)

            matched_controls = control_subset[
                control_subset['age'].between(age_range[0], age_range[1])
            ]

            if len(matched_controls) > max_controls_per_case:
                matched_controls = matched_controls.sample(max_controls_per_case, random_state=random_state)

            temp.append(matched_controls)

            control_subset = control_subset[~control_subset['ID'].isin(matched_controls['ID'])]

        matched_cases.append(pd.concat([case_subset] + temp))

    return pd.concat(matched_cases).drop_duplicates(subset='ID').reset_index(drop=True)
