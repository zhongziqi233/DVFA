<template>
    <div id="cloudMain"></div>
</template>
<script>
/* eslint-disable no-unused-vars,no-empty */
import * as d3 from 'd3';
import cloud from 'd3-cloud';
import axios from 'axios';

export default {
    name: 'cloudView',
    data() {
        return {
            data: null,
            size: { min: 10, max: 100 },
            scale: null,
        }
    },
    mounted() {
        // 获取数据
        axios.get('./mainWords.json').then((res) => {
            var d = res.data;
            // 数据再次处理(根据出现频率设置大小)
            const size = this.size;
            const scale =  d3.scaleLinear().domain([d[d.length - 1].rate, d[0].rate]).range([size.min, size.max]);
            this.scale = scale;
            for(let i = 0; i < d.length; i++)
                d[i].size = parseInt(scale(d[i].rate));
            this.data = d;
            console.log('cloud', this.data)
            // 初始化
            this.init();
        })
    },
    methods: {
        init() {
            const data = this.data;
            // 颜色设置
            const color = d3.scaleOrdinal(d3.schemeCategory10);
            const svg = d3.select("#cloudMain")
                .append("svg")
                .attr("width", "100%")
                .attr("height", "100%");
            const size = { w: parseInt(window.getComputedStyle(document.getElementById("cloudMain"), null).width.replace("px", '').replace('"', '')), 
                           h: parseInt(window.getComputedStyle(document.getElementById("cloudMain"), null).height.replace('px', '').replace('"', '')) };
            // 生成词云布局
            const layout = cloud()
                .size([size.w, size.h])
                .words(data)
                .padding(5)
                .rotate(function() { return Math.random() * 45 }) // 随机旋转
                .font('Impact')
                .fontSize(function(d) { return d.size })
                .on('end', draw);
            layout.start();
            // 绘制文字
            function draw(words) {
                svg.append('g')
                .attr('transform', `translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`)
                .selectAll('text')
                .data(words)
                .enter()
                .append('text')
                .attr('fill', (_, i) => color(i))
                .style('font-size', function(d) { return `${d.size}px` })
                .attr('transform', function(d) { return `translate(${[d.x, d.y]})rotate(${d.rotate})` })
                .text(function(d) { return d.text });
            }
        },
    }
}
</script>
<style scoped>
#cloudMain {
    width: 100%;
    height: 100%;
    float: left;
    overflow: hidden;
    font-family: Impact;
    text-anchor: middle;
    /* background-color: blueviolet; */
}
</style>