# Source found at: https://datatables.net/extensions/scroller/examples/initialisation/large_js_source.html



def generate_html_page(file_path, prj_name, title, df):
    """
    Write a dataframe to a HTML page.
    :param file_path: File path to save the HTML file.
    :param prj_name: Project name for the title.
    :param title: Title for the title.
    :param df: Dataframe for the data to display.
    :return:
    """
    print(file_path)
    with open(file_path, 'w') as f:
        f.write(header(prj_name=prj_name, title=title))     # Header and start of Body of HTML
        f.write(table(df))                                  # Table of HTML
        f.write(footer())                                   # End of body and HTML


def header(prj_name, title):
    hdr = """<!DOCTYPE html>"
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>{} - {}</title>
                
                        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css"  crossorigin="anonymous">
                
                        <!--link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css"-->
                
                       </head>
                
                    <body>
                    """.format(prj_name, title)

    return hdr


def footer():
    ftr = """<script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.2.min.js"></script>
                <script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js"></script>
                <script>
                $(function(){
                  $("#example").dataTable();
                })
                </script>
                
                </body>
                
                </html>"""
    return ftr


def table(df):
    """
    Convert the dataframe to an HTML Table
    In clude the id and class.
    :param df: Dataframe to convert
    :return:
    """
    # Example of table start
    # <table id="example" class="display" ..
    df_html = df.to_html(classes='display" id="example')

    return df_html
