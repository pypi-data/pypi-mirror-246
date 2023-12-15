# election_text_analysis

Note to Dr. Brambor and the teaching assistants: thank you for everything in this class! Based on Dr. Brambor's feedback, I reduced the scope of my project based on the proposal. I removed the lemmatization step as well as the n-grams steps. I also just focused on data from 2008-2020. I also focused more on the data steps we learned in this class rather than the analysis. I was able to use the timeseries file directly from ANES that had almost all questions normalized, but didn't contain the open-ended responses. For this project, I joined the open-ended responses from 2008, 2012, 2016, and 2020 with the timeseries data. I then built some functions to calculate the frequency of words across a set of responses.

## Package on PyPI

https://pypi.org/project/election_text_analysis/

## Docs

https://election-text-analysis.readthedocs.io/en/latest/

## Overview

Functions to load and analyzes open-ended data from the ANES election perception surveys conducted every 4 years.

ANES (American National Election Studies) conducts a large-scale survey every four years, coinciding with US Presidential elections. The survey focuses on voter preferences and election-related behavior, as well as questions on public opinion and attitudes. These studies are conducted as pre-election and post-election interviews. 

Some of the most interesting questions asked in the ANES survey are open-ended text responses. These include questions asking voters what they like (and dislike) about each party's candidate. For some years of data, these questions were asked for other positions as well (ie House and Senate candidates). 

These open-ended responses have the potential for fascinating analysis on how voter preferences and reasoning (in their own words) have changed over time. This module aims to make it easier to analyze those open-ended responses.

## Installation

```bash
$ pip install election_text_analysis
```

## Usage

    >>> from election_text_analysis import download_data, read_data, analyze

    >>> # Downloads all data necessary to analyze open-ends from 2008-2020
    >>> download_data.download_all()

    # Loads a dataframe of data over time, with open-ends from 2008-2020
    >>> df = read_data.read_all_data()


## Dataset

The full codebook for all columns can be found at https://electionstudies.org/anes_timeseries_cdf_codebook_var_20220916/

The "Year" variable is stored in column 'VCF0004'. For example, here is a count of rows of data for every year since 1984 (the first year we have open-ended data)

    >>> greater_than_1984 = df[df['VCF0004'] >= 1984]
    >>> greater_than_1984['VCF0004'].value_counts().sort_index()
    VCF0004
    1984    2257
    1986    2176
    1988    2040
    1990    1980
    1992    2485
    1994    1795
    1996    1714
    1998    1281
    2000    1807
    2002    1511
    2004    1212
    2008    2322
    2012    5914
    2016    4270
    2020    8280
    Name: count, dtype: int64

There are 8 open-ended columns: 
    
    open_ended_columns = ['Like About Democratic Candidate', 'Dislike About Democratic Candidate', 'Like About Republican Candidate', 'Dislike About Republican Candidate', 'Like About Democratic Party', 'Dislike About Democratic Party', 'Like About Republican Party', 'Dislike About Republican Party']

What people dislike about the Democratic Candidate vs the Republican Candidate in 2020:

    dem_dislike_2020   = df[df['VCF0004'] == 2020]['Dislike About Democratic Candidate']
    repub_dislike_2020 = df[df['VCF0004'] == 2020]['Dislike About Republican Candidate']
    analyze.summarize_word_frequency_differences(dem_dislike_2020, repub_dislike_2020, group_1_label="Dem 2020 dislikes", group_2_label="Repub 2020 dislikes")

    These words occurred more often in Dem 2020 dislikes:
            word  Dem 2020 dislikes freq  Repub 2020 dislikes freq
    0        age                7.729841                  0.219912
    1      biden                6.240370                  0.619752
    2        old                5.906523                  0.479808
    3      years                7.498716                  2.219112
    4       left                5.392912                  0.239904
    5   abortion                5.110426                  0.359856
    6      party                5.264510                  0.799680
    7     mental                4.571135                  0.419832
    8      taxes                4.725218                  0.839664
    9  socialist                3.775039                  0.019992
    
    
    These words occurred more often in Repub 2020 dislikes:
             word  Dem 2020 dislikes freq  Repub 2020 dislikes freq
    0      racist                1.129944                 11.735306
    1      people                5.136107                 13.114754
    2     country                7.524397                 13.954418
    3        lies                0.873138                  7.057177
    4        liar                1.206985                  7.277089
    5        lack                1.438110                  7.297081
    6  everything                2.670776                  8.256697
    7       covid                0.667694                  6.117553
    8    pandemic                0.308166                  5.317873
    9        self                0.256805                  3.118752


What people dislike about the Democratic Candidate in 2020 vs 2016

    dem_dislike_2016   = df[df['VCF0004'] == 2016]['Dislike About Democratic Candidate']
    analyze.summarize_word_frequency_differences(dem_dislike_2020, dem_dislike_2016, group_1_label="2020 Dem dislikes", group_2_label="2016 Dem dislikes")

    These words occurred more often in 2020 Dem dislikes:
            word  2020 Dem dislikes freq  2016 Dem dislikes freq
    0        age                7.729841                0.269750
    1      years                7.498716                1.078998
    2      biden                6.240370                0.000000
    3    country                7.524397                1.425819
    4  president                7.832563                1.888247
    5        old                5.906523                0.192678
    6       left                5.392912                0.346821
    7      party                5.264510                0.385356
    8     mental                4.571135                0.000000
    9      taxes                4.725218                0.385356
    
    
    These words occurred more often in 2016 Dem dislikes:
                word  2020 Dem dislikes freq  2016 Dem dislikes freq
    0           liar                1.206985               10.481696
    1           lies                0.873138                6.589595
    2         emails                0.051361                5.086705
    3          trust                1.386749                6.319846
    4          email                0.000000                4.393064
    5      dishonest                0.487930                4.662813
    6     dishonesty                0.128403                3.159923
    7  untrustworthy                0.205444                2.967245
    8        scandal                0.051361                2.543353
    9        clinton                0.359527                2.658960

What people dislike about the Republican Candidate in 2020 vs 2016

    repub_dislike_2016 = df[df['VCF0004'] == 2016]['Dislike About Republican Candidate']
    analyze.summarize_word_frequency_differences(repub_dislike_2020, repub_dislike_2016, group_1_label="2020 Repub dislikes", group_2_label="2016 Repub dislikes")
    
    These words occurred more often in 2020 Repub dislikes:
            word  2020 Repub dislikes freq  2016 Repub dislikes freq
    0    country                 13.954418                  2.522460
    1     people                 13.114754                  5.563234
    2      covid                  6.117553                  0.000000
    3  president                  9.496202                  3.420871
    4      trump                  7.117153                  1.105736
    5       lies                  7.057177                  1.243953
    6   pandemic                  5.317873                  0.000000
    7       liar                  7.277089                  2.073255
    8   american                  4.258297                  0.621977
    9     office                  4.258297                  0.691085
    
    
    These words occurred more often in 2016 Repub dislikes:
               word  2020 Repub dislikes freq  2016 Repub dislikes freq
    0    experience                  0.599760                  5.977885
    1         mouth                  1.939224                  3.489979
    2         views                  1.379448                  2.660677
    3         think                  4.938025                  6.081548
    4     political                  1.559376                  2.522460
    5    temperment                  0.039984                  0.967519
    6  inexperience                  0.059976                  0.932965
    7         women                  3.618553                  4.457498
    8         bigot                  0.899640                  1.727713
    9          know                  1.459416                  2.246026

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`election_text_analysis` was created by Nikhila Anand. It is licensed under the terms of the MIT license.

## Credits

`election_text_analysis` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
