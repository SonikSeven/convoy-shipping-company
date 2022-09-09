import pandas as pd
import sqlite3
import json


def convert_xlsx_to_csv(file_name):
    my_df = pd.read_excel(file_name, sheet_name="Vehicles")
    file_name = file_name[:file_name.rfind(".")] + ".csv"
    my_df.to_csv(file_name, index=False)
    print(f"{my_df.shape[0]} line{'s were' if my_df.shape[0] != 1 else ' was'} imported to {file_name}")
    return file_name


def correct_csv(file_name):
    my_df = pd.read_csv(file_name)
    counter = 0
    for column in my_df:
        for row, value in enumerate(my_df[column]):
            value = str(value)
            new_value = "".join(i for i in value if i.isdigit())
            if value != new_value:
                counter += 1
            my_df[column][row] = new_value
    file_name = file_name[:file_name.rfind(".")] + "[CHECKED].csv"
    my_df.to_csv(file_name, index=False)
    print(f"{counter} cell{'s were' if counter != 1 else ' was'} corrected in {file_name}")
    return file_name


def convert_csv_to_s3db(file_name):
    my_df = pd.read_csv(file_name)
    score_column = pd.DataFrame(pd.Series((0 for _ in range(my_df.shape[0])), name="score"))
    my_df = my_df.join(score_column)
    for i in range(my_df.shape[0]):
        fuel_consumed = my_df.loc[i][2] / 100 * 450
        pitstops = fuel_consumed / my_df.loc[i][1]
        my_df.loc[i][4] = 1
        if pitstops < 2:
            my_df.loc[i][4] += 1
        if pitstops < 1:
            my_df.loc[i][4] += 1
        if fuel_consumed <= 230:
            my_df.loc[i][4] += 1
        if my_df.loc[i][3] >= 20:
            my_df.loc[i][4] += 2
    file_name = file_name[:file_name.rfind("[CHECKED].csv")] + ".s3db"
    conn = sqlite3.connect(file_name)
    cursor_name = conn.cursor()
    cursor_name.execute("""CREATE TABLE convoy (vehicle_id INT PRIMARY KEY, engine_capacity INT NOT NULL,
                           fuel_consumption INT NOT NULL, maximum_load INT NOT NULL, score INT NOT NULL);""")
    my_df.to_sql("convoy", conn, if_exists="append", index=False)
    print(f"{my_df.shape[0]} record{'s were' if my_df.shape[0] != 1 else ' was'} inserted into {file_name}")
    return file_name


def convert_s3db_to_json_and_xml(file_name):
    conn = sqlite3.connect(file_name)
    my_df = pd.read_sql(
        "SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score > 3", conn)
    file_name = file_name[:file_name.rfind(".")] + ".json"
    my_df.to_json(file_name, orient="records")
    with open(file_name) as json_file:
        new_json = {"convoy": json.load(json_file)}
    with open(file_name, "w") as json_file:
        json.dump(new_json, json_file)
    print(f"{my_df.shape[0]} vehicle{'s were' if my_df.shape[0] != 1 else ' was'} saved into {file_name}")
    my_df = pd.read_sql(
        "SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score <= 3", conn)
    file_name = file_name[:file_name.rfind(".")] + ".xml"
    with open(file_name, "w") as xml_file:
        xml_file.write("<convoy></convoy>")
    if my_df.shape[0]:
        my_df.to_xml(file_name, index=False, root_name="convoy", row_name="vehicle", xml_declaration=False)
    print(f"{my_df.shape[0]} vehicle{'s were' if my_df.shape[0] != 1 else ' was'} saved into {file_name}")


def main():
    file_name = input("Input file name\n")
    if file_name.endswith(".xlsx"):
        file_name = convert_xlsx_to_csv(file_name)
    if file_name.endswith(".csv") and not file_name.endswith("[CHECKED].csv"):
        file_name = correct_csv(file_name)
    if file_name.endswith("[CHECKED].csv"):
        file_name = convert_csv_to_s3db(file_name)
    if file_name.endswith(".s3db"):
        convert_s3db_to_json_and_xml(file_name)


if __name__ == "__main__":
    main()
