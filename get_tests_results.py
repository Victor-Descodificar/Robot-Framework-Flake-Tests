import os
from selenium import webdriver
from pathlib import Path

"""
Flow
Store the path to all files reports from robot report.html in a list
Open each file using for loop
Once opened, scrap the page to get the test status
Store the test name and the status in a list
At the end, output the list test name and result to one flake_report.html

IMPORTANT: Need to have the output directory previously created.
"""


class FlakeTestsReport:

    def __init__(self, in_path: str, out_path: str):
        self.driver = None
        self.root_path = in_path
        self.files_list = []
        self.output_directory = out_path

    @staticmethod
    def get_build_number_sort(elem):
        return str(elem).split('-')[0]

    def get_files_path(self):
        logs_name = os.listdir(self.root_path)
        logs_name.sort(key=FlakeTestsReport.get_build_number_sort)

        for ln in logs_name:
            self.files_list.append(self.root_path + ln)

    def get_reports_status(self):
        self.driver = webdriver.Firefox(executable_path=os.getcwd() + '/geckodriver')
        final_list = []

        for fl in self.files_list:
            build_number = str(fl).split('/')[-1].split('-')[0]
            self.driver.get('file://' + fl)
            self.driver.find_element_by_id('radio-critical').click()
            test_name = self.driver.find_elements_by_xpath('//td[@class="details-col-name"]')
            test_result = self.driver.find_elements_by_xpath('//td[@class="details-col-status"]')
            list_size = len(test_name)

            for i in range(list_size):
                if not test_name[i].text in final_list:
                    final_list.append([build_number, test_name[i].text, test_result[i].text])
                else:
                    index = final_list.index(test_name[i].text)
                    final_list.insert(index + 1, test_result[i].text)

        self.driver.quit()

        return final_list

    def generate_final_report(self, final_list: list, first_build: int, last_build: int):

        # Create the build header for report
        build_header = ''
        for bq in range((last_build + 1) - first_build):
            build_header = build_header + '<th>Build ' + str(first_build + bq) + '</th>'

        new_column = '<td></td>'
        test = ''

        for fl in final_list:
            if fl[2].__eq__('PASS'):
                color = 'MediumSeaGreen'
            else:
                color = 'Tomato'

            test = test + '<tr><td>' + fl[1] + '</td>' + (int(fl[0]) - first_build) * new_column + '<td style = "background-color:' + color + ';">' + fl[2] + '</td></tr>'

        print('<tr><th>Test Name</th>' + build_header + '</tr>' + test)

    def output_html(self, tests_result: str):
        header = """
        <!DOCTYPE html>
        <html lang="en">
        <head><meta charset="UTF-8"><title>Flake tests report</title></head>
        <style>
            table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}
            td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}
            tr:nth-child(even) {background-color: #dddddd;}
        </style>
        <body>
        <table>
        """

        footer = """
        </table>
        </body>
        </html>
        """
        html = header + tests_result + footer

        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        report = open(self.output_directory + '/flake_report.html', 'w')
        report.write(html)
        report.close()
