<template>
  <div class="container">
      <button class="btn btn-primary" @click="fetchData()">Fetch Data</button>
      <input type="number" v-model="windowSize">
      <div class="row">
          <div class="col-8">
                <app-line-chart :chartData="data" :options="options"></app-line-chart>
          </div>
      </div>
      <p>TODO: add vue chart object with resource from the server here</p>

  </div>
</template>

<script>
import LineChart from '@/components/LineChart'
var moment = require('moment');

export default {
  created() {
    this.fetchData();
    this.setIntervalID = setInterval(this.fetchData, 1500);
  },
  beforeDestroy() {
    clearInterval(this.setIntervalID);
  },
  data() {
    return {
      windowSize: 10,
      setIntervalID: {},
      data: {
        labels: [],
        
        datasets: [          {
            fill: true,
            showLine: true,
            borderColor: '#f87979',
            backgroundColor: '#f87979',
            label: 'Conductivity Values',
            data: []
          }
        ]
      },
      rawData: [],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'YYYY-MM-DD h:mm:ss.SSS'
                    }
                }
            }]
        }
    }
    }
  },
  methods: {
    fetchData() {
      this.$http.get('api/measurement', {
        params: {
          window: 1
        }
      })
        .then(response => {
          return response.json();
        }).then(data => {
          if (data.length > 0) {
            const currentData = {
              x: moment(data[0][3]),
              y: data[0][5]
            };

            if (this.rawData.length > 0) {
              const last_index = this.rawData.length - 1;
              if (this.rawData[last_index] != currentData) {
                this.rawData.push(currentData);
              }
            } else {
              this.rawData.push(currentData);
            }

            if (this.rawData.length > this.windowSize) {
              this.rawData.shift();
            }
          }
          
          var labels = [];
          var values = [];
          data.forEach(row => {

            labels.push(row[3]);
            values.push({
              x: moment(row[3]),
              y: row[5]
            });
          });
          console.log(this.rawData);
          this.data = {
            datasets: [
              {
                fill: false,
                showLine: true,
                borderColor: '#f87979',
                backgroundColor: '#f87979',
                label: 'Conductivity Values',                
                data: this.rawData
              }
            ]
          };
        }).catch(
          error => {
            console.log(error);
        })
    }
  },
  components: {
    AppLineChart: LineChart
  }
}
</script>
