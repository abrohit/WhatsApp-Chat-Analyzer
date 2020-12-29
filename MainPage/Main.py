import re
import pandas as pd
import emoji
from collections import Counter
import datetime

import plotly
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

class ExtractData:

    def __init__(self, file_path):
        self.path = file_path
        self.data = []

    def load_file(self):
        file = open(self.path, 'r', encoding='utf-8')
        return file

    def Is_NewEntry(self, line: str) -> bool:
        date_time = '([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        test = re.match(date_time, line)
        if test is None:
            return False
        else:
            return True
    def Seperate_Data(self, line: str) -> tuple:

        data = line.split(' - ')
        date, time = data[0].split(', ')
        authMsg = data[1].split(':')

        if len(authMsg) > 1:
            author = authMsg[0]
            message = ' '.join(authMsg[1:])
            return (date, time, author, message)
        else:
            return None

    def Emojis_Check(self, message: str)-> list:

        final = []
        for char in message:
            if char in emoji.UNICODE_EMOJI:
                final.append(char)

        if len(final) == 0:
            return 0
        else:
            return final

    def Main_Process(self):

        full_message = []
        date=''
        time=''
        author=''

        file = self.load_file()
        file.readline() #skips the first line

        while True:
            line = file.readline()
            if not line:
                break #Stops the while loop at the end of file

            if self.Is_NewEntry(line):

                if len(full_message)>0:
                    temp = ' '.join(full_message)
                    modified_replaced = temp.replace('\n', ' ')
                    self.data.append([date, time, author, modified_replaced])

                full_message.clear()
                received = self.Seperate_Data(line)
                if received is not None:
                    date, time, author, message = received
                    full_message.append(message)
            else:
                full_message.append(line)

        file.close()

    def Change_Dataframe(self) -> object:

        df = pd.DataFrame(self.data, columns=['Date', 'Time', 'Author', 'Message'])
        df['Date'] = pd.to_datetime(df.Date)
        df['Emojis'] = df.Message.apply(self.Emojis_Check)
        df['Emoji_num'] = df.Emojis.str.len()

        return df

class StatGenerator:

    def __init__(self, dataframe):
        self.df = dataframe

    def ActivityOverDates(self):
        result = self.df.groupby('Date').sum()
        result = result.rename(columns={'Emoji_num': 'Number of Messages'})

        figure = px.line(result, x=result.index, y=result['Number of Messages'].values, labels={'y':'Number of Messages'})
        graph = plot(figure, output_type='div')
        return graph

    def MostUsedWords(self, number: int):
        result = Counter(" ".join(self.df['Message']).split()).most_common(number)
        obj = pd.DataFrame(result, columns =['Word', 'Frequency'])

        labels = obj['Word'].values
        values = obj['Frequency'].values
        figure = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        graph = plot(figure, output_type='div')
        return graph

    def MostActive(self, number: int):
        result = pd.DataFrame(self.df.Author.value_counts())
        result = result.rename(columns={'Author': 'Message Count'})

        if result.shape[0] > number:
            result = result[:number]

        figure = px.bar(result, x=result.index, y=result['Message Count'].values, labels={'y':'Number of Messages'})
        graph = plot(figure, output_type='div')
        return graph


    def NightOwls(self, number: int):
        temp = pd.to_datetime(self.df.Time)
        night_mask = ((temp.dt.hour >= 3) & (temp.dt.hour <=23))#Between 11pm and 3am
        result = pd.DataFrame(self.df[night_mask].Author.value_counts())
        result = result.rename(columns={'Author':'Message Count'})

        if result.shape[0] > number:
            result = result[:number]
        
        figure = px.bar(result, x=result.index, y=result['Message Count'].values, labels={'y':'Number of Messages'})
        graph = plot(figure, output_type='div')
        return graph
            
    def EarlyBirds(self, number: int):
        temp = pd.to_datetime(self.df.Time)
        morning_mask = (temp.dt.hour >= 6) & (temp.dt.hour <=9)#between 6am and 9am
        result = pd.DataFrame(self.df[morning_mask].Author.value_counts())
        result = result.rename(columns={'Author':'Message Count'})

        if result.shape[0] > number:
            result = result[:number]
        
        figure = px.bar(result, x=result.index, y=result['Message Count'].values, labels={'y':'Number of Messages'})
        graph = plot(figure, output_type='div')
        return graph

    def EmojiSpammers(self, number: int):
        result = pd.DataFrame(self.df.groupby('Author').Emoji_num.sum().sort_values(ascending=False))

        if result.shape[0] > number:
            result = result[:number]
        
        figure = px.bar(result, x=result.index, y=result['Emoji_num'].values, labels={'y':'Number of Emojis'})
        graph = plot(figure, output_type='div')
        return graph

    def TotalEmojis(self):
        return len([i for j in self.df.Emojis[self.df.Emojis!=0] for i in j])

    def UniqueEmojis(self):
        return len(set([i for j in self.df.Emojis[self.df.Emojis!=0] for i in j]))

    def FrequentEmojis(self, number: int):
        emojiList = [i for j in self.df.Emojis[self.df.Emojis!=0] for i in j]
        emoji_dict = dict(Counter(emojiList))
        emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
        result = pd.DataFrame(emoji_dict, columns=['Emoji', 'Frequency'])

        if result.shape[0] > number:
            result = result[:number]
        
        labels = result.Emoji.values
        values = result.Frequency.values
        figure = go.Figure(data=[go.Pie(labels=labels, values=values)])
        graph = plot(figure, output_type='div')
        return graph

def main():

    file_store = 'D:\Desktop\Programming\Whatsapp_Analyzer\Test.txt'

    yes = ExtractData(file_store)
    yes.Main_Process()
    df = yes.Change_Dataframe()

    stat = StatGenerator(df)
    print(stat.EmojiSpammers(5))

#main()
