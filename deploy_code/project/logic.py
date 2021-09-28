import requests
import pandas as pd


def pull_results():
    URL = "https://www.itjobswatch.co.uk/"
    page = requests.get(URL)

    df_list = pd.read_html(page.text)
    for df in df_list:
        if len(df) > 10:
            data = df

    title_headers = data.columns
    body_content = data.to_numpy()

    json_dict = []

    for i in range(len(body_content)):
        temp_dict = {}

        for x in range(len(title_headers)):
            temp_dict[title_headers[x]] = body_content[i][x]

        json_dict.append(temp_dict)

    return json_dict


if __name__ == "__main__":
    output = pull_results()

    for row in output:
        print(row)
