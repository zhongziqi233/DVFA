<template>
    <div id="mapMain"></div>
</template>
<script>
/* eslint-disable no-unused-vars */
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

export default {
    name: 'mapView',
    mounted() {
        this.init();
    },
    methods: {
        init() {
            // 配置Token(这里Token是私有的跟别人借的不方便展示)
            mapboxgl.accessToken = "pk.eyJ1IjoiMTMzNzM2ODU3OCIsImEiOiJjampreGJxOHY2MThyM3BvaHF6bzFpbnk5In0.ZSRSqnflAz3Z5aULV_JtaQ";
            // 创建新地图
            var map = new mapboxgl.Map({
                container: "mapMain",  // 地图容器
                style: "mapbox://styles/mapbox/light-v10",  // 地图样式（mapbox预设样式）
                maxZoom: 17,  // 设置最大最小缩放等级、默认缩放等级、默认中心
                minZoom: 1,
                zoom: 1,
                center: [120, 29],
                antialias: true,  // 打开抗锯齿
            });
        }
    }
}
</script>
<style scoped>
#mapMain {
    width: 100%;
    height: 100%;
    /* background-color: brown; */
}
</style>