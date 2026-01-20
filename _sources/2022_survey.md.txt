---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.18.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# 2022 Survey data analysis


## 1. Extract and read data

We are expecting a zip file containing all files related to the survey to be exported from the survey platform (e.g. Typeform). In that zipfile, there should be a `.csv` file containing the survey responses data. Make sure to only use data with no [personally identifiable information](https://en.wikipedia.org/wiki/Personal_data).

```python
import zipfile
import pathlib
import pandas as pd
import numpy as np

in_path = "/home/melissa/projects/napari-survey-data/no-pii"
out_path = "_data"

past_surveys = {
    "2022": "napari-survey-2022-partial-export.csv",
}

data = []
for year, csv_filename in past_surveys.items():
    zip_filename = f"{year}.zip"
    with zipfile.ZipFile(pathlib.Path(in_path, zip_filename), 'r') as zfile:
        zfile.extract(csv_filename, out_path)

    data.append(pd.read_csv(pathlib.Path(out_path, csv_filename)))
```

```python
data
```

## 2. Prepare 2022 data

```python
data_2022 = data[-1]
# Clean up unnecessary columns
#data_2022.drop(data_2022.columns[[0, 1]], axis=1, inplace=True)
#data_2022.drop(list(data_2022)[95:102], axis=1, inplace=True)
```

```python
data_2022
```

### Filter multiple choice data


Multiple choice questions are organized as multiple columns corresponding to each of the options available as answers.

For each of the answer columns, the contents are either NaN or the selected choice (i.e. same as the column name).

```python
data_2023[data_2023.columns[14]]
```

```python
questions_map = {
    "Which kind of organization(s) are you associated with?": (0,5),
    "Which of the following describe your current role?": (5, 13),
    #"Which domains / industries do you work in?": (13,),
    "Which of these best describes your Python programming experience level?": (14,),
    "Approximately how long have you used napari?": (15, 21),
    #"You indicated that you haven't used napari, or no longer use it. Please share why.": (21,),
    "How have you used napari?": (22, 29),
    "Which types of images have you worked with during the past year, or plan to work with in upcoming projects?": (29, 40),
    # "In the context of image visualization, annotation, and analysis, what tools do you use other than napari, and why?": (40,),  # Free form question
    # Indicate the degree to which you agree or disagree with the following statements in the context of *your* napari usage and/or contributions.
    # Strongly disagree, Somewhat disagree, Neutral, Somewhat agree, Strongly agree, Unfamiliar/not applicable
    "There are adequate napari tutorials": (41,),
    "There is adequate napari API documentation": (42,),
    "The napari community is welcoming and inclusive": (43,),
    "It is easy to contribute code to the napari project": (44,),
    "It is easy to contribute documentation to the napari project": (45,),
    "It is easy to develop plugins for napari": (46,),
    # "Feel free to elaborate here on your ratings in the previous question.": (47,),
    # Rate napari viewer on the following aspects.
    # Poor, Fair, Good, Very Good, Excellent, NA/Not sure
    "Ease of installation": (48,),
    "Conflicts due to software dependencies": (49,),
    "Start time": (50,),
    "Performance viewing data": (51,),
    "Existing feature set excluding plugins": (52,),
    "Pace of new feature development": (53,),
    "Introduction of breaking API changes": (54,),
    # "Feel free to elaborate here on your ratings in the previous question.": (55,),
    # Indicate the ways in which you have engaged in the [napari community](https://napari.org/stable/community/index.html).
    # Unfamiliar, Aware, Reader, Participant
    "GitHub issues/discussions": (56,),
    "GitHub code/doc. submissions/NAPs/reviews": (57,),
    "Image.sc forum": (58,),
    "napari Zulip chat": (59,),
    "Mastodon": (60,),
    "X (Twitter)": (61,),
    "Conferences": (62,),
    "Community meetings": (63,),
    "How satisfied or dissatisfied are you with your *experience using napari with plugins*?": (64,),
    # "Feel free to elaborate here on your choice in the previous question.": (65,),  # Free form question
    # Which sources do you use to find napari plugins?
    "I ask a colleague": (66,),
    "GitHub": (67,),
    "Image.sc forum": (68,),
    "napari hub": (69,),
    "napari plugin installation window": (70,),
    "Mastodon": (71,),
    "X (Twitter)": (72,),
    "napari Zulip chat": (73,),
    "Web search": (74,),
    "Other": (75,),
    "How often are you able to find a napari plugin that meets your needs?": (76,),
    # The napari team is considering opt-in, anonymous data gathering to better understand usage of napari, along with a public dashboard of aggregated data. The corresponding _napari Advancement Proposal_ on telemetry, [NAP-8](https://napari.org/dev/naps/8-telemetry.html) is open to discussion on Zulip chat, Image.sc forum, and GitHub, and you are welcome to participate. In the next two questions, we aim to better understand where the community stands, including users who may not be active in the discussion avenues. The proposal may or may not move forward depending on community feedback
    # The level of data collection is proposed to be adjustable:\n• Basic: includes software and hardware configuration information linked to an identifier updated weekly to prevent tracking any individual user.\n• Middle: basic level + names and versions of public plugins installed in stable versions of napari\n• Full: middle level + usage of plugin features/functions and corresponding [contributions](https://napari.org/stable/plugins/contributions.html), and type and size of image data
    "If a future version of napari were to introduce opt-in, anonymous data gathering, what would be your preferred course of action?": (77,),
    "Other": (78,),
    "What questions or concerns might you have about the introduction of opt-in, anonymous data gathering in a future version of napari (along with a public dashboard of the aggregated data on napari.org)?": (79,),
    # Select up to three areas of improvement from the following list that would be most valuable to you. We will use this information to help us prioritize the napari roadmap.",
    "Access napari in a Jupyter notebook/JupyterLab/other web-based UI": (80,),
    "View image data without the whole UI, and related API improvements to improve consistency and allow reuse of viewer components": (81,),
    "Better tools to annotate (e.g. manually segment) 3D data": (82,),
    "Multiple canvases, such as for orthogonal views, synced views, or simultaneous 2D/3D rendering": (83,),
    "Improved access to features from the GUI and better documentation": (84,),
    "Improved interactivity and performance when visualizing data": (85,),
    "Layer improvements (slicing performance, layer groups, consistency across layer types)": (86,),
    "Improved opening and saving of data": (87,),
    "Improved sharing of data between the viewer and plugins, or between different plugins": (88,),
    "Bug fixes": (89,),
    "Other": (90,),
    "Overall, how satisfied or dissatisfied are you with napari?": (91,),
    "Feel free to elaborate here on your rating in the previous question.": (92,),
    "Please share any additional thoughts, feedback, or suggestions to improve napari or napari hub.": (93,),
}
```

For multiple choice questions, answers span multiple columns, and we must combine them into a single column with the answers.

For single-option questions, answers are present in a single column.

```python
def process_columns(df_orig, cols, question):
    df = df_orig.replace(pd.NA, '')
    processed = df[df.columns[cols[0]]]
    if len(cols) == 1:
        return processed
    else:
        for col in df.columns[cols[1:]]:
            processed = np.where(df[col] != '', processed + ', ' + df[col], processed)
    return processed

def gencols(cols):
    if len(cols)>1:
        return range(cols[0], cols[1])
    return range(cols[0], cols[0]+1)
```

```python
new_df = pd.DataFrame()
for question, cols in questions_map.items():
    new_df[question] = process_columns(data_2023, gencols(cols), question)
```

```python
new_df
```

## Plots

```python
import matplotlib.pyplot as plt
```

```python
for question, cols in questions_map.items():
    pcols = gencols(cols)
    fig, ax = plt.subplots()
    ax.set_title(question)
    if len(pcols) == 1:
        col = pcols[0]
        col_data = data_2023[data_2023.columns[col]]
        items = col_data.dropna().unique()
        y = []
        yticks = []
        for item in items:
            y.append(col_data[col_data == item].count())
            yticks.append(item)
        ax.barh(range(len(items)), y, edgecolor="white", linewidth=0.5, tick_label=yticks)
    else:
        y = []
        yticks = []
        for col in pcols:
            y.append(data_2023[data_2023.columns[col]].count())
            yticks.append(data_2023.columns[col])
        ax.barh(pcols, y, edgecolor="white", linewidth=0.5, tick_label=yticks)
```

---

```python

```
