<template>
  <div id="component">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12 col-sm-4 col-lg-3">
          <div class="form-group">
            <label for="datePicker">Select date:</label>
            <datepicker id="datePicker"  v-model="selectedDate" @closed="refreshData()"></datepicker>
          </div>
          <div class="form-group">
            <label for="minTimeInput">Start time:</label>
            <vue-timepicker id="minTimeInput" v-model="minTime" format="HH:mm:ss" @change="refreshData()" hide-clear-button></vue-timepicker>
          </div>
          <div class="form-group">
            <label for="maxTimeInput">End time:</label>
            <vue-timepicker id="maxTimeInput" v-model="maxTime" format="HH:mm:ss" @change="refreshData()" hide-clear-button></vue-timepicker>
          </div>


          <button class="btn btn-primary" @click="download()">Download as CSV</button>
        </div>
        <div class="col-12 col-sm-8 col-lg-9">
          <app-line-chart :chartData="data" :options="options"></app-line-chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vue2-timepicker';
import LineChart from '@/components/LineChart'
var moment = require('moment');
var FileSaver = require('file-saver');

export default {
  data() {
    return {
      selectedDate: new Date(),
      minTime: {
        HH: new Date().getHours().toString(),
        mm: new Date().getMinutes().toString(),
        ss: new Date().getSeconds().toString(),
      },
      maxTime: {
        HH: new Date().getHours().toString(),
        mm: new Date().getMinutes().toString(),
        ss: new Date().getSeconds().toString(),
      },
      fromDate: new Date(),
      toDate: new Date(),
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
    refreshData() {      
      this.fromDate = new Date(
        this.selectedDate.getFullYear(),
        this.selectedDate.getMonth(),
        this.selectedDate.getDate(),
        parseInt(this.minTime.HH),
        parseInt(this.minTime.mm),
        parseInt(this.minTime.ss)
        );
      this.toDate = new Date(
        this.selectedDate.getFullYear(),
        this.selectedDate.getMonth(),
        this.selectedDate.getDate(),
        parseInt(this.maxTime.HH),
        parseInt(this.maxTime.mm),
        parseInt(this.maxTime.ss)
        );
      
      this.fetchData();
    },
    fetchData() {
      this.$http.get('api/measurement-in-range', {
        params: {
          from: moment(this.fromDate).format("YYYY-MM-DD HH:mm:ss"),
          to: moment(this.toDate).format("YYYY-MM-DD HH:mm:ss")
        }
      })
      .then(response => {
        return response.json();
      }).then(data => {
        console.log(data);
        this.rawData = [];
        
        data.forEach(row => {          
          this.rawData.push({
            x: moment(row[3]),
            y: row[5]
          });
        });

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
    download() {
      let csvData = 'time;value\n';
      this.rawData.forEach( item => {
        csvData += item.x.format("YYYY-MM-DD HH:mm:ss") + ";" + item.y.toString() + "\n";
      });

      var blob = new Blob([csvData], {type: "text/plain;charset=utf-8"});
      FileSaver.saveAs(blob, "lab_measurement_" + moment(this.fromDate).format("YYYY-MM-DD_HH-mm-ss") + "_" + moment(this.toDate).format("HH-mm-ss") + ".csv");      
    }
  },
  components: {
    Datepicker,
    VueTimepicker,
    AppLineChart: LineChart
  }
}
</script>

<style scoped>
#component {
  margin: 35px 20px;
}
</style>
