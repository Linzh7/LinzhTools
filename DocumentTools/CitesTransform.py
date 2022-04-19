import re


class Cite():
    author = 'Empty Author'
    title = 'Empty Title'
    transactions = 'Empty Transactions Name'
    press = 'Empty Press'
    year = None
    pages = None

    def MLA_init(self, text):
        ls = text.split('"')
        self.author = ls[0].strip()[:-1]
        self.title = ls[1].strip()
        ls = txt.split('"')[2].strip().split(".")
        self.transactions = ls[0].strip()
        self.year = re.findall(r'\d+', ls[1])[0]
        # self.author = re.findall(r'[a-zA-Z\u4e00-\u9fa5, ]+.', txt)[0]
        # self.title = re.findall(r'"+[a-zA-Z\u4e00-\u9fa5, \:\-]+."', txt)[0][1:-2]

    def GB_output(self):
        print(f'[Outout]\n{self.author}. {self.title}[C]. //{self.transactions}, {self.press}, {self.year}.')


txt = ''

a = Cite()
a.MLA_init(txt)
a.GB_output()
