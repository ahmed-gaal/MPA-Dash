import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
server = app.server

#if __name__ =='__main':
#    app.run_server(port=2020, debug=True)

app.title = 'Maamulka Dekkedda Muqdisho'
app.config.suppress_callback_exceptions = True