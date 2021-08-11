from connection_pool import get_connection
import matplotlib.pyplot as plt
import numpy as np


MENU_PROMPT = """
---- Menu ----

1. Show COVID-19 Deaths per State (01/01/2020 - 06/26/2021) chart 
2. Influenza:Pneumonia Deaths per State (2018-2019) chart
3. Show COVID-19 Deaths per State (01/01/2020 - 06/26/2021) and Influenza Deaths per State (2018-2019) chart
4. Exit

Enter your choice: """


SELECT_COVID19_DEATHS_PER_STATE = """SELECT usa_state, covid19_deaths 
FROM covid19 
ORDER BY usa_state;"""


SELECT_FLU_DEATHS_PER_STATE = """SELECT usa_state, SUM(deaths) 
FROM influenza 
GROUP BY usa_state
ORDER BY usa_state;"""


SELECT_COVID19_AND_FLU_DEATHS_PER_STATE = """SELECT covid19.usa_state, covid19.covid19_deaths,
(SELECT SUM(influenza.deaths) FROM influenza
WHERE covid19.usa_state = influenza.usa_state
GROUP BY influenza.usa_state) AS influenza_deaths
FROM covid19
ORDER BY usa_state;"""


def covid19deaths():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_COVID19_DEATHS_PER_STATE)
            return cursor.fetchall()


def influenzadeaths():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_FLU_DEATHS_PER_STATE)
            return cursor.fetchall()


def covid19fludeaths():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_COVID19_AND_FLU_DEATHS_PER_STATE)
            return cursor.fetchall()


def create_chart_covid19():
    covid19_deaths = covid19deaths()
    figure = plt.figure(figsize=(16, 12))
    axes = figure.add_subplot()
    figure.subplots_adjust(bottom=0.07, top=0.95, left=0.07, right=0.95)
    axes.set_title("COVID-19 Deaths per State (01/01/2020 - 06/26/2021)")
    axes.set_ylabel("Number of Deaths")

    axes.bar(
        range(len(covid19_deaths)),
        [covid19_death[1] for covid19_death in covid19_deaths],
        tick_label=[covid19_death[0] for covid19_death in covid19_deaths],
        facecolor="#4169E1",
        edgecolor="#000000"
    )
    plt.yticks(np.arange(0, (max(covid19_deaths, key=lambda x: x[1])[1]), 1000))


def create_chart_flu():
    flu_deaths = influenzadeaths()
    figure = plt.figure(figsize=(15, 11))
    axes = figure.add_subplot()
    figure.subplots_adjust(bottom=0.07, top=0.95, left=0.07, right=0.95)
    axes.set_title("Influenza:Pneumonia Deaths per State (2018-2019)")
    axes.set_ylabel("Number of Deaths")

    axes.bar(
        range(len(flu_deaths)),
        [flu_death[1] for flu_death in flu_deaths],
        tick_label=[flu_death[0] for flu_death in flu_deaths],
        facecolor="#FF8C00",
        edgecolor="#000000"
    )
    plt.yticks(np.arange(0, (max(flu_deaths, key=lambda x: x[1])[1]), 500))


def create_chart_covid19_and_flu():
    covid19_flu_deaths = covid19fludeaths()
    figure = plt.figure(figsize=(21, 12.5))
    axes = figure.add_subplot()
    figure.subplots_adjust(bottom=0.07, top=0.95, left=0.05, right=0.98)
    axes.set_title("COVID-19 (01/01/2020 - 06/26/2021) and Influenza:Pneumonia (2018-2019) Deaths per State (USA)")
    axes.set_ylabel("Number of Deaths")

    x_axis = np.arange(len(covid19_flu_deaths))
    bar_width = 0.4

    covid19_plot = axes.bar(
        x_axis,
        [covid19_flu_death[1] for covid19_flu_death in covid19_flu_deaths],
        width=bar_width,
        facecolor="#4169E1",
        edgecolor="#000000"
    )

    influenza_plot = axes.bar(
        x_axis + bar_width,
        [covid19_flu_death[2] for covid19_flu_death in covid19_flu_deaths],
        width=bar_width,
        facecolor="#FF8C00",
        edgecolor="#000000"
    )

    axes.legend((covid19_plot, influenza_plot), ("COVID-19 Deaths", "Influenza:Pneumonia Deaths"))
    plt.xticks(x_axis + bar_width/2, [covid19_flu_death[0] for covid19_flu_death in covid19_flu_deaths])
    plt.yticks(np.arange(0, (max(covid19_flu_deaths, key=lambda x: x[1])[1]), 1000))


MENU_OPTIONS = {
    "1": create_chart_covid19,
    "2": create_chart_flu,
    "3": create_chart_covid19_and_flu
}


def menu():
    while (selection := input(MENU_PROMPT)) != "4":
        try:
            MENU_OPTIONS[selection]()
            plt.show()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
