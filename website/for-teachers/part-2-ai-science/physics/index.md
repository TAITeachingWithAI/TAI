---
title: Physics
order: 1
---

# Physics

Teaching material for the physics lesson of Part 2: AI & Science.

## Lesson material

- [:material-file-pdf-box: Physics lesson: student version](physics_forstudents.pdf)
- [:material-file-pdf-box: Physics lesson: teacher version](physics_teachertrue.pdf)

!!! info "Which version do I need?"
    The **student version** is the worksheet you hand out. The **teacher version**
    is the same lesson including the worked answers, for your own preparation.

!!! tip "Sharing the material with your students"
    The worksheet refers to the files below **by name**, so you can download them
    and share them with your students in any way you like (for example in your
    school's learning platform). Students also need the planet file of their
    group's exoplanet from the [Exoplanet Files](../exoplanet-files/index.md).

## Emmy's prompt

**Emmy** is an AI research mentor. She is not an app but a prompt: students copy
the text of this file and paste it as the first message in a new chat with any AI
chatbot (for example ChatGPT, Gemini, Claude or Copilot). Emmy then guides them
through their own investigation with questions, and asks them to reflect on how
science works.

- [:material-file-document-outline: Emmy_prompt_exoplanet_lesson.txt](Emmy_prompt_exoplanet_lesson.txt){ target="_blank" }

## Star image for the experiment

Students display this image on their phone as the star. During the experiment
they move the "planet" in front of it while the light sensor records the dip in
brightness. Each student downloads it to their own phone.

- [:material-image-search: Open the star image in your browser](Star_image_for_phone.png){ target="_blank" }
- [:material-download: Download the star image](Star_image_for_phone.png){ download="Star_image_for_phone.png" }

<p style="text-align:center;">
  <img src="Star_image_for_phone.png" alt="Star image for the transit experiment" width="180"
       style="background:#000; border-radius:8px; padding:8px;">
</p>

## Data-analysis notebook

Students use this notebook in Google Colab to load and analyse their light-sensor
data: it draws the light curve, computes the transit depth, and lets students test
which relationship between transit depth and planet size fits their data. It
accepts exports from phyphox (Android), Physics Toolbox, the Arduino Science
Journal, or any plain CSV.

Click **Open in Colab** to run it in the browser without installing anything, or
download the file to share it yourself.

| Run it | Download |
| --- | --- |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TAITeachingWithAI/TAI/blob/main/website/for-teachers/part-2-ai-science/physics/Exoplanet_transit_analysis_notebook.ipynb) | [:material-notebook: Exoplanet_transit_analysis_notebook.ipynb](Exoplanet_transit_analysis_notebook.ipynb) |
