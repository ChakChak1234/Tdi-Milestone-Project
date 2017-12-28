import requests
import pandas
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral11
from bokeh.embed import components
from flask import Flask, render_template, request, redirect, session
from bokeh.embed import autoload_static
from bokeh.resources import CDN

app = Flask(__name__)

app.vars = {}


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph():
    #    if request.method == 'POST':
    app.vars['ticker'] = request.form['ticker']

    api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=n36teYQNRWq1xmudWvm3' % app.vars['ticker']
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)

    a = raw_data.json()
    df = pandas.DataFrame(a['dataset_data']['data'], columns=a['dataset_data']['column_names'])

    df['Date'] = pandas.to_datetime(df['Date'])

    # set min and max date times for plotting
    # x_min = df['Date'].min()
    # x_max = df['Date'].max()

    p = figure(title='Stock prices for %s' % app.vars['ticker'],
               x_axis_label='date',
               x_axis_type='datetime') # x_range = (x_min.timestamp(), x_max.timestamp())

    if request.form.get('Close'):
        p.line(x=df['Date'].values, y=df['Close'].values, line_width=2, line_color="blue", legend='Close')
    if request.form.get('Adj. Close'):
        p.line(x=df['Date'].values, y=df['Adj. Close'].values, line_width=2, line_color="green", legend='Adj. Close')
    if request.form.get('Open'):
        p.line(x=df['Date'].values, y=df['Open'].values, line_width=2, line_color="red", legend='Open')
    if request.form.get('Adj. Open'):
        p.line(x=df['Date'].values, y=df['Adj. Open'].values, line_width=2, line_color="purple", legend='Adj. Open')
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)


if __name__ == '__main__':
    app.run(port=33507)