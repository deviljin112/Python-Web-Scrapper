from bs4 import BeautifulSoup
import bs4
import requests


def headers(results):
    headers_list = []
    header = results.find("tr", class_="resultsHeader")
    for row in header:
        title = row.find("div")
        if isinstance(title, int) or title == None:
            continue
        else:
            headers_list.append(title.get_text(separator=" "))

    sub_header = results.find("th", class_="findJobsHdr")
    headers_list.append(sub_header.text)
    return headers_list


def body(results):
    body_list = []

    for section in results:
        section_list = []
        if type(section) is bs4.element.NavigableString:
            continue
        else:
            data = section.find_all("td")
            for row in data:
                if isinstance(row, int) or row == None:
                    continue
                else:
                    if row.text == "" or row.text == "\xa0":
                        continue
                    else:
                        section_list.append(row.text)

        if len(section_list) > 0:
            body_list.append(section_list)

    return body_list


def pull_results():
    URL = "https://www.itjobswatch.co.uk/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    output = soup.find("table", {"class": "results"})

    title_headers = headers(output)
    body_content = body(output)

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