import json
import os
import shutil
import sys

from jinja2 import Template


def generate_reporting(target_user, likes):
    # if we don't already have the output folder with CSS files, then create it
    # (otherwise we only re-create the HTML page)
    output_dir = f"html_output_{target_user}"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
        shutil.copytree("templates/css", output_dir + "/css")

    # load template
    with open("templates/index.html", "r", encoding="utf-8") as f:
        index_tpl = Template(f.read())
    # process template with likes data
    index_data = index_tpl.render(likes=likes)
    # write HTML output
    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(index_data)


if __name__ == '__main__':
    target_user = sys.argv[1]
    likes = json.load(open(f"data/likes_{target_user}.json", "r", encoding="utf-8"))
    generate_reporting(target_user, likes)
