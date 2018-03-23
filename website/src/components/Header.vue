<template>
  <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <router-link class="navbar-brand" to="/">iLab Pro</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <router-link tag="li" to="/data-viewer" class="nav-item" active-class="active">
                    <a class="nav-link">Live data</a>
                </router-link>                
                <router-link tag="li" to="/downloader" class="nav-item" active-class="active">
                    <a class="nav-link">Data download</a>
                </router-link>                
                <router-link tag="li" to="/video-creator" class="nav-item" active-class="active">
                    <a class="nav-link">Video creator</a>
                </router-link>                
            </ul>
        </div>
    </nav>
  </div>
</template>

<script>

</script>

<style>

</style>
