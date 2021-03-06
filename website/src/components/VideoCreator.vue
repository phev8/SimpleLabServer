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
          <p>Generating video on server, it can take a while... Be patient.</p>
        </div>
        
        <div class="col-12">
          List of videos
          <ul class="list-group">
            <li v-if="videos.length <= 0" class="list-group-item">No videos generated yet.</li>
            <li v-else v-for="video in videos" :key="video.link" class="list-group-item">              
              Signal plot from {{ video.start }}
              to {{ video.end }}
              <button style="float: right; margin: 0 10px;" class="btn btn-primary" @click="downloadVideo(video)">Download</button>
              <button style="float: right; margin: 0 10px;" class="btn btn-danger" @click="deleteVideo(video)">Remove</button>              
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
        this.processing = false;
        this.fetchVideos();
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
    async downloadVideo(video) {
      let response = await this.$http.get(video.link, {responseType: 'arraybuffer'});
      let blob = new Blob([response.data], {type:response.headers.get('content-type')});
      let filname = moment(video.end, "YYYY-MM-DD-HH-mm-ss").format("YYYY-MM-DD_HH-mm-ss") + "_" + moment(video.start, "YYYY-MM-DD-HH-mm-ss").format("YYYY-MM-DD_HH-mm-ss") + ".mp4";
      FileSaver.saveAs(blob, filname);
    },
    deleteVideo(video) {
      if (confirm('Are you sure you want to delete this video?')) {
        this.$http.get('api/delete-video', {
          params: {
            filename: video.link
          }
        }).then(
          response => {
            this.fetchVideos();
          }
        ).catch(
          error => {
            console.log(error);
            this.fetchVideos();
          }
        )
      }
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
