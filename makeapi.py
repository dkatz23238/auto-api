from autoapi import *

if __name__ == '__main__':
    auto_api_dict = load_dict("./auto-api.yml")
    rendered_template = render_temp(auto_api_dict)
    print(rendered_template)
