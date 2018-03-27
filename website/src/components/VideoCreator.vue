<template>
  <div id="component">
    <div class="container">
      
      <div class="card card-default">
        <div class="card-header">
          Create new plot video
        </div>
        <div class="card-body">
        <div class="row">
          <div class="col-12">
            <div class="row align-items-center">
              <div class="col-2">
                <div class="form-group">
                  <label for="datePicker">Select date:</label>
                  <datepicker id="datePicker" class="picker" v-model="selectedDate" @closed="refreshData()"></datepicker>
                </div>
              </div>
              <div class="col-2">
                <div class="form-group">
                  <label for="minTimeInput">Start time:</label>
                  <vue-timepicker id="minTimeInput" class="picker" v-model="minTime" format="HH:mm:ss" @change="refreshData()" hide-clear-button></vue-timepicker>
                </div>
              </div>
              <div class="col-2">
                <div class="form-group">
                  <label for="maxTimeInput">End time:</label>
                  <vue-timepicker id="maxTimeInput" class="picker" v-model="maxTime" format="HH:mm:ss" @change="refreshData()" hide-clear-button></vue-timepicker>
                </div>
              </div>
              <div class="col-2">
                <div class="form-group">
                  <label for="windowSize">Window Size</label>
                  <input type="number" class="form-control" min="10" max="120" v-model="windowSize">                  
                </div>
              </div>
              <div class="col-2">
                <button class="btn btn-primary" :disabled="processing"  @click="generatePlotVideo()">Generate Signal Video</button>
              </div>
            </div>            
          </div>
          </div>
        </div>
      </div>   
      <br>   

      <div class="row justify-content-center">        
        <app-loader :loading="processing" :size="'100px'"></app-loader>
        <div v-if="processing" class="col-12" style="text-align: center; margin: 25px;">
          <p>Generating video on server, it can take a while...</p>
        </div>
        
        <div class="col-12">
          List of videos
          <ul class="list-group">
            <li v-for="video in videos" class="list-group-item">
              {{ video.link }}
              <button class="btn btn-danger">Remove</button>
              <button class="btn btn-primary">Download</button>
            </li>
          </ul>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vue2-timepicker';
import LineChart from '@/components/LineChart'
import DotLoader from 'vue-spinner/src/DotLoader.vue'
var moment = require('moment');
var FileSaver = require('file-saver');

export default {
  computed: {
   videoList() {
     return this.videos;
   }
  },
  data() {
    return {
      processing: false,      
      windowSize: 15,
      videos: [],
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
  created() {
    this.fetchVideos();
  },
  methods: {
    generatePlotVideo() {
      this.processing = true;
      this.$http.get('api/plot-video-generator', {
        params: {
          from: moment(this.fromDate).format("YYYY-MM-DD HH:mm:ss"),
          to: moment(this.toDate).format("YYYY-MM-DD HH:mm:ss"),
          window: this.windowSize,
        }
      })
      .then(response => {
        return response.json();
      }).then(data => {
        console.log(data);
        this.videos.unshift(data);
        this.processing = false;
      }).catch(
        error => {
          this.processing = false;
          console.log(error)
      });
    },
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
    },
    fetchVideos() {
      this.$http.get('api/videos')
      .then(response => {
        return response.json();
      }).then(data => {
        console.log(data);
        this.videos = data;     
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
    AppLoader: DotLoader
  }
}
</script>

<style scoped>
#component {
  margin: 35px 20px;
}

.picker {
  width: 100%;
}
</style>
