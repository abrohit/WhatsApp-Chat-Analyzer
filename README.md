<h1 align="center">WhatsApp Chat Analyser</h1>
<p align="center">
  Analyzes Whatsapp groups to show some interesting facts!
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
* [Tech Stack](#tech-stack)
* [Behind the Project](#behind-the-project)
* [Screenshots](#screenshots)
* [Contact](#contact)


## About the Project

![preview](./Previews/preview.gif)

This web application analyzes your Whatsapp group chats and provides statistics of your Whatsapp group. You have to upload a text file of your Whatsapp group chats without media, which is processed by the web application and then generates bar graphs and pie charts. The group chats is instantly deleted. 

## Tech Stack
- Python
- Plotly
- Pandas
- Django
- HTML
- CSS / Bulma

## Behind the Project

The file ```MainPage/Main.py``` analyzes the Whatsapp group chats. The ```ExtractData()``` class extracts the data and outputs the extracted data in pandas dataframe. The ```StatGenerator()``` class analyzes the data and creates a bar graph or pie graph using plotly. The web application is made with Django Framework. 

## Screenshots
![pic1](./MainPage/static/main/1.png)

![pic2](./MainPage/static/main/2.png)

![pic3](./MainPage/static/main/3.png)

## Contact

Twitter : [abrohit05](https://twitter.com/abrohit05)

LinkedIn : [Rohit Manjunath](https://www.linkedin.com/in/rohitmanjunath/)

Website : [abrohit](https://abrohit.pythonanywhere.com/)

