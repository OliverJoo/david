import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress the specific FutureWarning from seaborn
warnings.filterwarnings('ignore', category=FutureWarning)


def main():
    try:
        train_df = pd.read_csv(os.path.join('level_1', 'data_source', 'train.csv'))
        test_df = pd.read_csv(os.path.join('level_1', 'data_source', 'test.csv'))

        print(f'\n=== Training data ===')
        print(train_df.describe())
        print(f'\n=== Test data ===')
        print(test_df.describe())

        train_df['Transported'] = train_df['Transported'].astype(int)
        analysis_results = []

        print('\n=== Training data Info ===')
        print(train_df.info())

        # 1. Numeric Feature Analysis
        transported_corr = train_df.corr(numeric_only=True)['Transported']
        print(f'\n=== Training data Corr ===')
        print(transported_corr.sort_values(ascending=False))

        for col, corr_value in transported_corr.items():
            if col != 'Transported':
                analysis_results.append([col, 'numeric', corr_value])

        # 2. Categorical Feature Analysis
        categorical_cols = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']
        for col in categorical_cols:
            if train_df[col].isnull().any():
                train_df[col] = train_df[col].fillna('Unknown')

            grouped_data = train_df.groupby(col)['Transported'].mean()
            for category_value, transport_rate in grouped_data.items():
                analysis_results.append([col, str(category_value), transport_rate])

        # --- Print the collected data --- #
        results_df = pd.DataFrame(analysis_results, columns=['Feature', 'Category/Value', 'Correlation/Rate'])
        corr_result_df = results_df.sort_values(by='Correlation/Rate', ascending=False)
        print(f'\n=== Transported Correlation Result(Total) ===')
        print(corr_result_df.to_string(index=False))
        print(f'\n=== Transported Correlation by Column High Value ===')
        print(f'{corr_result_df[:3]}')
        print(f'\n=== Transported Correlation by Column Low Value ===')
        print(f'{corr_result_df[-3:]}')

        print(f'\n=== Transported Flag by Age ===')
        age_median = train_df['Age'].median()
        train_df['Age_filled'] = train_df['Age'].fillna(age_median)

        # Create age groups (bins)
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
        labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
        train_df['AgeGroup'] = pd.cut(train_df['Age_filled'], bins=bins, labels=labels, right=False)

        print(f'\n=== Count by Age Group ===')
        print(f'\n{train_df["AgeGroup"].value_counts()}')

        # Group by AgeGroup and calculate the transport rate
        age_transport_rate = train_df.groupby('AgeGroup', observed=False)['Transported'].mean().reset_index()

        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.barplot(data=age_transport_rate, x='AgeGroup', y='Transported', palette='viridis')

        plt.title('Transported Rate by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Transported Rate')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        print(f'\n=== Age Group by Destination ===')
        destination_age_groups = train_df.groupby('Destination')['AgeGroup'].value_counts()
        print(destination_age_groups)

        plt.figure(figsize=(12, 8))
        sns.countplot(data=train_df, x='Destination', hue='AgeGroup')
        plt.title('Passenger Counts by Destination and Age Group')
        plt.xlabel('Destination')
        plt.ylabel('Count')
        plt.legend(title='Age Group')
        plt.show()

        # sns.catplot(data=train_df, x='AgeGroup', col='Destination', kind='count',
        #             height=5, aspect=1.5, col_wrap=2)
        # plt.suptitle('Passenger Counts by Age Group for Each Destination', y=1.02)
        # plt.show()

        # Concatenate train and test data for consistent preprocessing
        all_df = pd.concat([train_df, test_df], ignore_index=True)
        print("\n\nCombined DataFrame Info:")
        print(all_df.info())

    except (FileNotFoundError, IOError) as e:
        print(f'File not found : {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')


if __name__ == '__main__':
    main()
