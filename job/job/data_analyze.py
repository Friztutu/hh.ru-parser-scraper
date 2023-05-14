import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os


class Analyzer:

    def __init__(self, filename):
        self.df = pd.read_csv(f'csv_data/{filename}.csv', dtype={'salary': 'float64'})
        self.writer = Writer(filename)
        self.graph = Graphs(filename)

    def default_info(self):
        df_with_salary = self.df[self.df.salary != -1]
        df_with_experience = self.df[self.df.experience != -1]

        avg_salary = df_with_salary['salary'].mean()
        avg_experience = df_with_experience['experience'].mean()

        self.writer.write_title('Общая информация')
        self.writer.write_default_info(len(self.df), avg_salary, avg_experience)

        self.graph.draw_salary_graph(df_with_salary['salary'])

        df = self.df[(self.df.salary != -1) & (self.df.experience != -1)]
        self.graph.draw_experience_graph(df)
        self.graph.draw_salary_by_experience(df)

    def analyze_by_town(self):
        df = self.df[(self.df.salary != -1) & (self.df.experience != -1) & (self.df.town != 1)]

        title = 'Статистика по городам'
        table_title = 'Город'.ljust(40, ' ')\
                      + 'Вакансий'.ljust(40, ' ')\
                      + 'Cредняя з\п'.ljust(40,' ')\
                      + 'Средний требуемый опыт'.ljust(40, ' ')

        vacancy_by_town = df.groupby('town')['salary'].count()
        salary_by_town = df.groupby('town')['salary'].mean()
        avg_experience_by_town = df.groupby('town')['experience'].mean()

        self.writer.write_title(title)
        self.writer.write_table(table_title, df_table=(vacancy_by_town, salary_by_town, avg_experience_by_town))

        top_5 = salary_by_town.sort_values(ascending=False).head()

        self.graph.draw_top_town_by_salary(top_5)

    def analyze_by_company(self):
        df = self.df[(self.df.salary != -1) & (self.df.experience != -1) & (self.df.company != 1)]

        title = 'Статистика по компаниям'
        table_title = 'Компания'.ljust(40, ' ')\
                      + 'Вакансий'.ljust(40, ' ')\
                      + 'Cредняя з\п'.ljust(40,' ')\
                      + 'Средний требуемый опыт'.ljust(40, ' ')

        vacancy_by_company = df.groupby('company')['salary'].count()
        salary_by_company = df.groupby('company')['salary'].mean()
        avg_experience_by_company = df.groupby('company')['experience'].mean()

        self.writer.write_title(title)
        self.writer.write_table(
            table_title,
            df_table=(
                vacancy_by_company, salary_by_company, avg_experience_by_company
            )
        )

    def start(self):
        self.default_info()
        self.analyze_by_town()
        self.analyze_by_company()


class Writer:

    def __init__(self, filename: str) -> None:
        self.filename = filename

        if not os.path.exists(f'{filename}_analyze'):
            os.mkdir(f'{filename}_analyze')

        with open(f'{filename}_analyze/{self.filename}_analyze.txt', mode='w') as file:
            file.write('Заголовок'.center(200, '-'))
            file.write('\n\n\n')
            file.write(
                f'Отчет по запросу: {filename}, Время оформления: {datetime.today()}\n\n\n'
            )

    def write_title(self, title: str) -> None:
        with open(f'{self.filename}_analyze/{self.filename}_analyze.txt', mode='a') as file:
            file.write(title.center(200, '-'))
            file.write('\n\n\n')

    def write_default_info(self, len_df, avg_salary, avg_experience):
        with open(f'{self.filename}_analyze/{self.filename}_analyze.txt', mode='a') as file:
            file.write(f'Количество вакансий в таблице: {len_df}\n')
            file.write(f'Средняя зарплата по вакансиям: {avg_salary:.3f}\n')
            file.write(f'Средний опыт: {avg_experience:.3f}\n\n\n')

    def write_table(self, table_title, df_table, extra_info=tuple()):
        df1, df2, df3 = df_table
        with open(f'{self.filename}_analyze/{self.filename}_analyze.txt', mode='a') as file:
            for line in extra_info:
                file.write(line + '\n')
            file.write(table_title + '\n\n')
            for index, line1, line2, line3 in zip(df1.index, df1, df2, df3):
                file.write(
                    f'{index.ljust(40, " ")}' +
                    f'{float(line1):.1f}'.ljust(40, " ") +
                    f'{float(line2):.3f}'.ljust(40, " ") +
                    f'{float(line3):.3f}'.ljust(40, " ") +
                    '\n'
                )

            file.write('\n\n')


class Graphs:

    def __init__(self, filename):
        if not os.path.exists(f'{filename}_analyze/graphs'):
            os.mkdir(f'{filename}_analyze/graphs')

        self.filename = filename

    def draw_salary_graph(self, df):
        df.plot(kind='hist', title=self.filename)
        plt.savefig(f'{self.filename}_analyze/graphs/График_распределения_зарплат.png')

    def draw_top_town_by_salary(self, df):
        df.plot(x='town', y='salary', kind='bar', rot=5, fontsize=10, title=self.filename)
        plt.savefig(f'{self.filename}_analyze/graphs/лучшие_5_городов_по_зарплате.png')

    def draw_experience_graph(self, df):
        df.plot(x='salary', y='experience', title=self.filename, kind='hist')
        plt.savefig(f'{self.filename}_analyze/graphs/График_распределения_опыта.png')

    def draw_salary_by_experience(self, df):
        df.plot(x='salary', y='experience', title=self.filename, kind='scatter')
        plt.savefig(f'{self.filename}_analyze/graphs/График_опыта_к_зарплате.png')


def main(filename):
    a = Analyzer(filename)
    a.start()


if __name__ == '__main__':
    main('javascript')
