from tabulate import tabulate
import pandas as pd

def _show_filtered_data(filtered_df: pd.DataFrame, localizer):
    if filtered_df.empty:
        print(localizer.get_string(46))
        return
    print(f"\n{localizer.get_string(45)} ({len(filtered_df)})")
    print(tabulate(filtered_df, headers="keys", tablefmt="psql"))

def _filter_data(df: pd.DataFrame, localizer):
    print(f"\n=== {localizer.get_string(44)} ===")
    print(f"{localizer.get_string(69)}: {', '.join(df.columns)}")
    try:
        columns_to_show = input(localizer.get_string(60)).strip()
        if columns_to_show:
            columns = [col.strip() for col in columns_to_show.split(',')]
            df = df[columns]

        print(f"\n[1/2] {localizer.get_string(44)}...")
        filter_column = input(localizer.get_string(61)).strip()
        if filter_column not in df.columns:
            print(localizer.get_string(62))
            return

        filter_value = input(localizer.get_string(63).format(filter_column)).strip()
        filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]

        print(f"\n[2/2] {localizer.get_string(64)}...")
        sort_column = input(localizer.get_string(65)).strip()
        if sort_column and sort_column in filtered_df.columns:
            ascending = input(localizer.get_string(66)).strip().lower() == "y"
            filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

        print(f"\n{localizer.get_string(67)}")
        _show_filtered_data(filtered_df, localizer)
    except Exception as e:
        print(f"{localizer.get_string(47)}: {str(e)}")

class DataFrameViewer:
    def __init__(self, localizer):
        self.localizer = localizer
        self.page_size = 20

    def show_menu(self, df: pd.DataFrame):
        while True:
            print(f"\n{self.localizer.get_string(41)}")
            print("1. " + self.localizer.get_string(68))
            print("2. " + self.localizer.get_string(44))
            print("3. " + self.localizer.get_string(5))
            try:
                choice = int(input(f"{self.localizer.get_string(17)}: "))
                if choice == 1:
                    self._show_full_data(df)
                elif choice == 2:
                    _filter_data(df, self.localizer)
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _show_full_data(self, df: pd.DataFrame):
        print(f"\n{self.localizer.get_string(42)}: {len(df)}")
        for i in range(0, len(df), self.page_size):
            print(tabulate(df.iloc[i:i + self.page_size], headers="keys", tablefmt="psql"))
            if input(f"{self.localizer.get_string(43)} (y/n): ").lower() != "y":
                break