# Intelligent-interactive-systems
submitters - Omri Savir, Marina Kletselman, Tomer Hod

In order to run the system, you should open jupyter/colab notebook and write the following code:

! pip install streamlit -q

!wget -q -O - ipv4.icanhazip.com

! streamlit run site.py & npx localtunnel --port 8501

Link to colab file with this code:
https://colab.research.google.com/drive/10MQHM3gMuc7owdMq3EyDZONuDtOYL3eg?usp=sharing

Before running, the files site.py and apartments.csv, that you can download from this project, should be attached to the notebook locally.
Note that they should be attached with the exact same names.

After running you will receive a password (the password contains 4 numbers separated by ".") and a url address.
Go to the url address you received, enter the password you received and click on the "click to submit" button.
This will run the site.
The commands in the jupyter/colab notebook must remain running as long as you use the site.
