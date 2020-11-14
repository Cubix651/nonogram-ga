import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_best(values, category):
    value = values[values['category'] == category]['best'].values
    if len(value) == 0:
        return None
    return value[0]

def categories_key(c):
    if c == 'butterfly':
        return 999, 999
    (a, b) = map(int, c.split('x'))
    return a, b

def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

def show_chart(df, categories, annotate):
    competitors = df[df['category'].isin(categories)]['competitor'].unique()

    bar_width = 1.0 / (len(competitors)+1)
    global_x = np.arange(len(categories))

    plt.figure()
    for index, competitor in enumerate(competitors):
        values = df[df['competitor'] == competitor][['category', 'best']]
        all_values = [extract_best(values, category) for category in categories]
        selected_x = np.array([x for value, x in zip(all_values, global_x) if value != None])
        selected_y = np.array([y for y in all_values if y != None])
        bars = plt.bar(selected_x + (index * bar_width), selected_y, width=bar_width, label=competitor)
        if annotate:
            annotate_bars(bars)
    
    title = ','.join(categories)
    plt.title(','.join(categories))
    plt.xlabel('kategoria')
    plt.ylabel('fitness')
    plt.xticks(global_x + 1, categories)
    plt.legend()
    plt.savefig(f'results/{title}.png')
    plt.show()
    plt.close()
    return

def main():
    df = pd.read_csv('results/summary.csv', sep=';', names=['category', 'name', 'competitor', 'best'])
    mean = df.groupby(['category', 'competitor']).mean().reset_index()
    print(mean)
    categories = list(df['category'].unique())
    categories.sort(key=categories_key)
    for category in categories:
        show_chart(mean, [category], annotate=True)
    show_chart(mean, categories, annotate=False)
    

if __name__ == '__main__':
    main()