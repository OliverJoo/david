import pandas as pd
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # Mac OS
    plt.rc('font', family='AppleGothic')
else:  # Linux
    # apt-get install fonts-nanum*
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False


def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df

    except FileNotFoundError:
        print(f'File {file_path} not found.')
    except UnicodeError:
        print(f'Decoding error on {file_path}.')
    except Exception as e:
        print(f'Unexpected error: {e}')


def main():
    dataset_df = read_csv('problem2.csv')
    dataset_df = dataset_df.rename(columns={'시점': '연도'})
    print(dataset_df.describe())
    print(dataset_df.columns)

    dataset_df_normal = dataset_df[['일반가구원']]  # ?
    print("\n2015년 이후 일반가구원 통계")
    print(dataset_df_normal)

    filtered_df = dataset_df[['연도', '성별', '일반가구원']]
    print("\n2015년 이후 연도, 성별, 일반가구원 통계")
    # print(filtered_df.describe())
    print(filtered_df)

    grouped_data = filtered_df.groupby(['연도', '성별'])['일반가구원'].sum().reset_index()
    print("\n2015년 이후 연도별, 성별 일반가구원 통계")
    print(grouped_data)
    grouped_data_more = grouped_data.groupby(['연도'])['일반가구원'].sum().reset_index()
    print("\n2015년 이후 연도별 일반가구원 통계")
    print(grouped_data_more)

    age_filtered_df = dataset_df[['연도', '연령별', '일반가구원']]
    age_grouped_data = age_filtered_df.groupby(['연도', '연령별'])['일반가구원'].sum().reset_index()
    print("\n2015년 이후 연령별 일반가구원 통계")
    print(age_grouped_data)

    # 2015년 이후 연도별, 연령대별, 성별 일반가구원 통계 (개별 그래프)
    age_gender_grouped = dataset_df[['연도', '성별', '연령별', '일반가구원']].groupby(['연도', '성별', '연령별'])[
        '일반가구원'].sum().reset_index()

    years_to_plot = sorted(age_gender_grouped['연도'].unique())
    genders = age_gender_grouped['성별'].unique()
    age_order = sorted(age_gender_grouped['연령별'].unique())

    styles = {'남자': '-', '여자': '--'}
    markers = {'남자': 'o', '여자': 'x'}

    for year in years_to_plot:
        fig, ax = plt.subplots(figsize=(15, 8))

        year_data = age_gender_grouped[age_gender_grouped['연도'] == year]

        for gender in genders:
            gender_data = year_data[year_data['성별'] == gender]
            plot_data = gender_data.set_index('연령별').reindex(age_order).reset_index()

            if not plot_data['일반가구원'].isnull().all():
                ax.plot(plot_data['연령별'], plot_data['일반가구원'],
                        marker=markers.get(gender),
                        linestyle=styles.get(gender),
                        label=gender)

        ax.set_title(f'{year}년 연령대별, 성별 일반가구원 통계')
        ax.set_xlabel('연령별')
        ax.set_ylabel('일반가구원 수')
        ax.legend(title='성별')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()
