
import os
import dash
import dash_bootstrap_components as dbc
import dash_auth as da

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

valid_login = {
    str(os.environ.get('USER')): str(os.environ.get('PASS'))
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

auth = da.BasicAuth(
    app, valid_login
)
server = app.server

#if __name__ =='__main':
#    app.run_server(port=2020, debug=True)

app.title = 'Maamulka Dekkedda Muqdisho'
app.config.suppress_callback_exceptions = True