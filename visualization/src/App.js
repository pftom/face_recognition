import React, { Component } from 'react';
import echarts from 'echarts';
import tracedData from './trace.json';

import './App.css';

class App extends Component {

  componentDidMount() {
    // construct data
    const readyToRenderData = tracedData.map(item => {
      if (item.name === 'weige') {
        return [item.left, item.bottom];
      }
    });

    console.log('readyToRenderData', readyToRenderData);

    this.myChart = echarts.init(document.getElementById('renderChart'));

    this.option = {
        xAxis: {},
        yAxis: {},
        series: [{
            symbolSize: 20,
            data: readyToRenderData,
            type: 'scatter'
        }]
    };
  
   this.myChart.setOption(this.option);
  }

  render() {
    return (
      <div className="App">
        <div id="renderChart"></div>
      </div>
    );
  }
}

export default App;
