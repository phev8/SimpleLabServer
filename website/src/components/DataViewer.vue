<template>
  <div id="component">
  <div class="container-fluid">
    <div class="row">
      <div class="col-12 col-sm-4 col-lg-3">
        <div class="form-group">
          <label for="windowSize">Window Size:</label>
          <input class="form-control" type="number" v-model="windowSize" id="windowSize">
          <small id="windowSizeHelp" class="form-text text-muted">Number of maximum samples displayed at once.</small>
        </div>
        <button class="btn btn-light" @click="removeOldest()">Remove oldest sample</button>
      </div>
      <div class="col-12 col-sm-8 col-lg-9">
        <app-line-chart :chartData="data" :options="options"></app-line-chart>
      </div>
    </div>
  </div>
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
      windowSize: 60,
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
          }

          if (this.rawData.length > 0) {
            const last_index = this.rawData.length - 1
            if (this.rawData[last_index] !== currentData) {
              this.rawData.push(currentData);
            }
          } else {
            this.rawData.push(currentData);
          }

          if (this.rawData.length > this.windowSize) {
            this.rawData.shift();
          }
        }

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
          console.log(error)
      })
    },
    removeOldest() {
       this.rawData.shift();
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
    }
  },
  components: {
    AppLineChart: LineChart
  }
}
</script>

<style scoped>
#component {
  margin: 35px 20px;
}

</style>
