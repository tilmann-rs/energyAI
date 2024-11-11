import matplotlib.pyplot as plt


def plot_data(df, columns):
    df[columns].plot(figsize=(20, 10))
    plt.title('Energy Generation Over Time')
    plt.xlabel('Time')
    plt.ylabel('Power (MW)')
    plt.legend()
    plt.show()
