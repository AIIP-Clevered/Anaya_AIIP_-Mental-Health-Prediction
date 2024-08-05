# -*- coding: utf-8 -*-
"""Final Project - Anya

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K7LdKq68N38EFzt4-RMzIFXiDbguXL8j
"""

import pandas as pd

data = pd.read_csv('/content/Student_Mental_health (1).csv')

print(data.head())
print(data.shape)
print(data.info())
print(data.describe())

data.dropna(inplace=True)
data.columns = data.columns.str.strip()
print (data.columns)
data["Age"] = data["Age"].astype(int)
data["Do you have Depression?"] = data["Do you have Depression?"].apply(lambda x: x.strip().lower())
data["Do you have Anxiety?"] = data["Do you have Anxiety?"].apply(lambda x: x.strip().lower())
data["Do you have Panic attack?"] = data["Do you have Panic attack?"].apply(lambda x: x.strip().lower())
data["Did you seek any specialist for a treatment?"] = data["Did you seek any specialist for a treatment?"].apply(lambda x: x.strip().lower())
data["Choose your gender"] = data["Choose your gender"].apply(lambda x: x.strip().lower())
data["What is your course?"] = data["What is your course?"].apply(lambda x: x.strip().lower()[:3])
data["Your current year of Study"] = data["Your current year of Study"].apply(lambda x: int(x.strip().lower()[5]))
print(type(data["Age"]))
data["What is your CGPA?"] = data["What is your CGPA?"].apply(lambda x: (float(x.strip().split()[0])+float(x.strip().split()[2]))/2)
data["Marital status"] = data["Marital status"].apply(lambda x: x.strip().lower())
data.drop(columns=["Timestamp"], inplace=True)
print (data)
uni = list(data['What is your course?'].unique())
print(uni)
unid = {}
for i in uni:
  unid[i] = uni.index(i)
print(unid)
data.replace({"male": 0, "female": 1}, inplace=True)
data.replace(unid, inplace=True)
data.replace({"yes": 0, "no": 1}, inplace=True)

!pip install customtkinter

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np

A = data.drop(columns=['Do you have Depression?', 'Do you have Anxiety?', 'Do you have Panic attack?'], axis = 1)
B = data[['Do you have Depression?', 'Do you have Anxiety?', 'Do you have Panic attack?']]
a_train, a_test, b_train, b_test = train_test_split(A,B, test_size = 0.2, random_state = 42)
dtree = DecisionTreeClassifier()
dtree = dtree.fit(a_train, b_train)
predict = dtree.predict(a_test)
A=A.to_numpy()
B=B.to_numpy()
fig, axes = plt.subplots(figsize = (15,6),dpi=400)
tree.plot_tree(dtree,feature_names = A,class_names=B,filled=True)
plt.show()

!pip install ipywidgets

import ipywidgets as widgets
from IPython.display import display, clear_output
from gtts import gTTS
from IPython.display import Audio
age_entry = widgets.IntText(description="Age:")
gnd_entry = widgets.Text(description="Gender:")
crs_entry = widgets.Text(description="Course:")
yos_entry = widgets.IntText(description="year of study:")
gpa_entry = widgets.FloatText(description="GPA:")
mstat_entry = widgets.Text(description="Marital Status (y/n):")
spc_entry = widgets.Text(description="Specialist Treatment (y/n):")
# display(age_entry, gnd_entry, crs_entry, yos_entry, gpa_entry, mstat_entry, spc_entry)

def values(button):
  age = age_entry.value
  gnd = {"m": 0, "f": 1}.get(gnd_entry.value.strip().lower()[:3], -1) # Handle invalid gender input
  crs = unid.get(crs_entry.value.strip().lower()[:3], -1) # Handle invalid course input
  yos = yos_entry.value
  gpa = gpa_entry.value
  mstat = {"y":0,"n":1}.get(mstat_entry.value.strip().lower()[:3], -1) # Handle invalid marital status input
  spc = {"y":0,"n":1}.get(spc_entry.value.strip().lower()[:3], -1) # Handle invalid specialist treatment input
  if -1 in [gnd, crs, mstat, spc]:
    clear_output()
    display(title_label, age_entry, gnd_entry, crs_entry, yos_entry, gpa_entry, mstat_entry, spc_entry, button,
    widgets.HTML(value="<h3>Error: Please check your inputs for Gender, Course, Marital Status, and Specialist Treatment. Please check the dataset. </h3>"))
    return
  Prediction_result = ('Predict disorder: ', dtree.predict([[age, gnd, crs, yos, gpa, mstat, spc]]))
  ans = "Diagnosis\n"
  if Prediction_result[1][0][0] == 0:
    ans += "Depression Prediction = positive"
  elif Prediction_result[1][0][0] == 1:
    ans += "Depression Prediction = negative"
  if Prediction_result[1][0][1] == 0:
    ans += "\nAnxiety Prediction = positive"
  elif Prediction_result[1][0][1] == 1:
    ans += "\nAnxiety Prediction = negative"
  if Prediction_result[1][0][2] == 0:
    ans += "\nPanic Attack Prediction = positive"
    text = gTTS(ans, lang='en')
  elif Prediction_result[1][0][2] == 1:
    ans += "\nPanic Attack Prediction = negative"
    text = gTTS(ans, lang='en')
  clear_output()
  display(title_label, age_entry, gnd_entry, crs_entry, yos_entry, gpa_entry, mstat_entry, spc_entry, button, widgets.HTML(value=f"<h3>{ans}</h3>"))

button = widgets.Button(description="Predict Disorder")
button.on_click(values)
title_label = widgets.HTML(value="<h1>Mental Health Prediction App</h1>")
display(title_label, age_entry, gnd_entry, crs_entry, yos_entry, gpa_entry, mstat_entry, spc_entry, button)