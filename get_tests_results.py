import os
from selenium import webdriver

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

    def __init__(self):
        self.driver = None
        self.root_path = os.getcwd() + '/robot_reports/'
        self.files_list = []
        self.output_directory = os.getcwd() + '/flake_reports/flake_report.html'

    def get_files_path(self):
        logs_name = os.listdir(self.root_path)
        for ln in logs_name:
            self.files_list.append(self.root_path + ln)

    def open_browser(self):
        self.driver = webdriver.Firefox()

    def get_reports_status(self):
        self.driver = webdriver.Firefox()
        final_list = []

        for fl in self.files_list:
            self.driver.get('file://' + fl)
            self.driver.find_element_by_id('radio-critical').click()
            test_name = self.driver.find_elements_by_xpath('//td[@class="details-col-name"]')
            test_result = self.driver.find_elements_by_xpath('//td[@class="details-col-status"]')
            list_size = len(test_name)

            for i in range(list_size):
                if not test_name[i].text in final_list:
                    final_list.append(test_name[i].text)
                    final_list.append(test_result[i].text)
                    final_list.append('\n')
                else:
                    index = final_list.index(test_name[i].text)
                    final_list.insert(index + 1, test_result[i].text)

        self.driver.quit()

        return final_list

    @staticmethod
    def generate_final_report(final_list: list):
        test = ''
        line = ''
        en = ''
        test_qtd = 0
        max_executions = 0
        for fl in final_list:
            if not fl.__eq__('\n'):
                if fl.__eq__('PASS'):
                    test = test + '<td style = "background-color:MediumSeaGreen;">' + fl + '</td>'
                    test_qtd += 1
                elif fl.__eq__('FAIL'):
                    test = test + '<td style = "background-color:Tomato;">' + fl + '</td>'
                    test_qtd += 1
                else:
                    test = test + '<td>' + fl + '</td>'
                    if test_qtd > max_executions:
                        max_executions = test_qtd

                    test_qtd = 0

            else:
                line = line + '<tr>' + test + '</tr>'
                test = ''

        for me in range(max_executions):
            en = en + '<th>Execution number</th>'

        return '<tr><th>Test Name</th>' + en + '</tr>' + line

    @staticmethod
    def output_html(tests_result: str):
        header = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Flake tests report</title>
        </head>
        <body>
        <table>
        """

        footer = """
        </table>
        </body>
        </html>
        """
        html = header + tests_result + footer

        report = open(os.getcwd() + '/flake_reports/flake_report.html', 'w')
        report.write(html)
        report.close()


if __name__ == '__main__':
    ft = FlakeTestsReport()
    ft.get_files_path()
    report_results = ft.get_reports_status()
    test_report = FlakeTestsReport.generate_final_report(report_results)
    FlakeTestsReport.output_html(test_report)
