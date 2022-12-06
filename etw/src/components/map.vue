<template>
    <div class="mapBlock" id="mapMain">
        
    </div>
    <div class="mapBlock">
        <el-radio-group v-model="type" size="small">
            <el-radio label="0" border>人流</el-radio>
            <el-radio label="1" border>票价</el-radio>
        </el-radio-group>
    </div>
    
</template>
<script>
/* eslint-disable no-unused-vars,no-empty */
import axios from "axios";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

export default {
    name: 'mapView',
    data() {
      return {
        type: '0',
        data: null,
        map: null,
        max: { "sales": 0, "price": 0 },
      }  
    },
    mounted() {
        axios.get("./旅游景点.json").then((res) => {
            var d = res.data;
            var data = {"type": "FeatureCollection", "features": []}
            for(let piece in d) {
                if(d[piece].sales > this.max.sales) this.max.sales = d[piece].sales;
                if(d[piece].price > this.max.price) this.max.price = d[piece].price;
                let dp = { "type": "Feature", "properties": { "id": d[piece].id, "sales": d[piece].sales, "price": d[piece].price }, "geometry": { "type": "Point", "coordinates": [d[piece].coordinate.lng, d[piece].coordinate.lat] } }
                data.features.push(dp);
            }
            this.data = data;
            console.log('map', this.data)
            this.init();
        });
    },
    methods: {
        init() {
            // 配置Token(这里的Token是个人私有，不便展示)
            mapboxgl.accessToken = "pk.eyJ1IjoiMTMzNzM2ODU3OCIsImEiOiJjampreGJxOHY2MThyM3BvaHF6bzFpbnk5In0.ZSRSqnflAz3Z5aULV_JtaQ";
            // 创建新地图
            var bounds = [[60, 0],[150, 60]];
            var map = new mapboxgl.Map({
                container: "mapMain",
                style: "mapbox://styles/mapbox/light-v10",
                center: [105, 35],
                antialias: true,
                maxBounds: bounds,
            });
            this.map = map;
            this.addLayer();
        },
        addLayer() {
            var map = this.map;
            // 类别区分
            if(this.type == '0')
                var type = "sales";
            else if(this.type == '1')
                type = "price";
            map.on('load', () => {
                // 添加源
                map.addSource('tour', {
                    'type': 'geojson',
                    'data': this.data
                });
                // 添加热力图层
                map.addLayer({
                    'id': 'tour-heat',
                    'type': 'heatmap',
                    'source': 'tour',
                    'maxzoom': 9,
                    'paint': {
                        // 设置权重比例尺
                        'heatmap-weight': [
                            'interpolate',
                            ['linear'], ['get', type],
                            0, 0, this.max[type], 1
                        ],
                        // 设置总权重值
                        'heatmap-intensity': [
                            'interpolate',
                            ['linear'], ['zoom'],
                            0, 1, 9, 3
                        ],
                        // 设置颜色
                        'heatmap-color': [
                            'interpolate',
                            ['linear'], ['heatmap-density'],
                            0, 'rgba(33,102,172,0)',
                            0.2, 'rgb(103,169,207)',
                            0.4, 'rgb(209,229,240)',
                            0.6, 'rgb(253,219,199)',
                            0.8, 'rgb(239,138,98)',
                            1, 'rgb(178,24,43)'
                        ],
                        // 设置影响范围
                        'heatmap-radius': [
                            'interpolate',
                            ['linear'], ['zoom'],
                            0, 10, 10, 20
                        ],
                        // 根据缩放设置透明度
                        'heatmap-opacity': [
                            'interpolate',
                            ['linear'], ['zoom'],
                            7, 1, 9, 0
                        ]
                    }
                }, 'waterway-label');
                // 放大后的散点图层
                map.addLayer({
                    'id': 'tour-point',
                    'type': 'circle',
                    'source': 'tour',
                    'minzoom': 7,
                    'paint': {
                        // 设置散点半径
                        'circle-radius': [
                            'interpolate',
                            ['linear'], ['zoom'],
                            7, ['interpolate', ['linear'], ['get', type], 1, 1, 6, 4],
                            16, ['interpolate', ['linear'], ['get', type], 1, 5, 6, 50]
                        ],
                        // 设置颜色
                        'circle-color': [
                            'interpolate',
                            ['linear'], ['get', type],
                            this.max[type] / 5 * 0, 'rgba(33,102,172,0)',
                            this.max[type] / 5 * 1, 'rgb(103,169,207)',
                            this.max[type] / 5 * 2, 'rgb(209,229,240)',
                            this.max[type] / 5 * 3, 'rgb(253,219,199)',
                            this.max[type] / 5 * 4, 'rgb(239,138,98)',
                            this.max[type], 'rgb(178,24,43)'
                        ],
                        'circle-stroke-color': 'white',
                        'circle-stroke-width': 1,
                        // 设置缩放透明度
                        'circle-opacity': [
                            'interpolate',
                            ['linear'], ['zoom'],
                            7, 0, 8, 1
                        ]
                    }
                }, 'waterway-label');
            });
        }
    },
    watch: {
        type() {
            this.init();
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
.mapBlock {
    position: absolute;
}
</style>